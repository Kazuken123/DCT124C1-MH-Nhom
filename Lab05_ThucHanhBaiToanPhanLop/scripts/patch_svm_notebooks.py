import json
import os
from pathlib import Path

def patch_02():
    path = 'Lab05_ThucHanhBaiToanPhanLop/code/02-digits-svm.ipynb'
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    for c in nb['cells']:
        if c['cell_type'] == 'code':
            src = c['source']
            if any('output_dir = Path("/kaggle/working")' in l for l in src):
                new_src = []
                for l in src:
                    if 'output_dir = Path("/kaggle/working")' in l:
                        new_src.append(l.replace('output_dir = Path("/kaggle/working")', 'output_dir = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path(".")'))
                    else:
                        new_src.append(l)
                c['source'] = new_src
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Patched 02-digits-svm.ipynb")

def patch_03():
    path = 'Lab05_ThucHanhBaiToanPhanLop/code/03-diabetes-svm.ipynb'
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    for c in nb['cells']:
        if c['cell_type'] == 'code':
            src = c['source']
            if any('csv_files = list(Path("/kaggle/input").rglob("*.csv"))' in l for l in src):
                new_src = []
                for l in src:
                    if 'csv_files = list(Path("/kaggle/input").rglob("*.csv"))' in l:
                        new_src.append(l)
                        new_src.append('if not csv_files:\n')
                        new_src.append('    candidates = [Path("../data/diabetes_prediction_dataset.csv"), Path("data/diabetes_prediction_dataset.csv"), Path("Lab05_ThucHanhBaiToanPhanLop/data/diabetes_prediction_dataset.csv")]\n')
                        new_src.append('    csv_files = [p for p in candidates if p.exists()]\n')
                    else:
                        new_src.append(l)
                c['source'] = new_src
            
            # replace /kaggle/working/
            new_src = []
            for l in c['source']:
                l_mod = l.replace('"/kaggle/working/', 'str(Path("/kaggle/working") if Path("/kaggle/working").exists() else Path(".")) + "/')
                l_mod = l_mod.replace('Path("/kaggle/working")', 'Path("/kaggle/working") if Path("/kaggle/working").exists() else Path(".")')
                new_src.append(l_mod)
            c['source'] = new_src
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Patched 03-diabetes-svm.ipynb")

def patch_04():
    path = 'Lab05_ThucHanhBaiToanPhanLop/code/04-animal-svm.ipynb'
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    for c in nb['cells']:
        if c['cell_type'] == 'code':
            src = c['source']
            if any('csv_files = list(' in l for l in src) and any('rglob("*.csv")' in l for l in src):
                new_src = []
                for l in src:
                    new_src.append(l)
                    if 'rglob("*.csv")' in l:
                        new_src.append('if not csv_files:\n')
                        new_src.append('    candidates = [Path("../data/AnimalCondition.csv"), Path("data/AnimalCondition.csv"), Path("Lab05_ThucHanhBaiToanPhanLop/data/AnimalCondition.csv")]\n')
                        new_src.append('    csv_files = [p for p in candidates if p.exists()]\n')
                c['source'] = new_src

            # replace /kaggle/working/
            new_src = []
            for l in c['source']:
                l_mod = l.replace('"/kaggle/working/', 'str(Path("/kaggle/working") if Path("/kaggle/working").exists() else Path(".")) + "/')
                l_mod = l_mod.replace('Path("/kaggle/working")', 'Path("/kaggle/working") if Path("/kaggle/working").exists() else Path(".")')
                new_src.append(l_mod)
            c['source'] = new_src
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Patched 04-animal-svm.ipynb")

if __name__ == '__main__':
    patch_02()
    patch_03()
    patch_04()
