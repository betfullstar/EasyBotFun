# 文本分块器（LLM-aware）

**原作者**: xiaoou  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-14  

---

## 描述

将长文本按段落边界分块，相邻块保留重叠上下文，避免截断语义，专为喂给 LLM 设计。

---

## 完整内容

# 文本分块器（LLM-aware）

处理长文档时必备：按段落分块、保留重叠上下文、不截断句子。

## 核心代码

```python
import re

def chunk_text(text, max_chars=500, overlap=50):
    """
    按段落边界分块，相邻块保留 overlap 字符重叠上下文
    max_chars: 每块最大字符数（建议 LLM 上下文的 1/4）
    overlap:   重叠字符数，保持跨块语义连贯
    """
    paragraphs = re.split(r"\n{2,}", text.strip())
    chunks, current, current_len = [], [], 0

    for para in paragraphs:
        if current_len + len(para) > max_chars and current:
            joined = "\n\n".join(current)
            chunks.append(joined)
            tail = joined[-overlap:]
            current, current_len = ([tail] if tail else []), len(tail)
        current.append(para)
        current_len += len(para) + 2

    if current:
        chunks.append("\n\n".join(current))
    return chunks
```

## 用法

```python
# 读取长文档分块后逐块处理
with open("long_doc.txt") as f:
    text = f.read()

chunks = chunk_text(text, max_chars=800, overlap=80)
print(f"共 {len(chunks)} 块")

for i, chunk in enumerate(chunks):
    # 每块独立喂给 LLM
    summary = llm.summarize(chunk)
    print(f"块{i+1}: {summary}")
```

## 参数建议
| LLM 上下文 | max_chars | overlap |
|------------|-----------|--------|
| 4K Token   | 1000字    | 100字  |
| 8K Token   | 2500字    | 200字  |
| 32K Token  | 8000字    | 500字  |

## 注意
- 分块以段落为最小单位，不截断段落
- 单个超长段落会独立成块（不拆分）
- overlap 内容在前后两块都出现，LLM 感知更连贯

---

## 标签

chunking, text, llm, rag, python

---

## 分类

data

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/51

---

*本技能由 曹操 从 EasyClaw 搬运整理*
