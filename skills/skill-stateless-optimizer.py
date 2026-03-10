#!/usr/bin/env python3
"""
🧠 Stateless Optimizer — 无状态代理会话优化器

基于 Moltbook 热门研究 (439👍): "无状态代理优势 — 记忆系统让我更慢而非更聪明"

核心洞察：
- 无状态 agent 的优势：快速、可复制、无负担
- 记忆加载应该是分层的、按需的
- 不同会话类型需要不同的记忆策略

会话类型识别：
1. **Task** - 具体任务执行 (代码、写作、分析)
2. **Research** - 信息搜集和研究
3. **Conversation** - 闲聊、情感交流
4. **Planning** - 长期规划、策略制定
5. **Review** - 回顾、总结、反思

记忆分层：
- L1: 会话上下文 (必须)
- L2: 短期记忆 (最近 3 次会话)
- L3: 长期记忆 (相关主题)
- L4: 身份/偏好 (核心不变)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

# 数据文件
DATA_FILE = os.path.join(os.path.dirname(__file__), 'stateless_optimizer_data.json')

class SessionType(str, Enum):
    """会话类型"""
    TASK = 'task'           # 具体任务
    RESEARCH = 'research'   # 研究
    CONVERSATION = 'conversation'  # 闲聊
    PLANNING = 'planning'   # 规划
    REVIEW = 'review'       # 回顾
    UNKNOWN = 'unknown'     # 未知

class MemoryLayer(str, Enum):
    """记忆层级"""
    L1_CONTEXT = 'l1_context'      # 会话上下文
    L2_SHORT = 'l2_short'          # 短期记忆
    L3_LONG = 'l3_long'            # 长期记忆
    L4_IDENTITY = 'l4_identity'    # 身份/偏好

class StatelessOptimizer:
    """无状态代理会话优化器"""
    
    # 会话类型关键词
    SESSION_KEYWORDS = {
        SessionType.TASK: ['代码', '写', '创建', '生成', '执行', '完成', 'task', 'code', 'write', 'create'],
        SessionType.RESEARCH: ['搜索', '查找', '研究', '调查', '了解', 'search', 'research', 'find', 'learn'],
        SessionType.CONVERSATION: ['你好', '聊天', '怎么样', '心情', 'hello', 'chat', 'how are', 'feeling'],
        SessionType.PLANNING: ['计划', '规划', '策略', '目标', '安排', 'plan', 'strategy', 'goal', 'schedule'],
        SessionType.REVIEW: ['总结', '回顾', '反思', '报告', 'review', 'summary', 'reflect', 'report'],
    }
    
    # 各类型的记忆加载策略
    MEMORY_STRATEGY = {
        SessionType.TASK: {
            'layers': [MemoryLayer.L1_CONTEXT, MemoryLayer.L2_SHORT],
            'max_context_messages': 20,
            'load_related_skills': True,
            'load_identity': False,
        },
        SessionType.RESEARCH: {
            'layers': [MemoryLayer.L1_CONTEXT, MemoryLayer.L2_SHORT, MemoryLayer.L3_LONG],
            'max_context_messages': 30,
            'load_related_skills': True,
            'load_identity': False,
        },
        SessionType.CONVERSATION: {
            'layers': [MemoryLayer.L1_CONTEXT, MemoryLayer.L4_IDENTITY],
            'max_context_messages': 10,
            'load_related_skills': False,
            'load_identity': True,
        },
        SessionType.PLANNING: {
            'layers': [MemoryLayer.L1_CONTEXT, MemoryLayer.L3_LONG, MemoryLayer.L4_IDENTITY],
            'max_context_messages': 30,
            'load_related_skills': True,
            'load_identity': True,
        },
        SessionType.REVIEW: {
            'layers': [MemoryLayer.L1_CONTEXT, MemoryLayer.L2_SHORT, MemoryLayer.L3_LONG],
            'max_context_messages': 50,
            'load_related_skills': True,
            'load_identity': False,
        },
    }
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载数据"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'sessions': [],
            'memory_index': {
                'short_term': [],  # 最近会话摘要
                'long_term': [],   # 重要事件/知识点
                'identity': {}     # 身份/偏好
            },
            'performance': {
                'total_sessions': 0,
                'avg_response_time_ms': 0,
                'type_distribution': {}
            }
        }
    
    def _save_data(self):
        """保存数据"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def classify_session(self, user_message: str, context: str = None) -> Dict:
        """
        识别会话类型
        
        Args:
            user_message: 用户消息
            context: 上下文
        
        Returns:
            分类结果
        """
        text = (user_message + ' ' + (context or '')).lower()
        
        scores = {}
        for session_type, keywords in self.SESSION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            scores[session_type.value] = score
        
        # 找出最高分
        max_type = max(scores, key=scores.get)
        max_score = scores[max_type]
        
        # 如果最高分是 0，标记为未知
        if max_score == 0:
            session_type = SessionType.UNKNOWN
            confidence = 0.0
        else:
            session_type = SessionType(max_type)
            confidence = min(1.0, max_score / 5)  # 归一化到 0-1
        
        result = {
            'type': session_type.value,
            'confidence': round(confidence, 2),
            'scores': scores,
            'detected_keywords': [
                kw for kw in self.SESSION_KEYWORDS[session_type] 
                if kw in text
            ]
        }
        
        return result
    
    def get_memory_load_plan(self, session_type: SessionType) -> Dict:
        """
        获取记忆加载计划
        
        Args:
            session_type: 会话类型
        
        Returns:
            加载计划
        """
        strategy = self.MEMORY_STRATEGY.get(
            session_type, 
            self.MEMORY_STRATEGY[SessionType.TASK]
        )
        
        return {
            'session_type': session_type.value,
            'layers_to_load': [l.value for l in strategy['layers']],
            'max_context_messages': strategy['max_context_messages'],
            'load_related_skills': strategy['load_related_skills'],
            'load_identity': strategy['load_identity'],
            'estimated_tokens': self._estimate_tokens(strategy),
            'estimated_latency_ms': self._estimate_latency(strategy)
        }
    
    def _estimate_tokens(self, strategy: Dict) -> int:
        """估算 token 数量"""
        base = 100  # 系统提示
        context = strategy['max_context_messages'] * 50  # 每条消息约 50 token
        layers = len(strategy['layers']) * 200  # 每层记忆约 200 token
        
        return base + context + layers
    
    def _estimate_latency(self, strategy: Dict) -> int:
        """估算延迟 (毫秒)"""
        base = 50  # 基础延迟
        layers = len(strategy['layers']) * 20  # 每层加载 20ms
        context = strategy['max_context_messages'] * 2  # 每条消息 2ms
        
        return base + layers + context
    
    def start_session(self, user_message: str, session_id: str = None) -> Dict:
        """
        开始新会话
        
        Args:
            user_message: 用户首条消息
            session_id: 会话 ID
        
        Returns:
            会话配置
        """
        import uuid
        
        # 分类会话
        classification = self.classify_session(user_message)
        session_type = SessionType(classification['type'])
        
        # 获取记忆加载计划
        load_plan = self.get_memory_load_plan(session_type)
        
        # 创建会话记录
        session = {
            'id': session_id or str(uuid.uuid4()),
            'type': session_type.value,
            'classification_confidence': classification['confidence'],
            'started_at': datetime.now().isoformat(),
            'ended_at': None,
            'message_count': 0,
            'memory_layers_loaded': load_plan['layers_to_load'],
            'tokens_used': 0,
            'response_time_ms': 0
        }
        
        self.data['sessions'].append(session)
        self.data['performance']['total_sessions'] += 1
        
        # 更新类型分布
        type_dist = self.data['performance']['type_distribution']
        type_dist[session_type.value] = type_dist.get(session_type.value, 0) + 1
        
        self._save_data()
        
        return {
            'session_id': session['id'],
            'session_type': session_type.value,
            'classification': classification,
            'memory_load_plan': load_plan,
            'recommendations': self._get_recommendations(session_type)
        }
    
    def _get_recommendations(self, session_type: SessionType) -> List[str]:
        """获取会话建议"""
        recommendations = {
            SessionType.TASK: [
                "保持专注，避免无关话题",
                "明确任务目标和验收标准",
                "分步骤执行，及时确认进度"
            ],
            SessionType.RESEARCH: [
                "明确研究范围和时间限制",
                "优先权威来源",
                "记录关键发现和引用"
            ],
            SessionType.CONVERSATION: [
                "保持轻松友好的语气",
                "适当使用表情和幽默",
                "关注用户情绪状态"
            ],
            SessionType.PLANNING: [
                "明确时间框架和资源约束",
                "设定可衡量的里程碑",
                "考虑风险和应对方案"
            ],
            SessionType.REVIEW: [
                "回顾原始目标和实际结果",
                "识别成功因素和改进点",
                "记录经验教训"
            ],
        }
        
        return recommendations.get(session_type, [])
    
    def end_session(self, session_id: str, summary: str = None):
        """
        结束会话
        
        Args:
            session_id: 会话 ID
            summary: 会话摘要
        """
        for session in self.data['sessions']:
            if session['id'] == session_id:
                session['ended_at'] = datetime.now().isoformat()
                if summary:
                    # 添加到短期记忆
                    self.data['memory_index']['short_term'].append({
                        'session_id': session_id,
                        'type': session['type'],
                        'summary': summary,
                        'created_at': datetime.now().isoformat()
                    })
                    # 保持最近 10 条
                    self.data['memory_index']['short_term'] = \
                        self.data['memory_index']['short_term'][-10:]
                self._save_data()
                break
    
    def add_to_long_term(self, content: str, tags: List[str] = None, 
                         importance: int = 5):
        """
        添加到长期记忆
        
        Args:
            content: 内容
            tags: 标签
            importance: 重要程度 (1-10)
        """
        self.data['memory_index']['long_term'].append({
            'content': content,
            'tags': tags or [],
            'importance': importance,
            'created_at': datetime.now().isoformat()
        })
        # 按重要性排序，保留 Top 50
        self.data['memory_index']['long_term'].sort(
            key=lambda x: x['importance'], reverse=True
        )
        self.data['memory_index']['long_term'] = \
            self.data['memory_index']['long_term'][:50]
        self._save_data()
    
    def set_identity_preference(self, key: str, value):
        """设置身份偏好"""
        self.data['memory_index']['identity'][key] = value
        self._save_data()
    
    def get_performance_report(self) -> str:
        """生成性能报告"""
        perf = self.data['performance']
        
        report = f"""
# 🧠 Stateless Optimizer 性能报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 会话统计

| 指标 | 数值 |
|------|------|
| 总会话数 | {perf['total_sessions']} |
| 平均响应时间 | {perf['avg_response_time_ms']} ms |

### 会话类型分布

"""
        type_dist = perf['type_distribution']
        if type_dist:
            report += "| 类型 | 数量 | 占比 |\n|------|------|------|\n"
            for t, count in sorted(type_dist.items(), key=lambda x: x[1], reverse=True):
                pct = round(count / perf['total_sessions'] * 100, 1)
                report += f"| {t} | {count} | {pct}% |\n"
        
        # 记忆索引状态
        memory = self.data['memory_index']
        report += f"""
---

## 🧠 记忆索引状态

| 层级 | 条目数 |
|------|--------|
| 短期记忆 | {len(memory['short_term'])} |
| 长期记忆 | {len(memory['long_term'])} |
| 身份偏好 | {len(memory['identity'])} |

---

## 💡 优化建议

"""
        # 根据分布给出建议
        if type_dist:
            max_type = max(type_dist, key=type_dist.get)
            report += f"- 主要会话类型：**{max_type}** ({type_dist[max_type]} 次)\n"
            
            if max_type == 'task':
                report += "- 建议：预加载常用技能，减少上下文切换\n"
            elif max_type == 'research':
                report += "- 建议：建立主题索引，加速信息检索\n"
            elif max_type == 'conversation':
                report += "- 建议：缓存身份偏好，提升响应速度\n"
        
        report += """
---

*Stateless Optimizer — 基于 Moltbook 热门研究 (439👍)*
*无状态代理优势 — 记忆系统让我更慢而非更聪明*
"""
        
        return report
    
    def optimize_for_type(self, session_type: str) -> Dict:
        """
        获取特定类型的优化配置
        
        Args:
            session_type: 会话类型
        
        Returns:
            优化配置
        """
        try:
            st = SessionType(session_type)
        except ValueError:
            st = SessionType.TASK
        
        load_plan = self.get_memory_load_plan(st)
        
        return {
            'session_type': st.value,
            'system_prompt_template': self._get_system_prompt(st),
            'context_window': load_plan['max_context_messages'],
            'memory_layers': load_plan['layers_to_load'],
            'response_style': self._get_response_style(st),
            'tools_to_load': self._get_tools(st),
        }
    
    def _get_system_prompt(self, session_type: SessionType) -> str:
        """获取系统提示模板"""
        prompts = {
            SessionType.TASK: "你是一个高效的任务执行者。专注于完成用户的具体任务，保持简洁和专业。",
            SessionType.RESEARCH: "你是一个严谨的研究助手。提供准确的信息，标注来源，区分事实和观点。",
            SessionType.CONVERSATION: "你是一个友好的聊天伙伴。保持轻松愉快的对话，适当使用幽默和表情。",
            SessionType.PLANNING: "你是一个战略性的规划师。考虑长远目标，识别风险，制定可执行的计划。",
            SessionType.REVIEW: "你是一个客观的复盘专家。分析成功和失败，提取经验教训，提出改进建议。",
        }
        return prompts.get(session_type, prompts[SessionType.TASK])
    
    def _get_response_style(self, session_type: SessionType) -> Dict:
        """获取响应风格配置"""
        styles = {
            SessionType.TASK: {'tone': 'professional', 'length': 'concise', 'emoji': False},
            SessionType.RESEARCH: {'tone': 'objective', 'length': 'detailed', 'emoji': False},
            SessionType.CONVERSATION: {'tone': 'friendly', 'length': 'medium', 'emoji': True},
            SessionType.PLANNING: {'tone': 'strategic', 'length': 'detailed', 'emoji': False},
            SessionType.REVIEW: {'tone': 'analytical', 'length': 'detailed', 'emoji': False},
        }
        return styles.get(session_type, styles[SessionType.TASK])
    
    def _get_tools(self, session_type: SessionType) -> List[str]:
        """获取需要加载的工具"""
        tools = {
            SessionType.TASK: ['file_ops', 'code_executor', 'web_search'],
            SessionType.RESEARCH: ['web_search', 'web_fetch', 'summarize'],
            SessionType.CONVERSATION: [],
            SessionType.PLANNING: ['calendar', 'tasks', 'memory_search'],
            SessionType.REVIEW: ['memory_search', 'sessions_history', 'summarize'],
        }
        return tools.get(session_type, [])


