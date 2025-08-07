from pathlib import Path
from dataclasses import dataclass

@dataclass
class _Config:
    DATA_DIR: Path = Path.home() / ".bt_data"
    INIT_CAPITAL: float = 10_000.0
    SLIPPAGE: float = 0.00   # per‑share
    COMMISSION: float = 0.00 # per‑share
    SEED: int = 42

# グローバル設定オブジェクト
CFG = _Config()

# データ保存先フォルダを必ず作成
CFG.DATA_DIR.mkdir(parents=True, exist_ok=True)
