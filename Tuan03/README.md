# Kế Hoạch & Hướng Dẫn Thực Hiện Báo Cáo Dự Án: Dự Đoán Giá Nhà (House Prices)
> **Môn học:** Máy Học (Machine Learning) - Lớp: DCT124C1  
> **Dự án:** Dự đoán giá bất động sản dựa trên quy trình chuẩn **CRISP-DM**  
> **Kaggle Competition:** [House Prices - Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)  
> **Paper tham chiếu:** [Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project (Dean De Cock, 2011)](https://jse.amstat.org/v19n3/decock.pdf)  
> **Tệp báo cáo Word mẫu:** Bao_Cao_House_Prices_CRISP_DM_Headings_Only.docx

---

## 👥 Bảng Phân Công Công Việc Trong Nhóm

Nhóm gồm 4 thành viên với phân chia trách nhiệm tương ứng từng chương trong báo cáo:

| STT | Thành viên phụ trách | MSSV | Chương phụ trách (Theo CRISP-DM) | Nhiệm vụ cụ thể phụ trách |
| :-: | :--- | :-: | :--- | :--- |
| **1** | **Dương Gia Phát** | **3124411212** | **CHƯƠNG 1: Business Understanding**<br>**CHƯƠNG 6: Deployment & Maintenance** | - Phân tích bối cảnh bài toán định giá AVM<br>- Nghiên cứu Paper GS. Dean De Cock (2011)<br>- Thiết kế kiến trúc API FastAPI & Web Demo<br>- Kế hoạch giám sát Data Drift & Viết Báo cáo |
| **2** | **Văn Nguyễn Thành Đạt** | **3124411202** | **CHƯƠNG 2: Data Understanding**<br>**CHƯƠNG 3: Data Preparation** | - Thực hiện EDA, vẽ Heatmap Missing Values<br>- Phân tích phân phối giá SalePrice (Skewness)<br>- Lọc Outliers > 4000 sq ft theo Paper De Cock<br>- Xử lý Missing Value (Mean/Mode) & OHE |
| **3** | **Lê Văn Hiếu** | **3124411091** | **CHƯƠNG 4: Modeling**<br>*(Toàn bộ Chương 4)* | - Xây dựng Baseline Decision Tree<br>- Cài đặt mô hình XGBoost Regressor & RandomizedSearchCV<br>- Tuning siêu tham số tối ưu & xuất file nộp Kaggle<br>- Thiết kế & huấn luyện mạng Deep Learning ANN (Keras) |
| **4** | **Cái Trần Minh Tiến** | **3124411234** | **CHƯƠNG 5: Evaluation & Error Analysis** | - Tính toán các thang đo RMSLE, MAE, RMSE, R²<br>- Lập bảng tổng hợp so sánh định lượng các mô hình<br>- Trực quan hóa Predicted vs Actual & Residual Plot<br>- Đánh giá Feature Importance & Phân tích sai số thực tế |

---

## 📋 Chi Tiết Khung Sườn & Checklist Đề Mục

### CHƯƠNG 1: TỔNG QUAN DỰ ÁN VÀ BÀI TOÁN KINH DOANH (BUSINESS UNDERSTANDING)
*Phụ trách: **Dương Gia Phát***

- [ ] **1.1. Bối cảnh thực tiễn của thị trường bất động sản và nhu cầu định giá tự động (AVM)**
  - Thực trạng thẩm định giá truyền thống (tốn kém thời gian, chi phí, mang tính chủ quan).
  - Nhu cầu xây dựng mô hình định giá tự động (Automated Valuation Model - AVM) cho ngân hàng, cơ quan thuế và người mua/bán.
- [ ] **1.2. Nghiên cứu học thuật nền tảng: Bài báo của GS. Dean De Cock (2011)**
  - Giới thiệu bài báo *Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project*.
  - Lý do thay thế bộ dữ liệu Boston Housing (1978) đã lỗi thời về quy mô và giá trị kinh tế.
- [ ] **1.3. Mục tiêu kỹ thuật và thước đo đánh giá sai số (Kaggle RMSLE)**
  - Định nghĩa bài toán Hồi quy có giám sát (Supervised Regression).
  - Công thức và ý nghĩa của thước đo **Root Mean Squared Logarithmic Error (RMSLE)** chuẩn của Kaggle.
- [ ] **1.4. Tác động thực tế và giá trị ứng dụng của mô hình**
  - Khả năng sơ duyệt hồ sơ vay thế chấp tự động trong 50ms, giảm 70% chi phí thẩm định sơ bộ.

---

### CHƯƠNG 2: THẤU HIỂU VÀ KHÁM PHÁ DỮ LIỆU (DATA UNDERSTANDING)
*Phụ trách: **Văn Nguyễn Thành Đạt***

- [ ] **2.1. Nguồn gốc dữ liệu và tổng quan tập dữ liệu Ames Housing**
  - Dữ liệu thu thập từ Văn phòng Thẩm định Giá Thành phố Ames (Iowa, Mỹ) giai đoạn 2006–2010.
  - Cấu trúc tập Kaggle: Tập Train (1.460 dòng, 81 cột) và Tập Test (1.459 dòng, 80 cột).
- [ ] **2.2. Phân loại cấu trúc 79 đặc trưng giải thích**
  - 20 biến liên tục (diện tích các tầng, tầng hầm, ban công, sân...).
  - 14 biến rời rạc (số phòng ngủ, phòng tắm, chỗ đỗ xe gara, năm xây dựng...).
  - 23 biến định danh (khu dân cư Neighborhood, kiểu nhà, vật liệu ngoại thất...).
  - 23 biến thứ bậc (đánh giá chất lượng hoàn thiện từ Poor đến Excellent).
- [ ] **2.3. Khám phá phân phối biến mục tiêu SalePrice (Đặc tính Right-Skewed)**
  - Thống kê mô tả: Min, Max, Mean (180.921$), Median (163.000$).
  - Độ lệch phải (Skewness = 1.88) và cơ sở toán học cần biến đổi logarit $\log(1 + y)$.
- [ ] **2.4. Phân tích tương quan giữa các đặc trưng hàng đầu với giá nhà**
  - Ma trận tương quan Pearson: OverallQual ( = 0.79$), GrLivArea ( = 0.71$), GarageCars ( = 0.64$), TotalBsmtSF ( = 0.61$).

---

### CHƯƠNG 3: TIỀN XỬ LÝ DỮ LIỆU (DATA PREPARATION)
*Phụ trách: **Văn Nguyễn Thành Đạt***

- [ ] **3.1. Nhận diện và xử lý điểm ngoại lai (Outliers) theo khuyến nghị Dean De Cock**
  - Khuyến nghị từ tác giả De Cock: Loại bỏ các bất động sản có diện tích sinh hoạt GrLivArea > 4000 sq ft (các giao dịch bán nội bộ/bán một phần làm lệch mô hình).
- [ ] **3.2. Làm sạch và điền khuyết dữ liệu thiếu (Missing Value Imputation)**
  - Biến phân loại (cat_col): Điền giá trị xuất hiện nhiều nhất (mode) cho 18 cột (FireplaceQu, GarageType, BsmtQual...).
  - Biến số (num_col): Điền giá trị trung bình (mean) cho 11 cột (LotFrontage, GarageYrBlt, MasVnrArea...).
- [ ] **3.3. Loại bỏ các đặc trưng thừa, tỷ lệ rỗng cao (> 70%) và cột định danh Id**
  - Xóa 5 cột: Id, Alley (93.7% null), PoolQC (99.5% null), Fence (80.7% null), MiscFeature (96.3% null).
- [ ] **3.4. Mã hóa biến phân loại bằng One-Hot Encoding và xử lý đồng bộ Train/Test**
  - Nối tạm thời `final_df = pd.concat([train, test])` để đồng bộ các mức danh mục giữa Train và Test.
  - Áp dụng `pd.get_dummies(drop_first=True)` cho 39 cột dạng danh mục để tránh bẫy biến giả.
- [ ] **3.5. Đồng bộ hóa không gian đặc trưng và phân chia tập dữ liệu**
  - Loại bỏ các cột trùng tên -> Không gian dữ liệu chuẩn hóa thành **176 đặc trưng dạng số**.
  - Tách lại df_train (1.460 dòng) và df_test (1.459 dòng).

---

### CHƯƠNG 4: THIẾT KẾ KIẾN TRÚC MÔ HÌNH VÀ THUẬT TOÁN (MODELING)
*Phụ trách: **Lê Văn Hiếu***

- [ ] **4.1. Mô hình cơ sở (Baseline Model): Cây quyết định (Decision Tree)** *(Hiếu phụ trách)*
  - Khởi tạo cây quyết định đơn lẻ để làm mốc tham chiếu so sánh.
- [ ] **4.2. Mô hình thuật toán chủ lực: XGBoost Regressor (Extreme Gradient Boosting)** *(Hiếu phụ trách)*
  - Nguyên lý học tăng cường kết hợp cơ chế điều hòa L1/L2 chống overfitting.
- [ ] **4.3. Chiến lược tinh chỉnh siêu tham số tối ưu (Hyperparameter Tuning)** *(Hiếu phụ trách)*
  - Thiết lập RandomizedSearchCV với 5-Fold Cross Validation qua 50 lượt lặp.
  - Cấu hình tối ưu tìm được: n_estimators=900, max_depth=2, learning_rate=0.1, base_score=0.25, booster='gbtree'.
- [ ] **4.4. Mô hình Deep Learning: Mạng Nơ-ron Nhân tạo (ANN) với Keras** *(Hiếu phụ trách)*
  - Kiến trúc mạng: Input (176 nodes) -> Dense(50, ReLU) -> Dense(25, ReLU) -> Dense(50, ReLU) -> Output(1).
  - Hàm mất mát tùy biến: Root Mean Squared Error (RMSE).
  - Optimizer: Adamax, batch_size=10, epochs=1000, validation_split=0.25.

---

### CHƯƠNG 5: ĐÁNH GIÁ HIỆU SUẤT VÀ PHÂN TÍCH SAI SỐ (EVALUATION & ERROR ANALYSIS)
*Phụ trách: **Cái Trần Minh Tiến***

- [ ] **5.1. Các chỉ số đo lường hiệu năng hồi quy (RMSLE, RMSE, MAE, R²)**
  - Định nghĩa và công thức tính toán 4 chỉ số hồi quy.
- [ ] **5.2. Bảng so sánh kết quả định lượng giữa các mô hình**
  - Lập bảng đối chiếu giữa Decision Tree, ANN Keras và XGBoost Regressor trên tập kiểm định và Kaggle Score.
  - Nhận xét hiệu năng: XGBoost đạt kết quả tối ưu nhất với ^2 \approx 91.8\%$ và RMSLE $\approx 0.1265$.
- [ ] **5.3. Trực quan hóa kết quả: Predicted vs Actual và Phân phối phần dư**
  - Đồ thị phân tán Predicted vs Actual (bám sát đường phân giác  = x$).
  - Biểu đồ phần dư Residual Plot (kiểm tra phân phối sai số ngẫu nhiên quanh trục 0).
- [ ] **5.4. Đánh giá độ quan trọng của đặc trưng (Feature Importance)**
  - Top các biến có trọng số lớn nhất: OverallQual (32%), GrLivArea (21%), TotalBsmtSF (11%).
- [ ] **5.5. Phân tích sai số (Error Analysis) và các trường hợp dự đoán kém**
  - Hiện tượng sai số ở phân khúc nhà siêu sang (> 450.000$) và các giao dịch bán phát mãi (SaleCondition = Abnormal).
- [ ] **5.6. Giới hạn thực tế của mô hình**
  - Ràng buộc địa lý (thành phố Ames, bang Iowa) và thời gian (2006–2010), thiếu biến vĩ mô (lãi suất, lạm phát).

---

### CHƯƠNG 6: KẾ HOẠCH TRIỂN KHAI VÀ BẢO TRÌ (DEPLOYMENT & MAINTENANCE)
*Phụ trách: **Dương Gia Phát***

- [ ] **6.1. Đóng gói sản phẩm dự án (Pipeline, File mô hình, File nộp Kaggle)**
  - Đóng gói file trọng số: xgb_model.pkl, ann_model.h5.
  - Xuất file kết quả nộp Kaggle: sample_sub_xgb.csv, sample_sub_nn.csv.
- [ ] **6.2. Kiến trúc tích hợp phần mềm thực tế (RESTful API & Web Demo)**
  - Thiết kế RESTful API bằng FastAPI: Endpoint /api/v1/predict_price.
  - Xây dựng giao diện thử nghiệm Web UI bằng Streamlit cho phép người dùng kéo chọn diện tích, số phòng để nhận định giá.
- [ ] **6.3. Kế hoạch giám sát độ lệch dữ liệu (Data Drift) & Bảo trì định kỳ**
  - Thiết lập cơ chế giám sát Data Drift và Concept Drift theo từng quý.
  - Chiến lược Retrain định kỳ khi có giao dịch mua bán nhà mới từ phòng công chứng.
  - Quy trình Human-in-the-loop duyệt thủ công đối với bất động sản có giá trị > 500.000 USD.

---

### KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN & TÀI LIỆU THAM KHẢO
*Cả nhóm cùng phối hợp hoàn thiện*
- Tổng kết thành quả đạt được theo 6 bước CRISP-DM.
- Định hướng nâng cao: Kỹ thuật Stacking/Ensembling (XGBoost + LightGBM + CatBoost) và bổ sung dữ liệu tọa độ địa không gian.
- Danh mục tài liệu tham khảo: Paper GS. Dean De Cock (2011), Kaggle Ames Housing, Chen & Guestrin (XGBoost, 2016).

---

## 💻 Hướng Dẫn Chạy Mã Nguồn house_prices_model.py

### 1. Cài đặt môi trường
```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost keras tensorflow
```

### 2. Tải dữ liệu từ Kaggle
Tải các file sau từ cuộc thi [House Prices Kaggle](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data) và đặt vào cùng thư mục:
* train.csv
* test.csv
* sample_submission.csv

### 3. Thực thi mã nguồn
```bash
python house_prices_model.py
```
