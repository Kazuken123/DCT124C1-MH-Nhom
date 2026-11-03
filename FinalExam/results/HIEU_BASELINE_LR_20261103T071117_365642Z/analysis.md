# Phân tích Dummy và Logistic Regression — Lê Văn Hiếu

Run: HIEU_BASELINE_LR_20261103T071117_365642Z. Dữ liệu Train có 3539 sinh viên; Test 885 sinh viên được giữ riêng, chưa đánh giá.

## 1. Câu hỏi và thiết kế

Thực nghiệm kiểm tra LR cố định có cải thiện so với Dummy đoán lớp phổ biến nhất trên cùng 5 fold không, đồng thời tìm lớp còn khó và đánh giá gap train–validation. Không tuning hoặc chọn đặc trưng; không lựa chọn cấu hình theo Test. Tham số được ghi trước khi chạy, C=1, điều chuẩn L2, solver lbfgs, max_iter=2000, tol=1e-4, class_weight=None. Mức max_iter là giới hạn tối ưu để hội tụ, không phải số lượt chọn mô hình.

80/20 stratify, seed 42 và StratifiedKFold(5, shuffle=True, random_state=42) theo xác nhận của người dùng về leader Phát. Các file indices được tái tạo tại máy từ công thức đã xác nhận, cùng công thức notebook Đạt; chưa được so byte với bộ indices ngoài repo vì không có bộ đó trong checkout. Manifest lưu thứ tự dòng và hash để nhóm đối chiếu.

## 2. Kết quả CV (trung bình và độ lệch chuẩn 5 fold; ddof=0)

Dummy: Macro-F1 0.2220 ± 0.0002; Accuracy 0.4993 ± 0.0006; Recall Dropout 0.0000.

LR: Macro-F1 0.6997 ± 0.0099; Accuracy 0.7754 ± 0.0052; Recall Dropout 0.7748 ± 0.0218.

Chênh lệch Macro-F1 LR − Dummy: 0.4777 (thang 0–1). Dummy luôn dự đoán Graduate vì đây là lớp phổ biến nhất trong các phần train. Accuracy gần một nửa vẫn đi kèm Recall Dropout/Enrolled bằng 0; do đó không thể đánh giá chỉ bằng Accuracy. LR sử dụng thông tin đầu vào và cải thiện khả năng phân biệt lớp so với mốc này; chưa có căn cứ nói LR tốt nhất nhóm hoặc hiệu quả triển khai thực tế.

## 3. Phân tích dự đoán OOF trên Train

Mỗi sinh viên Train có đúng một dự đoán từ mô hình không học chính sinh viên đó ở fold tương ứng. Chỉ số từ toàn bộ dự đoán OOF được ghi riêng trong oof_summary.csv; không coi đó là kết quả Test và không thay thế CV mean bằng OOF F1.

Dropout: Precision 0.7980; Recall 0.7748; F1 0.7863; hỗ trợ 1137 mẫu.

Enrolled: Precision 0.5742; Recall 0.3780; F1 0.4558; hỗ trợ 635 mẫu.

Graduate: Precision 0.8047; Recall 0.9185; F1 0.8578; hỗ trợ 1767 mẫu.

Dropout: đúng 881/1137, bỏ sót 256, gồm 102 bị đoán Enrolled và 154 bị đoán Graduate. Ngược lại, 223 sinh viên thuộc hai lớp còn lại bị đoán Dropout. Cần cân nhắc cả bỏ sót và cảnh báo nhầm khi thảo luận mục tiêu hỗ trợ sinh viên.

Enrolled: đúng 240/635, nhầm sang Dropout 155 và Graduate 240. Lớp có F1 thấp nhất trong OOF LR là Enrolled; có thể liên hệ với mất cân bằng và chồng lấn thông tin, nhưng thí nghiệm hiện tại chưa cô lập nguyên nhân.

## 4. Overfitting, độ ổn định và giới hạn

LR Train Macro-F1 trung bình 0.7557; Validation 0.6997; gap trung bình 0.0559. Đây là chênh lệch trên cùng 5 fold, không phải chênh lệch Train–Test. Gap và độ lệch chuẩn là bằng chứng mô tả trong bộ chia này; gap nhỏ không chứng minh không overfitting, và chưa đủ để chẩn đoán underfitting hay bảo đảm ổn định trên cohort/cơ sở giáo dục khác.

Chỉ khảo sát một split, một cấu hình LR và tiền xử lý ban đầu. Chưa tuning C, thử trọng số lớp hoặc thực hiện ablation; các hướng này chưa được tính là kết quả đã hoàn thành. Bộ đặc trưng gốc có HK2 nên không diễn giải thành dự đoán ngay lúc nhập học. Không kết luận quan hệ nhân quả từ kết quả dự đoán.

## 5. Bằng chứng và bàn giao

fold_metrics.csv ghi từng fold; cv_summary.csv ghi mean/std; oof_predictions.csv, class_metrics_oof.csv và confusion_lr.csv truy vết lỗi; leakage_checks.csv kiểm tra trung bình scaler và số mẫu chỉ từ train từng fold; warnings.json ghi cảnh báo. lr_train_only.joblib là pipeline fit trên toàn bộ Train sau CV, chưa dùng để đánh giá Test. Chỉ nạp file joblib từ nguồn tin cậy.

Phát sử dụng make_lr() cùng cấu hình để fit lại pipeline mới cho mỗi fold trong đối chứng A/B/C; không dùng bộ scaler/encoder đã fit toàn Train để đánh giá fold. Giữ các biến đổi của cột gốc và tham số LR cố định; việc xử lý đặc trưng mới thuộc phần đối chứng của Phát.

## 6. Việc còn lại

Đối chiếu hash các file split/fold với bộ nhóm đang lưu, đồng bộ phương pháp đánh giá khi so LR với DT/RF, kiểm tra chéo, xác nhận người thực hiện hiểu và diễn giải được kết quả; chỉ đánh giá Test khi nhóm chốt bước đánh giá đó. Chưa push hoặc xác nhận nhóm đã nhận sản phẩm.
