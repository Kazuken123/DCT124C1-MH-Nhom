"""Fresh, unfitted LR v1 preprocessing; feature engineering comes later."""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import PREPROCESSING_CONFIG, read_preprocessing_config


def make_preprocessor(config_path=PREPROCESSING_CONFIG):
    """Build 18 scaled, 10 one-hot and 8 passthrough feature groups.

    Put this transformer inside the model Pipeline. Fit each new Pipeline on
    its own training fold; never fit on all rows before cross-validation.
    This configuration is for LR v1, not a required scaler for tree models.
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
