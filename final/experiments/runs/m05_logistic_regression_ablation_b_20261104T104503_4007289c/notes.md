# m05_logistic_regression ablation_b

Người thực hiện: Duong Gia Phat - 3124411212. Run: m05_logistic_regression_ablation_b_20261104T104503_4007289c.

Giả thuyết/mục tiêu: Ablation B: Evaluate fixed Logistic Regression without 2nd semester features (30 features) on shared 5 folds to measure performance impact of 2nd semester information.

CV 5-fold trên 3.539 dòng Train, cùng bộ chỉ số nhóm. Macro-F1: 0.6578 ± 0.0149 (ddof=0); Accuracy: 0.7462; Recall Dropout: 0.7528. Train Macro-F1: 0.7189; gap Train–Validation: 0.0612.

Macro-F1 OOF: 0.6583; tính riêng với CV mean. Xem class_metrics_oof.csv và confusion_matrix.csv để phân tích lớp khó và lỗi nhầm. Không tuning hoặc chọn đặc trưng trong run này. Model cuối được fit trên toàn Train để bàn giao, không dự đoán Test.

Run này không sử dụng Test để đánh giá. Test từng được notebook RF cũ sử dụng; đổi khung dự án không đặt lại lịch sử đó. Không kết luận mô hình tốt nhất nhóm hoặc hiệu quả dự đoán ngay lúc nhập học vì dữ liệu có HK2.

Các số được ghi từ lần chạy mới, không nhập lại kết quả lịch sử. Code tại lúc chạy còn đang chờ review; git_info.json lưu base commit và hash nguồn. Tracking cục bộ đã có; chưa đồng bộ W&B/Sheets vì chưa cấu hình trong checkout. Artifact model_train_only.joblib chỉ lưu cục bộ, bị Git bỏ qua.

Hướng tiếp theo: đối chiếu baseline trên cùng fold, phân tích lỗi từng lớp, sau đó thử một thay đổi có giả thuyết trong v2. Giữ v1 làm mốc; bản sau không bắt buộc tốt hơn.
