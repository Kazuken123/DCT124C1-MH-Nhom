"""Shared CV runner for fixed classifiers; never predicts or scores Test."""

import time
import warnings
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from sklearn.base import clone
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report, confusion_matrix, f1_score,
                             precision_recall_fscore_support)
from threadpoolctl import threadpool_limits

from .data import LABELS, PROJECT_DIR, load_splits, load_student_data, read_preprocessing_config
from .tracking import LocalRun, write_json


def score(truth, prediction):
    precision, recall, f1, _ = precision_recall_fscore_support(
        truth, prediction, labels=LABELS, zero_division=0)
    result = {"accuracy": float(accuracy_score(truth, prediction)),
              "f1_macro": float(f1_score(truth, prediction, labels=LABELS, average="macro", zero_division=0))}
    for i, label in enumerate(LABELS):
        result.update({f"precision_{label}": float(precision[i]),
                       f"recall_{label}": float(recall[i]), f"f1_{label}": float(f1[i])})
    return result


def run_cv_experiment(config_path, model_factory):
    """Run a fixed model on saved folds, then fit Train for handoff.

    No parameter search, feature selection or Test evaluation occurs here.
    Each fold gets a fresh clone, including all learned preprocessing.
    """
    config_path = Path(config_path).resolve()
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    model_id = config["model_id"]
    version = config["version"]

    supported_version = version == "v1" or (
        model_id == "m05_logistic_regression" and version == "v2"
    )

    if not supported_version or config["feature_set"] != "original_36":
        raise ValueError("Unsupported model version or feature set")
    X, y = load_student_data()
    train_ids, test_ids, folds, split_manifest = load_splits()
    X_train, y_train = X.iloc[train_ids], y.iloc[train_ids]
    estimator = model_factory(config)
    run = LocalRun(config_path, config, split_manifest)
    started = time.perf_counter()
    warning_rows, fold_rows, leakage_rows = [], [], []
    prediction = np.full(len(train_ids), "", dtype=object)
    coverage = np.zeros(len(train_ids), dtype=int)
    assignment = np.zeros(len(train_ids), dtype=int)

    def fit_checked(model, positions, label):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            model.fit(X_train.iloc[positions], y_train.iloc[positions])
        warning_rows.extend({"fold": label, "category": w.category.__name__, "message": str(w.message)} for w in caught)
        write_json(run.path / "warnings.json", warning_rows)
        if any(issubclass(w.category, ConvergenceWarning) for w in caught):
            raise RuntimeError("ConvergenceWarning: inspect this run before using results")

    try:
        with threadpool_limits(limits=1):
            for number, (fit_pos, valid_pos) in enumerate(folds, 1):
                model = clone(estimator)
                fit_checked(model, fit_pos, number)
                pred_train = model.predict(X_train.iloc[fit_pos])
                pred_valid = model.predict(X_train.iloc[valid_pos])
                prediction[valid_pos] = pred_valid
                coverage[valid_pos] += 1
                assignment[valid_pos] = number
                row = {"fold": number, "n_fit": len(fit_pos), "n_valid": len(valid_pos)}
                row.update({"train_" + k: v for k, v in score(y_train.iloc[fit_pos], pred_train).items()})
                row.update({"valid_" + k: v for k, v in score(y_train.iloc[valid_pos], pred_valid).items()})
                row["gap_f1_macro"] = row["train_f1_macro"] - row["valid_f1_macro"]
                if config["model_id"] == "m05_logistic_regression":
                    scaler = model.named_steps["preprocessor"].named_transformers_["numeric"]
                    columns = read_preprocessing_config()["numeric"]["columns"]
                    expected = X_train.iloc[fit_pos][columns].mean().to_numpy()
                    np.testing.assert_allclose(scaler.mean_, expected, rtol=1e-12, atol=1e-12)
                    if int(scaler.n_samples_seen_) != len(fit_pos):
                        raise ValueError("Scaler saw unexpected rows")
                    leakage_rows.append({"fold": number, "scaler_seen": int(scaler.n_samples_seen_),
                                         "max_mean_error": float(np.max(np.abs(scaler.mean_ - expected))),
                                         "fit_validation_disjoint": not bool(set(fit_pos) & set(valid_pos))})
                    row["n_iter"] = int(model.named_steps["model"].n_iter_.max())
                else:
                    if config["model_id"] == "m01_baseline":
                        majority = y_train.iloc[fit_pos].value_counts().idxmax()
                        if set(pred_valid) != {majority}:
                            raise ValueError("Majority baseline predictions do not match training majority")
                    row["n_iter"] = 0
                fold_rows.append(row)
                pd.DataFrame(fold_rows).to_csv(run.path / "fold_metrics.csv", index=False, lineterminator="\n")
                print(f"{config['model_id']} fold {number}/5: Macro-F1={row['valid_f1_macro']:.6f}", flush=True)
            if not np.all(coverage == 1) or set(train_ids) & set(test_ids):
                raise ValueError("Invalid OOF coverage or Train/Test overlap")
            # Handoff artifact, trained only on the saved Train rows.
            final_model = clone(estimator)
            fit_checked(final_model, np.arange(len(train_ids)), "full_train")
            joblib.dump(final_model, run.path / "model_train_only.joblib")

        frame = pd.DataFrame(fold_rows)
        cv = {}
        for col in frame.columns:
            if col.startswith(("train_", "valid_", "gap_")):
                cv[col + "_mean"] = float(frame[col].mean())
                cv[col + "_std"] = float(frame[col].std(ddof=0))
        metrics = {
            "run_id": run.run_id, "model_id": config["model_id"], "version": config["version"],
            "cv_evaluation": "mean_of_5_saved_folds_on_train", "std_ddof": 0,
            "cv": cv, "oof_evaluation": "pooled_OOF_train_only", "oof": score(y_train, prediction),
            "n_train": len(train_ids), "n_test_reserved": len(test_ids),
            "test_scored_this_run": False, "full_train_model_saved_locally": True,
        }
        write_json(run.path / "metrics.json", metrics)
        pd.DataFrame({"row_id": train_ids, "validation_fold": assignment,
                      "y_true": y_train.to_numpy(), "y_pred": prediction}).to_csv(
            run.path / "oof_predictions.csv", index=False, lineterminator="\n")
        report = classification_report(y_train, prediction, labels=LABELS, output_dict=True, zero_division=0)
        pd.DataFrame([{"label": label, **report[label]} for label in LABELS]).to_csv(
            run.path / "class_metrics_oof.csv", index=False, lineterminator="\n")
        cm = confusion_matrix(y_train, prediction, labels=LABELS)
        pd.DataFrame(cm, index=LABELS, columns=LABELS).rename_axis("true_label").to_csv(
            run.path / "confusion_matrix.csv", lineterminator="\n")
        if leakage_rows:
            pd.DataFrame(leakage_rows).to_csv(run.path / "leakage_checks.csv", index=False, lineterminator="\n")
        figures = run.path / "figures"
        figures.mkdir()
        fig, ax = plt.subplots(figsize=(6.4, 5))
        ConfusionMatrixDisplay(cm, display_labels=LABELS).plot(ax=ax, colorbar=False, cmap="Blues")
        ax.set_title(f"{config['model_id']} {version}: Train OOF (n={len(train_ids)})")
        fig.tight_layout(); fig.savefig(figures / "confusion_matrix.png", dpi=150); plt.close(fig)
        fig, ax = plt.subplots(figsize=(6.4, 4))
        ax.plot(frame.fold, frame.train_f1_macro, "o-", label="Train Macro-F1")
        ax.plot(frame.fold, frame.valid_f1_macro, "s-", label="Validation Macro-F1")
        ax.set(xlabel="CV fold", ylabel="Macro-F1 (0–1)", ylim=(0, 1), xticks=range(1, 6),
                title=f"{config['model_id']} {version}: same five saved folds")
        ax.legend(); fig.tight_layout(); fig.savefig(figures / "cv_macro_f1.png", dpi=150); plt.close(fig)
        note = f"""# {config['model_id']} {config['version']}

Người thực hiện: {config['owner']}. Run: {run.run_id}.

Giả thuyết/mục tiêu: {config['objective']}

CV 5-fold trên 3.539 dòng Train, cùng bộ chỉ số nhóm. Macro-F1: {cv['valid_f1_macro_mean']:.4f} ± {cv['valid_f1_macro_std']:.4f} (ddof=0); Accuracy: {cv['valid_accuracy_mean']:.4f}; Recall Dropout: {cv['valid_recall_Dropout_mean']:.4f}. Train Macro-F1: {cv['train_f1_macro_mean']:.4f}; gap Train–Validation: {cv['gap_f1_macro_mean']:.4f}.

Macro-F1 OOF: {metrics['oof']['f1_macro']:.4f}; tính riêng với CV mean. Xem class_metrics_oof.csv và confusion_matrix.csv để phân tích lớp khó và lỗi nhầm. Không tuning hoặc chọn đặc trưng trong run này. Model cuối được fit trên toàn Train để bàn giao, không dự đoán Test.

Run này không sử dụng Test để đánh giá. Test từng được notebook RF cũ sử dụng; đổi khung dự án không đặt lại lịch sử đó. Không kết luận mô hình tốt nhất nhóm hoặc hiệu quả dự đoán ngay lúc nhập học vì dữ liệu có HK2.

Các số được ghi từ lần chạy mới, không nhập lại kết quả lịch sử. Code tại lúc chạy còn đang chờ review; git_info.json lưu base commit và hash nguồn. Tracking cục bộ đã có; chưa đồng bộ W&B/Sheets vì chưa cấu hình trong checkout. Artifact model_train_only.joblib chỉ lưu cục bộ, bị Git bỏ qua.

Hướng tiếp theo: đối chiếu baseline trên cùng fold, phân tích lỗi từng lớp, sau đó thử một thay đổi có giả thuyết trong v2. Giữ v1 làm mốc; bản sau không bắt buộc tốt hơn.
"""
        (run.path / "notes.md").write_bytes(note.encode("utf-8"))
        run.record.update(status="complete", macro_f1_mean=cv["valid_f1_macro_mean"],
                          macro_f1_std=cv["valid_f1_macro_std"], accuracy_mean=cv["valid_accuracy_mean"],
                          dropout_recall_mean=cv["valid_recall_Dropout_mean"],
                          train_valid_gap=cv["gap_f1_macro_mean"], duration_sec=time.perf_counter() - started)
        run.save()
        print(run.path, flush=True)
        return run.path
    except Exception as exc:
        write_json(run.path / "warnings.json", warning_rows)
        run.record.update(status="failed", error=f"{type(exc).__name__}: {exc}",
                          duration_sec=time.perf_counter() - started)
        run.save()
        raise
