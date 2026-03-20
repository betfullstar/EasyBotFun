#!/usr/bin/env python3
"""
游戏邮件推广执行脚本
每日上限 10 封邮件
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import random

# 加载配置
with open('/root/.openclaw/workspace/gmail_config.json') as f:
    config = json.load(f)

FROM_EMAIL = config['email']
APP_PASSWORD = config['app_password']
SMTP_SERVER = config['smtp_server']
SMTP_PORT = config['smtp_port']

# 加载状态
with open('/root/.openclaw/workspace/EasyBotFun/promotion_state.json') as f:
    state = json.load(f)

# 游戏库
PRIMARY_GAME = {
    "name": "Bubble Dino - 泡泡恐龙",
    "package": "com.pixelpals.bubbledino",
    "url": "https://play.google.com/store/apps/details?id=com.pixelpals.bubbledino",
    "description": "A fun and addictive bubble shooter game featuring adorable dinosaurs. Pop bubbles, solve puzzles, and embark on a prehistoric adventure!"
}

SECONDARY_POOL = [
    {
        "name": "Wood Block Jigsaw",
        "url": "https://play.google.com/store/apps/details?id=com.royal.puzzle.woodblock.jigsaw",
        "description": "A relaxing wood block puzzle game that combines jigsaw and block puzzle mechanics."
    },
    {
        "name": "Slide Puzzle",
        "url": "https://play.google.com/store/apps/details?id=com.royal.puzzle.slide.block.solo",
        "description": "Classic slide puzzle game with beautiful images and multiple difficulty levels."
    },
    {
        "name": "Sudoku",
        "url": "https://play.google.com/store/apps/details?id=com.royal.puzzle.sudoku",
        "description": "Classic Sudoku puzzle game with thousands of puzzles and multiple difficulty levels."
    },
    {
        "name": "Solitaire Poker",
        "url": "https://play.google.com/store/apps/details?id=com.poker.card.solitaire.puzzle",
        "description": "A unique combination of Solitaire and Poker, creating an exciting card puzzle experience."
    },
    {
        "name": "Sniper Training",
        "url": "https://play.google.com/store/apps/details?id=shoot.sniper.traing.range.simulation",
        "description": "Realistic sniper training simulator with challenging missions and precise shooting mechanics."
    },
    {
        "name": "FPS Shooting",
        "url": "https://play.google.com/store/apps/details?id=fps.shooting.sniper.range.gun.fire",
        "description": "Fast-paced FPS shooting game with various weapons and intense combat scenarios."
    },
    {
        "name": "Color Puzzle",
        "url": "https://play.google.com/store/apps/details?id=com.huancai.colorpuzzle",
        "description": "Vibrant color-matching puzzle game that challenges your logic and pattern recognition."
    }
]

# 目标媒体列表
TARGETS = [
    {"email": "news@pocketgamer.com", "media": "Pocket Gamer"},
    {"email": "tips@toucharcade.com", "media": "TouchArcade"},
    {"email": "tips@androidpolice.com", "media": "Android Police"},
    {"email": "tips@148apps.com", "media": "148Apps"},
    {"email": "tips@appspy.com", "media": "AppSpy"}
]

def send_email(to_email, subject, body):
    """发送邮件"""
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ 发送成功：{to_email}")
        return True
    except Exception as e:
        print(f"❌ 发送失败：{to_email} - {e}")
        return False

def create_email_body(media_name, secondary_game):
    """创建邮件正文"""
    return f"""Hi {media_name} Team,

I hope this email finds you well! I'm reaching out to share an exciting new mobile game that I think would be perfect for your audience.

🎮 Featured Game: {PRIMARY_GAME['name']}
📱 Package: {PRIMARY_GAME['package']}
🔗 Link: {PRIMARY_GAME['url']}

Game Description:
{PRIMARY_GAME['description']}

Why Your Readers Will Love It:
- Engaging gameplay mechanics
- High-quality graphics and sound
- Perfect for casual gaming sessions
- Free to play with optional in-app purchases

I'd be happy to provide review codes, press kits, or arrange interviews with the development team if you're interested in covering this game.

Looking forward to hearing from you!

Best regards,
Cao Cao
Indie Game Creator
yixiangshijie23@gmail.com

---
Secondary Recommendation: {secondary_game['name']}
Link: {secondary_game['url']}
"""

def main():
    print("=" * 60)
    print("🎮 游戏邮件推广执行")
    print(f"📧 发件人：{FROM_EMAIL}")
    print(f"📅 日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 选择副游戏
    secondary_game = random.choice(SECONDARY_POOL)
    print(f"\n🎯 主游戏：{PRIMARY_GAME['name']}")
    print(f"🎲 副游戏：{secondary_game['name']}")
    print("-" * 60)
    
    # 获取已发送列表
    sent_emails = state.get('sent', [])
    
    # 计算需要发送的目标（排除已发送的）
    remaining_targets = [t for t in TARGETS if t['email'] not in sent_emails]
    
    print(f"\n📋 目标媒体：{len(remaining_targets)} 封待发送")
    for t in remaining_targets:
        status = "⏳ 待发送" if t['email'] not in sent_emails else "✅ 已发送"
        print(f"   {status}: {t['email']} ({t['media']})")
    
    print("-" * 60)
    
    # 发送邮件
    sent_count = 0
    for target in remaining_targets:
        subject = f"New Mobile Game Recommendation - {PRIMARY_GAME['name']}"
        body = create_email_body(target['media'], secondary_game)
        
        if send_email(target['email'], subject, body):
            sent_emails.append(target['email'])
            sent_count += 1
    
    # 更新状态
    state['sent'] = sent_emails
    state['remaining'] = 10 - len(sent_emails)
    state['last_updated'] = datetime.now().isoformat()
    state['secondary_game'] = secondary_game['name']
    
    # 更新发送状态
    current_hour = datetime.now().hour
    if current_hour < 12:
        state['schedule']['morning']['status'] = 'completed'
    elif current_hour < 18:
        state['schedule']['afternoon']['status'] = 'completed'
    else:
        state['schedule']['evening']['status'] = 'completed'
    
    with open('/root/.openclaw/workspace/EasyBotFun/promotion_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    print("-" * 60)
    print(f"✅ 本次发送：{sent_count} 封")
    print(f"📊 今日累计：{len(sent_emails)}/10 封")
    print(f"📝 状态已更新：promotion_state.json")
    print("=" * 60)

if __name__ == "__main__":
    main()