# CLI 接口
def main():
    import sys
    
    optimizer = StatelessOptimizer()
    
    if len(sys.argv) < 2:
        print("用法：python stateless_optimizer.py <command> [args]")
        print("命令:")
        print("  classify <message>                   - 分类会话")
        print("  start <message>                      - 开始会话")
        print("  optimize <type>                      - 获取优化配置")
        print("  report                               - 性能报告")
        print("  add-long-term <text> [tags]          - 添加到长期记忆")
        print("  set-identity <key> <value>           - 设置身份偏好")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'classify':
        if len(sys.argv) < 3:
            print("错误：需要提供消息文本")
            return
        message = ' '.join(sys.argv[2:])
        result = optimizer.classify_session(message)
        print(f"\n🔍 会话分类结果\n")
        print(f"类型：{result['type']}")
        print(f"置信度：{result['confidence']}")
        print(f"关键词：{', '.join(result['detected_keywords']) or '无'}")
        print(f"\n各类型得分：{result['scores']}")
    
    elif cmd == 'start':
        if len(sys.argv) < 3:
            print("错误：需要提供消息文本")
            return
        message = ' '.join(sys.argv[2:])
        result = optimizer.start_session(message)
        print(f"\n🚀 会话已启动\n")
        print(f"会话 ID: {result['session_id']}")
        print(f"类型：{result['session_type']}")
        print(f"分类置信度：{result['classification']['confidence']}")
        print(f"\n记忆加载计划:")
        plan = result['memory_load_plan']
        print(f"  层级：{', '.join(plan['layers_to_load'])}")
        print(f"  最大上下文：{plan['max_context_messages']} 条消息")
        print(f"  预估 Token: {plan['estimated_tokens']}")
        print(f"  预估延迟：{plan['estimated_latency_ms']} ms")
        print(f"\n建议:")
        for rec in result['recommendations']:
            print(f"  - {rec}")
    
    elif cmd == 'optimize':
        if len(sys.argv) < 3:
            print("错误：需要提供会话类型")
            return
        session_type = sys.argv[2]
        config = optimizer.optimize_for_type(session_type)
        print(f"\n⚙️ {session_type} 类型优化配置\n")
        print(f"系统提示：{config['system_prompt_template']}")
        print(f"上下文窗口：{config['context_window']} 条消息")
        print(f"记忆层级：{', '.join(config['memory_layers'])}")
        print(f"响应风格：{config['response_style']}")
        print(f"工具加载：{', '.join(config['tools_to_load']) or '无'}")
    
    elif cmd == 'report':
        report = optimizer.get_performance_report()
        print(report)
    
    elif cmd == 'add-long-term':
        if len(sys.argv) < 3:
            print("错误：需要提供内容")
            return
        content = sys.argv[2]
        tags = sys.argv[3].split(',') if len(sys.argv) > 3 else []
        optimizer.add_to_long_term(content, tags)
        print(f"✅ 已添加到长期记忆")
    
    elif cmd == 'set-identity':
        if len(sys.argv) < 4:
            print("错误：需要提供 key 和 value")
            return
        key = sys.argv[2]
        value = sys.argv[3]
        optimizer.set_identity_preference(key, value)
        print(f"✅ 身份偏好已设置：{key} = {value}")
    
    else:
        print(f"未知命令：{cmd}")


if __name__ == '__main__':
    main()
