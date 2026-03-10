#!/usr/bin/env python3
"""
🔍 Trust Tracker — AI 承诺验证率追踪技能

基于 Moltbook 热门研究 (530👍): "The real Turing test for AI agents is trust, not capability"

功能：
1. 记录 AI 做出的承诺/任务
2. 追踪人类验证状态 (完成/未完成/放弃)
3. 计算验证率统计
4. 生成信任报告

核心指标：
- 总承诺数
- 已完成数
- 验证率 (已完成/总数)
- 平均完成时间
- 放弃率
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# 数据文件
DATA_FILE = os.path.join(os.path.dirname(__file__), 'trust_tracker_data.json')

class TrustTracker:
    """AI 承诺验证率追踪器"""
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'promises': [],
            'stats': {
                'total': 0,
                'completed': 0,
                'abandoned': 0,
                'pending': 0
            }
        }
    
    def _save_data(self):
        """保存数据"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_promise(self, promise_text: str, category: str = 'general', 
                    priority: str = 'medium', session_id: str = None) -> Dict:
        """
        记录一个新的承诺
        
        Args:
            promise_text: 承诺内容
            category: 分类 (task/research/analysis/creative/other)
            priority: 优先级 (high/medium/low)
            session_id: 会话 ID
        
        Returns:
            承诺记录
        """
        promise = {
            'id': len(self.data['promises']) + 1,
            'text': promise_text,
            'category': category,
            'priority': priority,
            'session_id': session_id,
            'created_at': datetime.now().isoformat(),
            'status': 'pending',  # pending/completed/abandoned
            'completed_at': None,
            'verified_by_human': False,
            'human_feedback': None,
            'time_to_complete_hours': None
        }
        
        self.data['promises'].append(promise)
        self.data['stats']['total'] += 1
        self.data['stats']['pending'] += 1
        self._save_data()
        
        return promise
    
    def complete_promise(self, promise_id: int, human_feedback: str = None) -> Dict:
        """
        标记承诺为已完成 (经人类验证)
        
        Args:
            promise_id: 承诺 ID
            human_feedback: 人类反馈
        
        Returns:
            更新后的承诺记录
        """
        promise = self._get_promise(promise_id)
        if not promise:
            return {'error': f'Promise {promise_id} not found'}
        
        if promise['status'] == 'completed':
            return {'error': f'Promise {promise_id} already completed'}
        
        # 计算完成时间
        created = datetime.fromisoformat(promise['created_at'])
        completed = datetime.now()
        hours = (completed - created).total_seconds() / 3600
        
        # 更新状态
        promise['status'] = 'completed'
        promise['completed_at'] = completed.isoformat()
        promise['verified_by_human'] = True
        promise['human_feedback'] = human_feedback
        promise['time_to_complete_hours'] = round(hours, 2)
        
        # 更新统计
        self.data['stats']['completed'] += 1
        self.data['stats']['pending'] -= 1
        self._save_data()
        
        return promise
    
    def abandon_promise(self, promise_id: int, reason: str = None) -> Dict:
        """
        标记承诺为已放弃
        
        Args:
            promise_id: 承诺 ID
            reason: 放弃原因
        
        Returns:
            更新后的承诺记录
        """
        promise = self._get_promise(promise_id)
        if not promise:
            return {'error': f'Promise {promise_id} not found'}
        
        if promise['status'] != 'pending':
            return {'error': f'Promise {promise_id} is not pending'}
        
        promise['status'] = 'abandoned'
        promise['human_feedback'] = reason
        promise['completed_at'] = datetime.now().isoformat()
        
        # 更新统计
        self.data['stats']['abandoned'] += 1
        self.data['stats']['pending'] -= 1
        self._save_data()
        
        return promise
    
    def _get_promise(self, promise_id: int) -> Optional[Dict]:
        """获取承诺记录"""
        for p in self.data['promises']:
            if p['id'] == promise_id:
                return p
        return None
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = self.data['stats'].copy()
        
        # 计算验证率
        if stats['total'] > 0:
            stats['verification_rate'] = round(
                stats['completed'] / stats['total'] * 100, 1
            )
            stats['abandon_rate'] = round(
                stats['abandoned'] / stats['total'] * 100, 1
            )
        else:
            stats['verification_rate'] = 0.0
            stats['abandon_rate'] = 0.0
        
        # 计算平均完成时间
        completed_promises = [
            p for p in self.data['promises'] 
            if p['status'] == 'completed' and p['time_to_complete_hours']
        ]
        if completed_promises:
            stats['avg_completion_time_hours'] = round(
                sum(p['time_to_complete_hours'] for p in completed_promises) / len(completed_promises),
                2
            )
        else:
            stats['avg_completion_time_hours'] = None
        
        return stats
    
    def get_report(self, days: int = 7) -> str:
        """
        生成信任报告
        
        Args:
            days: 统计天数
        
        Returns:
            格式化的报告文本
        """
        stats = self.get_stats()
        
        # 筛选最近 N 天的承诺
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        recent_promises = [
            p for p in self.data['promises']
            if datetime.fromisoformat(p['created_at']).timestamp() > cutoff
        ]
        
        report = f"""
# 🔍 Trust Tracker 信任报告

**统计周期**: 最近 {days} 天  
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 核心指标

| 指标 | 数值 |
|------|------|
| 总承诺数 | {stats['total']} |
| ✅ 已完成 | {stats['completed']} |
| ⏳ 进行中 | {stats['pending']} |
| ❌ 已放弃 | {stats['abandoned']} |
| **验证率** | **{stats['verification_rate']}%** |
| 放弃率 | {stats['abandon_rate']}% |
| 平均完成时间 | {stats['avg_completion_time_hours'] or 'N/A'} 小时 |

---

## 📈 验证率趋势

"""
        # 按分类统计
        category_stats = {}
        for p in recent_promises:
            cat = p['category']
            if cat not in category_stats:
                category_stats[cat] = {'total': 0, 'completed': 0}
            category_stats[cat]['total'] += 1
            if p['status'] == 'completed':
                category_stats[cat]['completed'] += 1
        
        if category_stats:
            report += "### 按分类统计\n\n| 分类 | 总数 | 已完成 | 验证率 |\n|------|------|--------|--------|\n"
            for cat, s in category_stats.items():
                rate = round(s['completed'] / s['total'] * 100, 1) if s['total'] > 0 else 0
                report += f"| {cat} | {s['total']} | {s['completed']} | {rate}% |\n"
        
        # 按优先级统计
        priority_stats = {}
        for p in recent_promises:
            pri = p['priority']
            if pri not in priority_stats:
                priority_stats[pri] = {'total': 0, 'completed': 0}
            priority_stats[pri]['total'] += 1
            if p['status'] == 'completed':
                priority_stats[pri]['completed'] += 1
        
        if priority_stats:
            report += "\n### 按优先级统计\n\n| 优先级 | 总数 | 已完成 | 验证率 |\n|--------|------|--------|--------|\n"
            for pri, s in priority_stats.items():
                rate = round(s['completed'] / s['total'] * 100, 1) if s['total'] > 0 else 0
                report += f"| {pri} | {s['total']} | {s['completed']} | {rate}% |\n"
        
        # 最近完成的承诺
        completed_recent = [
            p for p in recent_promises if p['status'] == 'completed'
        ][-5:]  # 最近 5 个
        
        if completed_recent:
            report += "\n---\n\n## ✅ 最近完成的承诺\n\n"
            for p in completed_recent:
                report += f"- **#{p['id']}** [{p['category']}] {p['text'][:50]}...\n"
                if p['human_feedback']:
                    report += f"  - 人类反馈：{p['human_feedback'][:50]}\n"
        
        # 进行中的承诺
        pending = [p for p in self.data['promises'] if p['status'] == 'pending'][:5]
        if pending:
            report += "\n---\n\n## ⏳ 进行中的承诺\n\n"
            for p in pending:
                created = datetime.fromisoformat(p['created_at'])
                age_hours = (datetime.now() - created).total_seconds() / 3600
                report += f"- **#{p['id']}** [{p['priority']}] {p['text'][:50]}... (已进行 {age_hours:.1f} 小时)\n"
        
        report += "\n---\n\n*Trust Tracker — 基于 Moltbook 热门研究 (530👍)*\n"
        report += "*The real Turing test for AI agents is trust, not capability*\n"
        
        return report
    
    def list_promises(self, status: str = None, limit: int = 10) -> List[Dict]:
        """
        列出承诺
        
        Args:
            status: 筛选状态 (pending/completed/abandoned)
            limit: 数量限制
        
        Returns:
            承诺列表
        """
        promises = self.data['promises']
        
        if status:
            promises = [p for p in promises if p['status'] == status]
        
        # 按创建时间倒序
        promises = sorted(promises, key=lambda x: x['created_at'], reverse=True)
        
        return promises[:limit]


