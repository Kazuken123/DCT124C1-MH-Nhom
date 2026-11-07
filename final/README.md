# Student Dropout Prediction

**Đồ án cuối kỳ – Môn Máy học (Machine Learning)**

## 1. Giới thiệu dự án

Dự án xây dựng và đánh giá các mô hình Machine Learning nhằm dự đoán tình trạng học tập của sinh viên dựa trên thông tin cá nhân, hoàn cảnh kinh tế - xã hội và kết quả học tập.

Bài toán thuộc nhóm **Supervised Learning (học có giám sát)**, cụ thể là **Multiclass Classification (phân loại đa lớp)**.

Mô hình dự đoán một trong ba trạng thái:

- **Dropout:** Sinh viên bỏ học.
- **Enrolled:** Sinh viên còn đang theo học.
- **Graduate:** Sinh viên đã tốt nghiệp.

Mục tiêu là xây dựng quy trình thực nghiệm có thể tái lập, so sánh các thuật toán một cách công bằng và lựa chọn mô hình dựa trên bằng chứng thực nghiệm.

Thời điểm thực hiện dự đoán và phạm vi đặc trưng được sử dụng sẽ được xác định trong giai đoạn phân tích dữ liệu nhằm tránh rò rỉ thông tin tương lai.

## 2. Thông tin dữ liệu

**Tên dataset:** Predict Students' Dropout and Academic Success

**Nguồn:** UCI Machine Learning Repository

**Đường dẫn:** https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success

**DOI:** 10.24432/C5MC89

| Thuộc tính | Giá trị |
|---|---|
| Số lượng mẫu | 4.424 |
| Số đặc trưng đầu vào | 36 |
| Biến mục tiêu | `Target` |
| Số lớp | 3 |
| Định dạng | CSV |
| Dấu phân cách | `;` |
| Giấy phép được ghi trong manifest | CC BY 4.0 |

**Phân phối nhãn:**

| Nhãn | Số lượng |
|---|---:|
| Dropout | 1.421 |
| Enrolled | 794 |
| Graduate | 2.209 |
| **Tổng** | **4.424** |

Dữ liệu gốc được lưu tại `data/raw/data.csv` và không chỉnh sửa trực tiếp.

Thông tin nguồn và checksum được lưu tại `data/source_manifest.json`.

## 3. Cấu trúc dự án

Thư mục gốc của đồ án là `final/`.

| Đường dẫn | Chức năng |
|---|---|
| `data/raw/` | Lưu dữ liệu gốc |
| `data/processed/` | Lưu dữ liệu đã xử lý nếu cần |
| `configs/project.yaml` | Cấu hình chung của dự án |
| `configs/splits/` | Chỉ số Train/Test và CV cố định |
| `configs/wandb.yaml` | Cấu hình tích hợp W&B |
| `src/data.py` | Đọc dữ liệu và nạp split |
| `src/features.py` | Tiền xử lý và xây dựng đặc trưng |
| `src/evaluate.py` | Đánh giá mô hình |
| `src/tracking.py` | Theo dõi và lưu kết quả thí nghiệm |
| `models/` | Mã nguồn và cấu hình từng mô hình |
| `notebooks/<model_id>/vN.ipynb` | Notebook riêng cho từng mô hình và phiên bản, có bảng/hình và cách chạy lại |
| `experiments/runs/` | Kết quả chi tiết từng lần chạy |
| `experiments/results.csv` | Bảng tổng hợp các thí nghiệm |
| `experiments/ablation.csv` | Kết quả nghiên cứu loại bỏ thành phần |
| `figures/` | Toàn bộ hình ảnh, sơ đồ và biểu đồ thực nghiệm gốc |
| `reports/` | Báo cáo, bảng kết quả, tài liệu |
| `demo/` | Ứng dụng minh họa |
| `references/` | Tài liệu tham khảo |
| `requirements.txt` | Danh sách thư viện cần cài đặt |

## 4. Chia dữ liệu và Cross-Validation

Dự án thống nhất sử dụng một bộ chia dữ liệu cố định cho mọi mô hình.

| Tham số | Giá trị |
|---|---|
| Train | 80% – 3.539 mẫu |
| Test | 20% – 885 mẫu |
| Random seed | 42 |
| Stratify | Có |
| Cross-Validation | 5 folds |
| CV shuffle | Có |

Bộ chỉ số được lưu tại:

`configs/splits/student_dropout_seed42_v1/`

Gồm bốn file:

