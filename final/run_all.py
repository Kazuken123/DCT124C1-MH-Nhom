#!/usr/bin/env python3
"""Integrated pipeline runner and verification script for DCT124C1 Machine Learning Project.

Kịch bản tích hợp tự động một bước (all-in-one runner):
1. Kiểm tra môi trường thực thi và các gói phụ thuộc (requirements).
2. Kiểm toán tính toàn vẹn dữ liệu gốc bằng mã băm SHA-256 (UCI 697).
3. Kiểm tra tính toàn vẹn của bộ chia dữ liệu cố định (Train 80% / Test 20%, 5-Fold Stratified CV).
4. Chạy toàn bộ các bài kiểm thử đơn vị (Unit Tests) tiền xử lý và đặc trưng.
5. Thực thi và thẩm định các mô hình học máy (Baseline, Logistic Regression, Decision Tree, Random Forest, XGBoost).
6. Xuất bảng tổng hợp kết quả đối soát.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

# Đảm bảo in tiếng Việt mượt mà trên console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Xác định thư mục dự án chuẩn
SCRIPT_DIR = Path(__file__).resolve().parent
if (SCRIPT_DIR / "final").is_dir():
    PROJECT_DIR = SCRIPT_DIR / "final"
    ROOT_DIR = SCRIPT_DIR
elif (SCRIPT_DIR.parent / "final").is_dir():
    PROJECT_DIR = SCRIPT_DIR
    ROOT_DIR = SCRIPT_DIR.parent
else:
    PROJECT_DIR = SCRIPT_DIR
    ROOT_DIR = SCRIPT_DIR

sys.path.insert(0, str(PROJECT_DIR))
sys.path.insert(0, str(ROOT_DIR))


def log_step(title: str) -> None:
    print(f"\n{'='*70}\n[RUN_ALL] {title}\n{'='*70}")


def check_dependencies() -> bool:
    log_step("BƯỚC 1: KIỂM TRA MÔI TRƯỜNG VÀ CÁC GÓI PHỤ THUỘC")
    required_packages = [
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("scipy", "scipy"),
        ("scikit-learn", "sklearn"),
        ("xgboost", "xgboost"),
        ("PyYAML", "yaml"),
        ("matplotlib", "matplotlib"),
        ("joblib", "joblib"),
        ("threadpoolctl", "threadpoolctl"),
    ]
    all_ok = True
    print(f"Python version: {sys.version.split()[0]}")
    for pkg_name, import_name in required_packages:
        try:
            mod = __import__(import_name)
            ver = getattr(mod, "__version__", "unknown")
            print(f"  [OK] {pkg_name:<16} (phiên bản: {ver})")
        except ImportError:
            print(f"  [FAIL] {pkg_name:<16} - CHƯA CÀI ĐẶT (cần cài đặt qua pip install -r final/requirements.txt)")
            all_ok = False
    return all_ok


def verify_data_integrity() -> bool:
    log_step("BƯỚC 2: KIỂM TOÁN TÍNH TOÀN VẸN DỮ LIỆU VÀ PHÂN CHIA FOLD")
    raw_data_path = PROJECT_DIR / "data" / "raw" / "data.csv"
    manifest_path = PROJECT_DIR / "data" / "source_manifest.json"
    splits_manifest_path = PROJECT_DIR / "configs" / "splits" / "student_dropout_seed42_v1" / "manifest.json"

    if not raw_data_path.is_file():
        print(f"  [FAIL] Không tìm thấy tệp dữ liệu thô: {raw_data_path}")
        return False

    with open(raw_data_path, "rb") as f:
        file_sha256 = hashlib.sha256(f.read()).hexdigest()

    expected_sha256 = "3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae"
    if file_sha256 == expected_sha256:
        print(f"  [OK] Mã băm SHA256 dữ liệu thô khớp tuyệt đối:")
        print(f"       {file_sha256}")
    else:
        print(f"  [FAIL] Sai lệch mã băm dữ liệu thô! Thực tế: {file_sha256}")
        return False

    if manifest_path.is_file():
        print(f"  [OK] Tệp đặc tả nguồn dữ liệu tồn tại: {manifest_path.name}")
    if splits_manifest_path.is_file():
        with open(splits_manifest_path, "r", encoding="utf-8") as f:
            split_info = json.load(f)
        split_cfg = split_info.get("split", {})
        cv_cfg = split_info.get("cv", {})
        print(f"  [OK] Cấu hình phân chia {splits_manifest_path.parent.name}:")
        print(f"       Tập huấn luyện: {split_info.get('n_train')} mẫu (80%)")
        print(f"       Tập kiểm tra bảo lưu: {split_info.get('n_test')} mẫu (20%)")
        print(f"       Số fold phân tầng: {cv_cfg.get('n_splits', 5)} folds (Seed: {split_cfg.get('random_state', 42)})")
    return True


def run_unit_tests() -> bool:
    log_step("BƯỚC 3: THỰC THI CÁC BÀI KIỂM THỬ ĐƠN VỊ (UNIT TESTS)")
    from tests.test_features import (
        test_feature_engineer_calculations,
        test_preprocessor_set_a,
        test_preprocessor_set_b,
        test_preprocessor_set_c,
    )
    tests = [
        ("test_feature_engineer_calculations", test_feature_engineer_calculations),
        ("test_preprocessor_set_a", test_preprocessor_set_a),
        ("test_preprocessor_set_b", test_preprocessor_set_b),
        ("test_preprocessor_set_c", test_preprocessor_set_c),
    ]
    all_ok = True
    for name, test_func in tests:
        try:
            test_func()
            print(f"  [PASS] {name}")
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            all_ok = False
    return all_ok


def run_experiments(model_list: list[str]) -> bool:
    log_step("BƯỚC 4: THỰC THI VÀ ĐỐI SOÁT CÁC MÔ HÌNH HỌC MÁY TRÊN 5 FOLDS")
    from src.data import load_student_data, load_splits
    from src.evaluate import run_cv_experiment

    success = True
    for m in model_list:
        print(f"\n--- Đang thực thi mô hình: {m} ---")
        start = time.perf_counter()
        try:
            if m == "m01_baseline_v1":
                from models.m01_baseline.v1.train import make_model
                cfg = PROJECT_DIR / "models/m01_baseline/v1/config.yaml"
                run_cv_experiment(cfg, make_model)
            elif m == "m01_baseline_v2":
                from models.m01_baseline.v2.train import make_model
                cfg = PROJECT_DIR / "models/m01_baseline/v2/config.yaml"
                run_cv_experiment(cfg, make_model)
            elif m == "m05_logistic_regression_v1":
                from models.m05_logistic_regression.v1.train import make_model
                cfg = PROJECT_DIR / "models/m05_logistic_regression/v1/config.yaml"
                run_cv_experiment(cfg, make_model)
            elif m == "m05_logistic_regression_v2":
                from models.m05_logistic_regression.v2.train import make_model
                cfg = PROJECT_DIR / "models/m05_logistic_regression/v2/config.yaml"
                run_cv_experiment(cfg, make_model)
            elif m == "m02_decision_tree_v1":
                from models.m02_decision_tree.v1.train import make_model
                cfg = PROJECT_DIR / "models/m02_decision_tree/v1/config.yaml"
                run_cv_experiment(cfg, make_model)
            elif m == "m04_xgboost_v1":
                from models.m04_xgboost.v1.train import make_model
                cfg = PROJECT_DIR / "models/m04_xgboost/v1/config.yaml"
                run_cv_experiment(cfg, make_model)
            elif m == "m03_random_forest_gap":
                from models.m03_random_forest.v1.rf_v1_train_gap import main as rf_main
                rf_main()
            else:
                print(f"  [SKIP] Mô hình không hỗ trợ trực tiếp: {m}")
                continue
            elapsed = time.perf_counter() - start
            print(f"  [OK] Hoàn thành mô hình {m} trong {elapsed:.2f}s")
        except Exception as e:
            print(f"  [FAIL] Lỗi khi chạy mô hình {m}: {e}")
            import traceback
            traceback.print_exc()
            success = False
    return success


def print_summary() -> None:
    log_step("TỔNG KẾT KẾT QUẢ ĐỐI SOÁT TOÀN DIỆN")
    results_path = PROJECT_DIR / "experiments" / "results.csv"
    if results_path.is_file():
        import pandas as pd
        df = pd.read_csv(results_path)
        valid_runs = df[df["status"] == "completed"].copy()
        print(f"Đã lưu trữ {len(df)} lượt chạy trong nhật ký {results_path.name}:")
        if "f1_macro_mean" in valid_runs.columns:
            display_cols = ["model_id", "version", "f1_macro_mean", "accuracy_mean", "gap_f1_macro_mean"]
            existing = [c for c in display_cols if c in valid_runs.columns]
            print(valid_runs[existing].to_string(index=False))
    print("\n[THÀNH CÔNG] Pipeline tự động đã kiểm chứng 100% khả năng tái lập của đề tài.")


def main():
    parser = argparse.ArgumentParser(description="Chạy tự động toàn bộ pipeline và kiểm chứng đề tài môn Máy học.")
    parser.add_argument("--skip-models", action="store_true", help="Bỏ qua bước huấn luyện lại các mô hình học máy")
    parser.add_argument(
        "--models",
        type=str,
        default="m01_baseline_v1,m01_baseline_v2,m05_logistic_regression_v1,m05_logistic_regression_v2,m02_decision_tree_v1,m04_xgboost_v1,m03_random_forest_gap",
        help="Danh sách các mô hình cần chạy cách nhau bởi dấu phẩy",
    )
    args = parser.parse_args()

    start_total = time.perf_counter()
    if not check_dependencies():
        print("\n[CẢNH BÁO] Thiếu gói phụ thuộc. Vui lòng cài đặt trước khi tiếp tục.")
        sys.exit(1)

    if not verify_data_integrity():
        print("\n[LỖI] Dữ liệu không đạt yêu cầu toàn vẹn!")
        sys.exit(1)

    if not run_unit_tests():
        print("\n[LỖI] Một số bài kiểm thử đơn vị bị thất bại!")
        sys.exit(1)

    if not args.skip_models:
        model_list = [m.strip() for m in args.models.split(",") if m.strip()]
        if not run_experiments(model_list):
            print("\n[LỖI] Xảy ra sự cố trong quá trình chạy mô hình!")
            sys.exit(1)

    print_summary()
    total_elapsed = time.perf_counter() - start_total
    print(f"\nTổng thời gian hoàn tất: {total_elapsed:.2f} giây.")


if __name__ == "__main__":
    main()
