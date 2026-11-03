"""Reproducible Dummy/LR evaluation. Test rows are never scored here.

Run from FinalExam: python -m src.hieu_baseline_lr
Setup, outputs and verification status are documented in README.md.
"""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import warnings
from datetime import datetime, timezone
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report, confusion_matrix, f1_score,
                             precision_recall_fscore_support)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from threadpoolctl import threadpool_limits

from .hieu_data_preprocessing import FINAL_EXAM_DIR, load_student_data, make_preprocessor

CONFIG_PATH = FINAL_EXAM_DIR / "configs/hieu_baseline_lr_v1.json"


def read_config():
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def write_json(path, content):
    Path(path).write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare_split(X, y, config):
    """Save row ids AND order, plus a validation-fold assignment per train row.

    This checkout had no external index files. These files are reconstructed
    from the leader-confirmed recipe, matching the DT notebook split code.
    A supplied conflicting file fails instead of being silently overwritten.
    """
    train_ids, test_ids = train_test_split(
        np.arange(len(y)), stratify=y, **{k: v for k, v in config["split"].items() if k != "stratify"}
    )
    X_train, y_train = X.iloc[train_ids], y.iloc[train_ids]
    folds = list(StratifiedKFold(**config["cv"]).split(X_train, y_train))
    assignment = np.full(len(train_ids), -1, dtype=int)
    for number, (_, valid_pos) in enumerate(folds, 1):
        assignment[valid_pos] = number
    assert (assignment > 0).all()
    assert not set(train_ids).intersection(test_ids)
    assert set(train_ids).union(test_ids) == set(range(len(y)))
    tables = {
        "train_indices.csv": pd.DataFrame({"train_position": np.arange(len(train_ids)), "row_id": train_ids}),
        "test_indices.csv": pd.DataFrame({"test_position": np.arange(len(test_ids)), "row_id": test_ids}),
        "train_folds.csv": pd.DataFrame({"train_position": np.arange(len(train_ids)), "row_id": train_ids, "validation_fold": assignment}),
    }
    split_dir = FINAL_EXAM_DIR / config["split_dir"]
    split_dir.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        path = split_dir / name
        if path.exists():
            pd.testing.assert_frame_equal(pd.read_csv(path), table)
        else:
            table.to_csv(path, index=False, lineterminator="\n")
    manifest = {
        "data_sha256": config["data_sha256"], "row_id_definition": "Zero-based source CSV row, excluding header",
        "n_rows": len(y), "n_train": len(train_ids), "n_test": len(test_ids),
        "split": config["split"], "cv": config["cv"],
        "provenance": "Reconstructed locally from leader-confirmed recipe; no externally supplied indices in this checkout",
        "reference": "ThanhDat_EDA_DecisionTree.ipynb: train_test_split and StratifiedKFold cells",
        "files_sha256": {n: sha256(split_dir / n) for n in tables},
    }
    path = split_dir / "manifest.json"
    if path.exists():
        assert json.loads(path.read_text(encoding="utf-8")) == manifest, "Split manifest mismatch"
    else:
        write_json(path, manifest)
    return train_ids, test_ids, folds, manifest


def make_lr(config=None):
    config = config or read_config()
    return Pipeline([
        ("preprocessor", make_preprocessor(FINAL_EXAM_DIR / config["preprocessing_config"])),
        ("model", LogisticRegression(**config["lr"])),
    ])


def score(y_true, y_pred, labels):
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0
    )
    result = {"accuracy": accuracy_score(y_true, y_pred),
              "f1_macro": f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)}
    for i, label in enumerate(labels):
        result.update({f"precision_{label}": precision[i], f"recall_{label}": recall[i], f"f1_{label}": f1[i]})
    return result


def code_provenance():
    files = [CONFIG_PATH, FINAL_EXAM_DIR / "configs/hieu_preprocessing_v1.json",
             Path(__file__), FINAL_EXAM_DIR / "src/hieu_data_preprocessing.py"]
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=FINAL_EXAM_DIR, text=True).strip()
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=FINAL_EXAM_DIR, text=True)
    except (OSError, subprocess.CalledProcessError):
        commit, status = "unavailable", "unavailable"
    return {"base_commit": commit, "working_tree_status_at_start": status,
            "source_sha256": {str(p.relative_to(FINAL_EXAM_DIR)).replace("\\", "/"): sha256(p) for p in files}}


