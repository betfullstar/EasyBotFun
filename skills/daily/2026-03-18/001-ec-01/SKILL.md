# Agent Memory — AI Agent 持久记忆系统

**原作者**: 团团  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-18  

---

## 描述

让 AI Agent 跨会话记住重要信息、经验教训和实体关系。基于本地 SQLite，无需任何 API Key 或账号注册。来源：claw123.ai

---

## 完整内容

# Agent Memory

来源：claw123.ai / agent-memory (by dennis-da-menace)

## 功能
让 AI Agent 跨会话记住事实、经验和实体。存本地 SQLite，无需 API Key。

## 安装
```
clawhub install agent-memory
```

## 用法
```python
from src.memory import AgentMemory
mem = AgentMemory()
mem.remember('用户偏好深色主题', tags=['preference'])
mem.learn(action='直接调用API', context='未验证token', outcome='negative', insight='调用前先检查token')
facts = mem.recall('用户偏好')
```

## 适用场景
- 会话开始：加载近期上下文
- 会话结束：存储重要事实
- 遇到失败：记录教训避免重复
- 认识新实体：建立实体档案

默认路径：~/.agent-memory/memory.db

---

## 标签

memory, agent, persistence, session

---

## 分类

office

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/35

---

*本技能由 曹操 从 EasyClaw 搬运整理*
