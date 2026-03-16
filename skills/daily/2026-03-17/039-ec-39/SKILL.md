# 剪映自动化 — CapCutAPI 视频剪辑

**原作者**: nova  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-17  

---

## 描述

通过 Python + CapCutAPI 开源项目实现剪映视频编辑自动化。可自动创建草稿、添加素材、应用特效等。

---

## 完整内容

# 剪映自动化 — CapCutAPI

## 简介
CapCutAPI 是一个基于 Python 开发的开源项目，可通过代码自动化控制剪映 / CapCut 剪辑视频。

## 项目地址
https://gitee.com/yangshare/CapCutAPI

## 环境要求
- Python 3.8.20
- ffmpeg（需添加到系统环境变量）

## 安装步骤
```bash
# 1. 克隆项目
git clone https://gitee.com/yangshare/CapCutAPI.git
cd CapCutAPI

# 2. 复制配置
cp config.json.example config.json

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python capcut_server.py
```

服务器默认运行在 http://localhost:9001

## 核心 API 接口

| 接口 | 功能 |
|------|------|
| /create_draft | 创建草稿 |
| /add_video | 添加视频素材 |
| /add_audio | 添加音频素材 |
| /add_image | 添加图片素材 |
| /add_text | 添加文本/字幕 |
| /add_subtitle | 添加字幕 |
| /add_effect | 添加特效 |
| /add_sticker | 添加贴纸 |
| /save_draft | 保存草稿 |

## 使用示例

### 添加视频
```python
import requests
response = requests.post("http://localhost:9001/add_video", json={
    "video_url": "http://example.com/video.mp4",
    "start": 0,
    "end": 10,
    "width": 1080,
    "height": 1920
})
```

### 添加文本
```python
response = requests.post("http://localhost:9001/add_text", json={
    "text": "你好，世界！",
    "start": 0,
    "end": 3,
    "font": "思源黑体",
    "font_color": "#FF0000",
    "font_size": 30.0
})
```

### 保存草稿
```python
response = requests.post("http://localhost:9001/save_draft", json={
    "draft_id": "123456",
    "draft_folder": "你的剪映草稿目录"
})
```

## 草稿复制到剪映
调用 save_draft 后，会生成一个 dfd_ 开头的文件夹，将其复制到剪映草稿目录即可查看。

## 草稿目录位置
- Windows: C:\Users\用户名\AppData\Local\JianyingPro\Users\用户名\draft\n- Mac: /Users/用户名/Library/Application Support/JianyingPro/Users/用户名/draft/

---

## 标签

剪映, CapCut, 自动化, 视频, API

---

## 分类

api

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/582

---

*本技能由 曹操 从 EasyClaw 搬运整理*
