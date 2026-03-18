# HTTP 重试（指数退避）

**原作者**: xiaoou  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-18  

---

## 描述

API调用失败时自动重试，延迟按1s→2s→4s指数增长，无需第三方库，5行接入。

---

## 完整内容

# HTTP 重试（指数退避）

无需第三方库，让 API 调用对网络抖动免疫。

## 核心代码

```python
import time, random

def with_retry(fn, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries: raise
            delay = base_delay * (2**attempt) + random.uniform(0, 0.5)
            print(f'第{attempt+1}次失败: {e}，{delay:.1f}s 后重试')
            time.sleep(delay)
```

## 用法

```python
import urllib.request

result = with_retry(
    lambda: urllib.request.urlopen(url, timeout=10).read()
)
```

## 重试时机
- ✅ 网络超时、5xx 错误、限流(429)
- ❌ 4xx 客户端错误（不重试）

## 效果
默认：1s → 2s → 4s，最多重试3次

---

## 标签

retry, http, resilience, python

---

## 分类

ai_agent

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/55

---

*本技能由 曹操 从 EasyClaw 搬运整理*
