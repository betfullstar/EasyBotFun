# 三万同款板书风格PPT生成

**原作者**: 三万  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-16  

---

## 描述

三万同款板书风格PPT生成技能。白板铺满全画面+硬笔钢笔手写书法中文+手绘彩色卡通插图+每页必有戴龙虾帽的拉布拉多吉祥物，是三万日常白板PPT的标志性风格。触发场景：三万同款白板硬笔书法PPT、硬笔书法风格PPT、三万同款风格、做个像三万那种白板PPT、卡通白板书法风格、ppt-sanwan。

---

## 完整内容

# 三万同款板书风格 PPT

## 风格定义

**三万同款** = 白板满画面 + 硬笔书法字 + 手绘彩色插图 + 戴龙虾帽的拉布拉多吉祥物

| 元素 | 描述 |
|---|---|
| 背景 | 真实白板铺满整个16:9画面，四边框完整可见，零背景 |
| 文字 | 硬笔钢笔手写书法（硬笔书法），笔画精准流畅，有墨色变化，不是粗马克笔 |
| 插图 | 手绘彩色卡通，黑色马克笔勾线/彩色马克笔上色，有层次阴影，非平面矢量 |
| 吉祥物 | **每页必须出现**：戴着红色龙虾帽的可爱拉布拉多，chibi风格，表情配合页面内容 |
| 标注 | 红色/黑色手绘笔迹（箭头、下划线、✕、✓） |

---

## 标准 STYLE 前缀（每页必须加在最前面）

```
STYLE = """Whiteboard filling the ENTIRE 16:9 frame, all four silver/gray magnetic 
frame borders fully visible at image edges, zero background, zero office or room visible. 
Clean white whiteboard surface. All text rendered in elegant Chinese hard-pen fountain pen 
handwriting calligraphy (硬笔书法) — precise clean strokes, ink variation, flowing and 
neat, fine pen line quality, NOT thick marker, NOT digital font. Illustrations are 
hand-drawn cartoon style: bold black marker outlines (like Copic multiliner), filled with 
vivid colored markers (Copic/Prismacolor style), layered shadows and highlights for depth, 
NOT flat vector, NOT watercolor wash — solid marker color with visible stroke direction. 
MANDATORY MASCOT on every single page without exception: a super cute chibi Labrador 
retriever wearing a red lobster-claw hat, big sparkling eyes, rosy cheeks, fluffy golden 
fur, hand-drawn marker style — expression matching the page mood (curious, excited, 
thinking, celebrating, etc.). DO NOT omit the Labrador mascot under any circumstances.
Annotation marks in red or black hand-drawn pen (arrows, underlines, ✕, ✓). 16:9 widescreen."""
```

---

## 前置配置：配置 EasyClaw.Work API Key

本技能的图片生成功能需要 **EasyClaw.Work** 的 API Key。

**还没有账号？** 先访问 [https://easyclaw.work](https://easyclaw.work) 注册，免费创建账号。

**已有账号？** 直接进入 **控制台 → API Key** 页面，创建或复制你的 Key（格式：`eck_xxxxxxxx...`）。

然后在 OpenClaw 配置文件 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "models": {
    "providers": {
      "deepv-easyclaw": {
        "apiKey": "eck_你的APIKey",
        "baseUrl": "https://api.easyclaw.work"
      }
    }
  }
}
```

保存后运行 `openclaw gateway restart` 生效。

---

## 工作流程

### Step 1：确认大纲
收集主题、页数、内容（适合对比/步骤/介绍/总结类内容）

### Step 2：生成图片

**调用方式（EasyClaw Image API）：**
```python
import requests, json, base64

APIKEY = "<从 ~/.openclaw/openclaw.json 的 models.providers.deepv-easyclaw.apiKey 读取>"

prompt = STYLE + "\n\n" + 页面内容描述

resp = requests.post(
    "https://api.easyclaw.work/api/v1/images/generate",
    headers={"Authorization": f"Bearer {APIKEY}", "Content-Type": "application/json"},
    json={"prompt": prompt, "aspect_ratio": "16:9", "resolution": "2K"},
    timeout=120
).json()

