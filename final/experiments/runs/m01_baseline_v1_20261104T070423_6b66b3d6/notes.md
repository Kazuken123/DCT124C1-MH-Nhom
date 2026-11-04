# m01_baseline v1

Người thực hiện: Le Van Hieu - 3124411091. Run: m01_baseline_v1_20261104T070423_6b66b3d6.

Giả thuyết/mục tiêu: Establish the majority-class reference on the shared five folds.

CV 5-fold trên 3.539 dòng Train, cùng bộ chỉ số nhóm. Macro-F1: 0.2220 ± 0.0002 (ddof=0); Accuracy: 0.4993; Recall Dropout: 0.0000. Train Macro-F1: 0.2220; gap Train–Validation: 0.0000.

Macro-F1 OOF: 0.2220; tính riêng với CV mean. Xem class_metrics_oof.csv và confusion_matrix.csv để phân tích lớp khó và lỗi nhầm. Không tuning hoặc chọn đặc trưng trong run này. Model cuối được fit trên toàn Train để bàn giao, không dự đoán Test.

Run này không sử dụng Test để đánh giá. Test từng được notebook RF cũ sử dụng; đổi khung dự án không đặt lại lịch sử đó. Không kết luận mô hình tốt nhất nhóm hoặc hiệu quả dự đoán ngay lúc nhập học vì dữ liệu có HK2.

Các số được ghi từ lần chạy mới, không nhập lại kết quả lịch sử. Code tại lúc chạy còn đang chờ review; git_info.json lưu base commit và hash nguồn. Tracking cục bộ đã có; chưa đồng bộ W&B/Sheets vì chưa cấu hình trong checkout. Artifact model_train_only.joblib chỉ lưu cục bộ, bị Git bỏ qua.

Hướng tiếp theo: đối chiếu baseline trên cùng fold, phân tích lỗi từng lớp, sau đó thử một thay đổi có giả thuyết trong v2. Giữ v1 làm mốc; bản sau không bắt buộc tốt hơn.