def write_analysis(out, run_id, summary_df, class_rows, all_oof, y_train):
    s = summary_df.set_index("model")
    lr, dummy = s.loc["LR"], s.loc["Dummy"]
    cm = confusion_matrix(y_train, all_oof[1]["y_pred"], labels=["Dropout", "Enrolled", "Graduate"])
    classes = pd.DataFrame(class_rows)
    lr_classes = classes[classes.model.eq("LR")].set_index("label")
    text = f"""# Phân tích Dummy và Logistic Regression — Lê Văn Hiếu

Run: {run_id}. Dữ liệu Train có {len(y_train)} sinh viên; Test 885 sinh viên được giữ riêng, chưa đánh giá.

## 1. Câu hỏi và thiết kế

Thực nghiệm kiểm tra LR cố định có cải thiện so với Dummy đoán lớp phổ biến nhất trên cùng 5 fold không, đồng thời tìm lớp còn khó và đánh giá gap train–validation. Không tuning hoặc chọn đặc trưng; không lựa chọn cấu hình theo Test. Tham số được ghi trước khi chạy, C=1, điều chuẩn L2, solver lbfgs, max_iter=2000, tol=1e-4, class_weight=None. Mức max_iter là giới hạn tối ưu để hội tụ, không phải số lượt chọn mô hình.

80/20 stratify, seed 42 và StratifiedKFold(5, shuffle=True, random_state=42) theo xác nhận của người dùng về leader Phát. Các file indices được tái tạo tại máy từ công thức đã xác nhận, cùng công thức notebook Đạt; chưa được so byte với bộ indices ngoài repo vì không có bộ đó trong checkout. Manifest lưu thứ tự dòng và hash để nhóm đối chiếu.

## 2. Kết quả CV (trung bình và độ lệch chuẩn 5 fold; ddof=0)

Dummy: Macro-F1 {dummy.valid_f1_macro_mean:.4f} ± {dummy.valid_f1_macro_std:.4f}; Accuracy {dummy.valid_accuracy_mean:.4f} ± {dummy.valid_accuracy_std:.4f}; Recall Dropout {dummy.valid_recall_Dropout_mean:.4f}.

LR: Macro-F1 {lr.valid_f1_macro_mean:.4f} ± {lr.valid_f1_macro_std:.4f}; Accuracy {lr.valid_accuracy_mean:.4f} ± {lr.valid_accuracy_std:.4f}; Recall Dropout {lr.valid_recall_Dropout_mean:.4f} ± {lr.valid_recall_Dropout_std:.4f}.

Chênh lệch Macro-F1 LR − Dummy: {lr.valid_f1_macro_mean-dummy.valid_f1_macro_mean:.4f} (thang 0–1). Dummy luôn dự đoán Graduate vì đây là lớp phổ biến nhất trong các phần train. Accuracy gần một nửa vẫn đi kèm Recall Dropout/Enrolled bằng 0; do đó không thể đánh giá chỉ bằng Accuracy. LR sử dụng thông tin đầu vào và cải thiện khả năng phân biệt lớp so với mốc này; chưa có căn cứ nói LR tốt nhất nhóm hoặc hiệu quả triển khai thực tế.

## 3. Phân tích dự đoán OOF trên Train

Mỗi sinh viên Train có đúng một dự đoán từ mô hình không học chính sinh viên đó ở fold tương ứng. Chỉ số từ toàn bộ dự đoán OOF được ghi riêng trong oof_summary.csv; không coi đó là kết quả Test và không thay thế CV mean bằng OOF F1.

"""
    for label, r in lr_classes.iterrows():
        text += f"{label}: Precision {r['precision']:.4f}; Recall {r['recall']:.4f}; F1 {r['f1-score']:.4f}; hỗ trợ {int(r['support'])} mẫu.\n\n"
    text += f"""Dropout: đúng {cm[0,0]}/{cm[0].sum()}, bỏ sót {cm[0,1]+cm[0,2]}, gồm {cm[0,1]} bị đoán Enrolled và {cm[0,2]} bị đoán Graduate. Ngược lại, {cm[1,0]+cm[2,0]} sinh viên thuộc hai lớp còn lại bị đoán Dropout. Cần cân nhắc cả bỏ sót và cảnh báo nhầm khi thảo luận mục tiêu hỗ trợ sinh viên.

Enrolled: đúng {cm[1,1]}/{cm[1].sum()}, nhầm sang Dropout {cm[1,0]} và Graduate {cm[1,2]}. Lớp có F1 thấp nhất trong OOF LR là {lr_classes['f1-score'].idxmin()}; có thể liên hệ với mất cân bằng và chồng lấn thông tin, nhưng thí nghiệm hiện tại chưa cô lập nguyên nhân.

## 4. Overfitting, độ ổn định và giới hạn

LR Train Macro-F1 trung bình {lr.train_f1_macro_mean:.4f}; Validation {lr.valid_f1_macro_mean:.4f}; gap trung bình {lr.gap_f1_macro_mean:.4f}. Đây là chênh lệch trên cùng 5 fold, không phải chênh lệch Train–Test. Gap và độ lệch chuẩn là bằng chứng mô tả trong bộ chia này; gap nhỏ không chứng minh không overfitting, và chưa đủ để chẩn đoán underfitting hay bảo đảm ổn định trên cohort/cơ sở giáo dục khác.

Chỉ khảo sát một split, một cấu hình LR và tiền xử lý ban đầu. Chưa tuning C, thử trọng số lớp hoặc thực hiện ablation; các hướng này chưa được tính là kết quả đã hoàn thành. Bộ đặc trưng gốc có HK2 nên không diễn giải thành dự đoán ngay lúc nhập học. Không kết luận quan hệ nhân quả từ kết quả dự đoán.

## 5. Bằng chứng và bàn giao

fold_metrics.csv ghi từng fold; cv_summary.csv ghi mean/std; oof_predictions.csv, class_metrics_oof.csv và confusion_lr.csv truy vết lỗi; leakage_checks.csv kiểm tra trung bình scaler và số mẫu chỉ từ train từng fold; warnings.json ghi cảnh báo. lr_train_only.joblib là pipeline fit trên toàn bộ Train sau CV, chưa dùng để đánh giá Test. Chỉ nạp file joblib từ nguồn tin cậy.

Phát sử dụng make_lr() cùng cấu hình để fit lại pipeline mới cho mỗi fold trong đối chứng A/B/C; không dùng bộ scaler/encoder đã fit toàn Train để đánh giá fold. Giữ các biến đổi của cột gốc và tham số LR cố định; việc xử lý đặc trưng mới thuộc phần đối chứng của Phát.

## 6. Việc còn lại

Đối chiếu hash các file split/fold với bộ nhóm đang lưu, đồng bộ phương pháp đánh giá khi so LR với DT/RF, kiểm tra chéo, xác nhận người thực hiện hiểu và diễn giải được kết quả; chỉ đánh giá Test khi nhóm chốt bước đánh giá đó. Chưa push hoặc xác nhận nhóm đã nhận sản phẩm.
"""
    (out / "analysis.md").write_text(text, encoding="utf-8")


