"""Run XGBoost v1 on the shared Student Dropout folds."""

import sys
from pathlib import Path

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier


PROJECT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_DIR))

from src.evaluate import run_cv_experiment


class StudentDropoutXGBoost(ClassifierMixin, BaseEstimator):
    def __init__(self, params):
        self.params = params
# Huấn luyện mô hình
    def fit(self, X, y):
        self.label_encoder_ = LabelEncoder()
        encoded_labels = self.label_encoder_.fit_transform(y)
        self.classes_ = self.label_encoder_.classes_

        self.model_ = XGBClassifier(**self.params)
        self.model_.fit(X, encoded_labels)
        return self
# Dự đoán và trả lại nhãn chữ
    def predict(self, X):
        encoded_predictions = self.model_.predict(X)
        return self.label_encoder_.inverse_transform(encoded_predictions)

# Tạo đối tượng từ cấu hình
def make_model(config):
    return StudentDropoutXGBoost(config["params"])

# Khởi động lần chạy
if __name__ == "__main__":
    config_path = Path(__file__).with_name("config.yaml")
    run_cv_experiment(config_path, make_model)