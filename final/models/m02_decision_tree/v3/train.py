"""Run Decision Tree v3 on the saved cross-validation folds."""

import sys
from pathlib import Path

from sklearn.tree import DecisionTreeClassifier


PROJECT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_DIR))

from src.evaluate import run_cv_experiment


def make_model(config):
    return DecisionTreeClassifier(**config["params"])


if __name__ == "__main__":
    config_path = Path(__file__).with_name("config.yaml")
    run_cv_experiment(config_path, make_model)