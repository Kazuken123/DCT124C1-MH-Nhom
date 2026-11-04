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
| `experiments/runs/` | Kết quả chi tiết từng lần chạy |
| `experiments/results.csv` | Bảng tổng hợp các thí nghiệm |
| `experiments/ablation.csv` | Kết quả nghiên cứu loại bỏ thành phần |
| `reports/` | Biểu đồ, bảng kết quả, báo cáo |
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
| `m10_ensemble` | Ensemble | Dự kiến, chỉ triển khai khi có cơ sở |

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

Lệnh đọc và kiểm chứng dữ liệu dự kiến:

`python3 final/src/data.py`

Các lệnh huấn luyện, đánh giá và đồng bộ W&B/Sheets sẽ được bổ sung sau khi mã nguồn tương ứng được triển khai và kiểm thử. Hiện README không cam kết các lệnh đó đã chạy được.

## 11. Báo cáo cuối kỳ

Báo cáo thực hiện theo cấu trúc 5 chương trong đề bài:

1. **Giới thiệu:** Bối cảnh, mục tiêu, bài toán.
2. **Cơ sở lý thuyết:** Các thuật toán và phương pháp được chọn.
3. **Dữ liệu và phương pháp:** EDA, preprocessing, pipeline và thiết kế thực nghiệm.
4. **Thực nghiệm, kết quả và thảo luận:** So sánh mô hình, phân tích lỗi và kết quả.
5. **Kết luận và hướng phát triển:** Champion, hạn chế và cải tiến.

Sản phẩm hoàn thiện gồm báo cáo, slide, mã nguồn, README và demo theo yêu cầu giảng viên.

## 12. Trạng thái dự án

- [x] Tạo cấu trúc dự án `final/`.
- [x] Đưa cấu trúc lên nhánh `main`.
- [x] Có dữ liệu gốc và source manifest.
- [x] Khôi phục bộ chỉ số Train/Test và CV vào thư mục làm việc.
- [ ] Xác nhận bộ split đã được commit và kiểm tra phân phối lớp theo từng fold.
- [ ] Hoàn thiện `src/data.py`.
- [ ] Hoàn thiện `src/features.py`.
- [ ] Hoàn thiện `src/evaluate.py`.
- [ ] Hoàn thiện `src/tracking.py`.
- [ ] Cấu hình W&B và nhật ký Google Sheets.
- [ ] Huấn luyện và đánh giá Dummy baseline.
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