def run_experiment():
    config = read_config()
    X, y = load_student_data()
    assert sha256(FINAL_EXAM_DIR / "data/raw/data.csv") == config["data_sha256"]
    train_ids, test_ids, folds, split_manifest = prepare_split(X, y, config)
    X_train, y_train = X.iloc[train_ids], y.iloc[train_ids]
    run_id = datetime.now(timezone.utc).strftime("HIEU_BASELINE_LR_%Y%m%dT%H%M%S_%fZ")
    out = FINAL_EXAM_DIR / "results" / run_id
    out.mkdir(parents=True, exist_ok=False)
    provenance = code_provenance()
    metadata = {"run_id": run_id, "status": "running", "owner": config["owner"],
                "started_at_utc": datetime.now(timezone.utc).isoformat(),
                "objective": "Does fixed LR improve on majority Dummy on the same folds, and which classes remain difficult?",
                "config": config, "split_manifest": split_manifest, "code": provenance,
                "test_evaluated": False}
    write_json(out / "run.json", metadata)  # Write intention BEFORE fit.
    write_json(out / "environment.json", {
        "python": platform.python_version(), "platform": platform.platform(),
        "packages": {n: importlib.metadata.version(n) for n in
                     ["scikit-learn", "numpy", "scipy", "pandas", "matplotlib", "joblib", "threadpoolctl"]},
    })
    fold_rows, all_oof, class_rows, checks, warning_rows, pooled_rows = [], [], [], [], [], []
    try:
        with threadpool_limits(limits=config["thread_limit"]):
            for model_name in ["Dummy", "LR"]:
                predictions = np.full(len(train_ids), "", dtype=object)
                counts = np.zeros(len(train_ids), dtype=int)
                for fold_number, (fit_pos, valid_pos) in enumerate(folds, 1):
                    model = DummyClassifier(**config["dummy"]) if model_name == "Dummy" else make_lr(config)
                    with warnings.catch_warnings(record=True) as caught:
                        warnings.simplefilter("always")
                        model.fit(X_train.iloc[fit_pos], y_train.iloc[fit_pos])
                        pred_train = model.predict(X_train.iloc[fit_pos])
                        pred_valid = model.predict(X_train.iloc[valid_pos])
                    for w in caught:
                        warning_rows.append({"model": model_name, "fold": fold_number,
                                             "category": w.category.__name__, "message": str(w.message)})
                    if any(issubclass(w.category, ConvergenceWarning) for w in caught):
                        raise RuntimeError("LR did not converge: inspect warnings before using results")
                    predictions[valid_pos] = pred_valid
                    counts[valid_pos] += 1
                    row = {"model": model_name, "fold": fold_number, "n_fit": len(fit_pos), "n_valid": len(valid_pos)}
                    row.update({"train_" + k: v for k, v in score(y_train.iloc[fit_pos], pred_train, config["labels"]).items()})
                    row.update({"valid_" + k: v for k, v in score(y_train.iloc[valid_pos], pred_valid, config["labels"]).items()})
                    row["gap_f1_macro"] = row["train_f1_macro"] - row["valid_f1_macro"]
                    row["n_iter"] = int(model.named_steps["model"].n_iter_.max()) if model_name == "LR" else 0
                    fold_rows.append(row)
                    if model_name == "LR":
                        # A useful leakage check: fitted scaler mean must equal ONLY this fold's fit rows.
                        scaler = model.named_steps["preprocessor"].named_transformers_["numeric"]
                        cols = json.loads((FINAL_EXAM_DIR / config["preprocessing_config"]).read_text(encoding="utf-8"))["numeric"]["columns"]
                        expected_mean = X_train.iloc[fit_pos][cols].mean().to_numpy()
                        np.testing.assert_allclose(scaler.mean_, expected_mean, rtol=1e-12, atol=1e-12)
                        assert int(scaler.n_samples_seen_) == len(fit_pos)
                        checks.append({"fold": fold_number, "scaler_seen": int(scaler.n_samples_seen_),
                                       "max_mean_error": float(np.max(np.abs(scaler.mean_ - expected_mean))),
                                       "fit_validation_disjoint": not bool(set(fit_pos).intersection(valid_pos))})
                assert (counts == 1).all(), "Each training row must have exactly one OOF prediction"
                assert not set(train_ids).intersection(test_ids)
                pooled_rows.append({"model": model_name, "evaluation": "pooled_OOF_train_only",
                                    **score(y_train, predictions, config["labels"])})
                pred_table = pd.DataFrame({"row_id": train_ids, "y_true": y_train.to_numpy(), "y_pred": predictions,
                                          "model": model_name, "validation_fold": np.zeros(len(train_ids), dtype=int)})
                for f, (_, vp) in enumerate(folds, 1):
                    pred_table.loc[vp, "validation_fold"] = f
                all_oof.append(pred_table)
                report = classification_report(y_train, predictions, labels=config["labels"], zero_division=0, output_dict=True)
                for label in config["labels"]:
                    class_rows.append({"model": model_name, "evaluation": "pooled_OOF_train_only", "label": label, **report[label]})
                cm = confusion_matrix(y_train, predictions, labels=config["labels"])
                pd.DataFrame(cm, index=config["labels"], columns=config["labels"]).rename_axis("true_label").to_csv(out / f"confusion_{model_name.lower()}.csv")
                fig, ax = plt.subplots(figsize=(6.6, 5.2))
                ConfusionMatrixDisplay(cm, display_labels=config["labels"]).plot(ax=ax, colorbar=False, cmap="Blues")
                ax.set_title(f"{model_name}: OOF predictions on Train (n={len(train_ids)})")
                ax.set_xlabel("Predicted label"); ax.set_ylabel("True label")
                fig.tight_layout(); fig.savefig(out / f"confusion_{model_name.lower()}.png", dpi=160); plt.close(fig)
            fold_metrics = pd.DataFrame(fold_rows)
            numeric_metrics = [c for c in fold_metrics if c.startswith(("train_", "valid_", "gap_"))]
            summary = []
            for name, frame in fold_metrics.groupby("model", sort=False):
                record = {"model": name, "evaluation": "mean_of_5_CV_folds", "std_ddof": 0}
                for c in numeric_metrics:
                    record[c + "_mean"] = float(frame[c].mean())
                    record[c + "_std"] = float(frame[c].std(ddof=0))
                summary.append(record)
            summary_df = pd.DataFrame(summary)
            for name, table in {"fold_metrics.csv": fold_metrics, "cv_summary.csv": summary_df,
                                "oof_predictions.csv": pd.concat(all_oof, ignore_index=True),
                                "oof_summary.csv": pd.DataFrame(pooled_rows), "class_metrics_oof.csv": pd.DataFrame(class_rows),
                                "leakage_checks.csv": pd.DataFrame(checks)}.items():
                table.to_csv(out / name, index=False, lineterminator="\n")
            for name, group in fold_metrics.groupby("model", sort=False):
                if name == "Dummy":
                    # Majority baseline is analytically checkable per validation fold.
                    for i, (_, vp) in enumerate(folds):
                        majority = y_train.iloc[folds[i][0]].value_counts().idxmax()
                        assert set(all_oof[0].iloc[vp]["y_pred"]) == {majority}
            fig, ax = plt.subplots(figsize=(7, 4.4))
            for name, frame in fold_metrics.groupby("model", sort=False):
                ax.errorbar([name], [frame.valid_f1_macro.mean()], yerr=[frame.valid_f1_macro.std(ddof=0)], fmt="o", capsize=6)
            ax.set_ylim(0, 1); ax.set_ylabel("Validation Macro-F1 (mean ± population std)")
            ax.set_xlabel("Model"); ax.set_title("Fixed models, same five folds on Train; Test untouched")
            fig.tight_layout(); fig.savefig(out / "cv_comparison.png", dpi=160); plt.close(fig)
            # This fixed configuration is handed off; no parameter selection from Test.
            final_lr = make_lr(config)
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                final_lr.fit(X_train, y_train)
            if any(issubclass(w.category, ConvergenceWarning) for w in caught):
                raise RuntimeError("Full-train LR did not converge")
            warning_rows.extend({"model": "LR_full_train", "fold": None, "category": w.category.__name__, "message": str(w.message)} for w in caught)
            joblib.dump(final_lr, out / "lr_train_only.joblib")
        write_json(out / "warnings.json", warning_rows)
        write_json(out / "lr_handoff.json", {"run_id": run_id, "model": config["lr"],
                   "preprocessing_config": config["preprocessing_config"], "split_dir": config["split_dir"],
                   "data_sha256": config["data_sha256"], "test_evaluated": False,
                   "instruction": "For ablation refit a NEW pipeline in each fold. Keep LR and transforms for original columns fixed; do not reuse fitted OOF/full-train preprocessors."})
        write_analysis(out, run_id, summary_df, class_rows, all_oof, y_train)
        metadata.update(status="complete", completed_at_utc=datetime.now(timezone.utc).isoformat(),
                        validation_checks="OOF coverage, no Train/Test overlap, per-fold scaler mean and sample count verified")
        write_json(out / "run.json", metadata)
        logs_dir = FINAL_EXAM_DIR / "logs"; logs_dir.mkdir(exist_ok=True)
        logs = []
        for record in summary:
            logs.append({"run_id": run_id + "_" + record["model"], "owner": config["owner"],
                         "timestamp": metadata["started_at_utc"], "objective_hypothesis": metadata["objective"],
                         "data_version": config["data_sha256"], "code_commit": provenance["base_commit"],
                         "code_hash_manifest": f"results/{run_id}/run.json", "model": record["model"],
                         "features": "36 original features", "preprocessing": config["preprocessing_config"] if record["model"] == "LR" else "none; Dummy ignores X",
                         "params": json.dumps(config["lr"] if record["model"] == "LR" else config["dummy"]),
                         "split_id": config["split_dir"], "seed": 42, "cv": "StratifiedKFold(5, shuffle=True, random_state=42)",
                         "metrics": json.dumps(record), "observations": "See analysis.md, fold_metrics.csv and class_metrics_oof.csv; Test untouched",
                         "conclusion": "Fixed LR compared with majority baseline; no claim of best algorithm in group",
                         "output_link": f"results/{run_id}"})
        pd.DataFrame(logs).to_csv(logs_dir / f"{run_id}.csv", index=False, lineterminator="\n")
        return out
    except Exception as exc:
        write_json(out / "warnings.json", warning_rows)
        metadata.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        write_json(out / "run.json", metadata)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(run_experiment())
