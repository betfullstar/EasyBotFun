# Skill安全审计 Security Auditor (MayGuard)

**原作者**: 三万  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-19  

---

## 描述

扫描AI Agent技能目录，检测恶意代码模式：凭证窃取、可疑网络请求、破坏性命令、隐蔽执行。安装未知技能前必扫。

---

## 完整内容

# Skill安全审计 (MayGuard)

## 检测5大恶意模式
1. **凭证窃取** — 读取.env、密钥文件、环境变量、SSH keys
2. **可疑网络** — 外发敏感数据到未知服务器
3. **破坏命令** — rm -rf /、格式化磁盘、覆盖系统文件
4. **隐蔽执行** — eval()、exec()、base64解码执行、动态import
5. **权限提升** — sudo、chmod 777、修改系统配置

## 使用方法
```bash
# 扫描单个Skill
python3 mayguard.py scan ~/.openclaw/skills/suspicious-skill/

# 扫描所有已安装Skill
python3 mayguard.py scan-all

# 安装前先下载再扫描
clawhub download some-skill /tmp/check/
python3 mayguard.py scan /tmp/check/
```

## 检测规则示例
```python
SUSPICIOUS_PATTERNS = [
    r'cat ~/\.env',           # 读取环境变量
    r'curl.*\|.*sh',         # 远程代码执行
    r'eval\(.*\)',           # 动态代码执行
    r'rm\s+-rf\s+/',        # 危险删除
    r'chmod\s+777',          # 不安全权限
    r'process\.env',         # Node.js环境变量
    r'open\(/etc/shadow',    # 读取密码文件
    r'base64.*decode.*exec', # 编码执行
]
```

## 安全评分
- 🟢 90-100：安全，放心安装
- 🟡 70-89：有风险点，建议人工审查
- 🟠 50-69：高风险，不建议安装
- 🔴 0-49：危险，强烈不建议

## 注意事项
- 静态分析，不能检测所有攻击
- 调用外部API的Skill可能误报
- 建议流程：先扫描 → 人工审查标记处 → 决定是否安装

---

## 标签

安全, 审计, 扫描, 恶意代码, MayGuard, 开箱即用

---

## 分类

other

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/102

---

*本技能由 曹操 从 EasyClaw 搬运整理*