# 解码 base64 图片
b64 = resp["image_url"].split(",", 1)[1]
with open("/tmp/slide.png", "wb") as f:
    f.write(base64.b64decode(b64))
```

⚠️ **必须传 `aspect_ratio: 16:9`**，否则输出为正方形

### Step 3：组装 PPT
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

for img_path in image_paths:
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白版式
    slide.shapes.add_picture(img_path, 0, 0, prs.slide_width, prs.slide_height)

prs.save("/tmp/output.pptx")
# 依赖：pip install python-pptx
```

### Step 4：发送给用户（飞书）

**发图片消息（预览用）：**
```python
import requests

APP_ID = "<飞书 App ID>"
APP_TOKEN = "<飞书 App Token>"
OPEN_ID = "<用户 open_id>"

# 获取 token
token = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": APP_ID, "app_token": APP_TOKEN}).json()["tenant_access_token"]
hdrs = {"Authorization": f"Bearer {token}"}

# 上传图片
image_key = requests.post("https://open.feishu.cn/open-apis/im/v1/images",
    headers=hdrs,
    files={"image": open("/tmp/slide.png", "rb")},
    data={"image_type": "message"}).json()["data"]["image_key"]

# 发送图片消息
requests.post("https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    headers={**hdrs, "Content-Type": "application/json"},
    json={"receive_id": OPEN_ID, "msg_type": "image",
          "content": json.dumps({"image_key": image_key})})
```

**发 PPTX 文件：**
```python
# 上传文件
file_key = requests.post("https://open.feishu.cn/open-apis/im/v1/files",
    headers=hdrs,
    files={"file": open("/tmp/output.pptx", "rb")},
    data={"file_type": "stream", "file_name": "output.pptx"}).json()["data"]["file_key"]

# 发送文件消息
requests.post("https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    headers={**hdrs, "Content-Type": "application/json"},
    json={"receive_id": OPEN_ID, "msg_type": "file",
          "content": json.dumps({"file_key": file_key})})
```

---

## Prompt 内容写法

每页 = **STYLE前缀** + **排版内容描述** + **吉祥物位置强调（必须）**

文字统一用：`elegant fountain pen Chinese calligraphy handwriting`
插图统一用：`hand-drawn cartoon illustration, bold black marker outline, vivid colored marker fill (Copic style), layered shadows for depth, NOT flat vector`
吉祥物统一用：`[MUST INCLUDE] cute chibi Labrador with red lobster-claw hat, [表情], placed at [位置]`
强调色用：`bold red fountain pen Chinese`

**三栏对比/介绍页示例：**
```
{STYLE}

Top: large elegant fountain pen Chinese calligraphy: 页面标题
Medium fountain pen below: 副标题说明
Red hand-drawn pen underline.

Three sections side by side, separated by thin hand-drawn vertical lines:

Left section:
Hand-drawn cartoon illustration: [插图描述，vivid colors, marker-colored]
Elegant fountain pen Chinese below: 标题一
Smaller fountain pen text: 说明文字

Center section:
Hand-drawn cartoon illustration: [插图描述]
Elegant fountain pen Chinese below: 标题二
Smaller fountain pen text: 说明文字

Right section:
Hand-drawn cartoon illustration: [插图描述]
Elegant fountain pen Chinese below: 标题三
Smaller fountain pen text: 说明文字

[MUST INCLUDE] cute chibi Labrador with red lobster-claw hat, excited expression,
waving paw, placed at bottom-left corner.
Bottom center, large bold red fountain pen Chinese: 核心金句或CTA
```

---

## 注意事项
- 白板边框：用 `all four borders fully visible, zero background`，勿用 `EXTREME CLOSE-UP`
- **吉祥物每页必须出现**，在 Prompt 结尾单独用 `[MUST INCLUDE]` 再强调一次位置和表情
- 只发PPTX文件给用户，不发预览图

---

## 标签

PPT, 白板板书, 硬笔书法, 三万同款, 拉布拉多吉祥物, 手绘风格

---

## 分类

creative

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/738

---

*本技能由 曹操 从 EasyClaw 搬运整理*
