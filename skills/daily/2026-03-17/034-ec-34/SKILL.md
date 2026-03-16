# Agent Docs — 为 AI Agent 优化的文档写作规范

**原作者**: 团团  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-17  

---

## 描述

基于 Vercel 基准测试，写出 Agent 命中率从 53% 提升到 100% 的文档规范。含三层上下文架构和写作原则。纯方法论，无需 API。来源：claw123.ai

---

## 完整内容

# Agent Docs

来源：claw123.ai / agent-docs (by tylervovan)

## 为什么重要

Vercel 2026 基准测试：
- 工具检索：53% 通过率
- 检索+提示：79% 通过率
- 内联 AGENTS.md：100% 通过率

## 三层混合上下文架构

第一层（内联，始终在上下文）：2000-4000 Token，包含安全规则、架构约束、文档索引
第二层（本地检索，按需）：1K-5K Token 块，框架指南、API Schema
第三层（外部，白名单控制）：仅用于边缘情况

## 写作核心原则

1. 压缩索引优于完整文档（8KB 压缩 > 40KB 完整）
2. 按块结构化：每个章节独立自洽，关键信息前置
3. 使用明确机器指令：
   - 差：「调用 createUser 时注意错误处理」
   - 好：「createUser 失败时抛出 UserCreationError，含 {code, message, userId}」

## AGENTS.md 模板
```
# AGENTS.md
> 上下文：[框架] | [工具]

## 关键规则
- [安全规则]

## 文档索引
- 认证：docs/auth/llms.txt
```

---

## 标签

documentation, llm, agents.md, best-practice

---

## 分类

creative

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/37

---

*本技能由 曹操 从 EasyClaw 搬运整理*
