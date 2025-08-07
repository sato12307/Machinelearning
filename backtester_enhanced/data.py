"""
Price & IV data loader with local on‑disk cache.
"""
from __future__ import annotations
from pathlib import Path
from typing import Literal
import pandas as pd
import yfinance as yf

from .config import CFG

def _cache_path(ticker: str, kind: Literal["px", "iv"] = "px") -> Path:
    return CFG.DATA_DIR / f"{ticker}.{kind}.parquet"

def _download_price(ticker: str, start: str | None = None, end: str | None = None) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    df.index.name = "date"
    return df

def load_price_history(ticker: str, *, start: str | None = None, end: str | None = None, force: bool = False) -> pd.DataFrame:
    """Return OHLCV DataFrame (Adj Close included)."""
    p = _cache_path(ticker, "px")
    if p.exists() and not force:
        return pd.read_parquet(p)

    df = _download_price(ticker, start=start, end=end)
    df.to_parquet(p)
    return df
