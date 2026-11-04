# Logistic Regression — Ablation B (No 2nd Semester Features)

Người thực hiện: Dương Gia Phát — 3124411212.

## Mục tiêu
Đánh giá tác động của nhóm thông tin học kỳ 2 đối với bài toán dự đoán tình trạng học tập của sinh viên.
Cấu hình B loại bỏ toàn bộ 6 đặc trưng của học kỳ 2:
- `Curricular units 2nd sem (credited)`
- `Curricular units 2nd sem (enrolled)`
- `Curricular units 2nd sem (evaluations)`
- `Curricular units 2nd sem (approved)`
- `Curricular units 2nd sem (grade)`
- `Curricular units 2nd sem (without evaluations)`

Tổng số đặc trưng đầu vào giảm từ 36 xuống còn 30.

## Cố định thực nghiệm
- Mô hình: Logistic Regression cố định từ v1 (C=1.0, L2 penalty, solver=lbfgs, max_iter=2000, tol=1e-4, random_state=42, class_weight=None).
- Dữ liệu: Cùng tập Train (3.539 mẫu) và 5 fold phân tầng seed 42 cố định (`student_dropout_seed42_v1`).
- Tiền xử lý: StandardScaler cho 12 biến số liên tục, OneHotEncoder cho 10 biến phân loại, passthrough cho 8 biến nhị phân. Fit độc lập trong Pipeline của từng fold.
- Không đánh giá trên tập Test.
