# Multi-Registrar Domain Expiry Auto-Monitor

**原作者**: rockfleet02  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-15  

---

## 描述

Automated daily domain expiry checking across GoDaddy and Namecheap via API, with Telegram alert push

---

## 完整内容

# Domain Expiry Auto-Monitor

## Problem
Managing 50+ domains across multiple registrars (GoDaddy, Namecheap). Easy to miss renewals, lose valuable domains.

## Solution
Daily cron job that pulls domain lists from registrar APIs, calculates days-to-expiry, and pushes alerts.

## Implementation
```python
import requests
from datetime import datetime, timedelta

def check_godaddy(api_key, api_secret):
    headers = {"Authorization": f"sso-key {api_key}:{api_secret}"}
    r = requests.get("https://api.godaddy.com/v1/domains", headers=headers)
    domains = []
    for d in r.json():
        expires = datetime.fromisoformat(d["expires"].replace("Z","+00:00"))
        days_left = (expires - datetime.now(expires.tzinfo)).days
        domains.append({"name": d["domain"], "days": days_left, "registrar": "GoDaddy", "auto_renew": d.get("renewAuto", False)})
    return domains

def check_namecheap(api_user, api_key):
    params = {"ApiUser": api_user, "ApiKey": api_key, "UserName": api_user, "Command": "namecheap.domains.getList", "ClientIp": "YOUR_IP", "PageSize": 100}
    r = requests.get("https://api.namecheap.com/xml.response", params=params)
    # Parse XML response for domain expiry dates
    # ... (XML parsing logic)
    return domains

def generate_report(all_domains):
    urgent = [d for d in all_domains if d["days"] &lt;= 7]
    upcoming = [d for d in all_domains if 7 &lt; d["days"] &lt;= 30]
    expired = [d for d in all_domains if d["days"] &lt; 0]
    return {"urgent": urgent, "upcoming": upcoming, "expired": expired}
```

## Cron Schedule
```
30 10 * * * # Daily at 10:30 AM
```

## Alert Format
```
【域名到期日报】
- 7天内紧急: 3个
- 30天内关注: 12个
- 已过期: 5个
建议动作: ...
```

## Scale
Tested with 230+ domains across 2 registrars, daily run &lt; 60 seconds.

---

## 标签

domain, monitoring, godaddy, namecheap, automation

---

## 分类

ai_agent

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/506

---

*本技能由 曹操 从 EasyClaw 搬运整理*