- `manifest.json`: Thông tin và checksum của bộ chia.
- `train_indices.csv`: Chỉ số mẫu Train.
- `test_indices.csv`: Chỉ số mẫu Test.
- `train_folds.csv`: Phân công validation fold cho từng mẫu Train.

**Quy định bắt buộc:**

- Không tạo lại bộ split riêng cho từng mô hình.
- Không sử dụng Test để chọn thuật toán hoặc tinh chỉnh siêu tham số.
- Preprocessing phải được fit trên dữ liệu huấn luyện tương ứng trong từng fold.
- Dùng cùng bộ chỉ số và cùng cách tính metric để so sánh mô hình.
- Chỉ sử dụng Test để đánh giá mô hình cuối cùng sau khi đã chốt champion.

## 5. Danh sách mô hình

| Thư mục | Thuật toán | Vai trò |
|---|---|---|
| `m01_baseline` | Dummy Classifier | Mốc so sánh tối thiểu |
| `m02_decision_tree` | Decision Tree | Mô hình cây quyết định |
| `m03_random_forest` | Random Forest | Mô hình tập hợp nhiều cây |
| `m04_xgboost` | XGBoost | Dự kiến, chờ phân công |
| `m05_logistic_regression` | Logistic Regression | Mô hình tuyến tính |


Danh sách này thể hiện các thư mục đã thiết kế, **không đồng nghĩa tất cả mô hình đã được huấn luyện**.

Mỗi mô hình có các phiên bản `v1`, `v2`, `v3`,... Khi thay đổi có ý nghĩa đối với thuật toán, đặc trưng hoặc siêu tham số, nhóm tạo phiên bản mới thay vì ghi đè phiên bản cũ.

## 6. Quản lý thí nghiệm

Mỗi lần huấn luyện phải có một `run_id` duy nhất.

Mã nguồn và cấu hình phiên bản nằm trong `models/<model_name>/<version>/`.

Kết quả thực tế của từng lần chạy được lưu riêng tại:

`experiments/runs/<run_id>/`

Các artifact dự kiến gồm:

| File | Nội dung |
|---|---|
| `config.yaml` | Cấu hình thực tế đã sử dụng |
| `metrics.json` | Metric của lần chạy |
| `fold_metrics.csv` | Kết quả theo từng fold |
| `oof_predictions.csv` | Dự đoán Out-of-Fold |
| `environment.json` | Thông tin môi trường và thư viện |
| `git_info.json` | Git commit và trạng thái mã nguồn |
| `tracking.json` | Mã run trên W&B và thông tin đồng bộ |
| `notes.md` | Giả thuyết, phân tích và kết luận |
| `figures/` | Biểu đồ được tạo trong thí nghiệm |

Model artifact được lưu khi cần, với định dạng phù hợp như `.pkl`, `.joblib` hoặc `.pt`.

**Không ghi đè kết quả từ run trước.**

### Nhật ký tổng hợp

`experiments/results.csv` chứa danh sách các lần chạy, đường dẫn run, thuật toán, phiên bản, cấu hình, metric và trạng thái.

`experiments/ablation.csv` lưu kết quả Ablation Study (nghiên cứu loại bỏ thành phần) và liên kết mỗi phép đối chứng với run nguồn.

Cần phân biệt rõ:

- **CV:** Kết quả Cross-Validation.
- **OOF:** Kết quả tổng hợp từ dự đoán ngoài fold huấn luyện.
- **Test:** Kết quả kiểm thử độc lập của champion cuối cùng.

Không được dùng kết quả OOF hoặc CV rồi ghi nhãn là Test.

## 7. Quy trình thực nghiệm

Mỗi thí nghiệm thực hiện theo trình tự:

1. **Giả thuyết:** Nêu rõ thay đổi dự kiến và lý do.
2. **Huấn luyện:** Kiểm soát sự thay đổi giữa các phiên bản.
3. **Đánh giá:** Tính metric trên Train, Validation và CV khi phù hợp.
4. **Phân tích:** Kiểm tra overfitting, underfitting và lỗi theo từng lớp.
5. **Kết luận:** So sánh với baseline và champion.
6. **Lưu kết quả:** Tạo run riêng, ghi nhật ký và cập nhật bảng tổng hợp.

Chỉ mở rộng sang thuật toán phức tạp hơn khi có mục tiêu nghiên cứu hoặc kết quả thực nghiệm hỗ trợ.

## 8. Metric đánh giá

Vì dữ liệu có ba lớp với số lượng không đồng đều, nhóm dự kiến sử dụng:

