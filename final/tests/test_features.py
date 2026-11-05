"""Unit tests for feature engineering and preprocessor pipelines."""

import numpy as np
import pandas as pd

from final.src.data import PROJECT_DIR, load_student_data, read_preprocessing_config
from final.src.features import (
    GRADE_DIFF_COL,
    RATIO_SEM1_COL,
    RATIO_SEM2_COL,
    FeatureEngineer,
    make_preprocessor,
)


def test_feature_engineer_calculations():
    sample = pd.DataFrame({
        "Curricular units 1st sem (enrolled)": [0, 5, 6],
        "Curricular units 1st sem (approved)": [0, 4, 6],
        "Curricular units 1st sem (grade)": [0.0, 12.0, 15.0],
        "Curricular units 2nd sem (enrolled)": [0, 0, 6],
        "Curricular units 2nd sem (approved)": [0, 0, 5],
        "Curricular units 2nd sem (grade)": [0.0, 0.0, 14.0],
    })
    fe = FeatureEngineer()
    res = fe.transform(sample)

    assert RATIO_SEM1_COL in res.columns
    assert RATIO_SEM2_COL in res.columns
    assert GRADE_DIFF_COL in res.columns

    # Check safe division (enrolled == 0 -> 0.0)
    assert res[RATIO_SEM1_COL].iloc[0] == 0.0
    assert res[RATIO_SEM2_COL].iloc[0] == 0.0
    assert res[RATIO_SEM2_COL].iloc[1] == 0.0

    # Check regular ratio
    assert np.isclose(res[RATIO_SEM1_COL].iloc[1], 4 / 5)
    assert np.isclose(res[RATIO_SEM1_COL].iloc[2], 1.0)
    assert np.isclose(res[RATIO_SEM2_COL].iloc[2], 5 / 6)

    # Check grade diff
    assert np.isclose(res[GRADE_DIFF_COL].iloc[0], 0.0)
    assert np.isclose(res[GRADE_DIFF_COL].iloc[1], -12.0)
    assert np.isclose(res[GRADE_DIFF_COL].iloc[2], -1.0)


def test_preprocessor_set_a():
    X, _ = load_student_data()
    prep = make_preprocessor(PROJECT_DIR / "configs/lr_preprocessing_v1.json")
    out = prep.fit_transform(X.iloc[:50])
    assert out.shape[0] == 50
    # Categorical one-hot encodes to multiple columns, binary passthrough, numeric standardized
    assert out.shape[1] > 36


def test_preprocessor_set_b():
    X, _ = load_student_data()
    prep = make_preprocessor(PROJECT_DIR / "configs/lr_preprocessing_ablation_b.json")
    out = prep.fit_transform(X.iloc[:50])
    assert out.shape[0] == 50
    # Should have fewer columns than Set A because 6 numeric features were dropped
    prep_a = make_preprocessor(PROJECT_DIR / "configs/lr_preprocessing_v1.json")
    out_a = prep_a.fit_transform(X.iloc[:50])
    assert out.shape[1] == out_a.shape[1] - 6


def test_preprocessor_set_c():
    X, _ = load_student_data()
    fe = FeatureEngineer()
    X_fe = fe.transform(X.iloc[:50])
    prep = make_preprocessor(PROJECT_DIR / "configs/lr_preprocessing_ablation_c.json")
    out = prep.fit_transform(X_fe)
    assert out.shape[0] == 50
    # Should have 3 more columns than Set A because 3 numeric features were added
    prep_a = make_preprocessor(PROJECT_DIR / "configs/lr_preprocessing_v1.json")
    out_a = prep_a.fit_transform(X.iloc[:50])
    assert out.shape[1] == out_a.shape[1] + 3
