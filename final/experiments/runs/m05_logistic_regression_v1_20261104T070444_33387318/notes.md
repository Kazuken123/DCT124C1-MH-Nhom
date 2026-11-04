# m05_logistic_regression v1

Người thực hiện: Le Van Hieu - 3124411091. Run: m05_logistic_regression_v1_20261104T070444_33387318.

Giả thuyết/mục tiêu: Compare fixed L2 Logistic Regression with majority Dummy; examine per-class errors and train-validation gap.

CV 5-fold trên 3.539 dòng Train, cùng bộ chỉ số nhóm. Macro-F1: 0.6997 ± 0.0099 (ddof=0); Accuracy: 0.7754; Recall Dropout: 0.7748. Train Macro-F1: 0.7557; gap Train–Validation: 0.0559.

Macro-F1 OOF: 0.7000; tính riêng với CV mean. Xem class_metrics_oof.csv và confusion_matrix.csv để phân tích lớp khó và lỗi nhầm. Không tuning hoặc chọn đặc trưng trong run này. Model cuối được fit trên toàn Train để bàn giao, không dự đoán Test.

Run này không sử dụng Test để đánh giá. Test từng được notebook RF cũ sử dụng; đổi khung dự án không đặt lại lịch sử đó. Không kết luận mô hình tốt nhất nhóm hoặc hiệu quả dự đoán ngay lúc nhập học vì dữ liệu có HK2.

Các số được ghi từ lần chạy mới, không nhập lại kết quả lịch sử. Code tại lúc chạy còn đang chờ review; git_info.json lưu base commit và hash nguồn. Tracking cục bộ đã có; chưa đồng bộ W&B/Sheets vì chưa cấu hình trong checkout. Artifact model_train_only.joblib chỉ lưu cục bộ, bị Git bỏ qua.

Hướng tiếp theo: đối chiếu baseline trên cùng fold, phân tích lỗi từng lớp, sau đó thử một thay đổi có giả thuyết trong v2. Giữ v1 làm mốc; bản sau không bắt buộc tốt hơn.

## Nhận xét riêng của LR so với Dummy

Macro-F1 CV tăng từ 0,2220 lên 0,6997; Accuracy CV tăng khoảng 27,61 điểm phần trăm. Dummy không phát hiện Dropout hoặc Enrolled; LR phân biệt được cả ba nhãn.

Trong dự đoán OOF trên Train, LR nhận đúng 881/1.137 Dropout, bỏ sót 256 (102 đoán Enrolled, 154 đoán Graduate). Có 223 cảnh báo Dropout nhầm từ hai lớp còn lại. Enrolled là lớp khó nhất: Precision 0,5742, Recall 0,3780, F1 0,4558; 155 mẫu bị đoán Dropout và 240 mẫu bị đoán Graduate. Graduate có F1 0,8578. Đây là số từ OOF gộp, không phải trung bình các fold và không phải Test.

Train Macro-F1 trung bình khoảng 0,7557, Validation khoảng 0,6997, gap khoảng 0,0559. Gap và biến động giữa năm fold mô tả bộ chia hiện có; chưa chứng minh khả năng tổng quát sang trường/năm học khác. Chưa cô lập nguyên nhân khiến Enrolled khó phân biệt.

V2 có thể thử một yếu tố như C hoặc class_weight, giữ nguyên fold và các phần còn lại. Cần theo dõi đánh đổi giữa Recall Dropout, F1 Enrolled và Macro-F1; không mặc định bản sau tốt hơn và không dùng Test để chọn.