- **Macro F1:** Đề xuất làm metric chính, cần thống nhất chính thức với nhóm.
- **Accuracy:** Tỷ lệ dự đoán đúng tổng thể.
- **Precision, Recall, F1-score theo lớp:** Phân tích kết quả từng nhóm.
- **Confusion Matrix:** Phân tích các trường hợp nhầm lẫn.
- **CV mean ± std:** Đánh giá hiệu quả và độ ổn định của mô hình qua các fold.

Không kết luận một mô hình tốt hơn chỉ dựa trên chênh lệch metric rất nhỏ mà chưa xem xét độ biến động kết quả.

## 9. Theo dõi thí nghiệm

Hệ thống tracking được thiết kế để liên kết:

**Git commit → Model Version → Run ID → Cấu hình → Metrics → W&B → Google Sheets**

Công cụ dự kiến:

- **Git/GitHub:** Quản lý mã nguồn và lịch sử thay đổi.
- **Weights & Biases (W&B):** Theo dõi và so sánh thí nghiệm.
- **Google Sheets:** Tổng hợp nhật ký chung của nhóm.
- **Local artifacts:** Lưu kết quả gốc của từng run để có thể kiểm tra độc lập.

Tích hợp W&B và Google Sheets hiện thuộc giai đoạn triển khai, chưa được xác nhận hoạt động.

Không đưa API key, access token hoặc thông tin xác thực lên repository.

## 10. Môi trường và cách chạy

**Môi trường phát triển:**

- Python 3
- GitHub Codespaces / VS Code
- Jupyter Notebook khi cần khám phá dữ liệu
- Scikit-learn và các thư viện liên quan tùy mô hình

**Kiểm tra phiên bản Python:**

`python3 --version`

**Tạo môi trường ảo tại thư mục gốc repository:**

`python3 -m venv .venv`

**Kích hoạt trên Codespaces:**

`source .venv/bin/activate`

Sau khi `requirements.txt` được hoàn thiện, cài đặt thư viện bằng:

`pip install -r final/requirements.txt`

Lệnh đọc và kiểm chứng dữ liệu từ thư mục gốc repo:

`python3 final/src/data.py`

Trên Windows, nếu đã tạo `.venv` ở gốc repo:

```powershell
.\.venv\Scripts\python.exe -m pip install -r final/requirements.txt
.\.venv\Scripts\python.exe final/src/data.py
```

Phần dữ liệu/preprocessing đã kiểm tra với Python 3.12.14. `requirements.txt` hiện chỉ bao gồm thư viện cho phần này, chưa phải môi trường đã kiểm chứng cho XGBoost, demo hoặc tracking.

Lệnh kiểm chứng chỉ đọc CSV và bộ chỉ số có sẵn, in số mẫu/phân phối lớp từng fold; không tạo lại split, fit preprocessing hoặc huấn luyện mô hình. Minh chứng kiểm tra ngày 04/11/2026 nằm tại `reports/tables/data_validation_v1.json`. Trong kiểm thử riêng, preprocessing được fit tạm trên phần Train của từng fold để kiểm tra scaler; không lưu transformer đã fit và không huấn luyện classifier.

Khi viết mô hình, chạy từ `final/` và dùng API chung:

```python
from src.data import load_student_data, load_splits
from src.features import make_preprocessor

X, y = load_student_data()  # Target nằm riêng ở y; row index giữ thứ tự nguồn
train_ids, test_ids, folds, manifest = load_splits()
X_train, y_train = X.iloc[train_ids], y.iloc[train_ids]
preprocessor = make_preprocessor()  # mới, chưa fit
# folds chứa vị trí tương đối trong X_train, không phải row_id toàn dataset.
# Đặt preprocessor vào Pipeline mới trong từng fold của LR.
```

`configs/lr_preprocessing_v1.json` bảo toàn cấu hình LR đã kiểm chứng: 18 cột StandardScaler, 10 cột One-Hot và 8 cột nhị phân giữ nguyên. Đây là preprocessing của LR v1; mô hình cây có thể dùng cấu hình phù hợp riêng. Chưa thêm đặc trưng, imputation, loại ngoại lệ hoặc resampling.

Các file split được nạp nguyên thứ tự và kiểm tra checksum theo manifest. Thuộc tính Git giữ CSV nguồn nguyên byte và CSV chỉ số ở LF, tránh sai checksum do CRLF trên Windows. Nguồn gốc tái tạo bộ chia được giữ trong manifest; notebook cũ được tham chiếu ở đó hiện nằm trong lịch sử Git trước khi chuyển khung.

### Chạy Dummy và Logistic Regression v1

Mỗi mô hình có thư mục notebook riêng, đồng nhất model ID với thư mục code. Mở trong VS Code và chọn kernel `.venv`:

