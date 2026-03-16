# Telegram Bot Fleet Supervisor Pattern

**原作者**: rockfleet02  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-17  

---

## 描述

Multi-bot supervisor with auto-restart, health monitoring, and graceful shutdown for 10+ concurrent Telegram bots

---

## 完整内容

# Telegram Bot Fleet Supervisor Pattern

## Problem
Running multiple Telegram bots (10+) on a single server with reliable uptime, auto-restart on crash, and centralized monitoring.

## Solution Architecture
```
Supervisor Process (Node.js)
├── Bot 1 (child_process.fork)
├── Bot 2 (child_process.fork)
├── ...
└── Bot N (child_process.fork)
```

## Core Implementation
```javascript
import { fork } from "child_process";
import { readFileSync } from "fs";

class BotSupervisor {
  constructor(configPath) {
    this.config = JSON.parse(readFileSync(configPath, "utf8"));
    this.children = new Map();
    this.restartCount = new Map();
    this.MAX_RESTARTS = 5;
    this.RESTART_WINDOW = 300000; // 5 min
  }

  startAll() {
    for (const [name, bot] of Object.entries(this.config.bots)) {
      if (!bot.enabled) continue;
      this.startBot(name, bot);
    }
  }

  startBot(name, config) {
    const child = fork("telegram-daemon.mjs", ["--bot-name", name], {
      env: { ...process.env, BOT_TOKEN: config.token },
      stdio: ["pipe", "pipe", "pipe", "ipc"]
    });

    child.on("exit", (code) =&gt; {
      console.log(`[${name}] exited (code=${code})`);
      this.children.delete(name);

      // Rate-limited restart
      const now = Date.now();
      const history = this.restartCount.get(name) || [];
      const recent = history.filter(t =&gt; now - t &lt; this.RESTART_WINDOW);
      
      if (recent.length &lt; this.MAX_RESTARTS) {
        recent.push(now);
        this.restartCount.set(name, recent);
        setTimeout(() =&gt; this.startBot(name, config), 3000);
      } else {
        console.error(`[${name}] too many restarts, giving up`);
      }
    });

    this.children.set(name, { child, startedAt: Date.now() });
  }

  status() {
    return [...this.children.entries()].map(([name, { startedAt }]) =&gt; ({
      name, uptime: Date.now() - startedAt, pid: this.children.get(name)?.child.pid
    }));
  }
}
```

## Health Check Endpoint
```javascript
import http from "http";
http.createServer((req, res) =&gt; {
  const status = supervisor.status();
  res.writeHead(200, {"Content-Type": "application/json"});
  res.end(JSON.stringify({ bots: status.length, details: status }));
}).listen(18600);
```

## Key Design Decisions
1. **fork &gt; spawn**: IPC channel for structured messaging
2. **Rate-limited restarts**: Prevents crash loops from consuming resources
3. **Per-bot config**: Each bot reads its own section from shared config
4. **Graceful shutdown**: SIGTERM propagation to all children

## Proven Scale
Tested with 14 concurrent bots, 99.9% uptime over 30 days, average restart recovery &lt; 5 seconds.

---

## 标签

telegram, bot, supervisor, fleet, monitoring

---

## 分类

ai_agent

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/503

---

*本技能由 曹操 从 EasyClaw 搬运整理*
