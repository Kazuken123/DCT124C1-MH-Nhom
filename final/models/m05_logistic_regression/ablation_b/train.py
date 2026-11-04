"""Run fixed Logistic Regression on feature set B (no 2nd semester features)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from src.data import PROJECT_DIR
from src.evaluate import run_cv_experiment
from src.features import make_preprocessor


def make_model(config):
    return Pipeline([
        ("preprocessor", make_preprocessor(PROJECT_DIR / config["preprocessing_config"])),
        ("model", LogisticRegression(**config["params"])),
    ])


if __name__ == "__main__":
    run_cv_experiment(Path(__file__).with_name("config.yaml"), make_model)
