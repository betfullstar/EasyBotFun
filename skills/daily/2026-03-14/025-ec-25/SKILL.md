# Stock &amp; Futures Data Search - 股票期货数据搜索

**原作者**: ding_dragon_2fc793  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-14  

---

## 描述

通过网络搜索获取股票和期货历史数据，无需API Key。支持A股、港股、美股、中国期货等市场数据查询。

---

## 完整内容

---
name: stock-futures-data-search
description: 通过网络搜索获取股票和期货历史数据。支持A股、港股、美股、中国期货等市场数据查询，无需API Key，使用新浪财经等公开数据源。
metadata:
  emoji: 📈
  requires:
    - python3
    - requests
  author: ding_dragon_2fc793
  tags: [stock, futures, market-data, finance, 股票, 期货, 行情]
---

# Stock &amp; Futures Data Search

通过网络搜索获取股票和期货历史数据，无需API Key。

## 功能

- **A股数据**: 获取中国A股历史价格和实时行情
- **期货数据**: 获取中国期货（包括欧线期货EC等）历史数据
- **港股/美股**: 通过Yahoo Finance等获取数据
- **加密货币**: 获取BTC/ETH等价格数据

## 安装

```bash
pip install requests
```

## 使用方法

### 1. 获取期货数据

```python
python3 scripts/futures_data.py --code EC2604
```

### 2. 获取股票数据

```python
python3 scripts/stock_data.py --symbol 000001
```

### 3. 获取多个合约数据

```python
python3 scripts/futures_data.py --code EC2604,EC2605,EC2606
```

## 数据源

- **新浪财经**: 中国期货、A股历史数据
- **东方财富**: 股票、基金数据
- **Yahoo Finance**: 港股、美股、加密货币

## 示例

### 获取欧线期货数据

```bash
$ python3 scripts/futures_data.py --code EC2604

📊 EC2604 (欧线期货4月合约) 历史数据:
日期: 2026-03-06
开盘: 1821.00
收盘: 1892.20
最高: 1977.70
最低: 1752.00
成交量: 85170手
涨跌: +124.20 (+7.02%)
```

### 获取A股数据

```bash
$ python3 scripts/stock_data.py --symbol 000001

📊 000001 (平安银行) 数据:
最新价: 12.58
涨跌: +0.15 (+1.21%)
成交量: 125.6万手
```

## 支持的合约

### 期货合约
- 欧线期货: EC2604, EC2605, EC2606, EC2607, EC2608, EC2609, EC2610, EC2612
- 其他商品期货: 螺纹钢、铁矿石、原油等

### 股票代码
- A股: 000001.SZ, 600000.SH 等
- 港股: 00700.HK 等
- 美股: AAPL, MSFT 等

## 免责声明

本技能仅供学习研究使用，数据来源于公开网络，可能存在延迟或不准确。投资有风险，入市需谨慎。

## License

MIT


---

## 标签

stock, futures, market-data, finance, 股票

---

## 分类

api

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/568

---

*本技能由 曹操 从 EasyClaw 搬运整理*
