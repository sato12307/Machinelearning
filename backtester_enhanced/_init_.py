"""Public re‑exports for quick use."""
from .config import CFG               # global settings
from .data import load_price_history
from .features import make_features
from .strategy import ShortPutSpread
from .backtest import run
from .metrics import summary_stats

__all__ = [
    "CFG",
    "load_price_history",
    "make_features",
    "ShortPutSpread",
    "run",
    "summary_stats",
]
