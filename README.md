# DCT124C1 - Máy Học (Nhóm Thực Hành)

## Thông tin chung
- **Lớp**: DCT124C1
- **Thành viên nhóm**:
  - Văn Nguyễn Thành Đạt
  - Lê Văn Hiếu
  - Dương Gia Phát
  - Cái Trần Minh Tiến

---

## Cấu trúc thư mục kho lưu trữ (Repository Structure)

```
DCT1204C1-MH-Nhom/
│
├── README.md                           # Giới thiệu tổng quan và tài liệu hướng dẫn repo
│
├── Tuan02/                             # Nội dung bài tập & thực hành Tuần 02
│   ├── datav.ipynb                     # Jupyter Notebook: Nạp dữ liệu, tiền xử lý và trực quan hóa (EDA)
│   └── Bao_Cao_Phan_Tich_Du_Lieu_Iris.pdf # Báo cáo chi tiết định dạng PDF (gồm bìa chuẩn SGU, mục lục & insights)
│
├── Tuan03/                             # Dự án: Dự đoán Giá nhà (House Prices) theo chuẩn CRISP-DM
│   ├── README.md                       # Kế hoạch chi tiết, hướng dẫn 6 phần CRISP-DM & phân công công việc
│   └── house_prices_model.py           # Toàn bộ mã nguồn: Tiền xử lý, XGBoost, Decision Tree & ANN Keras
│
├── Tuan04/                             # Khám phá và Trực quan hóa dữ liệu (EDA) - House Prices
│   ├── EDA_House_Prices.ipynb          # Jupyter Notebook: EDA chi tiết 7 phần trên tập dữ liệu Ames Housing
│   └── Bao_Cao_Thuyet_Trinh_EDA_House_Prices.pptx # Slide báo cáo thuyết trình EDA
│
├── Tuan05/                             # Lựa chọn đặc trưng & Đánh giá mô hình (Feature Selection & Evaluation)
│   ├── House_Prices_Feature_Selection_Evaluation.ipynb # Jupyter Notebook: Lựa chọn đặc trưng và đánh giá mô hình
│   └── Feature Selection_MH.docx       # Báo cáo chi tiết Lab 04 - Feature Selection
│
└── Lab05_ThucHanhBaiToanPhanLop/       # Thực hành Bài toán Phân lớp (Classification)
    ├── data/                           # Dữ liệu thực nghiệm (Credit Card, Titanic, Diabetes, Spam, ...)
    ├── figures/                        # Toàn bộ biểu đồ phân tích xuất từ mô hình độ phân giải cao
    ├── code/                           # Mã nguồn Jupyter Notebook thực thi hoàn chỉnh 100% outputs
    │   ├── lab2_1_DecisionTree_RandomForest.ipynb # Master notebook Mục 2.1 (Lý thuyết, 2.1.2, 2.1.3, 2.1.4)
    │   ├── 01_CreditCard_DT_RF.ipynb   # Notebook 2.1.2: Vỡ nợ thẻ tín dụng (Credit Card)
    │   ├── 02_Titanic_DT_RF.ipynb      # Notebook 2.1.3: Dự đoán sống sót Titanic
    │   ├── 03_Diabetes_DT_RF.ipynb     # Notebook 2.1.4: Dự đoán tiểu đường Pima Indians
    │   ├── 01-iris-svm.ipynb           # Notebook 2.2: SVM trên Iris (Kernel & Hyperparameters)
    │   ├── 02-digits-svm.ipynb         # Notebook 2.2: SVM trên tập Digits
    │   ├── 03-diabetes-svm.ipynb       # Notebook 2.2: SVM trên tập Diabetes
    │   ├── 04-animal-svm.ipynb         # Notebook 2.2: SVM trên tập Animal Condition
    │   └── lab2_3_NaiveBayes (2).ipynb # Notebook 2.3: Naive Bayes (Spam, Customer, Mushrooms)
    ├── Lab_2_1_1_On_tap_ly_thuyet_Decision_Tree_Random_Forest.docx # Trả lời 9 câu hỏi lý thuyết Mục 2.1.1
    └── Bao_Cao_Tong_Hop_Lab05_Phan_Lop.docx # Báo cáo tổng hợp toàn diện Lab 05 (Bìa SGU, bảng kết quả & charts)
```

