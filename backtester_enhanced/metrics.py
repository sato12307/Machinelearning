"""
Basic performance metrics.
"""
import numpy as np
import pandas as pd

def summary_stats(equity: pd.Series, freq: str = "D") -> dict[str, float]:
    rets = equity.pct_change().dropna()
    ann_factor = {"D": 252, "W": 52, "M": 12}[freq]
    ann_ret = (1 + rets.mean()) ** ann_factor - 1
    ann_vol = rets.std() * np.sqrt(ann_factor)
    sharpe  = ann_ret / ann_vol if ann_vol else np.nan
    cummax  = equity.cummax()
    dd      = (equity - cummax) / cummax
    max_dd  = dd.min()
    return {
        "TotalReturn": equity.iloc[-1] / equity.iloc[0] - 1,
        "AnnualReturn": ann_ret,
        "AnnualVol": ann_vol,
        "Sharpe": sharpe,
        "MaxDD": max_dd,
        "Trades": np.count_nonzero(rets)
    }
