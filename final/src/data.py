"""Load verified UCI data and the group's saved split; never fit a model.

From the repository root: python final/src/data.py
From final/: python -m src.data
"""

import hashlib
import json
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data/raw/data.csv"
SOURCE_MANIFEST = PROJECT_DIR / "data/source_manifest.json"
PREPROCESSING_CONFIG = PROJECT_DIR / "configs/lr_preprocessing_v1.json"
SPLIT_DIR = PROJECT_DIR / "configs/splits/student_dropout_seed42_v1"
LABELS = ("Dropout", "Enrolled", "Graduate")


def read_preprocessing_config(config_path=PREPROCESSING_CONFIG):
    """Validate the LR column groups, without fitting any transformation."""
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    transformers = {"numeric": "StandardScaler", "categorical": "OneHotEncoder",
                    "binary": "passthrough"}
    columns = []
    for group, transformer in transformers.items():
        if config[group]["transformer"] != transformer:
            raise ValueError(f"Unsupported transformer for {group}")
        columns.extend(config[group]["columns"])
    expected_count = config.get("n_features", 36)
    if len(columns) != expected_count or len(set(columns)) != expected_count or "Target" in columns:
        raise ValueError(f"Expected {expected_count} distinct features, excluding Target")
    return config


def load_student_data(csv_path=DATA_PATH):
    """Return X, y in source order; row IDs are zero-based source positions.

    Only column-name boundary whitespace is stripped in memory. The source
    bytes, values, row order and categorical codes are preserved.
    """
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    config = read_preprocessing_config()
    payload = Path(csv_path).read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != source["csv_sha256"] or digest != config["data_csv_sha256"]:
        raise ValueError("Dataset SHA-256 does not match the verified source")
    frame = pd.read_csv(BytesIO(payload), sep=source["delimiter"], encoding="utf-8-sig")
    frame.columns = frame.columns.str.strip()
    expected = {"Target"}
    for group in ("numeric", "categorical", "binary"):
        expected.update(config[group]["columns"])
    if not frame.columns.is_unique or set(frame.columns) != expected:
        raise ValueError("Unexpected dataset columns")
    if len(frame) != source["n_rows"] or frame.isna().any().any():
        raise ValueError("Unexpected row count or missing values")
    if frame.duplicated().any():
        raise ValueError("Unexpected duplicate source rows")
    if frame.Target.value_counts().to_dict() != source["target_counts"]:
        raise ValueError("Unexpected target labels or class counts")
    binary = frame[config["binary"]["columns"]]
    if not binary.isin([0, 1]).all().all():
        raise ValueError("Non-binary value in a binary feature")
    return frame.drop(columns="Target"), frame.Target.copy()


def load_splits(split_dir=SPLIT_DIR):
    """Return train IDs, test IDs, CV position pairs and the saved manifest.

    Reads existing files only; does not generate, sort or overwrite split IDs.
    CV positions index X.iloc[train_ids], not the entire source dataset.
    """
    split_dir = Path(split_dir)
    manifest = json.loads((split_dir / "manifest.json").read_text(encoding="utf-8"))
    _, y = load_student_data()
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    if manifest["data_sha256"] != source["csv_sha256"]:
        raise ValueError("Split belongs to a different dataset")
    if manifest["split"] != {"test_size": 0.2, "random_state": 42, "stratify": True}:
        raise ValueError("Split does not match the agreed 80/20 stratified seed 42")
    if manifest["cv"] != {"n_splits": 5, "shuffle": True, "random_state": 42}:
        raise ValueError("CV does not match the agreed five-fold seed 42")
    tables = {}
    columns = {
        "train_indices.csv": ["train_position", "row_id"],
        "test_indices.csv": ["test_position", "row_id"],
        "train_folds.csv": ["train_position", "row_id", "validation_fold"],
    }
    for name, expected_columns in columns.items():
        payload = (split_dir / name).read_bytes()
        if hashlib.sha256(payload).hexdigest() != manifest["files_sha256"][name]:
            raise ValueError(f"Split checksum mismatch: {name}")
        table = pd.read_csv(BytesIO(payload))
        if list(table.columns) != expected_columns or table.isna().any().any():
            raise ValueError(f"Invalid split schema: {name}")
        if not all(pd.api.types.is_integer_dtype(dtype) for dtype in table.dtypes):
            raise ValueError(f"Non-integer split values: {name}")
        if not np.array_equal(table.iloc[:, 0], np.arange(len(table))):
            raise ValueError(f"Split position order mismatch: {name}")
        tables[name] = table
    train_ids = tables["train_indices.csv"].row_id.to_numpy()
    test_ids = tables["test_indices.csv"].row_id.to_numpy()
    combined = np.concatenate([train_ids, test_ids])
    if not np.array_equal(np.sort(combined), np.arange(len(y))):
        raise ValueError("Train/Test must cover each source row exactly once")
    sizes = (manifest["n_rows"], manifest["n_train"], manifest["n_test"])
    if sizes != (len(y), len(train_ids), len(test_ids)):
        raise ValueError("Split sizes do not match the manifest")
    fold_table = tables["train_folds.csv"]
    if not np.array_equal(fold_table.row_id.to_numpy(), train_ids):
        raise ValueError("Fold rows do not match the saved Train order")
    assignment = fold_table.validation_fold.to_numpy()
    if set(assignment) != set(range(1, 6)):
        raise ValueError("Expected fold assignments 1 through 5")
    folds = []
    for number in range(1, 6):
        fit_pos = np.flatnonzero(assignment != number)
        valid_pos = np.flatnonzero(assignment == number)
        if set(y.iloc[train_ids[valid_pos]]) != set(LABELS):
            raise ValueError(f"Missing validation class in fold {number}")
        folds.append((fit_pos, valid_pos))
    return train_ids, test_ids, folds, manifest


def validate_data():
    """Produce a read-only audit summary; no preprocessing is fit."""
    X, y = load_student_data()
    train_ids, test_ids, folds, manifest = load_splits()
    counts = lambda ids: {label: int((y.iloc[ids] == label).sum()) for label in LABELS}
    return {
        "data_sha256": manifest["data_sha256"],
        "n_rows": len(y), "n_features": X.shape[1],
        "n_train": len(train_ids), "n_test": len(test_ids),
        "train_class_counts": counts(train_ids), "test_class_counts": counts(test_ids),
        "validation_folds": [
            {"fold": number, "n_fit": len(fit), "n_valid": len(valid),
             "class_counts": counts(train_ids[valid])}
            for number, (fit, valid) in enumerate(folds, 1)
        ],
        "fitted_preprocessor_saved": False, "model_trained": False,
        "test_scored": False,
    }


if __name__ == "__main__":
    print(json.dumps(validate_data(), ensure_ascii=False, indent=2))