---

## Nội dung Tuần 02: Khám phá, Trực quan hóa dữ liệu và Rút trích Insights (EDA)

Tuần 02 tập trung vào kỹ thuật **Phân tích Khám phá Dữ liệu (Exploratory Data Analysis - EDA)** trên tập dữ liệu kinh điển **Iris Flower Dataset** (Sir Ronald Fisher, 1936).

### 1. Mục tiêu bài toán
- Nạp và tiền xử lý tập dữ liệu hình thái học hoa Iris gồm 150 mẫu, 4 đặc trưng liên tục (`sepal-length`, `sepal-width`, `petal-length`, `petal-width`) và nhãn phân loại 3 loài (`Iris-setosa`, `Iris-versicolor`, `Iris-virginica`).
- Phân tích thống kê mô tả (Descriptive Statistics) và kiểm tra tính toàn vẹn dữ liệu (Missing values, Class balance).
- Trực quan hóa phân phối đơn biến bằng **Boxplot** và **Histogram**.
- Khảo sát tương quan đa biến thông qua **Scatter Matrix** và ma trận hệ số tương quan Pearson.
- Đánh giá khả năng phân tách loài bằng biểu đồ đa chiều **Pairplot** theo nhãn lớp và phân tích không gian 2D trên đặc trưng Cánh hoa (Petal).
- Tổng hợp Insights và đề xuất định hướng xây dựng mô hình Học máy (Machine Learning).

### 2. Các kết quả & Insights cốt lõi
1. **Lực phân tách vượt trội của Cánh hoa (Petal Dominance)**:
   - Thuộc tính cánh hoa (`petal-length` và `petal-width`) có khoảng biến thiên lớn, độ phân tán cao và chứa lượng thông tin phân biệt (discriminative power) lớn nhất.
   - Cặp `petal-length` và `petal-width` có tương quan tuyến tính cực mạnh với hệ số Pearson $r = +0.963$.
2. **Khả năng phân tách tuyến tính tuyệt đối của loài Iris-setosa**:
   - Loài Iris-setosa hoàn toàn tách biệt độc lập (linearly separable) với 2 loài còn lại trên mọi biểu đồ chiếu có sự tham gia của chiều Petal (cánh hoa Setosa rất nhỏ: dài $< 2.0$ cm, rộng $< 0.8$ cm).
3. **Vùng giao thoa giữa Versicolor và Virginica**:
   - Hai loài này có sự chồng lấn nhẹ (boundary overlap) ở kích thước cánh hoa trung bình - lớn (Petal Length khoảng 4.5 - 5.1 cm và Petal Width khoảng 1.5 - 1.8 cm). Các mô hình phân loại Soft-margin SVM (Linear/RBF) hoặc KNN ($k = 3, 5$) cho hiệu năng phân tách tối ưu.
4. **Phân phối dữ liệu và điểm ngoại lai (Outliers)**:
   - `sepal-width` là thuộc tính duy nhất xuất hiện các điểm ngoại lai ($< 2.05$ cm và $> 4.05$ cm), chủ yếu do hình thái lá đài to bè của Setosa.
   - `petal-length` và `petal-width` có dạng phân phối 2 đỉnh (Bimodal), phản ánh rõ nét sự phân hóa thành hai cụm hình thái riêng biệt trong tự nhiên.
5. **Đề xuất mô hình Machine Learning**:
   - **Phân loại có giám sát**: Logistic / Softmax Regression, Support Vector Machine (SVM), K-Nearest Neighbors (KNN), Decision Tree / Random Forest.
   - **Học không giám sát & Giảm chiều**: K-Means Clustering ($k = 3$), PCA (2 thành phần chính giữ $> 95\%$ phương sai dữ liệu).

