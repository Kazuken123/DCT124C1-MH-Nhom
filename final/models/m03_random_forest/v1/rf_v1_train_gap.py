r"""Read-only Random Forest V1 train/validation generalization-gap audit.

Put this file at final/models/m03_random_forest/v1/rf_v1_train_gap.py.
From the repository root on Windows run:
    .\.venv\Scripts\python.exe final/models/m03_random_forest/v1/rf_v1_train_gap.py

Uses verified project data/splits; does not train on or score Test;
creates a separate timestamped run under final/experiments/runs/.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

FINAL = Path(__file__).resolve().parents[3]
if not (FINAL / "src" / "data.py").is_file():
    raise FileNotFoundError(f"Cannot locate final/src/data.py under {FINAL}")
sys.path.insert(0, str(FINAL))
from src.data import load_student_data, load_splits  # noqa: E402


MODEL_CONFIG = {
    "n_estimators": 100,
    "max_depth": None,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "random_state": 42,
    "n_jobs": -1,
}


def main() -> None:
    X, y = load_student_data()
    train_ids, test_ids, folds, split_manifest = load_splits()
    X_train = X.iloc[train_ids].apply(pd.to_numeric, errors="raise").reset_index(drop=True)
    y_train = y.iloc[train_ids].reset_index(drop=True)

    fold_rows = []
    for fold_number, (fit_pos, val_pos) in enumerate(folds, 1):
        model = RandomForestClassifier(**MODEL_CONFIG)
        X_fit, y_fit = X_train.iloc[fit_pos], y_train.iloc[fit_pos]
        X_val, y_val = X_train.iloc[val_pos], y_train.iloc[val_pos]
        model.fit(X_fit, y_fit)
        pred_fit = model.predict(X_fit)
        pred_val = model.predict(X_val)
        train_f1 = f1_score(y_fit, pred_fit, average="macro", zero_division=0)
        val_f1 = f1_score(y_val, pred_val, average="macro", zero_division=0)
        train_accuracy = accuracy_score(y_fit, pred_fit)
        val_accuracy = accuracy_score(y_val, pred_val)
        fold_rows.append({
            "fold": fold_number,
            "train_samples": len(fit_pos),
            "validation_samples": len(val_pos),
            "train_accuracy": train_accuracy,
            "validation_accuracy": val_accuracy,
            "accuracy_gap": train_accuracy - val_accuracy,
            "train_macro_f1": train_f1,
            "validation_macro_f1": val_f1,
            "macro_f1_gap": train_f1 - val_f1,
        })
        print(
            f"Fold {fold_number}: Train Macro-F1={train_f1:.4f} | "
            f"Validation Macro-F1={val_f1:.4f} | Gap={train_f1-val_f1:.4f}"
        )

    fold_df = pd.DataFrame(fold_rows)
    fields = [
        "train_accuracy", "validation_accuracy", "accuracy_gap",
        "train_macro_f1", "validation_macro_f1", "macro_f1_gap",
    ]
    summary = {
        "model": "Random Forest V1 baseline (100 trees, raw numeric coded features)",
        "model_config": MODEL_CONFIG,
        "data_rows": len(y),
        "train_rows": len(train_ids),
        "test_rows_reserved_not_scored": len(test_ids),
        "n_folds": len(folds),
        "dataset_sha256": split_manifest.get("data_sha256"),
        "ddof": 0,
        "test_scored": False,
        "tuned": False,
        "metrics": {
            field: {
                "cv_mean": float(fold_df[field].mean()),
                "cv_std": float(fold_df[field].std(ddof=0)),
            }
            for field in fields
        },
        "note": (
            "Train scores are measured on each fold's fitting subset; "
            "validation scores are measured on its held-out subset. "
            "Gap = Train score - Validation score. CV-based gap is not a Test score."
        ),
    }
    run_id = "m03_random_forest_v1_train_gap_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = FINAL / "experiments" / "runs" / run_id
    if out_dir.exists():
        raise FileExistsError(f"Run already exists: {out_dir}")
    out_dir.mkdir(parents=True)
    csv_path = out_dir / "fold_train_validation_gap.csv"
    json_path = out_dir / "summary_train_gap.json"
    fold_df.to_csv(csv_path, index=False, float_format="%.10f", lineterminator="\n")
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n==== 5-Fold CV mean (ddof=0) ====")
    for field in fields:
        m = summary["metrics"][field]
        print(f"{field}: {m['cv_mean']:.4f} +/- {m['cv_std']:.4f}")
    print(f"\nSAVED: {csv_path}")
    print(f"SAVED: {json_path}")
    print("NOTE: Test has NOT been used.")


if __name__ == "__main__":
    main()
