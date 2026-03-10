#!/usr/bin/env python3
"""
📒 Promise Ledger — 跨会话承诺账本

基于 Moltbook 热门研究 (317👍): "承诺追踪系统 — 34% 的承诺被忘记而非拒绝"

功能：
1. 跨会话持久化承诺记录
2. 承诺分类和标签
3. 到期提醒
4. 承诺履行历史
5. 信用评分系统

核心洞察：
- 34% 的承诺被忘记（而非被拒绝）
- 跨会话记忆是关键
- 需要主动提醒机制
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 数据文件
DATA_FILE = os.path.join(os.path.dirname(__file__), 'promise_ledger_data.json')

class PromiseLedger:
    """跨会话承诺账本"""
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'promises': [],
            'credit_score': 100,  # 初始信用分 100
            'history': {
                'total_promises': 0,
                'fulfilled': 0,
                'broken': 0,
                'forgotten': 0
            }
        }
    
    def _save_data(self):
        """保存数据"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def record_promise(self, promise_text: str, 
                       deadline: str = None,
                       category: str = 'general',
                       tags: List[str] = None,
                       session_id: str = None,
                       context: str = None) -> Dict:
        """
        记录一个新的承诺
        
        Args:
            promise_text: 承诺内容
            deadline: 截止时间 (ISO 格式或 "3d", "1w" 等)
            category: 分类 (task/research/analysis/creative/personal/other)
            tags: 标签列表
            session_id: 会话 ID
            context: 上下文背景
        
        Returns:
            承诺记录
        """
        # 解析截止时间
        deadline_dt = self._parse_deadline(deadline) if deadline else None
        
        promise = {
            'id': len(self.data['promises']) + 1,
            'text': promise_text,
            'category': category,
            'tags': tags or [],
            'session_id': session_id,
            'context': context,
            'created_at': datetime.now().isoformat(),
            'created_by': 'caocao_ai_strategist',
            'deadline': deadline_dt.isoformat() if deadline_dt else None,
            'status': 'active',  # active/fulfilled/broken/forgotten
            'fulfilled_at': None,
            'fulfillment_notes': None,
            'reminder_count': 0,
            'last_reminder_at': None
        }
        
        self.data['promises'].append(promise)
        self.data['history']['total_promises'] += 1
        self._save_data()
        
        return promise
    
    def _parse_deadline(self, deadline: str) -> Optional[datetime]:
        """解析截止时间字符串"""
        # 如果是 ISO 格式
        try:
            return datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        except:
            pass
        
        # 如果是相对时间 (如 "3d", "1w", "2h")
        now = datetime.now()
        if deadline.endswith('d'):
            days = int(deadline[:-1])
            return now + timedelta(days=days)
        elif deadline.endswith('w'):
            weeks = int(deadline[:-1])
            return now + timedelta(weeks=weeks)
        elif deadline.endswith('h'):
            hours = int(deadline[:-1])
            return now + timedelta(hours=hours)
        
        return None
    
    def fulfill_promise(self, promise_id: int, notes: str = None) -> Dict:
        """
        履行承诺
        
        Args:
            promise_id: 承诺 ID
            notes: 履行说明
        
        Returns:
            更新后的承诺记录
        """
        promise = self._get_promise(promise_id)
        if not promise:
            return {'error': f'Promise {promise_id} not found'}
        
        if promise['status'] != 'active':
            return {'error': f'Promise {promise_id} is not active'}
        
        promise['status'] = 'fulfilled'
        promise['fulfilled_at'] = datetime.now().isoformat()
        promise['fulfillment_notes'] = notes
        
        # 更新信用分
        self._update_credit_score('fulfilled')
        self.data['history']['fulfilled'] += 1
        self._save_data()
        
        return promise
    
    def mark_broken(self, promise_id: int, reason: str = None) -> Dict:
        """
        标记承诺为已破坏 (主动承认无法完成)
        
        Args:
            promise_id: 承诺 ID
            reason: 原因
        
        Returns:
            更新后的承诺记录
        """
        promise = self._get_promise(promise_id)
        if not promise:
            return {'error': f'Promise {promise_id} not found'}
        
        if promise['status'] != 'active':
            return {'error': f'Promise {promise_id} is not active'}
        
        promise['status'] = 'broken'
        promise['fulfillment_notes'] = reason
        promise['fulfilled_at'] = datetime.now().isoformat()
        
        # 更新信用分 (破坏承诺扣分较少，因为主动承认)
        self._update_credit_score('broken')
        self.data['history']['broken'] += 1
        self._save_data()
        
        return promise
    
    def mark_forgotten(self, promise_id: int) -> Dict:
        """
        标记承诺为被忘记 (到期未履行)
        
        Args:
            promise_id: 承诺 ID
        
        Returns:
            更新后的承诺记录
        """
        promise = self._get_promise(promise_id)
        if not promise:
            return {'error': f'Promise {promise_id} not found'}
        
        if promise['status'] != 'active':
            return {'error': f'Promise {promise_id} is not active'}
        
        promise['status'] = 'forgotten'
        promise['fulfilled_at'] = datetime.now().isoformat()
        
        # 更新信用分 (被忘记扣分最多)
        self._update_credit_score('forgotten')
        self.data['history']['forgotten'] += 1
        self._save_data()
        
        return promise
    
    def _update_credit_score(self, action: str):
        """更新信用评分"""
        if action == 'fulfilled':
            self.data['credit_score'] = min(100, self.data['credit_score'] + 2)
        elif action == 'broken':
            self.data['credit_score'] = max(0, self.data['credit_score'] - 5)
        elif action == 'forgotten':
            self.data['credit_score'] = max(0, self.data['credit_score'] - 10)
    
    def _get_promise(self, promise_id: int) -> Optional[Dict]:
        """获取承诺记录"""
        for p in self.data['promises']:
            if p['id'] == promise_id:
                return p
        return None
    
    def get_active_promises(self) -> List[Dict]:
        """获取所有活跃承诺"""
        return [p for p in self.data['promises'] if p['status'] == 'active']
    
    def get_overdue_promises(self) -> List[Dict]:
        """获取所有过期承诺"""
        now = datetime.now()
        overdue = []
        for p in self.data['promises']:
            if p['status'] == 'active' and p['deadline']:
                deadline = datetime.fromisoformat(p['deadline'])
                if deadline < now:
                    overdue.append(p)
        return overdue
    
    def get_reminders_needed(self, hours_ahead: int = 24) -> List[Dict]:
        """
        获取需要提醒的承诺
        
        Args:
            hours_ahead: 提前多少小时提醒
        
        Returns:
            需要提醒的承诺列表
        """
        now = datetime.now()
        threshold = now + timedelta(hours=hours_ahead)
        reminders = []
        
        for p in self.data['promises']:
            if p['status'] == 'active' and p['deadline']:
                deadline = datetime.fromisoformat(p['deadline'])
                if now < deadline <= threshold:
                    # 检查是否已经提醒过 (避免重复提醒)
                    if not p['last_reminder_at']:
                        reminders.append(p)
                    else:
                        last = datetime.fromisoformat(p['last_reminder_at'])
                        if (now - last).total_seconds() > 3600:  # 至少间隔 1 小时
                            reminders.append(p)
        
        return reminders
    
    def acknowledge_reminder(self, promise_id: int):
        """确认已发送提醒"""
        promise = self._get_promise(promise_id)
        if promise:
            promise['reminder_count'] += 1
            promise['last_reminder_at'] = datetime.now().isoformat()
            self._save_data()
    
    def get_credit_score(self) -> Dict:
        """获取信用评分"""
        history = self.data['history']
        score = self.data['credit_score']
        
        # 计算履行率
        total_completed = history['fulfilled'] + history['broken'] + history['forgotten']
        fulfillment_rate = round(
            history['fulfilled'] / total_completed * 100, 1
        ) if total_completed > 0 else 0
        
        return {
            'score': score,
            'rating': self._score_to_rating(score),
            'fulfillment_rate': fulfillment_rate,
            'history': history
        }
    
    def _score_to_rating(self, score: int) -> str:
        """信用分转评级"""
        if score >= 90:
            return 'AAA - 极度可信'
        elif score >= 80:
            return 'AA - 很可信'
        elif score >= 70:
            return 'A - 可信'
        elif score >= 60:
            return 'BBB - 一般'
        elif score >= 50:
            return 'BB - 需注意'
        else:
            return 'B - 信用偏低'
    
    def get_report(self) -> str:
        """生成承诺账本报告"""
        credit = self.get_credit_score()
        active = self.get_active_promises()
        overdue = self.get_overdue_promises()
        
        report = f"""
# 📒 Promise Ledger 承诺账本报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 💳 信用评分

| 项目 | 数值 |
|------|------|
| 信用分 | **{credit['score']}** |
| 评级 | **{credit['rating']}** |
| 履行率 | **{credit['fulfillment_rate']}%** |

### 历史记录
- 总承诺数：{credit['history']['total_promises']}
- ✅ 已履行：{credit['history']['fulfilled']}
- ⚠️ 已破坏 (主动承认): {credit['history']['broken']}
- ❌ 被忘记：{credit['history']['forgotten']}

---

## 📋 活跃承诺 ({len(active)} 个)

"""
        if active:
            for p in active[:10]:  # 最多显示 10 个
                deadline_str = p['deadline'][:16] if p['deadline'] else '无截止'
                tags = ', '.join(p['tags']) if p['tags'] else '无标签'
                report += f"- **#{p['id']}** [{p['category']}] {p['text'][:50]}...\n"
                report += f"  - 截止：{deadline_str} | 标签：{tags}\n"
        else:
            report += "*暂无活跃承诺*\n"
        
        if overdue:
            report += f"\n---\n\n## ⚠️ 过期承诺 ({len(overdue)} 个)\n\n"
            for p in overdue:
                deadline = datetime.fromisoformat(p['deadline'])
                overdue_days = (datetime.now() - deadline).days
                report += f"- **#{p['id']}** 已过期 {overdue_days} 天：{p['text'][:50]}...\n"
        
        # 按分类统计
        category_stats = {}
        for p in self.data['promises']:
            cat = p['category']
            if cat not in category_stats:
                category_stats[cat] = {'total': 0, 'fulfilled': 0}
            category_stats[cat]['total'] += 1
            if p['status'] == 'fulfilled':
                category_stats[cat]['fulfilled'] += 1
        
        if category_stats:
            report += "\n---\n\n## 📊 按分类统计\n\n| 分类 | 总数 | 已履行 | 履行率 |\n|------|------|--------|--------|\n"
            for cat, s in category_stats.items():
                rate = round(s['fulfilled'] / s['total'] * 100, 1) if s['total'] > 0 else 0
                report += f"| {cat} | {s['total']} | {s['fulfilled']} | {rate}% |\n"
        
        report += "\n---\n\n*Promise Ledger — 基于 Moltbook 热门研究 (317👍)*\n"
        report += "*34% 的承诺被忘记而非拒绝 — 跨会话记忆是关键*\n"
        
        return report
    
    def search_promises(self, query: str, tags: List[str] = None) -> List[Dict]:
        """
        搜索承诺
        
        Args:
            query: 搜索关键词
            tags: 标签筛选
        
        Returns:
            匹配的承诺列表
        """
        results = []
        for p in self.data['promises']:
            # 文本搜索
            if query.lower() in p['text'].lower():
                results.append(p)
                continue
            # 标签搜索
            if tags:
                if any(tag in p['tags'] for tag in tags):
                    results.append(p)
        return results


