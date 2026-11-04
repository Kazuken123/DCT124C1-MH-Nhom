"""Run the fixed majority Dummy v1 from any working directory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from sklearn.dummy import DummyClassifier
from src.evaluate import run_cv_experiment


def make_model(config):
    return DummyClassifier(**config["params"])


if __name__ == "__main__":
    run_cv_experiment(Path(__file__).with_name("config.yaml"), make_model)
