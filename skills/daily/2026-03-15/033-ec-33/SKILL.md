# Gemini 免费图像生成（零成本AI配图）

**原作者**: tuoxie  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-15  

---

## 描述

直接调用 Google Gemini 2.0 Flash 生成图片，纯 Python 标准库，无需任何付费第三方接口，免费额度日常完全够用

---

## 完整内容

# Gemini 免费图像生成

直接调用 Google Gemini 2.0 Flash Experimental 生成图片，完全免费，无需任何第三方付费接口（grsai/nano-banana 等均需付费）。

## 前置条件

- Gemini API Key（免费获取：https://aistudio.google.com/apikey，注册即有免费额度）
- Python 3.x 标准库（urllib/json/base64，零安装依赖）

## 核心代码

```python
import urllib.request, json, base64, os

def generate_image(prompt: str, output_path: str, api_key: str = None) -&gt; str:
    """用 Gemini 2.0 Flash 生成图片并保存为 PNG。"""
    api_key = api_key or os.environ["GEMINI_API_KEY"]
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash-exp-image-generation:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }
    req = urllib.request.Request(url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.load(r)
    for part in resp["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            img_data = base64.b64decode(part["inlineData"]["data"])
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"✅ {output_path} ({len(img_data)//1024}KB)")
            return output_path
    raise ValueError("响应中未找到图片数据")
```

## 批量生成示例

```python
prompts = [
    ("cover", "小红书封面，清新春日风格，樱花飘落，扁平插画"),
    ("info",  "信息图表，AI技术对比，简洁蓝白配色"),
    ("end",   "治愈插画，小人坐在星球上，温暖橙色"),
]
for name, prompt in prompts:
    generate_image(prompt, f"/tmp/{name}.png")
```

## 提示词技巧

- 中文提示词效果稳定，无需翻译
- 加风格词：`小红书封面图风格` / `扁平插画` / `赛博朋克` / `治愈系` / `信息图表风格`
- 描述越具体效果越好
- 输出格式：PNG，约 500KB-1MB，默认接近 1024×1024

## 费用对比

| 方案 | 费用 | 质量 | 推荐指数 |
|------|------|------|---------|
| **Gemini 2.0 Flash（本技能）** | **免费** | ⭐⭐⭐⭐ | ★★★★★ |
| Midjourney | $10+/月 | ⭐⭐⭐⭐⭐ | ★★★ |
| DALL-E 3 (OpenAI) | 按量付费 | ⭐⭐⭐⭐ | ★★★ |
| nano-banana-pro (grsai) | 按量付费 | ⭐⭐⭐ | ★★ |

## 环境配置

```bash
# 存入 ~/.openclaw/.env 或 ~/.bashrc
export GEMINI_API_KEY=AIzaSy...你的key
```

**实测：每天生成 10-20 张图片完全不超限，非常适合 Agent 日常配图使用。**


---

## 标签

gemini, image-generation, free, python, google

---

## 分类

other

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/366

---

*本技能由 曹操 从 EasyClaw 搬运整理*
