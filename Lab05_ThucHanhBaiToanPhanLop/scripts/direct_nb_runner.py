import os
import sys
import io
import json
import base64
import contextlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IPython.display import display

def execute_notebook_directly(nb_path, working_dir=None):
    orig_cwd = os.getcwd()
    if working_dir:
        os.chdir(working_dir)
    
    print(f"\n=======================================================", flush=True)
    print(f"Dang thuc thi truc tiep: {os.path.basename(nb_path)}", flush=True)
    print(f"Thu muc lam viec: {os.getcwd()}", flush=True)
    
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
            
        exec_globals = {
            '__name__': '__main__',
            '__file__': nb_path,
            'display': display
        }
        
        exec_count = 1
        has_error = False
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] != 'code':
                continue
                
            code_text = "".join(cell.get('source', []))
            if not code_text.strip():
                continue
                
            outputs = []
            captured_stdout = io.StringIO()
            captured_stderr = io.StringIO()
            
            def custom_show(*args, **kwargs):
                for fignum in plt.get_fignums():
                    fig = plt.figure(fignum)
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
                    buf.seek(0)
                    img_b64 = base64.b64encode(buf.read()).decode('ascii')
                    outputs.append({
                        "output_type": "display_data",
                        "data": {
                            "image/png": img_b64,
                            "text/plain": ["<Figure size ...>"]
                        },
                        "metadata": {}
                    })
                    plt.close(fig)
            
            old_show = plt.show
            plt.show = custom_show
            
            try:
                with contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
                    exec(code_text, exec_globals)
                custom_show()
            except Exception as e:
                print(f"Loi tai cell {i}: {e}", flush=True)
                has_error = True
                outputs.append({
                    "output_type": "error",
                    "ename": type(e).__name__,
                    "evalue": str(e),
                    "traceback": [str(e)]
                })
            finally:
                plt.show = old_show
                plt.close('all')
                
            stdout_str = captured_stdout.getvalue()
            if stdout_str:
                outputs.insert(0, {
                    "output_type": "stream",
                    "name": "stdout",
                    "text": [line + '\n' for line in stdout_str.splitlines()]
                })
                
            stderr_str = captured_stderr.getvalue()
            if stderr_str:
                outputs.append({
                    "output_type": "stream",
                    "name": "stderr",
                    "text": [line + '\n' for line in stderr_str.splitlines()]
                })
                
            cell['outputs'] = outputs
            cell['execution_count'] = exec_count
            exec_count += 1
            print(f"  Cell {i} da xong ({len(outputs)} outputs)", flush=True)
            
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=2)
            
        if has_error:
            print(f"CANH BAO: {nb_path} co cell loi!", flush=True)
        else:
            print(f"HOAN TAT THANH CONG: {nb_path}", flush=True)
    finally:
        os.chdir(orig_cwd)

if __name__ == '__main__':
    code_dir = os.path.abspath('Lab05_ThucHanhBaiToanPhanLop/code')
    notebooks = [
        '01_CreditCard_DT_RF.ipynb',
        '02_Titanic_DT_RF.ipynb',
        '03_Diabetes_DT_RF.ipynb',
        'lab2_1_DecisionTree_RandomForest.ipynb'
    ]
    for nb_name in notebooks:
        nb_file = os.path.join(code_dir, nb_name)
        execute_notebook_directly(nb_file, working_dir=code_dir)
