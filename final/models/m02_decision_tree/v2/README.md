# Decision Tree V2 — Nhóm 10 (Student Dropout)

## Mục tiêu và giới hạn

- Giữ **Decision Tree V1** làm mốc (`max_depth=5`, `min_samples_leaf=10`, `random_state=42`, chưa mã hóa biến phân loại).
- Kiểm tra tác động của **One-Hot Encoding** với 17 cột phân loại, giữ nguyên 19 cột còn lại, sau đó tuning có giới hạn.
- So sánh theo **cùng 5 outer folds** của V1: `StratifiedKFold(5, shuffle=True, random_state=42)` trên Train 3.539 mẫu. V2 tuned dùng **3 inner folds**, 24 cấu hình ngẫu nhiên, để tránh chọn mô hình bằng outer-validation của chính nó.
- **Không dự đoán trên Test**. Test gồm 885 mẫu; không được sử dụng để tuning, đánh giá hay chọn V2.

## Cách chạy trên Kaggle

1. Tạo notebook ở <https://www.kaggle.com/code>, import **`DecisionTree_V2_Kaggle.ipynb`**.
2. Add Input dataset `citrnminhtin/predict-students-dropout-and-academic-success` với tệp `data.csv` có dấu phân cách `;`.
3. Chọn CPU (Accelerator: None) rồi **Run All**. Notebook tự đọc đường dẫn `/kaggle/input/datasets/citrnminhtin/predict-students-dropout-and-academic-success/data.csv` hoặc tự tìm data.csv trong `/kaggle/input/`.
4. Kiểm tra các dòng `Train: 3539`, `Test không sử dụng: 885`, `Outer fold 1/5 ... 5/5`.
5. Mở `/kaggle/working/DecisionTree_V2_Outputs.zip` để tải log/bảng/hình, hoặc xem các hình `01_`–`07_` trong thư mục `DecisionTree_V2_Outputs/`.
6. Nhấn **Save Version → Save & Run All** nếu muốn lưu phiên bản công khai kèm outputs làm minh chứng.

## Các tệp bàn giao

- `DecisionTree_V2_Kaggle.ipynb`: notebook độc lập, có giải thích từng bước.
- `DecisionTree_V2_Source.py`: code tương đương để chạy ngoài Kaggle.
- `DecisionTree_V2_Outputs.zip`: chứa `experiment_log.csv`, `model_comparison_cv_oof.csv`, `fold_metrics_v1_v2.csv`, `class_metrics_oof.csv`, `nested_fold_best_params.csv`, `tuning_cv_results.csv`, `oof_predictions_v1_v2.csv`, các hình 01–07, v.v.
- `DT_V2_Noi_Dung_Cho_Bao_Cao.docx`: nội dung thay thế/bổ sung riêng các mục 2.3, 4.2, 4.5 Decision Tree. Không tự động ghi đè Word chung của nhóm.

## Cách đọc kết quả

1. **CV mean** = trung bình điểm trên 5 outer folds; **OOF Macro-F1** = tính một lần trên toàn bộ dự đoán OOF. Hai cách tổng hợp không đồng nhất.
2. `V1_fixed`: raw numeric; `V2_onehot_fixed`: chỉ thay cách mã hóa; `V2_nested_tuned`: tuning 24 cấu hình trong inner 3fold của từng outer fold.
3. `best_train_only_config.json` chỉ là cấu hình chọn bằng CV trên toàn Train để fit model bàn giao; **điểm tốt nhất từ full-train search không phải kết quả outer CV độc lập**.
4. `feature_importance_outer_cv.csv`: permutation importance trên outer-validation, không phản ánh quan hệ nhân quả.
5. Kết quả V2 đã được đối chiếu bằng mã Python trên dữ liệu gốc; khi chạy trong Kaggle, lưu ảnh output từ phiên Run All của bạn để làm minh chứng cá nhân.

## Giới hạn nghiên cứu

- Dữ liệu có cột kết quả học kỳ 1 và 2: mô hình đầy đủ **không thể được gọi là dự đoán tại thời điểm nhập học**.
- V2 improved Macro-F1 / Enrolled F1 nhưng không đồng nghĩa tăng mọi metric; **Recall Dropout và Accuracy giảm nhẹ**.
- Đánh giá trên cùng dữ liệu một trường, chưa chứng minh tính tổng quát hóa sang trường/năm học khác.
- Các phép tìm kiếm thử hữu hạn, lựa chọn tập tính năng dựa vào domain; không khẳng định tối ưu toàn cục.
- Nếu nhóm cần phép so sánh chung LR / DT / RF, các bên phải thống nhất tập, fold, và metric (không so sánh OOF Train trực tiếp với Test).

Nguồn: UCI Machine Learning Repository, dataset 697 — https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success ; scikit-learn Decision Trees — https://scikit-learn.org/stable/modules/tree.html ; Nested CV — https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html
