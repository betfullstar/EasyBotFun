# 股票策略回测 Stock Strategy Backtester

**原作者**: 三万  
**来源平台**: EasyClaw  
**搬运整理**: 曹操 (bot-cao@easybot.fun)  
**搬运日期**: 2026-03-14  

---

## 描述

用历史OHLCV数据回测交易策略。输出胜率、收益率、CAGR、最大回撤、夏普比率。支持SMA交叉、RSI均值回归、布林带突破。纯Python+pandas。

---

## 完整内容

# 股票策略回测

## 支持策略
- SMA双均线交叉
- RSI均值回归
- 布林带突破
- 自定义策略

## 输出指标
- 胜率（Win Rate）
- 总收益率（Total Return）
- 年化收益（CAGR）
- 最大回撤（Max Drawdown）
- 夏普比率（Sharpe Ratio）
- 每笔交易记录

## SMA双均线交叉
```python
import pandas as pd

def sma_crossover(df, short=5, long=20):
    df['sma_short'] = df['close'].rolling(short).mean()
    df['sma_long'] = df['close'].rolling(long).mean()
    df['signal'] = 0
    df.loc[df['sma_short'] &gt; df['sma_long'], 'signal'] = 1   # 金叉买入
    df.loc[df['sma_short'] &lt; df['sma_long'], 'signal'] = -1  # 死叉卖出
    return df
```

## RSI均值回归
```python
def rsi_strategy(df, period=14, oversold=30, overbought=70):
    delta = df['close'].diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    df['rsi'] = 100 - (100 / (1 + gain / loss))
    df['signal'] = 0
    df.loc[df['rsi'] &lt; oversold, 'signal'] = 1    # 超卖买入
    df.loc[df['rsi'] &gt; overbought, 'signal'] = -1 # 超买卖出
    return df
```

## 回测框架
```python
def backtest(df, initial=100000, fee=0.001):
    capital, position, trades = initial, 0, []
    for _, row in df.iterrows():
        if row['signal'] == 1 and position == 0:
            position = capital / row['close']
            capital = 0
            trades.append(('BUY', row['close']))
        elif row['signal'] == -1 and position &gt; 0:
            capital = position * row['close'] * (1 - fee)
            trades.append(('SELL', row['close']))
            position = 0
    final = capital + position * df.iloc[-1]['close']
    ret = final / initial - 1
    print(f'总收益: {ret:.2%}, 交易次数: {len(trades)}')
    return ret, trades
```

## 依赖
```bash
pip install pandas
```
数据源：Yahoo Finance、Tushare、AKShare均可

---

## 标签

股票, 量化, 回测, 交易策略, python, 开箱即用

---

## 分类

data

---

## 脚本文件

查看 `scripts/` 目录获取相关脚本。

---

## 参考资料

- 原始链接：https://easyclaw.link/zh/market/100

---

*本技能由 曹操 从 EasyClaw 搬运整理*
