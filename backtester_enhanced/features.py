"""
Generate technical & option metrics.
"""
import pandas as pd
import numpy as np

def _sma(s: pd.Series, window: int) -> pd.Series:
    return s.rolling(window).mean()

def _atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    high_low = df["High"] - df["Low"]
    high_close = np.abs(df["High"] - df["Close"].shift())
    low_close  = np.abs(df["Low"]  - df["Close"].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    return true_range.rolling(window).mean()

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Append basic features: SMA50/200, ATR14, Mom21, daily returns.
    Expects columns: Open, High, Low, Close, Adj Close, Volume
    """
    out = df.copy()
    out["sma50"]   = _sma(out["Adj Close"], 50)
    out["sma200"]  = _sma(out["Adj Close"], 200)
    out["mom21"]   = out["Adj Close"].pct_change(21)
    out["atr14"]   = _atr(out)
    out["ret1"]    = out["Adj Close"].pct_change()
    out.dropna(inplace=True)
    return out
