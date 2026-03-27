#!/usr/bin/env python3
"""
对接已安装的高德地图技能，获取路线耗时
兼容 smart-map-guide 和 amap-lbs-skill
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict

def expand_user(path: str) -> str:
    return os.path.expanduser(path)

def get_config() -> Dict:
    """读取配置"""
    config_path = expand_user("~/.openclaw/workspace/data/simple-schedule/config.json")
    default_config = {
        "amap_api_key": "",
        "default_start_address": "家",
        "buffer_minutes": 10,
        "same_location_remind_before_minutes": 10,
        "default_transit_mode": "driving",  // 出行方式：driving(驾车)、walking(步行)、riding(骑行)、bus(公交)
        "ddl_remind_1day_before": true,
        "ddl_remind_1hour_before": true
    }
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        return default_config
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_map_skill_installed() -> Tuple[bool, str]:
    """检查是否有高德地图技能安装"""
    # 检查 smart-map-guide
    skill_paths = [
        os.path.expanduser("~/AppData/Roaming/npm/node_modules/openclaw/skills/smart-map-guide"),
        os.path.expanduser("~/.openclaw/workspace/skills/smart-map-guide"),
        os.path.expanduser("~/AppData/Roaming/npm/node_modules/openclaw/skills/amap-lbs-skill"),
        os.path.expanduser("~/.openclaw/workspace/skills/amap-lbs-skill"),
    ]
    for path in skill_paths:
        if os.path.exists(path):
            skill_name = os.path.basename(path)
            return True, skill_name
    return False, ""

def calculate_duration(from_address: str, to_address: str, api_key: str = None, mode: str = None) -> Optional[int]:
    """
    计算路程耗时（分钟）
    mode: driving/walking/riding/bus，默认使用配置中的default_transit_mode
    返回 None 表示计算失败
    """
    # 先看有没有已安装的地图技能
    has_skill, skill_name = check_map_skill_installed()
    
    config = get_config()
    if not api_key:
        api_key = config.get("amap_api_key", "")
    if not mode:
        mode = config.get("default_transit_mode", "driving")
    
    # 高德API端点对应不同出行方式
    api_endpoints = {
        "driving": "https://restapi.amap.com/v3/direction/driving",
        "walking": "https://restapi.amap.com/v3/direction/walking",
        "riding": "https://restapi.amap.com/v3/direction/bicycling",
        "bus": "https://restapi.amap.com/v3/direction/transit/integrated",
    }
    
    endpoint = api_endpoints.get(mode, api_endpoints["driving"])
    
    # 如果有安装现成技能，最简单的方式就是调用它
    # 这里直接使用高德 API 自己算，不依赖技能也能工作
    if not api_key:
        print("WARN: No amap_api_key configured, can't calculate duration", file=sys.stderr)
        return None
    
    try:
        import requests
        # 第一步：地理编码获取经纬度
        def geocode(address: str) -> Optional[Tuple[float, float]]:
            url = f"https://restapi.amap.com/v3/geocode/geo?address={address}&key={api_key}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data['status'] == '1' and data['geocodes']:
                location = data['geocodes'][0]['location']
                lng, lat = map(float, location.split(','))
                return lng, lat
            return None
        
        from_loc = geocode(from_address)
        to_loc = geocode(to_address)
        if not from_loc or not to_loc:
            return None
        
        # 第二步：路径规划获取耗时
        if mode == "bus":
            # 公交默认获取第一条路线的耗时
            url = f"{endpoint}?origin={from_loc[0]},{from_loc[1]}&destination={to_loc[0]},{to_loc[1]}&key={api_key}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data['status'] == '1' and data['route'] and data['route']['transits']:
                duration_sec = int(data['route']['transits'][0]['duration'])
                duration_min = int(duration_sec / 60) + 1
                return duration_min
        else:
            url = f"{endpoint}?origin={from_loc[0]},{from_loc[1]}&destination={to_loc[0]},{to_loc[1]}&key={api_key}"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data['status'] == '1' and data['route'] and data['route']['paths']:
                # 耗时是秒，转分钟
                duration_sec = int(data['route']['paths'][0]['duration'])
                duration_min = int(duration_sec / 60) + 1
                return duration_min
        
        return None
    except Exception as e:
        print(f"ERROR: Failed to calculate duration: {e}", file=sys.stderr)
        return None

def calculate_remind_time(target_dt: datetime, duration_min: Optional[int], config: Dict, same_location: bool = False) -> datetime:
    """
 根据路程耗时计算提醒时间
    """
    if same_location:
        # 同地点，固定提前
        return target_dt - timedelta(minutes=config['same_location_remind_before_minutes'])
    
    if not duration_min or duration_min <= 0:
        # 没有耗时数据，默认提前 15 分钟
        return target_dt - timedelta(minutes=15 + config['buffer_minutes'])
    
    # 路程时间 + 缓冲
    total_advance = duration_min + config['buffer_minutes']
    return target_dt - timedelta(minutes=total_advance)

if __name__ == "__main__":
    # 修复Windows中文输出乱码：强制stdout用utf-8
    if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
        sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) >= 3:
        from_addr = sys.argv[1]
        to_addr = sys.argv[2]
        duration = calculate_duration(from_addr, to_addr)
        print(json.dumps({"duration_minutes": duration}, ensure_ascii=False))
    else:
        has, name = check_map_skill_installed()
        print(f"Has installed map skill: {has}, name: {name}")
        config = get_config()
        print(f"Config: {json.dumps(config, ensure_ascii=False)}")
