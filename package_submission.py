#!/usr/bin/env python3
"""Package the midterm submission into Nhom10_StudentDropout_GiuaKy.zip."""

import os
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def package():
    zip_filename = "Nhom10_StudentDropout_GiuaKy.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)

    # Export clean experiment log from Google Sheets or sheet_latest
    exp_log_src = "sheet_latest.csv"
    exp_log_dest = "Experiment_Log.csv"
    if os.path.exists(exp_log_src):
        import shutil
        shutil.copy(exp_log_src, exp_log_dest)

    files_to_include = [
        "BaoCao_TienDo_GiuaKy_Nhom10.docx",
        "BaoCao_TienDo_GiuaKy_Nhom10.pptx",
        "AUDIT_REPORT.md",
        "REPORT_BLUEPRINT.md",
        "README.md",
        "requirements.txt",
        "run_all.py",
        "test_all.py",
        "Experiment_Log.csv"
    ]

    folders_to_include = [
        "figures_report",
        "final"
    ]

    print(f"Creating {zip_filename}...")
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add root individual files
        for f in files_to_include:
            if os.path.exists(f):
                zf.write(f, arcname=f)
                print(f"  + Added file: {f}")
            else:
                print(f"  ! Warning: {f} not found")

        # Add folders
        for folder in folders_to_include:
            p_folder = Path(folder)
            if p_folder.is_dir():
                for root, dirs, files in os.walk(p_folder):
                    # Skip __pycache__ and git metadata
                    dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith(".")]
                    for file in files:
                        if file.endswith((".pyc", ".DS_Store")):
                            continue
                        full_path = Path(root) / file
                        arcname = full_path.relative_to(p_folder.parent)
                        zf.write(full_path, arcname=str(arcname))
                print(f"  + Added folder: {folder}/")

    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"\n[THÀNH CÔNG] Đã tạo gói nộp bài: {zip_filename} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    package()
