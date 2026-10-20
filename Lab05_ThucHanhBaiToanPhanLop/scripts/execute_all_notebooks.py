import os
import sys
import asyncio
import nbformat
from nbclient import NotebookClient

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sys.stdout.reconfigure(encoding='utf-8')

code_dir = os.path.abspath('Lab05_ThucHanhBaiToanPhanLop/code')

notebooks_to_run = [
    '01_CreditCard_DT_RF.ipynb',
    '02_Titanic_DT_RF.ipynb',
    '03_Diabetes_DT_RF.ipynb',
    'lab2_1_DecisionTree_RandomForest.ipynb',
    '01-iris-svm.ipynb',
    '02-digits-svm.ipynb',
    'lab2_3_NaiveBayes.ipynb'
]

for nb_name in notebooks_to_run:
    nb_path = os.path.join(code_dir, nb_name)
    if not os.path.exists(nb_path):
        print(f"File not found: {nb_path}")
        continue
    print(f"\n>>> Dang thuc thi notebook: {nb_name} ...", flush=True)
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        client = NotebookClient(nb, timeout=300, kernel_name='python3', resources={'metadata': {'path': code_dir}})
        client.execute()
        
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        
        output_count = sum(len(c.get('outputs', [])) for c in nb.cells if c.cell_type == 'code')
        print(f"Thanh cong: {nb_name} da luu voi {output_count} outputs.", flush=True)
    except Exception as e:
        print(f"Loi khi thuc thi {nb_name}: {e}", flush=True)
