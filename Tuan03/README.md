# Kế Hoạch & Hướng Dẫn Thực Hiện Báo Cáo Dự Án: Dự Đoán Giá Nhà (House Prices)
> **Môn học:** Máy Học (Machine Learning) - Lớp DCT1204C1  
> **Dự án:** Dự đoán giá bất động sản dựa trên quy trình chuẩn **CRISP-DM**  
> **Kaggle Competition:** [House Prices - Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)  
> **Paper tham chiếu:** [Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project (Dean De Cock, 2011)](https://jse.amstat.org/v19n3/decock.pdf)  

---

## 👥 Danh sách Thành viên & Gợi ý Phân công Công việc

Nhóm gồm 4 thành viên:
1. **Dương Gia Phát**
2. **Văn Nguyễn Thành Đạt**
3. **Lê Văn Hiếu**
4. **Cái Trần Minh Tiến**

### Bảng phân chia trách nhiệm dự kiến:

| Thành viên phụ trách | Nhiệm vụ chính (Theo CRISP-DM) | Sản phẩm đầu ra cần nộp |
| :--- | :--- | :--- |
| **Dương Gia Phát** | **Bước 1: Business Understanding** (Tổng quan & Bài toán định giá nhà)<br>**Bước 6: Deployment & Maintenance** (Kế hoạch API, Web Demo, Giám sát Drift) | - Soạn thảo Phần 1 & Phần 6 của Báo cáo.<br>- Thiết kế kịch bản sử dụng thực tế (Use-case AVM cho ngân hàng/người mua). |
| **Thành Đạt** | **Bước 2: Data Understanding** (Nguồn gốc, EDA, Heatmap, Tương quan)<br>**Bước 3: Data Preparation** (Lọc Outliers theo Paper De Cock, Xử lý Null, One-Hot Encoding) | - Soạn thảo Phần 2 của Báo cáo.<br>- Chạy code EDA, xuất các biểu đồ trực quan (Heatmap missing, phân phối `SalePrice`). |
| **Thành viên 3** | **Bước 4: Modeling (Phần 1 - Tree-based Models)**<br>- Xây dựng Decision Tree (Baseline)<br>- Cấu hình & Tuning siêu tham số XGBoost Regressor bằng `RandomizedSearchCV` | - Soạn thảo Phần 3 (Mục XGBoost & Decision Tree).<br>- Lưu checkpoint `xgb_model.pkl` và xuất file nộp `sample_sub_xgb.csv`. |
| **Thành viên 4** | **Bước 4: Modeling (Phần 2 - Deep Learning ANN)**<br>**Bước 5: Evaluation & Error Analysis**<br>- Huấn luyện mạng ANN Keras đa tầng<br>- Đo lường RMSLE, MAE, $R^2$, vẽ biểu đồ Predicted vs Actual & Residuals<br>- Phân tích sai số và giới hạn mô hình | - Soạn thảo Phần 4 & Phần 5 của Báo cáo.<br>- Lưu model `nn_model.h5`, xuất biểu đồ huấn luyện Loss/Val_Loss và Residual Plot. |

---

## 📋 Chi Tiết Các Bước Cần Thực Hiện Cho Từng Phần Báo Cáo

### PHẦN 1: TỔNG QUAN DỰ ÁN (EXECUTIVE SUMMARY)
*Tương ứng CRISP-DM: Bước 1 - Business Understanding (Thấu hiểu bài toán)*

- [ ] **1.1. Lý do xây dựng mô hình AI:**
  - Nêu thực trạng: Định giá bất động sản truyền thống phụ thuộc chuyên viên định giá, tốn thời gian, chi phí cao và có độ trễ lớn.
  - Mục tiêu: Xây dựng Mô hình Định giá Tự động (**Automated Valuation Model - AVM**) dựa trên Machine Learning để đưa ra mức giá khách quan, tức thì.
- [ ] **1.2. Bối cảnh nghiên cứu (Paper Dean De Cock 2011):**
  - Giới thiệu bộ dữ liệu **Ames Housing Dataset** được công bố bởi GS. Dean De Cock (Truman State University) nhằm thay thế bộ dữ liệu *Boston Housing (1978)* đã quá lỗi thời về mặt thời gian và quy mô.
  - Mục tiêu bài toán: Dự đoán giá bán nhà ở (`SalePrice`) tại thành phố Ames, Iowa dựa trên 79 biến giải thích.
- [ ] **1.3. Mục tiêu kỹ thuật:**
  - Bài toán Hồi quy có giám sát (Supervised Regression).
  - Tối ưu hóa thước đo sai số logarit chuẩn của Kaggle: **RMSLE** (Root Mean Squared Logarithmic Error).
- [ ] **1.4. Tóm tắt kết quả & Tác động thực tế:**
  - Tóm tắt ngắn gọn các mô hình thử nghiệm: Decision Tree (Cơ sở), Deep Learning (ANN), và Gradient Boosting (XGBoost).
  - Kết quả: XGBoost Regressor cho độ chính xác cao nhất và ổn định nhất.
  - Ứng dụng thực tế: Hỗ trợ cơ quan thuế (Ames Assessor's Office) áp thuế công bằng, giúp các ngân hàng thẩm định tài sản thế chấp và hỗ trợ người dân tham khảo giá trước khi giao dịch.

---

### PHẦN 2: DỮ LIỆU HUẤN LUYỆN (DATA SPECIFICATION)
*Tương ứng CRISP-DM: Bước 2 & 3 - Data Understanding & Data Preparation*

- [ ] **2.1. Nguồn gốc & Cấu trúc dữ liệu:**
  - **Nguồn gốc:** Dữ liệu thực tế từ Văn phòng Thẩm định Giá Thành phố Ames, bang Iowa (Mỹ), thu thập các giao dịch trong giai đoạn 2006–2010.
  - **Kích thước:**
    - Tập Train: 1.460 dòng, 81 cột (gồm `Id`, 79 đặc trưng và biến mục tiêu `SalePrice`).
    - Tập Test: 1.459 dòng, 80 cột (chỉ có `Id` và 79 đặc trưng).
  - **Phân loại 79 đặc trưng:**
    - 20 biến liên tục: Diện tích sàn sinh hoạt (`GrLivArea`), diện tích tầng hầm (`TotalBsmtSF`), diện tích lô đất (`LotArea`)...
    - 14 biến rời rạc: Số phòng ngủ, số phòng tắm, sức chứa gara (`GarageCars`), năm xây dựng (`YearBuilt`)...
    - 23 biến định danh (Nominal): Khu dân cư (`Neighborhood`), kiểu nhà (`BldgType`), vật liệu ngoại thất...
    - 23 biến thứ bậc (Ordinal): Đánh giá chất lượng tổng thể (`OverallQual`), chất lượng hoàn thiện hầm/bếp/ngoại thất...
- [ ] **2.2. Phân tích khám phá dữ liệu (EDA):**
  - Vẽ biểu đồ phân phối giá nhà (`SalePrice`): Nhận xét hiện tượng lệch phải (*Right-skewed*), đa số tập trung ở mức 100.000$ - 250.000$.
  - Tìm ra các yếu tố có tương quan cao nhất với giá bán: `OverallQual` ($r \approx 0.79$), `GrLivArea` ($r \approx 0.71$), `GarageCars`, `TotalBsmtSF`.
- [ ] **2.3. Xử lý điểm ngoại lai (Outliers) theo Paper:**
  - Dẫn chứng Paper De Cock: Đề xuất loại bỏ 5 căn nhà có diện tích sinh hoạt > 4.000 sq ft (trong đó có 3 điểm bán nội bộ/bán một phần với giá rẻ bất thường làm sai lệch mô hình).
- [ ] **2.4. Làm sạch dữ liệu khuyết (Missing Values):**
  - Loại bỏ các cột thiếu > 70%: `Alley`, `PoolQC`, `Fence`, `MiscFeature` và cột định danh `Id`.
  - Biến phân loại (`cat_col`): Điền giá trị xuất hiện nhiều nhất (`mode`) cho `FireplaceQu`, `GarageType`, `BsmtQual`...
  - Biến số (`ncat_col`): Điền giá trị trung bình (`mean`) cho `LotFrontage`, `GarageYrBlt`, `MasVnrArea`...
- [ ] **2.5. Mã hóa đặc trưng (Feature Encoding):**
  - Ghép nối Train và Test (`final_df = pd.concat([train, test])`) để đồng bộ danh mục.
  - Áp dụng **One-Hot Encoding** (`pd.get_dummies(drop_first=True)`) cho 39 cột dạng text.
  - Sau khi mã hóa, không gian đặc trưng mở rộng thành **176 đặc trưng dạng số**.
- [ ] **2.6. Phân chia tập huấn luyện & kiểm thử:**
  - Tách lại `df_train` (1.460 dòng, 176 biến) và `df_test` (1.459 dòng).
  - Tách biến độc lập `x_train` và nhãn `y_train` (`SalePrice`).

---

### PHẦN 3: KIẾN TRÚC MÔ HÌNH & THUẬT TOÁN (MODEL ARCHITECTURE & ALGORITHMS)
*Tương ứng CRISP-DM: Bước 4 - Modeling (Xây dựng mô hình)*

- [ ] **3.1. Mô hình 1: XGBoost Regressor (Thuật toán chủ lực):**
  - **Lý do chọn:** Thuật toán Gradient Boosting dựa trên cây quyết định tối ưu hàng đầu cho dữ liệu dạng bảng, tự động nắm bắt tương tác phi tuyến và có cơ chế điều hòa L1/L2 chống quá khớp (Overfitting).
  - **Dò siêu tham số với `RandomizedSearchCV`:** 
    - Thực hiện 5-Fold Cross-Validation qua 50 lượt thử (`n_iter=50`).
    - Tìm kiếm các siêu tham số: `n_estimators`, `max_depth`, `learning_rate`, `min_child_weight`, `booster`, `base_score`.
  - **Bộ thông số tối ưu:**
    - `booster = 'gbtree'`
    - `n_estimators = 900`
    - `max_depth = 2` (cây nông hạn chế học vẹt)
    - `learning_rate = 0.1`
    - `min_child_weight = 1`
    - `objective = 'reg:squarederror'`
- [ ] **3.2. Mô hình 2: Baseline Decision Tree:**
  - **Lý do chọn:** Đóng vai trò mô hình cây quyết định cơ bản để so sánh mốc tham chiếu.
- [ ] **3.3. Mô hình 3: Mạng Nơ-ron Nhân tạo (ANN với Keras):**
  - **Lý do chọn:** Khảo sát năng lực học biểu diễn phi tuyến tính của Deep Learning trên dữ liệu dạng bảng.
  - **Kiến trúc mạng (Topology):**
    - Input: 176 neuron.
    - Hidden Layer 1: Dense 50, activation `ReLU`, `he_uniform`.
    - Hidden Layer 2: Dense 25, activation `ReLU`, `he_uniform`.
    - Hidden Layer 3: Dense 50, activation `ReLU`, `he_uniform`.
    - Output: Dense 1 (giá nhà dự đoán).
  - **Cấu hình huấn luyện:**
    - Loss tùy biến: `Root Mean Squared Error (RMSE)`.
    - Optimizer: `Adamax`.
    - Siêu tham số: `batch_size = 10`, `epochs = 1000`, `validation_split = 0.25`.

---

### PHẦN 4: ĐÁNH GIÁ HIỆU SUẤT (EVALUATION & METRICS)
*Tương ứng CRISP-DM: Bước 5 - Evaluation (Đánh giá)*

- [ ] **4.1. Tiêu chí đo lường định lượng (Metrics):**
  - **RMSLE (Root Mean Squared Logarithmic Error):** Chỉ số chính thức của Kaggle, đánh giá sai số theo tỷ lệ phần trăm thay vì số tiền tuyệt đối, đảm bảo tính công bằng giữa nhà giá rẻ và nhà giá cao.
  - **MAE (Mean Absolute Error):** Đo độ lệch giá trung bình bằng tiền USD thực tế.
  - **RMSE (Root Mean Squared Error):** Đo lường mức độ phạt sai số lớn.
  - **$R^2$ Score:** Đo lường tỷ lệ phần trăm phương sai giá nhà được giải thích bởi mô hình.
- [ ] **4.2. Bảng so sánh hiệu năng các mô hình:**
  - Lập bảng so sánh giữa XGBoost, Decision Tree và ANN trên tập Train, Validation và điểm nộp Kaggle (Public Score).
  - Nhận xét: XGBoost vượt trội nhờ khả năng tối ưu trên dữ liệu dạng bảng có kích thước vừa phải (~1460 dòng).
- [ ] **4.3. Đồ thị trực quan hóa kết quả:**
  - **Biểu đồ Predicted vs Actual:** So sánh giá thực tế vs giá dự đoán (các điểm càng bám sát đường $y=x$ càng tốt).
  - **Biểu đồ Residual Plot (Phần dư):** Đảm bảo phần dư phân bố đối xứng quanh mốc 0, không có hình nan quạt (heteroscedasticity).
  - **Biểu đồ Feature Importance:** Top 10 đặc trưng ảnh hưởng lớn nhất đến giá nhà của XGBoost (`OverallQual`, `GrLivArea`, `TotalBsmtSF`...).

---

### PHẦN 5: PHÂN TÍCH SAI SỐ & GIỚI HẠN (ERROR ANALYSIS & LIMITATIONS)

- [ ] **5.1. Phân tích các trường hợp sai số lớn:**
  - Căn nhà có giá trị siêu cao (> 400.000$): Mô hình có xu hướng dự đoán thấp hơn giá thật (*underestimate*) do thiếu mẫu nhà siêu sang.
  - Căn nhà có điều kiện bán bất thường (`SaleCondition = 'Abnormal'`): Bị ngân hàng phát mãi, thanh lý dưới giá thị trường làm mô hình dự đoán cao hơn giá bán thực tế.
  - Ngoại lai diện tích lớn (> 4.000 sq ft): Biến động giá bất thường như cảnh báo của paper De Cock.
- [ ] **5.2. Giới hạn của mô hình:**
  - **Phạm vi địa lý & Thời gian:** Dữ liệu chỉ áp dụng tại thành phố Ames (Iowa, Mỹ) giai đoạn 2006–2010. Không thể dùng định giá cho thị trường khác hoặc thời điểm hiện tại khi trượt giá/lạm phát đã thay đổi.
  - **Thiếu biến số kinh tế vĩ mô:** Chưa có dữ liệu về lãi suất vay ngân hàng, lạm phát, việc làm theo từng năm.
  - **Hạn chế của phương pháp điền khuyết Mean/Mode đơn giản:** Cần nâng cấp lên KNN Imputer hoặc điền theo nhóm khu phố (`Neighborhood`).

---

### PHẦN 6: TRIỂN KHAI & BẢO TRÌ (DEPLOYMENT & MAINTENANCE)
*Tương ứng CRISP-DM: Bước 6 - Deployment (Triển khai)*

- [ ] **6.1. Đóng gói sản phẩm (Exporting Artifacts):**
  - Lưu file mô hình nhị phân: `xgb_model.pkl`, `nn_model.h5`.
  - Xuất file nộp kết quả cuộc thi Kaggle: `sample_sub_xgb.csv`, `sample_sub_nn.csv`.
  - Xây dựng một End-to-End Pipeline hoàn chỉnh để tự động làm sạch và mã hóa dữ liệu khi có căn nhà mới được đưa vào.
- [ ] **6.2. Phương thức tích hợp vào hệ thống thực tế:**
  - **RESTful API (FastAPI):** Endpoint `/predict_price` nhận thông tin căn nhà dạng JSON và phản hồi giá ước tính trong 50ms.
  - **Giao diện Web Demo (Streamlit / Gradio):** Cho phép chuyên viên hoặc người dùng kéo chọn diện tích, số phòng, khu dân cư để xem khoảng giá gợi ý.
- [ ] **6.3. Kế hoạch giám sát & Bảo trì lâu dài:**
  - **Theo dõi Data Drift & Concept Drift:** Giám sát xem xu hướng thị trường bất động sản có thay đổi không (ví dụ: vật liệu mới xuất hiện, giá đất tăng vọt).
  - **Retrain định kỳ:** Định kỳ cập nhật lại trọng số mô hình khi có thêm giao dịch nhà đất mới được công chứng.
  - **Quy trình kết hợp con người (Human-in-the-loop):** Với các căn nhà dị biệt hoặc giá trị trên 500.000$, giá của AI chỉ là mức tham chiếu ban đầu, cần có chuyên viên thẩm định duyệt lần cuối.

---

## 💻 Hướng Dẫn Chạy Mã Nguồn `house_prices_model.py`

### 1. Cài đặt môi trường
Đảm bảo đã cài đặt các thư viện cần thiết:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost keras tensorflow
```

### 2. Tải dữ liệu thi Kaggle
Tải các file sau từ cuộc thi [House Prices Kaggle](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data) và đặt cùng thư mục với script:
* `train.csv`
* `test.csv`
* `sample_submission.csv`

### 3. Thực thi script
Chạy toàn bộ quy trình từ tải dữ liệu, tiền xử lý, huấn luyện đến xuất kết quả:
```bash
python house_prices_model.py
```
Sau khi chạy xong, các tệp sau sẽ được tự động tạo ra:
* `xgb_model.pkl`: Mô hình XGBoost đã tinh chỉnh siêu tham số.
* `nn_model.h5`: Trọng số mô hình mạng Nơ-ron nhân tạo Keras.
* `sample_sub_xgb.csv`: File dự đoán của XGBoost sẵn sàng nộp lên Kaggle.
* `sample_sub_nn.csv`: File dự đoán của mạng ANN.
