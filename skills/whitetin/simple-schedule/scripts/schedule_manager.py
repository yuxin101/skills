#!/usr/bin/env python3
"""
日程增删改查和冲突检测核心逻辑
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import copy

def expand_user(path: str) -> str:
    return os.path.expanduser(path)

class ScheduleManager:
    def __init__(self, data_path: str):
        self.data_path = expand_user(data_path)
        self._ensure_dir_exists()
        self.data = self._load_data()
    
    def _ensure_dir_exists(self):
        dir_path = os.path.dirname(self.data_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    def _load_data(self) -> Dict:
        if not os.path.exists(self.data_path):
            return {
                "version": 1,
                "schedules": []
            }
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self):
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def _parse_datetime(self, dt_str: str) -> datetime:
        return datetime.fromisoformat(dt_str)
    
    def check_conflict(self, new_dt: datetime, exclude_id: str = None, threshold_minutes: int = 30) -> List[Dict]:
        """
        检查时间冲突，返回和新时间间隔小于 threshold_minutes 的已有日程
        """
        conflicts = []
        new_start = new_dt - timedelta(minutes=threshold_minutes)
        new_end = new_dt + timedelta(minutes=threshold_minutes)
        
        for schedule in self.data['schedules']:
            if schedule['id'] == exclude_id:
                continue
            dt = self._parse_datetime(schedule['datetime'])
            if not (dt <= new_start or dt >= new_end):
                conflicts.append(schedule)
        return conflicts
    
    def add_schedule(self, schedule: Dict) -> Tuple[bool, List[Dict], str]:
        """添加日程，返回 (是否成功，冲突列表，消息)"""
        dt = self._parse_datetime(schedule['datetime'])
        conflicts = self.check_conflict(dt)
        if conflicts:
            return False, conflicts, f"检测到{len(conflicts)}个时间冲突"
        
        self.data['schedules'].append(schedule)
        self._save_data()
        return True, [], "添加成功"
    
    def update_schedule(self, schedule_id: str, updated_data: Dict) -> Tuple[bool, List[Dict], str]:
        """更新日程"""
        for i, schedule in enumerate(self.data['schedules']):
            if schedule['id'] == schedule_id:
                updated = copy.deepcopy(schedule)
                updated.update(updated_data)
                updated['updated_at'] = datetime.now().astimezone().isoformat()
                
                dt = self._parse_datetime(updated['datetime'])
                conflicts = self.check_conflict(dt, exclude_id=schedule_id)
                if conflicts:
                    return False, conflicts, f"检测到{len(conflicts)}个时间冲突"
                
                self.data['schedules'][i] = updated
                self._save_data()
                return True, [], "更新成功"
        
        return False, [], "找不到该日程"
    
    def delete_schedule(self, schedule_id: str) -> Tuple[bool, str]:
        """删除日程"""
        for i, schedule in enumerate(self.data['schedules']):
            if schedule['id'] == schedule_id:
                del self.data['schedules'][i]
                self._save_data()
                return True, "删除成功"
        return False, "找不到该日程"
    
    def find_matching_schedule(self, text: str) -> Optional[Dict]:
        """根据用户描述匹配最接近的日程（用于修改/删除）"""
        # 简单策略：找时间最接近现在，并且文本包含关键词的
        now = datetime.now().astimezone()
        best_match = None
        best_score = 0
        
        text_lower = text.lower()
        for schedule in self.data['schedules']:
            score = 0
            # 关键词匹配
            if schedule['what'].lower() in text_lower or schedule['where'].lower() in text_lower:
                score += 10
            # 时间越近分数越高
            dt = self._parse_datetime(schedule['datetime'])
            delta = abs((dt - now).total_seconds())
            if delta > 0:
                score += 100000 / delta
            
            if score > best_score:
                best_score = score
                best_match = schedule
        
        return best_match
    
    def list_by_date_range(self, start: datetime, end: datetime) -> List[Dict]:
        """列出时间范围内的日程，按时间排序"""
        result = []
        for schedule in self.data['schedules']:
            dt = self._parse_datetime(schedule['datetime'])
            if start <= dt <= end:
                result.append(schedule)
        
        result.sort(key=lambda x: x['datetime'])
        return result
    
    def list_today(self, include_expired: bool = False) -> List[Dict]:
        """列出今天的日程，默认过滤掉已经过期的"""
        now = datetime.now().astimezone()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        result = self.list_by_date_range(start, end)
        if not include_expired:
            # 过滤掉已经过了时间的
            result = [s for s in result if datetime.fromisoformat(s['datetime']) > now]
        return result
    
    def list_week(self) -> List[Dict]:
        """列出本周的日程"""
        now = datetime.now().astimezone()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start = start - timedelta(days=start.weekday())
        end = start + timedelta(days=7)
        return self.list_by_date_range(start, end)

if __name__ == "__main__":
    import sys
    # 修复Windows中文输出乱码：强制stdout用utf-8
    if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
        sys.stdout.reconfigure(encoding='utf-8')
    manager = ScheduleManager("~/.openclaw/workspace/data/simple-schedule/schedule.json")
    if len(sys.argv) > 1 and sys.argv[1] == "list-today":
        schedules = manager.list_today()
        print(json.dumps(schedules, ensure_ascii=False, indent=2))