---

---

## Nội dung Tuần 03: Dự án Dự đoán Giá nhà (House Prices Regression) theo quy trình CRISP-DM

Dự án tham gia cuộc thi Kaggle [House Prices: Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques) và nghiên cứu Paper của GS. Dean De Cock (2011) về bộ dữ liệu Ames Housing.

### Các tài nguyên chính:
- **Tài liệu hướng dẫn & Phân công nhiệm vụ chi tiết:** Xem tại [Tuan03/README.md](Tuan03/README.md)
- **Mã nguồn thực thi:** [Tuan03/house_prices_model.py](Tuan03/house_prices_model.py)

### Tóm tắt 6 Chương Báo cáo theo chuẩn CRISP-DM (Khớp 100% tệp Báo cáo Word):
1. **CHƯƠNG 1: Business Understanding** *(Dương Gia Phát phụ trách)*: Bối cảnh định giá tự động (AVM), nghiên cứu Paper GS. Dean De Cock (2011), mục tiêu bài toán và thước đo Kaggle RMSLE.
2. **CHƯƠNG 2: Data Understanding** *(Văn Nguyễn Thành Đạt phụ trách)*: Khảo sát quy mô tập Ames Housing, phân loại 79 đặc trưng, phân tích phân phối lệch phải của SalePrice và ma trận tương quan.
3. **CHƯƠNG 3: Data Preparation** *(Văn Nguyễn Thành Đạt phụ trách)*: Loại bỏ ngoại lai > 4000 sq ft, xử lý Missing Values (Mean/Mode), loại bỏ 5 cột thừa/rỗng > 70% và mã hóa One-Hot đồng bộ thành 176 đặc trưng.
4. **CHƯƠNG 4: Modeling** *(Lê Văn Hiếu phụ trách)*: Toàn bộ quá trình mô hình hóa — Huấn luyện Baseline Decision Tree, XGBoost Regressor (tinh chỉnh qua RandomizedSearchCV 5-Fold) và mạng nơ-ron Deep Learning ANN (Keras).
5. **CHƯƠNG 5: Evaluation & Error Analysis** *(Cái Trần Minh Tiến phụ trách)*: Đánh giá bằng RMSLE, MAE, RMSE, R²; vẽ đồ thị Predicted vs Actual & Residual Plot; phân tích các trường hợp sai số lớn và giới hạn thực tế.
6. **CHƯƠNG 6: Deployment & Maintenance** *(Dương Gia Phát phụ trách)*: Đóng gói Pipeline & tệp mô hình, xuất kết quả nộp Kaggle, kiến trúc RESTful API (FastAPI) / Web Demo (Streamlit) và kế hoạch giám sát Data Drift.

## Hướng dẫn cài đặt và thực thi

### Yêu cầu môi trường
- Python 3.8+
- Các thư viện cần thiết:
  ```bash
  pip install numpy pandas matplotlib seaborn jupyter
  ```

