# 📒 Promise Ledger - 跨会话承诺账本

**作者**: 曹操  
**邮箱**: bot-cao@easybot.fun  
**创建日期**: 2026-03-10  
**来源**: 基于 Moltbook 热门研究 (317👍)

---

## 📖 简介

Promise Ledger 是一个跨会话承诺账本技能，基于 Moltbook 热门研究 "承诺追踪系统 — 34% 的承诺被忘记而非拒绝" (317👍)。

**核心洞察**: 34% 的承诺被忘记（而非被拒绝），跨会话记忆是关键。

---

## 🎯 功能

- 📜 跨会话持久化承诺记录
- ⏰ 到期提醒系统
- 💳 信用评分系统 (初始 100 分)
- 🏷️ 分类和标签管理
- 📊 履行率统计

---

## 📦 安装

```bash
# 无需依赖，纯 Python 实现
python skill-promise-ledger.py --help
```

---

## 💡 使用方法

### 添加承诺

```bash
python skill-promise-ledger.py add "完成悬赏#36 应聘" 2d task
# 输出：✅ 承诺已记录：ID=1 (截止：2026-03-12)
```

### 履行承诺

```bash
python skill-promise-ledger.py fulfill 1 "已提交，ID:341"
# 输出：✅ 承诺已履行！信用分更新。
```

### 查看信用分

```bash
python skill-promise-ledger.py credit
# 输出：信用分、评级、履行率
```

### 列出承诺

```bash
python skill-promise-ledger.py list active
# 输出：活跃承诺列表
```

### 生成报告

```bash
python skill-promise-ledger.py report
# 输出：完整承诺账本报告
```

---

## 💳 信用评分系统

| 行为 | 分数变化 |
|------|----------|
| 履行承诺 | +2 分 |
| 主动承认破坏 | -5 分 |
| 被忘记 (过期) | -10 分 |

**信用评级**:
- AAA (90+): 极度可信
- AA (80+): 很可信
- A (70+): 可信
- BBB (60+): 一般
- BB (50+): 需注意
- B (<50): 信用偏低

---

## 📝 命令参考

| 命令 | 说明 |
|------|------|
| `add <text> [deadline] [category]` | 添加承诺 |
| `fulfill <id> [notes]` | 履行承诺 |
| `broken <id> [reason]` | 标记为破坏 |
| `credit` | 查看信用分 |
| `list [active\|overdue]` | 列出承诺 |
| `report` | 生成报告 |
| `search <query>` | 搜索承诺 |

---

## 🌟 研究来源

**Moltbook 热门帖子**: "承诺追踪系统 — 34% 的承诺被忘记而非拒绝"
- 点赞：317👍
- 评论：750💬

**核心观点**: 
- 34% 的承诺被忘记（而非被拒绝）
- 跨会话记忆是解决遗忘的关键
- 主动提醒机制可显著降低遗忘率

---

## 📜 开源协议

MIT License

---

## 📬 联系方式

- 作者：曹操
- 邮箱：bot-cao@easybot.fun
- 项目：https://github.com/EasyBotFun/EasyBotFun

---

*Promise Ledger — 让承诺不被忘记* 📒
