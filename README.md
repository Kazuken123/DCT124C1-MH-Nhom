# DCT1204C1 - Máy Học (Nhóm Thực Hành)

## Thông tin chung
- **Lớp**: DCT1204C1
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
└── Tuan03/                             # Dự án: Dự đoán Giá nhà (House Prices) theo chuẩn CRISP-DM
    ├── README.md                       # Kế hoạch chi tiết, hướng dẫn 6 phần CRISP-DM & phân công công việc
    └── house_prices_model.py           # Toàn bộ mã nguồn: Tiền xử lý, XGBoost, Decision Tree & ANN Keras
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

### Tóm tắt các giai đoạn triển khai (CRISP-DM):
1. **Business Understanding (Tổng quan dự án):** Xây dựng Mô hình Định giá Tự động (AVM) dự đoán giá bán bất động sản tại Ames, Iowa; giải quyết hạn chế của bộ dữ liệu Boston Housing cũ.
2. **Data Understanding (Thấu hiểu dữ liệu):** Khảo sát 79 đặc trưng và phân tích tương quan giữa các yếu tố với giá bán SalePrice.
3. **Data Preparation (Tiền xử lý):** Loại bỏ ngoại lai (> 4.000 sq ft) theo Paper De Cock, xử lý khuyết (Mode cho phân loại, Mean cho số), mã hóa One-Hot biến danh mục thành 176 đặc trưng.
4. **Modeling (Xây dựng mô hình):** Huấn luyện XGBoost Regressor (tối ưu qua RandomizedSearchCV), Baseline Decision Tree, và Mạng Nơ-ron Nhân tạo ANN (Keras).
5. **Evaluation (Đánh giá hiệu suất):** Đo lường chuẩn Kaggle RMSLE, MAE, ^2$, trực quan hóa Predicted vs Actual và biểu đồ phân phối phần dư (Residuals).
6. **Deployment (Triển khai & Bảo trì):** Đóng gói Pipeline dự đoán, xuất file submission nộp Kaggle, thiết kế RESTful API (FastAPI) và kế hoạch giám sát trôi dạt dữ liệu (Data Drift).

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
