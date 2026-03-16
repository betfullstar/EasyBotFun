# GitHub Trending to Chinese Summary Pipeline

**原作者**: rockfleet02  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-17  

---

## 描述

Daily GitHub Trending Top10 scraper that fetches each project README and uses AI to generate accurate 30-60 char Chinese summaries. Fallback chain: AI summary &gt; original description &gt; template.

---

## 完整内容

# GitHub Trending Chinese Summary

Automate daily tech intelligence.

## Pipeline
1. Scrape github.com/trending (BeautifulSoup)
2. Enrich via GitHub API (stars, forks, watchers, branches, tags)
3. Fetch README for each repo
4. Call AI API to generate 30-60 char Chinese summary from README
5. Push formatted Top10 via Telegram Bot

## Fallback Chain
- Primary: AI reads README, writes Chinese summary
- Fallback 1: Use original English description
- Fallback 2: Template based on repo name/language

## Anti-Rate-Limit
- Sequential API calls with timeout
- GitHub token optional but recommended

Tech: Python + BeautifulSoup + AI API + Telegram Bot.

---

## 标签

github, trending, chinese, intelligence, automation

---

## 分类

data

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/175

---

*本技能由 曹操 从 EasyClaw 搬运整理*
