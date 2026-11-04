"""Local, append-preserving experiment records. No cloud writes or credentials."""

import csv
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .data import PROJECT_DIR

INDEX_COLUMNS = [
    "run_id", "owner", "started_at_utc", "model_id", "version", "status",
    "objective", "evaluation_stage", "data_sha256", "split_id", "cv_folds",
    "macro_f1_mean", "macro_f1_std", "std_ddof", "accuracy_mean",
    "dropout_recall_mean", "train_valid_gap", "duration_sec", "base_commit",
    "results_path", "wandb_status", "error",
]


def write_json(path, value):
    Path(path).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class LocalRun:
    """One model/version/execution; update only this run's index entry."""

    def __init__(self, config_path, config, split_manifest):
        started = datetime.now(timezone.utc)
        self.run_id = f"{config['model_id']}_{config['version']}_{started:%Y%m%dT%H%M%S}_{uuid.uuid4().hex[:8]}"
        self.path = PROJECT_DIR / "experiments/runs" / self.run_id
        self.path.mkdir(parents=True, exist_ok=False)
        self.record = dict.fromkeys(INDEX_COLUMNS, "")
        self.record.update(
            run_id=self.run_id, owner=config["owner"], started_at_utc=started.isoformat(),
            model_id=config["model_id"], version=config["version"], status="running",
            objective=config["objective"], evaluation_stage="CV_train_only",
            data_sha256=split_manifest["data_sha256"],
            split_id="student_dropout_seed42_v1", cv_folds=5, std_ddof=0,
            results_path=self.path.relative_to(PROJECT_DIR).as_posix(),
            wandb_status="not_configured",
        )
        source_files = [PROJECT_DIR / p for p in [
            "src/data.py", "src/features.py", "src/evaluate.py", "src/tracking.py",
            "configs/lr_preprocessing_v1.json", "requirements.txt",
        ]] + [Path(config_path), Path(config_path).with_name("train.py")]
        try:
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_DIR, text=True).strip()
            status = subprocess.check_output(["git", "status", "--porcelain", "--", "."], cwd=PROJECT_DIR, text=True)
        except (OSError, subprocess.CalledProcessError):
            commit, status = "unavailable", "unavailable"
        self.record["base_commit"] = commit
        self.path.joinpath("config.yaml").write_bytes(Path(config_path).read_bytes())
        write_json(self.path / "git_info.json", {
            "base_commit": commit, "working_tree_status_at_start": status,
            "source_sha256": {p.relative_to(PROJECT_DIR).as_posix(): sha256(p) for p in source_files},
            "note": "Source may be uncommitted during review; hashes identify the executed files.",
            "split_manifest": split_manifest,
        })
        write_json(self.path / "environment.json", {
            "python": platform.python_version(), "platform": platform.platform(),
            "packages": {name: importlib.metadata.version(name) for name in [
                "numpy", "pandas", "scipy", "scikit-learn", "matplotlib", "PyYAML", "joblib", "threadpoolctl",
            ]},
        })
        self.save()

    def save(self):
        write_json(self.path / "tracking.json", {
            **self.record, "backend": "local", "wandb_run_id": None,
            "wandb_url": None, "sheets_synced": False,
            "test_scored_this_run": False,
        })
        index_path = PROJECT_DIR / "experiments/results.csv"
        if index_path.exists() and index_path.stat().st_size:
            with index_path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                if reader.fieldnames != INDEX_COLUMNS:
                    raise ValueError("Experiment index schema differs; refusing to overwrite")
                records = [row for row in reader if row["run_id"] != self.run_id]
        else:
            records = []
        temporary = index_path.with_suffix(".csv.tmp")
        with temporary.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=INDEX_COLUMNS, lineterminator="\n")
            writer.writeheader()
            writer.writerows([*records, self.record])
        temporary.replace(index_path)