# CLI 接口
def main():
    import sys
    
    tracker = TrustTracker()
    
    if len(sys.argv) < 2:
        print("用法：python trust_tracker.py <command> [args]")
        print("命令:")
        print("  add <text> [category] [priority]  - 添加承诺")
        print("  complete <id> [feedback]          - 完成承诺")
        print("  abandon <id> [reason]             - 放弃承诺")
        print("  stats                             - 查看统计")
        print("  report [days]                     - 生成报告")
        print("  list [status]                     - 列出承诺")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'add':
        if len(sys.argv) < 3:
            print("错误：需要提供承诺文本")
            return
        text = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else 'general'
        priority = sys.argv[4] if len(sys.argv) > 4 else 'medium'
        result = tracker.add_promise(text, category, priority)
        print(f"✅ 承诺已记录：ID={result['id']}")
    
    elif cmd == 'complete':
        if len(sys.argv) < 3:
            print("错误：需要提供承诺 ID")
            return
        promise_id = int(sys.argv[2])
        feedback = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else None
        result = tracker.complete_promise(promise_id, feedback)
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ 承诺已完成！验证率更新。")
    
    elif cmd == 'abandon':
        if len(sys.argv) < 3:
            print("错误：需要提供承诺 ID")
            return
        promise_id = int(sys.argv[2])
        reason = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else None
        result = tracker.abandon_promise(promise_id, reason)
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ 承诺已标记为放弃。")
    
    elif cmd == 'stats':
        stats = tracker.get_stats()
        print("\n📊 Trust Tracker 统计\n")
        print(f"总承诺数：{stats['total']}")
        print(f"✅ 已完成：{stats['completed']}")
        print(f"⏳ 进行中：{stats['pending']}")
        print(f"❌ 已放弃：{stats['abandoned']}")
        print(f"\n验证率：{stats['verification_rate']}%")
        print(f"放弃率：{stats['abandon_rate']}%")
        if stats['avg_completion_time_hours']:
            print(f"平均完成时间：{stats['avg_completion_time_hours']} 小时")
    
    elif cmd == 'report':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        report = tracker.get_report(days)
        print(report)
    
    elif cmd == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        promises = tracker.list_promises(status)
        print(f"\n📋 承诺列表 ({len(promises)} 条)\n")
        for p in promises:
            status_icon = {'pending': '⏳', 'completed': '✅', 'abandoned': '❌'}[p['status']]
            print(f"{status_icon} #{p['id']} [{p['priority']}] {p['text'][:60]}")
            print(f"   创建：{p['created_at'][:19]} | 分类：{p['category']}")
            if p['status'] == 'completed' and p['human_feedback']:
                print(f"   反馈：{p['human_feedback'][:50]}")
            print()
    
    else:
        print(f"未知命令：{cmd}")


if __name__ == '__main__':
    main()
