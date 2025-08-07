"""
Vectorised equity curve construction.
"""
import pandas as pd
import numpy as np
from .config import CFG
from .strategy import BaseStrategy

def run(strategy: BaseStrategy, feats: pd.DataFrame) -> pd.DataFrame:
    trades = strategy.backtest(feats)
    if not trades:
        raise RuntimeError("No trades generated.")
    equity = pd.Series(CFG.INIT_CAPITAL, index=feats.index)
    capital = CFG.INIT_CAPITAL
    for t in trades:
        capital += t.pnl
        equity.loc[t.close_date:] = capital
    return equity.to_frame("equity")
