"""
Bootstrap Monte‑Carlo simulation for tail‑risk eval.
"""
import numpy as np
import pandas as pd

def mc_summary(equity: pd.Series, *, horizon_days: int = 252, n_paths: int = 2000, seed: int = 42) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    daily_ret = equity.pct_change().dropna().to_numpy()
    paths = rng.choice(daily_ret, size=(n_paths, horizon_days))
    cum = (1 + paths).prod(axis=1)
    return {
        "Mean": float(cum.mean()),
        "Std":  float(cum.std()),
        "5%VaR": float(np.percentile(cum, 5) - 1),
        "1%VaR": float(np.percentile(cum, 1) - 1),
    }
