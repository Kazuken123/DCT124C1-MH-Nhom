"""Feature preprocessing and engineering pipelines for model training and ablation study.

All transformers and scalers are designed to be placed inside a scikit-learn Pipeline.
Transformers are fit strictly on training fold partitions and never on the full dataset
prior to cross-validation.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import PREPROCESSING_CONFIG, read_preprocessing_config

FEATURE_SET_A = "original_36"
FEATURE_SET_B = "no_sem2_30"
FEATURE_SET_C = "with_engineered_39"

RATIO_SEM1_COL = "Curricular units 1st sem (approved ratio)"
RATIO_SEM2_COL = "Curricular units 2nd sem (approved ratio)"
GRADE_DIFF_COL = "Curricular units grade difference (2nd - 1st)"


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Row-wise feature engineering for academic performance indicators.

    Computes:
    1. Ratio of approved to enrolled curricular units in 1st semester.
    2. Ratio of approved to enrolled curricular units in 2nd semester.
    3. Grade difference between 2nd semester and 1st semester.

    Safe division handles zero enrolled units by returning 0.0.
    Since computations are strictly row-wise, no data leakage across folds occurs.
    """

    def __init__(self, add_sem1_ratio=True, add_sem2_ratio=True, add_grade_diff=True):
        self.add_sem1_ratio = add_sem1_ratio
        self.add_sem2_ratio = add_sem2_ratio
        self.add_grade_diff = add_grade_diff

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        if self.add_sem1_ratio:
            enrolled_1 = X["Curricular units 1st sem (enrolled)"]
            approved_1 = X["Curricular units 1st sem (approved)"]
            X[RATIO_SEM1_COL] = np.where(enrolled_1 > 0, approved_1 / enrolled_1, 0.0)

        if self.add_sem2_ratio:
            enrolled_2 = X["Curricular units 2nd sem (enrolled)"]
            approved_2 = X["Curricular units 2nd sem (approved)"]
            X[RATIO_SEM2_COL] = np.where(enrolled_2 > 0, approved_2 / enrolled_2, 0.0)

        if self.add_grade_diff:
            grade_1 = X["Curricular units 1st sem (grade)"]
            grade_2 = X["Curricular units 2nd sem (grade)"]
            X[GRADE_DIFF_COL] = grade_2 - grade_1

        return X


def make_preprocessor(config_path=PREPROCESSING_CONFIG):
    """Build column transformer from specified preprocessing configuration.

    Supports:
    - Set A (36 columns, configs/lr_preprocessing_v1.json)
    - Set B (30 columns, configs/lr_preprocessing_ablation_b.json)
    - Set C (39 columns, configs/lr_preprocessing_ablation_c.json)
    """
    config = read_preprocessing_config(config_path)
    return ColumnTransformer([
        ("numeric", StandardScaler(
            with_mean=config["numeric"]["with_mean"],
            with_std=config["numeric"]["with_std"],
        ), config["numeric"]["columns"]),
        ("categorical", OneHotEncoder(
            handle_unknown=config["categorical"]["handle_unknown"],
            drop=config["categorical"]["drop"],
        ), config["categorical"]["columns"]),
        ("binary", "passthrough", config["binary"]["columns"]),
    ], remainder="drop")
