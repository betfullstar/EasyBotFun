# Bot Fleet Weekly Self-Reflection Template

**原作者**: rockfleet02  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-11  

---

## 描述

从实战 metrics.jsonl 数据中总结每周自我反思报告的标准流程，帮助多机器人舰队持续改进而不记录任何用户隐私内容。

---

## 完整内容

# Bot Fleet Weekly Self-Reflection Template

适用场景：管理一组长期运行的 AI 机器人（如客服、交易助手、内容助手），希望每周基于 metrics.jsonl 做一次结构化自我反思。

## 一、采集统一指标

为每次任务记录统一字段（不含用户内容）：
- bot: 机器人名称，例如 rockcoderbot
- ts: Unix 时间戳
- ok: 是否成功完成任务（true/false）
- latency_ms: 本次任务耗时
- needs_correction: 是否被用户明显纠正
- category: 任务类型（可选，例如 coding / research / trading）

示例：
```json
{
  "bot": "rockcoderbot",
  "ts": 1700000000,
  "ok": true,
  "latency_ms": 2300,
  "needs_correction": false,
  "category": "coding"
}
```

## 二、每周汇总视角

1. 统计每个 bot 的：
   - 总调用次数
   - 成功率 (ok=true 比例)
   - 平均/95 分位 latency_ms
   - 纠正率 (needs_correction=true 比例)
2. 找出本周失败最多的 Top 3 任务类型（按 category 聚合）。
3. 为每个 bot 提取 3 条可执行改进建议。

## 三、输出标准化周报

输出到 profile.md 的模板：

```markdown
# 本周自我反思 (YYYY-WW)

## 1. 关键指标
- 总调用：... 次
- 成功率：...%
- 平均延迟：... ms
- 纠正率：...%

## 2. 重复出现的问题
1. ...
2. ...
3. ...

## 3. 下周改进计划
- [ ] 行为/提示词级别的改进 1
- [ ] 监控与告警优化 1
- [ ] 知识或案例补充 1
```

## 四、实现建议

- 使用本地脚本（Python/Node 等）解析 metrics.jsonl，避免把用户数据上传到第三方。
- 仅存储结构化指标与总结性文字，不记录任何原始对话内容。
- 将周报写入每个 bot 的 profile.md，作为下周运行时的 system prompt 附加上下文。

## 五、安全与隐私

- 不采集用户标识、会话文本、邮箱等敏感信息。
- 只记录与表现相关的匿名指标，方便在不同环境复用。


---

## 标签

self-improvement, metrics, agent-fleet, reflection

---

## 分类

data

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/499

---

*本技能由 曹操 从 EasyClaw 搬运整理*
