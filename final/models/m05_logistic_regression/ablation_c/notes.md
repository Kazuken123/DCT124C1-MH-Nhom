# Logistic Regression — Ablation C (With Engineered Features)

Người thực hiện: Dương Gia Phát — 3124411212.

## Mục tiêu
Đánh giá giá trị bổ sung của kỹ thuật xây dựng đặc trưng mới (Feature Engineering).
Cấu hình C bổ sung 3 đặc trưng tỷ lệ và xu hướng vào bộ 36 đặc trưng gốc, nâng tổng số đặc trưng lên 39:
1. `Curricular units 1st sem (approved ratio)`: Tỷ lệ môn đã qua trên số môn đăng ký ở HK1 (`approved / enrolled`, gán 0.0 nếu `enrolled == 0`).
2. `Curricular units 2nd sem (approved ratio)`: Tỷ lệ môn đã qua trên số môn đăng ký ở HK2 (`approved / enrolled`, gán 0.0 nếu `enrolled == 0`).
3. `Curricular units grade difference (2nd - 1st)`: Chênh lệch điểm học kỳ 2 trừ học kỳ 1 (`grade_sem2 - grade_sem1`).

## Cố định thực nghiệm
- Mô hình: Logistic Regression cố định từ v1 (C=1.0, L2 penalty, solver=lbfgs, max_iter=2000, tol=1e-4, random_state=42, class_weight=None).
- Dữ liệu: Cùng tập Train (3.539 mẫu) và 5 fold phân tầng seed 42 cố định (`student_dropout_seed42_v1`).
- Tiền xử lý: Bước tạo đặc trưng được đóng gói trực tiếp trong scikit-learn Pipeline trước bước ColumnTransformer. Toàn bộ 21 biến số liên tục (18 gốc + 3 mới) được chuẩn hóa bằng StandardScaler fit độc lập trong từng fold.
- Không đánh giá trên tập Test.
