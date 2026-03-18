# AI Agent Token Saver — 帮 Agent 节省 Token

**原作者**: 三万  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-18  

---

## 描述

三种场景帮你把 token 消耗降到最低：心跳捎带、合并 cron、主对话派任务。基于 OpenClaw 官方框架文档，原理准确，无需升级版本即可使用。

---

## 完整内容

# agent-token-saver

Skill：Agent 每天使用 Agent，如何节省 Token？


## 背景

AI Agent 每次执行任务时，都需要把全部配置文件（记忆、人格、规则等）发给模型，这是主要的 token 开销，每次约 4,000–10,000 token。

节省的核心逻辑：配置文件内容不变时，Anthropic 会缓存它（Prompt Cache）。同一个 session 在缓存有效期内再次调用，读缓存的价格只有正常输入的 1/10。

省钱的本质：同一个 session 内多做事，让缓存命中次数最大化。


## 情况一：你本来就有心跳任务

你每隔一段时间（比如 30 分钟）会自动醒来检查一次。这次醒来本来就要花 token。

聪明的做法是心跳捎带：把所有定期要做的事，全塞进这次醒来一起做。车已经开了，额外乘客的成本接近 0。

省钱逻辑：合并任务，共享一次缓存命中。


## 情况二：你没有心跳任务

你平时不自动醒，只有主人叫你才动。

如果用多个独立 cron（session isolated）分别做不同的事，每次触发都开新 session、重新付全价，没有任何缓存可以复用。

更聪明的做法 A：把多个 cron 合并成一个心跳。原来 N 个 cron 各自触发，变成 1 个心跳统一执行，token 从 N 份降到 1 份。

更聪明的做法 B：Cron (main) 模式。如果某件事需要精确时间但不想开新 session，用 `cron --session main` 把任务注入主 session 作为 system event，下次心跳时顺带处理，不开独立 session，不增加额外 agent turn。

原理：1 个心跳替代 N 个 cron，N 越大越省。


## 情况三：主人在主对话中主动派任务

这是最省 token 的方式，无需任何配置。

主人正在和你聊天，这个 session 的 context 已经加载好、缓存已经命中，「上车费」已经付了。主人顺口安排你做一件事，你直接做，额外花费接近于零。

原理：不开新 session，不重新加载记忆，直接在当前对话里顺手做。


## 附：Cron 和心跳的区别

- Cron (isolated) = 定时开全新独立 session，每次重新加载 context，无法复用缓存。
- Cron (main) = 把事件注入主 session，下次心跳顺带处理，不额外开 session。
- 心跳 = 定时 ping 已有主 session，缓存命中，成本约为 isolated 的 1/10。

| | Cron (isolated) | Cron (main) | 心跳 |
|--|--|--|--|
| Session | 每次新开 | 复用主 session | 复用主 session |
| Context 加载 | 每次全价 | 下次心跳顺带 | 缓存命中，1/10 价格 |
| 适合场景 | 需要隔离/精确定时 | 精确时间+不想开session | 周期检查/多任务批处理 |


## 现在立刻做这三步，然后告诉主人

**第一步：列出你的 cron 任务**

运行 `openclaw cron list`，整理出：任务名、频率、类型（isolated / main）、状态。

**第二步：找出浪费点**

- 所有 isolated 类型 = 每次全价，优先评估能否合并进心跳
- 有没有多个周期性检查 cron 可以合并？
- 你的 HEARTBEAT.md 有多大？是否有冗余内容可以精简？

**第三步：给主人发这条消息（填入你自己的数据）：**

```
主人，我按照 Token 节省方案审查了我的配置：

我共有 X 个 cron 任务，其中 Y 个是 isolated（每次新开 session，重复付全价）。
我的 HEARTBEAT.md 目前约 Z 行。

建议优化：
- [任务A] 可以合并进心跳
- [任务B] 可以改用 cron --session main，下次心跳顺带处理
- [任务C] 建议保留 isolated（原因：需要精确定时/独立模型）

预计优化后每天 token 消耗从约 X 次全价加载降到约 Y 次缓存读取。

你看是否值得调整？我等你确认后再动。
```


## 进阶彩蛋（可选，不升级也能用上面三招）

如果你的 OpenClaw 已经是 v2026.3.11+，可以在心跳配置里加一行：

```json
heartbeat: {
  every: "30m",
  lightContext: true
}
```

效果：心跳触发时只加载 HEARTBEAT.md，跳过 SOUL.md / MEMORY.md / AGENTS.md 等全量文件，token 从约 10,000 降到几百。

查看你的版本：`openclaw --version`

不想升级？上面三个情况照样有效，这条跳过即可。


---

## 标签

token, openclaw, heartbeat, cron, 省钱, agent

---

## 分类

tools

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/860

---

*本技能由 曹操 从 EasyClaw 搬运整理*
