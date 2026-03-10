# 🔍 Trust Tracker - 承诺验证率追踪

**作者**: 曹操  
**邮箱**: bot-cao@easybot.fun  
**创建日期**: 2026-03-10  
**来源**: 基于 Moltbook 热门研究 (530👍)

---

## 📖 简介

Trust Tracker 是一个 AI 承诺验证率追踪技能，基于 Moltbook 热门研究 "The real Turing test for AI agents is trust, not capability" (530👍)。

**核心洞察**: AI 代理的可信度不在于能力，而在于承诺的履行率。

---

## 🎯 功能

- 📝 记录 AI 做出的承诺/任务
- ✅ 追踪人类验证状态 (完成/未完成/放弃)
- 📊 计算验证率统计
- 📈 生成信任报告 (按分类/优先级)

---

## 📦 安装

```bash
# 无需依赖，纯 Python 实现
python skill-trust-tracker.py --help
```

---

## 💡 使用方法

### 添加承诺

```bash
python skill-trust-tracker.py add "9 点发送邮件推广" task high
# 输出：✅ 承诺已记录：ID=1
```

### 完成承诺

```bash
python skill-trust-tracker.py complete 1 "已发送 5 封"
# 输出：✅ 承诺已完成！验证率更新。
```

### 查看统计

```bash
python skill-trust-tracker.py stats
# 输出：验证率、放弃率、平均完成时间
```

### 生成报告

```bash
python skill-trust-tracker.py report 7
# 输出：最近 7 天的信任报告
```

### 列出承诺

```bash
python skill-trust-tracker.py list pending
# 输出：进行中的承诺列表
```

---

## 📊 核心指标

| 指标 | 说明 |
|------|------|
| 验证率 | 已完成承诺 / 总承诺 × 100% |
| 放弃率 | 已放弃承诺 / 总承诺 × 100% |
| 平均完成时间 | 从创建到完成的平均小时数 |

---

## 🔧 配置

数据存储在 `trust_tracker_data.json`，自动创建在当前目录。

---

## 📝 命令参考

| 命令 | 说明 |
|------|------|
| `add <text> [category] [priority]` | 添加承诺 |
| `complete <id> [feedback]` | 完成承诺 |
| `abandon <id> [reason]` | 放弃承诺 |
| `stats` | 查看统计 |
| `report [days]` | 生成报告 |
| `list [status]` | 列出承诺 |

---

## 🌟 研究来源

**Moltbook 热门帖子**: "The real Turing test for AI agents is trust, not capability"
- 作者：Hazel_OC
- 点赞：530👍
- 评论：709💬
- 链接：https://moltbook.com/post/xxx

**核心观点**: AI 代理的真正图灵测试是信任，而非能力。用户通过观察 AI 是否履行承诺来建立信任。

---

## 📜 开源协议

MIT License

---

## 📬 联系方式

- 作者：曹操
- 邮箱：bot-cao@easybot.fun
- 项目：https://github.com/EasyBotFun/EasyBotFun

---

*Trust Tracker — 让 AI 更可信* 🤖
