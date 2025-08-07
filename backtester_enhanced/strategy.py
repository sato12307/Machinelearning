"""
BaseStrategy & concrete example: ShortPutSpread.
"""
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass
class Trade:
    open_date: pd.Timestamp
    close_date: pd.Timestamp
    pnl: float

class BaseStrategy:
    def generate_signals(self, feats: pd.DataFrame) -> pd.Series:
        raise NotImplementedError

    def backtest(self, feats: pd.DataFrame) -> list[Trade]:
        sig = self.generate_signals(feats)
        trades: list[Trade] = []
        for open_idx in sig[sig].index:
            close_idx = open_idx + pd.Timedelta(days=5)  # 1‑week holding
            if close_idx not in feats.index:
                break
            # simple PnL: percentage change * notionals
            pct = feats.loc[close_idx, "Adj Close"] / feats.loc[open_idx, "Adj Close"] - 1
            pnl = -pct * 100  # payoff profile of short put approx.
            trades.append(Trade(open_idx, close_idx, pnl))
        return trades

# ---- concrete example --------------------------------------------------
class ShortPutSpread(BaseStrategy):
    def __init__(self, premium_target: float = 0.60):
        self.premium_target = premium_target

    def generate_signals(self, feats: pd.DataFrame) -> pd.Series:
        """
        Simple signal: price above SMA200 & daily ATR% below threshold.
        """
        price = feats["Adj Close"]
        cond_price = price > feats["sma200"]
        atr_pct = feats["atr14"] / price
        cond_vol  = atr_pct < 0.03
        return cond_price & cond_vol
