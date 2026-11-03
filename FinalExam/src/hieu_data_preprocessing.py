"""Read the verified student dataset and build an unfitted LR preprocessor."""

import hashlib
import json
from io import BytesIO
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FINAL_EXAM_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = FINAL_EXAM_DIR / "data/raw/data.csv"
DEFAULT_CONFIG_PATH = FINAL_EXAM_DIR / "configs/hieu_preprocessing_v1.json"


def _read_config(config_path):
    with Path(config_path).open(encoding="utf-8") as handle:
        config = json.load(handle)
    expected_transformers = {
        "numeric": "StandardScaler",
        "categorical": "OneHotEncoder",
        "binary": "passthrough",
    }
    for group, transformer in expected_transformers.items():
        if config[group]["transformer"] != transformer:
            raise ValueError(f"Bo bien doi chua duoc ho tro cho nhom {group}.")
    columns = [
        column
        for group in ("numeric", "categorical", "binary")
        for column in config[group]["columns"]
    ]
    if len(columns) != len(set(columns)):
        raise ValueError("Cau hinh co cot lap lai giua cac nhom.")
    if "Target" in columns:
        raise ValueError("Target khong duoc nam trong cac cot dau vao.")
    return config


def load_student_data(csv_path=DEFAULT_DATA_PATH, config_path=DEFAULT_CONFIG_PATH):
    """Return X and y without sorting, sampling, dropping rows, or fitting.

    The byte hash must match the recorded source. Column names are stripped
    before checking schema. The returned row index follows source CSV order.
    """
    config = _read_config(config_path)
    payload = Path(csv_path).read_bytes()
    if hashlib.sha256(payload).hexdigest() != config["data_csv_sha256"]:
        raise ValueError("SHA-256 cua CSV khong khop cau hinh du lieu.")
    frame = pd.read_csv(BytesIO(payload), sep=";", encoding="utf-8-sig")
    frame.columns = frame.columns.str.strip()
    if not frame.columns.is_unique:
        raise ValueError("Ten cot trung nhau sau khi chuan hoa.")
    expected = {"Target"}
    for group in ("numeric", "categorical", "binary"):
        expected.update(config[group]["columns"])
    if set(frame.columns) != expected:
        raise ValueError("Schema CSV khong khop cau hinh tien xu ly.")
    if frame.isna().any().any():
        raise ValueError("Phat hien gia tri thieu; can kiem tra lai du lieu.")
    if set(frame["Target"].unique()) != {"Dropout", "Enrolled", "Graduate"}:
        raise ValueError("Tap nhan khong khop bai toan phan lop ba nhan.")
    return frame.drop(columns="Target"), frame["Target"].copy()


def make_preprocessor(config_path=DEFAULT_CONFIG_PATH):
    """Build a fresh, unfitted ColumnTransformer from the saved configuration."""
    config = _read_config(config_path)
    return ColumnTransformer(
        transformers=[
            (
                "numeric",
                StandardScaler(
                    with_mean=config["numeric"]["with_mean"],
                    with_std=config["numeric"]["with_std"],
                ),
                config["numeric"]["columns"],
            ),
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown=config["categorical"]["handle_unknown"],
                    drop=config["categorical"]["drop"],
                ),
                config["categorical"]["columns"],
            ),
            ("binary", "passthrough", config["binary"]["columns"]),
        ],
        remainder="drop",
    )