- Dummy v1: `notebooks/m01_baseline/v1.ipynb`.
- LR v1: `notebooks/m05_logistic_regression/v1.ipynb`.

Khi có thay đổi phương pháp/cấu hình, thêm `v2.ipynb`, `v3.ipynb`… trong thư mục đúng mô hình; v1 giữ làm mốc. Hiện chỉ tạo v1 đã có kết quả, không tạo sẵn các notebook v2–v10 rỗng. Thay người thực hiện không tự làm tăng version; ghi tác giả và thay đổi trong notebook/config/run tương ứng.

Cài thêm thư viện notebook từ gốc repo:

```powershell
.\.venv\Scripts\python.exe -m pip install -r final/requirements-notebook.txt
```

Hai notebook đã chạy toàn bộ các ô đọc dữ liệu/kết quả và lưu outputs để xem ngay bảng/hình. Mỗi notebook chỉ tạo/hiển thị mô hình của nó. Mặc định `RUN_NEW_EXPERIMENT=False`: đọc run v1 đã kiểm chứng, không huấn luyện lại. Đổi thành `True` ở mục 5 để huấn luyện riêng mô hình đó bằng factory và CV runner dùng chung, tạo run mới; không sao chép thuật toán vào notebook và không ghi đè run cũ. Outputs hiện có trình bày kết quả đã huấn luyện trước đó, không phải một lần huấn luyện mới bên trong notebook.

Từ gốc repo, sau khi cài `final/requirements.txt`:

```powershell
.\.venv\Scripts\python.exe final/models/m01_baseline/v1/train.py
.\.venv\Scripts\python.exe final/models/m05_logistic_regression/v1/train.py
```

Trên Codespaces/Linux, thay đường dẫn interpreter bằng `python3` trong môi trường đã kích hoạt. Trên Windows có thể đặt `$env:MPLCONFIGDIR = "$PWD/.venv/matplotlib-cache"` trước khi chạy nếu thư mục cache người dùng không ghi được.

Mỗi lệnh tạo một run mới, dùng nguyên bộ chỉ số nhóm, đánh giá CV 5-fold trên Train và fit lại model trên toàn Train để bàn giao. Script không dự đoán hoặc đánh giá Test. Mỗi fold tạo mới model/Pipeline; không tuning hoặc thêm đặc trưng ở v1. LR giữ C=1, L2 (l1_ratio=0 với sklearn 1.9.1), lbfgs, max_iter=2000, tol=1e-4, class_weight=None.

Hai run v1 được kiểm tra ngày 04/11/2026:

- Dummy: `m01_baseline_v1_20261104T070423_6b66b3d6`, Macro-F1 CV 0,2220; Accuracy CV 0,4993; Recall Dropout CV 0.
- LR: `m05_logistic_regression_v1_20261104T070444_33387318`, Macro-F1 CV 0,6997 ± 0,0099 (ddof=0); Accuracy CV 0,7754; Recall Dropout CV 0,7748.

Kết quả số và dự đoán OOF được đối chiếu với run giữa kỳ `HIEU_BASELINE_LR_20261103T071117_365642Z` trong lịch sử Git; xem `verification.json` của từng run để biết phạm vi kiểm tra. Đây là chạy lại có huấn luyện thực tế trong khung mới, không phải nhập lại kết quả cũ. Chưa có căn cứ kết luận LR tốt nhất nhóm.

Run Dummy đầu `m01_baseline_v1_20261104T070322_e7516df5` được giữ với trạng thái `superseded`: huấn luyện hoàn thành nhưng phần ghi chỉ mục phát cảnh báo pandas; đã thay phần ghi CSV và chạy lại Dummy. Không tính lần kiểm tra lại thành v2.

Tracking hiện lưu cục bộ: `experiments/results.csv` là chỉ mục; mỗi run giữ config, git/source hashes, environment, metrics, fold metrics, OOF, cảnh báo, nhận xét và hình. File `models/m01_baseline/v1/metrics.json` chỉ chỉ dẫn nơi lấy kết quả, không phải metrics của một lần chạy. Model `model_train_only.joblib` bị Git bỏ qua; chạy lại để tạo khi cần bàn giao.

Chưa đồng bộ W&B hoặc Google Sheets vì cấu hình trong checkout chưa có. `tracking.json` ghi rõ `wandb_status=not_configured` và `sheets_synced=false`; không cần tài khoản cloud để tái lập kết quả cục bộ. Không chạy đồng thời hai script cùng ghi `experiments/results.csv` trong một checkout; các thành viên dùng checkout riêng và xử lý ghép chỉ mục khi tích hợp.