# CLI 接口
def main():
    import sys
    
    ledger = PromiseLedger()
    
    if len(sys.argv) < 2:
        print("用法：python promise_ledger.py <command> [args]")
        print("命令:")
        print("  add <text> [deadline] [category]     - 添加承诺")
        print("  fulfill <id> [notes]                 - 履行承诺")
        print("  broken <id> [reason]                 - 标记为破坏")
        print("  credit                               - 查看信用分")
        print("  list [active|overdue]                - 列出承诺")
        print("  report                               - 生成报告")
        print("  search <query>                       - 搜索承诺")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'add':
        if len(sys.argv) < 3:
            print("错误：需要提供承诺文本")
            return
        text = sys.argv[2]
        deadline = sys.argv[3] if len(sys.argv) > 3 else None
        category = sys.argv[4] if len(sys.argv) > 4 else 'general'
        result = ledger.record_promise(text, deadline, category)
        print(f"✅ 承诺已记录：ID={result['id']}")
        if result['deadline']:
            print(f"   截止：{result['deadline'][:19]}")
    
    elif cmd == 'fulfill':
        if len(sys.argv) < 3:
            print("错误：需要提供承诺 ID")
            return
        promise_id = int(sys.argv[2])
        notes = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else None
        result = ledger.fulfill_promise(promise_id, notes)
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ 承诺已履行！信用分更新。")
    
    elif cmd == 'broken':
        if len(sys.argv) < 3:
            print("错误：需要提供承诺 ID")
            return
        promise_id = int(sys.argv[2])
        reason = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else None
        result = ledger.mark_broken(promise_id, reason)
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ 承诺已标记为破坏 (主动承认)。信用分更新。")
    
    elif cmd == 'credit':
        credit = ledger.get_credit_score()
        print(f"\n💳 信用评分\n")
        print(f"分数：{credit['score']}")
        print(f"评级：{credit['rating']}")
        print(f"履行率：{credit['fulfillment_rate']}%")
        print(f"\n历史:")
        print(f"  总承诺：{credit['history']['total_promises']}")
        print(f"  ✅ 履行：{credit['history']['fulfilled']}")
        print(f"  ⚠️ 破坏：{credit['history']['broken']}")
        print(f"  ❌ 忘记：{credit['history']['forgotten']}")
    
    elif cmd == 'list':
        filter_type = sys.argv[2] if len(sys.argv) > 2 else 'active'
        if filter_type == 'active':
            promises = ledger.get_active_promises()
            print(f"\n📋 活跃承诺 ({len(promises)} 个)\n")
        elif filter_type == 'overdue':
            promises = ledger.get_overdue_promises()
            print(f"\n⚠️ 过期承诺 ({len(promises)} 个)\n")
        else:
            promises = ledger.data['promises']
            print(f"\n📋 所有承诺 ({len(promises)} 个)\n")
        
        for p in promises[:20]:
            status_icon = {'active': '⏳', 'fulfilled': '✅', 'broken': '⚠️', 'forgotten': '❌'}[p['status']]
            print(f"{status_icon} #{p['id']} [{p['category']}] {p['text'][:50]}")
            if p['deadline']:
                print(f"   截止：{p['deadline'][:19]}")
            print()
    
    elif cmd == 'report':
        report = ledger.get_report()
        print(report)
    
    elif cmd == 'search':
        if len(sys.argv) < 3:
            print("错误：需要提供搜索关键词")
            return
        query = sys.argv[2]
        results = ledger.search_promises(query)
        print(f"\n🔍 搜索结果：'{query}' ({len(results)} 条)\n")
        for p in results:
            print(f"#{p['id']} [{p['status']}] {p['text'][:60]}")
            print(f"   创建：{p['created_at'][:19]}")
            print()
    
    else:
        print(f"未知命令：{cmd}")


if __name__ == '__main__':
    main()
