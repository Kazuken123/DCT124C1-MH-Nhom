# Logistic Regression v1 — cấu hình cố định

Người thực hiện: Lê Văn Hiếu — 3124411091.

Kế thừa cấu hình đã kiểm chứng trong khung giữa kỳ; thay cách tổ chức code và lưu run, không đổi mô hình/đặc trưng để tạo cải thiện giả. L2 (l1_ratio=0 với sklearn 1.9.1), C=1, lbfgs, max_iter=2000, tol=1e-4, class_weight=None. Encoding/scaling được fit mới trong Pipeline của mỗi fold.

V1 không tuning, không thêm đặc trưng hoặc điều chỉnh ngưỡng. Các hướng v2 có thể là C, class_weight hoặc biểu diễn đặc trưng; mỗi thí nghiệm đổi có mục đích, ghi tác giả, giả thuyết và bản kế thừa. Chọn theo Train-CV, không lựa chọn bằng Test.

Kết quả thật theo run nằm trong `experiments/runs/<run_id>/` và chỉ mục `experiments/results.csv`, model_id=m05_logistic_regression. Không bắt buộc v2 tốt hơn v1. Ablation A/B/C bằng LR cố định vẫn cần tách thành các thí nghiệm có feature set rõ ràng.