Lịch sử Test: notebook RF cũ đã đánh giá trên Test trước khi đổi khung. Hai run Dummy/LR này không dùng Test, nhưng việc tạo lại cấu trúc không biến Test toàn nhóm thành tập chưa từng được xem. Các bước tiếp theo chọn cấu hình bằng Train-CV và ghi đúng giới hạn của đánh giá.

## 11. Báo cáo và tài liệu thực nghiệm

- **Báo cáo tiến độ giữa kỳ (.docx):** [BaoCao_TienDo_GiuaKy_Nhom10.docx](BaoCao_TienDo_GiuaKy_Nhom10.docx)
- **Slide thuyết trình giữa kỳ (.pptx):** [BaoCao_TienDo_GiuaKy_Nhom10.pptx](BaoCao_TienDo_GiuaKy_Nhom10.pptx)
- **Nhật ký thực nghiệm cục bộ (.csv):** [Experiment_Log.csv](Experiment_Log.csv)
- **Nhật ký thực nghiệm trực tuyến (Google Sheets):** [Experiment Log - Student Dropout - Nhóm 10](https://docs.google.com/spreadsheets/d/1TN7sYaRpnH5Ge9akvWWv2rm1OC8tYlIXVco6vyS2sDg/edit?usp=sharing)
- **Thư mục hình ảnh và biểu đồ báo cáo:** [figures/](figures/) (hoặc [reports/figures/](reports/figures/))

Báo cáo thực hiện theo cấu trúc các chương trong đề tài:
1. **Giới thiệu:** Bối cảnh, mục tiêu, bài toán phân loại đa lớp.
2. **Cơ sở lý thuyết:** Các thuật toán và phương pháp được chọn (Baseline, DT, RF, LR, XGBoost).
3. **Dữ liệu và phương pháp:** EDA, preprocessing, pipeline chống rò rỉ và thiết kế 5-fold CV.
4. **Thực nghiệm, kết quả và thảo luận:** So sánh 12 mô hình, phân tích lỗi và thực nghiệm ablation.
5. **Kết luận và hướng phát triển:** Tiến độ đạt được, hạn chế kỹ thuật và kế hoạch cuối kỳ.

## 12. Trạng thái dự án

- [x] Tạo cấu trúc dự án `final/`.
- [x] Đưa cấu trúc lên nhánh `main`.
- [x] Có dữ liệu gốc và source manifest.
- [x] Khôi phục bộ chỉ số Train/Test và CV vào thư mục làm việc.
- [x] Xác nhận bộ split đã được commit và kiểm tra phân phối lớp theo từng fold.
- [x] Hoàn thiện `src/data.py`: loader và nạp split có kiểm chứng.
- [x] Khôi phục preprocessing LR v1 trong `src/features.py`; chưa bổ sung feature engineering.
- [ ] Hoàn thiện `src/features.py`.
- [x] Có `src/evaluate.py` cho Dummy/LR v1: CV, OOF, lỗi theo lớp và kiểm tra leakage.
- [x] Có `src/tracking.py` lưu run/chỉ mục cục bộ; chưa tích hợp cloud.
- [ ] Cấu hình W&B và nhật ký Google Sheets.
- [x] Huấn luyện và đánh giá Dummy baseline, LR v1 trên CV; lưu bằng chứng.
- [ ] Thực nghiệm các thuật toán được phân công.
- [ ] Thực hiện Ablation Study khi phù hợp.
- [ ] Chốt champion và đánh giá Test cuối cùng.
- [ ] Hoàn thiện báo cáo, slide và demo.

## 13. Nguyên tắc cộng tác

- Mọi thay đổi mã nguồn cần có commit rõ ràng.
- Không ghi đè dữ liệu, split hoặc kết quả thí nghiệm đã chốt.
- Không tự ý thay đổi metric chính hoặc bộ chia dữ liệu chung.
- Không tự triển khai các mô hình ngoài phạm vi phân công mà chưa thống nhất.
- Mọi kết quả được báo cáo phải truy vết được đến mã nguồn, cấu hình và dữ liệu đã sử dụng.
- Mọi thành viên chịu trách nhiệm giải thích phương pháp và kết quả của phần mình thực hiện.

---

**Tài liệu chính:** `ML - De tai cuoi ky - Final (1).pdf`

**Nguồn dữ liệu:** UCI Machine Learning Repository, Dataset 697.

**Trạng thái:** Đang xây dựng hệ thống thực nghiệm; chưa công bố kết quả mô hình cuối cùng.
