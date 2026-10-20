import os
import zipfile
import shutil

def package():
    base_dir = os.path.abspath('Lab05_ThucHanhBaiToanPhanLop')
    workspace_dir = os.path.abspath('.')
    
    zip_name_primary = 'Lab05_ModelTraining_LeVanHieu_3124411091.zip'
    zip_path_primary = os.path.join(workspace_dir, zip_name_primary)
    
    zip_name_secondary = 'Lab05_ModelTraining_HoTen_MaSV.zip'
    zip_path_secondary = os.path.join(workspace_dir, zip_name_secondary)

    # Allowed scripts in scripts/ folder
    clean_scripts = {
        'build_full_report.py',
        'generate_theory_docx.py',
        'execute_all_notebooks.py',
        'patch_svm_notebooks.py'
    }

    # Remove old zips if existing
    for z in [zip_path_primary, zip_path_secondary]:
        if os.path.exists(z):
            os.remove(z)

    print(f"Packaging {zip_name_primary} ...")
    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(zip_path_primary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(base_dir):
            rel_dir = os.path.relpath(root, base_dir)
            
            # Skip hidden and cache directories
            if rel_dir != '.' and any((part.startswith('.') and part != '.') or part == '__pycache__' for part in rel_dir.split(os.sep)):
                continue

            for f in sorted(files):
                # Filter unwanted files
                if f.startswith('.') or f.endswith('.pyc') or f == '.keep':
                    continue
                
                # In scripts/ folder, include only clean scripts
                if rel_dir == 'scripts' and f not in clean_scripts:
                    continue
                
                # Skip legacy lab.docx template if Bao_Cao_Tong_Hop and dedicated docs are present,
                # but keep lab.docx as reference if needed. Let's keep it.

                file_path = os.path.join(root, f)
                arcname = os.path.join(rel_dir, f) if rel_dir != '.' else f
                # Normalize zip path with forward slash
                arcname = arcname.replace(os.sep, '/')
                
                zipf.write(file_path, arcname)
                file_count += 1
                total_uncompressed_bytes += os.path.getsize(file_path)

    # Make exact copy for Lab05_ModelTraining_HoTen_MaSV.zip
    shutil.copy2(zip_path_primary, zip_path_secondary)

    compressed_size = os.path.getsize(zip_path_primary)
    print("\n" + "="*70)
    print("DONG GOI THANH CONG!")
    print(f"File zip chinh : {zip_path_primary}")
    print(f"Dung luong     : {compressed_size:,} bytes ({compressed_size / (1024*1024):.2f} MB)")
    print(f"So luong files : {file_count} files")
    print(f"Dung luong goc : {total_uncompressed_bytes:,} bytes ({total_uncompressed_bytes / (1024*1024):.2f} MB)")
    print(f"File copy alias: {zip_path_secondary}")
    print("="*70)

if __name__ == '__main__':
    package()
