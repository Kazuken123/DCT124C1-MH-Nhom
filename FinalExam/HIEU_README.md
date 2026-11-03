# Phần giữa kỳ của Lê Văn Hiếu

Phạm vi: kiểm tra dữ liệu, thiết kế preprocessing, Dummy baseline và Logistic Regression (LR), phân tích lỗi và bàn giao cấu hình LR. Không bao gồm mô hình của các thành viên khác hoặc ứng dụng demo.

## Mở file nào?

- `Hieu_DataUnderstanding.ipynb`: notebook kiểm tra dữ liệu và khởi tạo preprocessing; không huấn luyện mô hình.
- `src/hieu_data_preprocessing.py`: hàm đọc dữ liệu và tạo preprocessing chưa fit.
- `src/hieu_baseline_lr.py`: thực nghiệm Dummy/LR bằng Python script; không có notebook Dummy/LR riêng.
- `configs/hieu_preprocessing_v1.json`: 18 cột StandardScaler, 10 cột One-Hot, 8 cột giữ nguyên.
- `configs/hieu_baseline_lr_v1.json`: cấu hình cố định của thực nghiệm.
- `configs/splits/student_dropout_seed42_v1/`: thứ tự dòng Train/Test và fold đã lưu.

## Dữ liệu và cấu hình chung

CSV nguồn nằm tại `data/raw/data.csv`, phân cách bằng dấu `;`, mã hóa UTF-8 có BOM. Hàm đọc kiểm tra SHA-256 theo manifest, chỉ loại khoảng trắng ở hai đầu tên cột, không thay đổi thứ tự dòng hoặc ghi đè nguồn.

Người dùng đã báo Phát xác nhận 80/20 stratify, seed 42 và CV 5-fold. Các file chỉ số trong checkout được tái tạo theo công thức `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` và phép chia trong notebook Đạt. Manifest ghi rõ nguồn gốc này; chưa có bằng chứng đối chiếu với một bộ indices bên ngoài checkout. Khi bàn giao, nhóm cần dùng đúng cùng các file hoặc đối chiếu thứ tự dòng/fold, không chỉ cùng seed.

Trạng thái `pending_group_confirmation_no_indices_created` trong cấu hình preprocessing v1 ghi nhận thời điểm thiết kế ban đầu, không phải trạng thái điều phối mới nhất. Giữ bản v1 để đối chiếu với hash ghi trong lần chạy cũ; trạng thái của thực nghiệm được ghi riêng trong cấu hình Dummy/LR và run manifest.

## Chuẩn bị môi trường

Các lệnh dưới đây chạy từ thư mục `FinalExam`, với Python 3.12 được cài trên máy. Nếu máy chưa có lệnh `python`, cần chọn đúng Python đã cài trước. Không sử dụng môi trường đang được tạo dở.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-hieu.txt
```

Trong VS Code, mở notebook và chọn kernel của `.venv`. Việc cài đặt từ danh sách phiên bản này chưa được xác minh lại trong môi trường sạch của lượt dọn repo; danh sách dựa trên `environment.json` của lần chạy có sẵn.

## Chạy Dummy/LR

```powershell
.\.venv\Scripts\python.exe -m src.hieu_baseline_lr
```

Lệnh này thực sự huấn luyện mô hình và sinh một run mới. Chỉ chạy khi đã sẵn sàng kiểm chứng; không cần chạy lại để xem kết quả cũ. Chạy từ `FinalExam` để import module đúng.

Mỗi fold tạo pipeline LR mới; scaler/encoder và mô hình chỉ fit trên phần train của fold. Dummy dùng `most_frequent`. Script lưu chỉ số train/validation, dự đoán OOF và fit một LR trên toàn bộ Train để bàn giao; không đánh giá Test, không tuning hoặc tạo đặc trưng mới.

## Kết quả và trạng thái kiểm chứng

Run có sẵn: `HIEU_BASELINE_LR_20261103T063912_624622Z` trong `results/` và log tương ứng trong `logs/`.

- Đã rà code và kiểm tra tính nhất quán của dự đoán đã lưu với Accuracy/Macro-F1 từng fold, mean/std và nhãn nguồn.
- Chưa tái chạy mô hình để xác minh khả năng tái lập trong chat chính; chưa coi đây là phần người học đã hoàn tất hoặc kết quả đã bàn giao cho nhóm.
- `run.json` ghi `status=complete` là trạng thái được lưu bởi lần chạy trước, không thay thế xác nhận tái lập hiện tại. Các hash trong đó mô tả phiên bản code khi chạy; thay đổi hướng dẫn sau đó không sửa lịch sử này.
- Chưa đánh giá Test. Không so CV mean, OOF và Test như cùng một loại kết quả.

Những file cần dùng:

- `fold_metrics.csv`, `cv_summary.csv`: kết quả từng fold và mean/std.
- `oof_predictions.csv`, `class_metrics_oof.csv`, `oof_summary.csv`, `confusion_*.csv/png`: kiểm tra lỗi và hình báo cáo.
- `run.json`, `environment.json`, `warnings.json`, `leakage_checks.csv`: truy vết cấu hình, môi trường và kiểm tra.
- `analysis.md`, `lr_handoff.json`: nhận xét từ run và thông tin bàn giao.
- `logs/<run_id>.csv`: log của Dummy/LR.

`lr_train_only.joblib` được sinh khi chạy và giữ cục bộ, không đưa vào Git. Model đã huấn luyện chỉ là tài nguyên tùy chọn; Phát cần tạo pipeline mới từ cấu hình để đánh giá từng fold trong A/B/C, không dùng lại preprocessing đã fit toàn Train.

Giữ các kết quả theo run để truy vết; không xóa bằng chứng chỉ để giảm số file. `.venv`, cache, ZIP nguồn và model sinh ra không thuộc gói commit.

## Bàn giao còn lại

1. Kiểm chứng lần chạy Dummy/LR và người thực hiện hiểu được từng bước.
2. Hoàn thiện 3.7, 4.1, phần LR ở 4.5/4.7 và Chương 5/6 từ kết quả được xác minh.
3. Bàn giao cấu hình LR, preprocessing, split/fold và log cho Phát/Tiến.
4. Kiểm tra chéo, hoàn thiện tài liệu; push GitHub chỉ sau khi người dùng yêu cầu.
