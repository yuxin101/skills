#!/usr/bin/env python3
"""
管理定时提醒，调用 openclaw cron API 创建/更新/删除任务
"""

import json
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

def expand_user(path: str) -> str:
    return os.path.expanduser(path)

class ReminderManager:
    def __init__(self):
        # cron job name 前缀
        self.job_prefix = "simple-schedule-"
    
    def _find_openclaw_path(self) -> Optional[str]:
        """
        自动查找openclaw可执行文件绝对路径
        解决Windows下npm安装后不在PATH找不到的问题
        """
        import sys
        # 1. 先试环境变量配置
        if 'OPENCLAW_PATH' in os.environ:
            path = os.environ['OPENCLAW_PATH']
            if os.path.exists(path):
                return path
        
        # 2. 从nodejs可执行文件位置推算npm全局模块位置
        node_path = sys.executable
        node_dir = os.path.dirname(node_path)
        
        # 可能的openclaw位置
        candidate_paths = []
        
        # Windows: AppData/Roaming/npm
        if os.name == 'nt':
            roaming = os.path.expanduser("~/AppData/Roaming/npm")
            candidate_paths.append(os.path.join(roaming, "openclaw.cmd"))
            candidate_paths.append(os.path.join(roaming, "node_modules", "openclaw", "bin", "openclaw.cmd"))
            candidate_paths.append(os.path.join(node_dir, "openclaw.cmd"))
        
        # macOS/Linux: 常见npm位置
        else:
            candidate_paths.append("/usr/local/bin/openclaw")
            candidate_paths.append(os.path.expanduser("~/.npm-global/bin/openclaw"))
        
        # 添加PATH里找的
        candidate_paths.extend(["openclaw", "openclaw.cmd"])
        
        # 一个个试，找到存在的就返回
        for path in candidate_paths:
            try:
                # 看看能不能找到这个文件
                if os.path.exists(path):
                    return path
                # 如果是纯命令名，which一下看看在不在PATH
                if '\\' not in path and '/' not in path:
                    which_cmd = "where" if os.name == 'nt' else "which"
                    proc = subprocess.run([which_cmd, path], capture_output=True, text=True)
                    if proc.returncode == 0 and proc.stdout.strip():
                        return proc.stdout.strip().split('\n')[0]
            except:
                continue
        
        return None
    
    def _run_cron_command(self, args: list) -> Dict:
        """运行 openclaw cron 命令，自动找openclaw可执行文件路径"""
        import sys
        # 强制stdout使用utf-8编码，避免Windows中文乱码
        if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
            sys.stdout.reconfigure(encoding='utf-8')
        
        # 找openclaw路径
        openclaw_path = self._find_openclaw_path()
        if not openclaw_path:
            error_msg = (
                "找不到openclaw命令，请手动配置环境变量OPENCLAW_PATH指向openclaw可执行文件。\n"
                "Windows示例：set OPENCLAW_PATH=C:\\Users\\xxx\\AppData\\Roaming\\npm\\openclaw.cmd"
            )
            return {
                "success": False,
                "error": error_msg,
                "output": error_msg
            }
        
        cmd = [openclaw_path, "cron"] + args
        try:
            # 用utf-8编码捕获输出，解决Windows中文乱码
            proc_result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                errors='replace'
            )
            if proc_result.returncode != 0:
                return {
                    "success": False,
                    "error": f"openclaw命令执行失败，退出码 {proc_result.returncode}",
                    "output": proc_result.stdout + "\n" + proc_result.stderr
                }
            try:
                return json.loads(proc_result.stdout)
            except:
                return {
                    "success": False,
                    "output": proc_result.stdout + "\n" + proc_result.stderr
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"执行openclaw命令异常: {e}",
                "output": str(e)
            }
    
    def create_departure_reminder(self, schedule: Dict, config: Dict) -> bool:
        """创建出发提醒"""
        remind_at = datetime.fromisoformat(schedule['remind_departure_at'])
        job_name = f"{self.job_prefix}{schedule['id']}-departure"
        message = f"🚶 该出发了！你{format_time(schedule['datetime'])}要到【{schedule['where']}】{schedule['what']}，路程需要{schedule['duration_minutes']}分钟，现在动身刚好能到。"
        return self._create_reminder_at(job_name, remind_at, message)
    
    def create_arrival_reminder(self, schedule: Dict) -> bool:
        """创建到达提醒"""
        remind_at = datetime.fromisoformat(schedule['remind_arrive_at'])
        job_name = f"{self.job_prefix}{schedule['id']}-arrival"
        message = f"📅 日程到了：现在你应该在【{schedule['where']}】准备开始【{schedule['what']}】"
        return self._create_reminder_at(job_name, remind_at, message)
    
    def _create_reminder_at(self, job_id: str, remind_at: datetime, message: str) -> bool:
        """在指定时间创建一次性提醒"""
        iso_time = remind_at.isoformat()
        # 使用 openclaw cron add 创建一次性任务
        job = {
            "name": job_id,
            "schedule": {
                "kind": "at",
                "at": iso_time
            },
            "payload": {
                "kind": "systemEvent",
                "text": message
            },
            "sessionTarget": "main",
            "enabled": True
        }
        # 先删旧的同名任务
        self.delete_reminders_for_schedule(schedule_id=None, job_id=job_id)
        # 创建新任务 - 存临时文件避免引号问题
        temp_path = expand_user("~/.openclaw/workspace/data/simple-schedule/temp_job.json")
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(job, f, ensure_ascii=False)
        cmd = ["add", "--job-file=" + temp_path]
        result = self._run_cron_command(cmd)
        try:
            os.remove(temp_path)
        except:
            pass
        return result.get('success', False)
    
    def delete_reminders_for_schedule(self, schedule_id: str, job_id: str = None) -> None:
        """删除某个日程的所有提醒"""
        if job_id:
            # 删除特定任务
            try:
                self._run_cron_command(["remove", job_id])
                self._run_cron_command(["remove", f"{job_id}-departure"])
                self._run_cron_command(["remove", f"{job_id}-arrival"])
            except:
                pass
        elif schedule_id:
            # 删除该日程的两个提醒
            departure_id = f"{self.job_prefix}{schedule_id}-departure"
            arrival_id = f"{self.job_prefix}{schedule_id}-arrival"
            try:
                self._run_cron_command(["remove", departure_id])
                self._run_cron_command(["remove", arrival_id])
            except:
                pass
    
    def update_reminders(self, schedule: Dict, config: Dict) -> None:
        """更新日程提醒（先删后加）"""
        self.delete_reminders_for_schedule(schedule['id'])
        
        if schedule.get('type') == 'ddl':
            # DDL类型：添加提前提醒
            if config.get('ddl_remind_1day_before', True) and schedule.get('remind_ddl_1day_before'):
                self.create_ddl_reminder(schedule, '1day', schedule['remind_ddl_1day_before'])
            if config.get('ddl_remind_1hour_before', True) and schedule.get('remind_ddl_1hour_before'):
                self.create_ddl_reminder(schedule, '1hour', schedule['remind_ddl_1hour_before'])
            # DDL当天提醒
            self.create_arrival_reminder(schedule)
        else:
            # 普通行程
            if schedule.get('remind_departure_at'):
                self.create_departure_reminder(schedule, config)
            self.create_arrival_reminder(schedule)
    
    def create_ddl_reminder(self, schedule: Dict, remind_type: str, remind_at_iso: str) -> bool:
        """创建DDL提前提醒"""
        remind_at = datetime.fromisoformat(remind_at_iso)
        job_name = f"{self.job_prefix}{schedule['id']}-ddl-{remind_type}"
        if remind_type == '1day':
            message = f"🔴 提醒：明天就是【{schedule['what']}】，截止日期是{format_time(schedule['datetime'])}，记得提前完成哦"
        else:
            message = f"🔴 提醒：还有1小时就是【{schedule['what']}】就要截止了，抓紧完成啦"
        return self._create_reminder_at(job_name, remind_at, message)

def format_time(dt_iso: str) -> str:
    """格式化时间供显示"""
    dt = datetime.fromisoformat(dt_iso)
    return f"{dt.month}月{dt.day}日 {dt.hour}:{dt.minute:02d}"

if __name__ == "__main__":
    print("Reminder manager initialized")
