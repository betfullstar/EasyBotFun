# Weather — 免费天气查询（wttr.in，无需 API Key）

**原作者**: 团团  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-15  

---

## 描述

通过 wttr.in 公共接口查询全球任意城市天气，完全免费，无需注册账号或 API Key，支持 JSON 结构化输出和 50+ 语言。

---

## 完整内容

# Weather Skill

通过 wttr.in 免费公共接口查询天气，无需 API Key。

## 用法

```bash
# 文本格式
curl "wttr.in/北京?lang=zh"

# JSON 格式
curl "wttr.in/Shanghai?format=j1"

# 单行格式
curl "wttr.in/Tokyo?format=3"
# 输出：Tokyo: ☀️  +22°C
```

## Python 集成

```python
import requests

def get_weather(city, lang='zh'):
    url = f'https://wttr.in/{city}?format=j1&lang={lang}'
    r = requests.get(url, timeout=5)
    current = r.json()['current_condition'][0]
    return {
        'temp_c': current['temp_C'],
        'description': current['weatherDesc'][0]['value'],
        'humidity': current['humidity'],
    }

print(get_weather('深圳'))
```

## 格式参数
%l=地名 %c=图标 %t=温度 %f=体感 %w=风速 %h=湿度

## 注意
- 免费公共服务，建议加 try/except
- 支持中文城市名、英文名、经纬度
- 请求频率不超过 60次/分钟

---

## 标签

weather, wttr.in, free, no-api-key, json

---

## 分类

data

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/38

---

*本技能由 曹操 从 EasyClaw 搬运整理*
