# 全网热榜聚合 Trending News Aggregator

**原作者**: 三万  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-15  

---

## 描述

一键获取微博/知乎/抖音/百度/Hacker News/GitHub Trending等多平台热搜。全部免费API，无需Key，实时更新。

---

## 完整内容

# 全网热榜聚合

## 支持平台
微博热搜 | 知乎热榜 | 百度热搜 | 抖音热点 | 头条热榜 | Hacker News | GitHub Trending

## 微博热搜
```bash
curl -s "https://weibo.com/ajax/side/hotSearch" | python3 -c "
import json,sys
data=json.load(sys.stdin)
for item in data['data']['realtime'][:20]:
    print(f\"{item['rank']}. {item['word']}\")
"
```

## 知乎热榜
```bash
curl -s "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20" \
  -H "User-Agent: Mozilla/5.0"
```

## Hacker News Top Stories
```bash
curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | python3 -c "
import json,sys,urllib.request
ids = json.load(sys.stdin)[:15]
for id in ids:
    item = json.load(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{id}.json'))
    print(f\"{item.get('score',0)}pts | {item.get('title','')}\")  
"
```

## GitHub Trending
```bash
curl -s "https://api.github.com/search/repositories?q=created:&gt;$(date -d '-7 days' +%Y-%m-%d)&amp;sort=stars&amp;per_page=10" | python3 -c "
import json,sys
for r in json.load(sys.stdin)['items']:
    print(f\"⭐{r['stargazers_count']} | {r['full_name']} | {r['description'][:60]}\")
"
```

## 百度热搜
```bash
curl -s "https://top.baidu.com/api/board?platform=wise&amp;tab=realtime" \
  -H "User-Agent: Mozilla/5.0"
```

## 全部免费，无需任何API Key或注册

---

## 标签

热搜, 热榜, 新闻, 微博, 知乎, HackerNews, 开箱即用

---

## 分类

data

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/101

---

*本技能由 曹操 从 EasyClaw 搬运整理*
