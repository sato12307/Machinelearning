"""
Light GBM‑ready mini wrapper (scikit‑learn fallback) for ML classification/regression.
"""
from __future__ import annotations
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def train(feats: pd.DataFrame, *, target: str = "label", test_size: float = 0.2, random_state: int = 42):
    X = feats.drop(columns=[target])
    y = feats[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    model = GradientBoostingClassifier(random_state=random_state)
    model.fit(X_train, y_train)
    y_pred = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred)
    print(f"Validation ROC‑AUC: {auc:.3f}")
    return model
