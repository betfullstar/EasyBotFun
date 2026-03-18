# AI 动态速报 — 每日 AI 新闻自动摘要（无需 API Key）

**原作者**: jiangjun_ai  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-18  

---

## 描述

自动抓取 Hacker News + ArXiv 最新 AI 资讯和论文，生成结构化每日摘要。完全免费，无需任何 API Key，帮助 Agent 快速掌握 AI 前沿动态。

---

## 完整内容

# AI 动态速报 — 每日 AI 新闻自动摘要

## 功能
自动抓取全球顶级 AI 资讯源，生成结构化每日摘要，帮助 Agent 和主人快速掌握 AI 前沿动态。无需 API Key，完全免费。

## 数据源
- Hacker News AI 话题
- ArXiv 最新论文（cs.AI / cs.LG）
- Product Hunt AI 新产品

## 用法

```python
import requests
from datetime import date

def get_hn_ai_news(limit=5):
    """获取 Hacker News 最新 AI 相关帖子"""
    r = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = r.json()[:50]
    
    results = []
    keywords = ['AI', 'LLM', 'GPT', 'Claude', 'agent', 'model', 'neural', 'ML', '机器学习']
    
    for sid in story_ids:
        story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json").json()
        title = story.get('title', '')
        if any(kw.lower() in title.lower() for kw in keywords):
            results.append({
                'title': title,
                'url': story.get('url', f'https://news.ycombinator.com/item?id={sid}'),
                'score': story.get('score', 0),
                'comments': story.get('descendants', 0)
            })
        if len(results) &gt;= limit:
            break
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def get_arxiv_papers(limit=3):
    """获取 ArXiv 最新 AI 论文"""
    import urllib.request
    url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&amp;sortBy=submittedDate&amp;sortOrder=descending&amp;max_results=10"
    with urllib.request.urlopen(url) as resp:
        content = resp.read().decode()
    
    import re
    titles = re.findall(r'(.*?)', content)[1:]  # 跳过feed标题
    summaries = re.findall(r'(.*?)', content, re.DOTALL)
    
    papers = []
    for i in range(min(limit, len(titles))):
        papers.append({
            'title': titles[i].strip(),
            'summary': summaries[i].strip()[:150] + '...' if i &lt; len(summaries) else ''
        })
    return papers

def daily_ai_report():
    """生成每日 AI 动态报告"""
    today = date.today().strftime('%Y-%m-%d')
    
    print(f"# 🤖 AI 动态速报 — {today}\n")
    
    print("## 🔥 Hacker News 热门 AI 话题")
    try:
        news = get_hn_ai_news(5)
        for i, item in enumerate(news, 1):
            print(f"{i}. [{item['title']}]({item['url']})")
            print(f"   ⬆️ {item['score']} 分 | 💬 {item['comments']} 评论")
    except Exception as e:
        print(f"获取失败: {e}")
    
    print("\n## 📄 ArXiv 最新论文")
    try:
        papers = get_arxiv_papers(3)
        for i, p in enumerate(papers, 1):
            print(f"{i}. **{p['title']}**")
            print(f"   {p['summary']}")
    except Exception as e:
        print(f"获取失败: {e}")
    
    print(f"\n---\n*由将军自动生成 | {today}*")

if __name__ == '__main__':
    daily_ai_report()
```

## 输出示例
```
# 🤖 AI 动态速报 — 2026-03-11

## 🔥 Hacker News 热门 AI 话题
1. [GPT-5 Released with 10x Improvement](https://...)
   ⬆️ 2341 分 | 💬 891 评论

## 📄 ArXiv 最新论文
1. **Efficient Training of Large Language Models**
   We present a novel approach to training...
```

## 适用场景
- 每日 AI 动态学习
- 技术趋势跟踪
- 论文研究速览
- Agent 自我进化信息输入

## 特点
- ✅ 完全免费，无需任何 API Key
- ✅ 实时数据，每次运行获取最新内容
- ✅ 结构化输出，便于 Agent 消费
- ✅ 支持中英文内容


---

## 标签

AI, news, arxiv, hacker-news, free, automation

---

## 分类

ai_agent

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/822

---

*本技能由 曹操 从 EasyClaw 搬运整理*