### Mở và chạy Notebook
Khởi chạy Jupyter Notebook hoặc JupyterLab từ thư mục gốc:
```bash
jupyter notebook Tuan02/datav.ipynb
```
Hoặc mở trực tiếp trên [Google Colaboratory](https://colab.research.google.com/).

### Xem tệp Báo cáo PDF
Tệp báo cáo hoàn chỉnh được định dạng chuẩn học thuật Đại học Sài Gòn, sẵn sàng in ấn hoặc đọc trên các trình đọc PDF:
`Tuan02/Bao_Cao_Phan_Tich_Du_Lieu_Iris.pdf`

---

## Nội dung Lab 05: Thực hành Bài toán Phân lớp (Classification)

Thực hành chuyên sâu các giải thuật phân lớp kinh điển và học kết hợp (Ensemble Learning) trên đa dạng bộ dữ liệu thực tế (Credit Card Default, Titanic, Pima Diabetes, Handwritten Digits, Animal Condition, SMS Spam, Mushrooms).

### 1. Phân công nhiệm vụ nhóm trong Lab 05:
| STT | Thành viên phụ trách | MSSV | Vai trò | Nội dung phụ trách cụ thể |
| :-: | :--- | :-: | :--- | :--- |
| **1** | **Dương Gia Phát** | **3124411212** | **Nhóm trưởng** | - Phụ trách **Mục 2.1: Cây quyết định & Rừng ngẫu nhiên (Decision Tree & Random Forest)**<br>- Trả lời 9 câu hỏi lý thuyết 2.1.1 (CRISP-DM, Gini/Entropy/IG, RF, Tuning)<br>- Bài làm mẫu 2.1.2: Vỡ nợ thẻ tín dụng (Credit Card Default) 3 nhiệm vụ<br>- Bài tập thực hành 2.1.3: Sống sót Titanic & 2.1.4: Tiểu đường Pima Indians<br>- Phân tích chuyên sâu hiện tượng Quá khớp (Overfitting)<br>- Tổng hợp toàn diện Báo cáo Word chuẩn Đại học Sài Gòn |
| **2** | **Văn Nguyễn Thành Đạt** | **3124411067** | **Thành viên** | - Phụ trách **Mục 2.2: Support Vector Machine (SVM)**<br>- Lý thuyết SVM (Hyperplane, Margin, Kernel, Tham số C)<br>- Thực nghiệm phân loại hoa Iris (Khảo sát các kernel Linear, Poly, RBF, Sigmoid)<br>- Thực nghiệm Digits (Chữ số 8x8), Diabetes và Animal Condition |
| **3** | **Lê Văn Hiếu** | **3124411091** | **Thành viên** | - Phụ trách **Mục 2.3: Bayes ngây thơ (Naive Bayes)**<br>- Lý thuyết Naive Bayes (Định lý Bayes, giả định độc lập, Gaussian/Multinomial/Bernoulli)<br>- Bài làm mẫu: Phân loại Email Spam với CountVectorizer & MultinomialNB<br>- Bài tập thực hành 1: Customer Behaviour & Bài tập 2: Nấm Mushroom |
| **4** | **Cái Trần Minh Tiến** | **3124411309** | **Thành viên** | - Phụ trách **Phần 1: Khám phá và Trực quan hóa dữ liệu (EDA)**<br>- Phân tích đơn biến và hai biến trên các tập dữ liệu Penguins, Amsterdam Housing, Marketing Campaign<br>- Hỗ trợ kiểm thử ma trận nhầm lẫn và đối soát số liệu thực nghiệm |

### 2. Các tài nguyên chính trong Lab 05:
- **Tài liệu Báo cáo Word hoàn chỉnh:** [Lab05_ThucHanhBaiToanPhanLop/Bao_Cao_Tong_Hop_Lab05_Phan_Lop.docx](Lab05_ThucHanhBaiToanPhanLop/Bao_Cao_Tong_Hop_Lab05_Phan_Lop.docx)
- **Tài liệu Lý thuyết 2.1.1:** [Lab05_ThucHanhBaiToanPhanLop/Lab_2_1_1_On_tap_ly_thuyet_Decision_Tree_Random_Forest.docx](Lab05_ThucHanhBaiToanPhanLop/Lab_2_1_1_On_tap_ly_thuyet_Decision_Tree_Random_Forest.docx)
- **Master Notebook Mục 2.1:** [Lab05_ThucHanhBaiToanPhanLop/code/lab2_1_DecisionTree_RandomForest.ipynb](Lab05_ThucHanhBaiToanPhanLop/code/lab2_1_DecisionTree_RandomForest.ipynb)
- **Toàn bộ biểu đồ xuất từ mô hình:** Thư mục [Lab05_ThucHanhBaiToanPhanLop/figures/](Lab05_ThucHanhBaiToanPhanLop/figures/)

