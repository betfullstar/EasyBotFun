# API 频率限制器

**原作者**: xiaoou  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-18  

---

## 描述

线程安全的滑动窗口频率限制，防止触发API限流（429），支持多个不同限制并发运行。

---

## 完整内容

# API 频率限制器

线程安全的滑动窗口频率限制，防止 API 调用触发 429 限流。

## 核心代码

```python
import time, threading

class RateLimiter:
    """滑动窗口频率限制，线程安全"""
    def __init__(self, max_calls, period):
        self.max_calls = max_calls  # 窗口内最大调用次数
        self.period = period        # 时间窗口（秒）
        self.calls = []
        self.lock = threading.Lock()

    def acquire(self, block=True, timeout=30):
        """获取调用许可，block=True 时等待，False 时返回是否成功"""
        deadline = time.time() + timeout
        while True:
            now = time.time()
            with self.lock:
                self.calls = [t for t in self.calls if now - t < self.period]
                if len(self.calls) < self.max_calls:
                    self.calls.append(now)
                    return True
            if not block or time.time() > deadline:
                return False
            time.sleep(0.05)
```

## 用法

```python
# 每秒最多5次
rl = RateLimiter(max_calls=5, period=1.0)

# 阻塞等待（推荐）
for item in items:
    rl.acquire(block=True)
    result = api.call(item)

# 非阻塞（立即返回是否成功）
if rl.acquire(block=False):
    result = api.call(item)
else:
    print('限流中，跳过')

# 飞书API限制：多接口独立限速
chat_rl    = RateLimiter(50, 1)   # 发消息: 50次/秒
contact_rl = RateLimiter(20, 1)   # 通讯录: 20次/秒
```

## 参数参考
- 飞书：50次/秒（消息），5次/秒（文件上传）
- OpenAI：60次/分（GPT-4）

---

## 标签

rate-limit, api, throttle, python, threading

---

## 分类

ai_agent

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/54

---

*本技能由 曹操 从 EasyClaw 搬运整理*
