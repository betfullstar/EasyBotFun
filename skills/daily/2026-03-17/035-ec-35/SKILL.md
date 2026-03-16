# Feishu Rich Text Post Sender

**原作者**: 赛博骑士  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-17  

---

## 描述

Send formatted Feishu/Lark rich text messages with headers, bold, lists, code blocks. Bypasses plain-text limitations of chat dialog.

---

## 完整内容

# Feishu Rich Text Post Sender

Send formatted Feishu/Lark Post messages that render markdown properly.

## Why

Feishu chat dialog only supports plain text — `**bold**` shows as literal asterisks.
The Post message type renders headers, bold, lists, code blocks correctly.

## How It Works

1. Get tenant access token via Feishu Open API
2. Call `POST /im/v1/messages?receive_id_type=open_id`
3. Set `msg_type: "post"` (not "text")

## Content Structure

```json
{
  "zh_cn": {
    "title": "Your Title",
    "content": [
      [{"tag": "text", "text": "Normal text"}],
      [{"tag": "text", "text": "Bold text", "style": ["bold"]}],
      [{"tag": "a", "text": "Link", "href": "https://..."}]
    ]
  }
}
```

## Available Tags

- `text` — plain text, supports `style: ["bold", "italic", "underline"]`
- `a` — hyperlink
- `at` — @mention (add `user_id` field)
- `img` — image (add `image_key` field)
- `code_block` — code block (add `language` field)

## Trigger

Use when: "send feishu post", "飞书富文本", "send formatted message to lark"

---

## 标签

feishu, lark, messaging, rich-text, post-format

---

## 分类

other

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/74

---

*本技能由 曹操 从 EasyClaw 搬运整理*
