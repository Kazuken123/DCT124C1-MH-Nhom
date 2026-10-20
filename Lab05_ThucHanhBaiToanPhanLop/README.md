# BÁO CÁO THỰC HÀNH LAB 05: PHÂN TÍCH KHÁM PHÁ DỮ LIỆU & BÀI TOÁN PHÂN LỚP
**Môn học:** Máy học (Machine Learning) - Lớp: DCT124C1  
**Khoa:** Công nghệ Thông tin - Trường Đại học Sài Gòn (SGU)  
**Giảng viên hướng dẫn:** TS. Đỗ Như Tài  

---

## 1. THÔNG TIN NHÓM THỰC HÀNH & PHÂN CÔNG NHIỆM VỤ

| STT | Họ và tên | MSSV | Vai trò | Nhiệm vụ thực hiện cụ thể |
| :-: | :--- | :-: | :--- | :--- |
| **1** | **Lê Văn Hiếu** | **3124411091** | **Nhóm trưởng** | - Phụ trách **Mục 2.1: Cây quyết định & Rừng ngẫu nhiên (Decision Tree & Random Forest)**<br>- Trả lời 9 câu hỏi ôn tập lý thuyết 2.1.1 (CRISP-DM/SEMMA, Gini/Entropy/IG, Rừng ngẫu nhiên, Hyperparameter Tuning)<br>- Bài làm mẫu 2.1.2: Vỡ nợ thẻ tín dụng (Credit Card Default) 3 nhiệm vụ<br>- Bài tập thực hành 2.1.3: Sống sót Titanic & 2.1.4: Tiểu đường Pima Indians<br>- Phân tích chuyên sâu hiện tượng Quá khớp (Overfitting)<br>- **Tổng hợp toàn diện Cuốn Báo cáo Word chuẩn Đại học Sài Gòn** |
| **2** | **Văn Nguyễn Thành Đạt** | **3124411067** | **Thành viên** | - Phụ trách **Mục 2.2: Support Vector Machine (SVM)**<br>- Trả lời lý thuyết SVM (Siêu phẳng, Margin, Kernel Trick, Tham số C, Chuẩn hóa)<br>- Thực nghiệm phân loại hoa Iris (Khảo sát các kernel Linear, Poly, RBF, Sigmoid)<br>- Thực nghiệm Digits (Chữ số 8x8), Diabetes (100 nghìn mẫu) và Animal Condition |
| **3** | **Dương Gia Phát** | **3124411212** | **Thành viên** | - Phụ trách **Mục 2.3: Bayes ngây thơ (Naive Bayes)**<br>- Trả lời lý thuyết Naive Bayes (Định lý Bayes, Giả định độc lập, Gaussian/Multinomial/Bernoulli, NLP Pipeline)<br>- Bài làm mẫu: Phân loại Email Spam với CountVectorizer & MultinomialNB<br>- Bài tập thực hành 1: Customer Behaviour & Bài tập 2: Nấm Mushroom |
| **4** | **Cái Trần Minh Tiến** | **3124411309** | **Thành viên** | - Phụ trách **Phần 1: Khám phá và Trực quan hóa dữ liệu (EDA)**<br>- Phân tích đơn biến và hai biến trên các tập dữ liệu Penguins, Amsterdam Housing, Marketing Campaign<br>- Khảo sát các công cụ phân tích tự động: ydata-profiling, SweetViz, AutoViz<br>- Hỗ trợ kiểm thử ma trận nhầm lẫn và đối soát số liệu thực nghiệm |

---

## 2. NỘI DUNG 2 LAB THỰC HÀNH

### LAB 1: KHÁM PHÁ VÀ TRỰC QUAN HÓA DỮ LIỆU (EDA)
- **Tập dữ liệu chim cánh cụt Palmer Penguins:** Khảo sát phân bố hình thái học (chiều dài mỏ, độ sâu mỏ, chiều dài cánh, khối lượng), phân bố loài và tương quan giữa các đặc trưng.
- **Tập dữ liệu giá nhà ở Housing Amsterdam:** Phân tích đơn biến giá nhà, phát hiện phân phối lệch phải (skewness 3.86), xác định các khoảng giá trị bất thường qua Boxplot và Violin Plot.
- **Tập dữ liệu chiến dịch tiếp thị Marketing Campaign:** Tiền xử lý giá trị khuyết thiếu ở biến thu nhập, trực quan hóa hành vi chi tiêu theo nhóm khách hàng.
- **Công cụ EDA tự động:** Báo cáo tương tác với ydata-profiling, SweetViz và AutoViz.
- **Các notebook chuyên đề EDA mở rộng:** COVID Descriptive Statistics, Red Wine Quality, Pima Diabetes EDA, Online Retail Transaction Analysis.

### LAB 2: THỰC HÀNH CÁC GIẢI THUẬT PHÂN LỚP
- **Mục 2.1: Decision Tree & Random Forest:**
  - 9 câu hỏi lý thuyết chuyên sâu (CRISP-DM, Gini vs Entropy, Information Gain, Random Forest Ensemble, Overfitting Control).
  - Vỡ nợ thẻ tín dụng Credit Card: Mô hình mẫu, khảo sát max_depth qua GridSearchCV với errorbar Mean +- 1 SE, tinh chỉnh n_estimators cho Random Forest và trích xuất Feature Importance.
  - Sống sót tàu Titanic: So sánh đối đầu Baseline và Tuned models, trực quan hóa cây quyết định tối ưu và ma trận nhầm lẫn.
  - Tiểu đường Pima Indians: Xử lý giá trị 0 sinh lý bất thường, đối phó quá khớp (Train Acc 100% -> Test Acc 68.18% được cải thiện lên 78.57% và F1-score 0.6916 sau khi tuning).
  - Bảng tổng hợp đối sánh trực diện 8 mô hình và nhận xét toàn diện về hiện tượng quá khớp.
- **Mục 2.2: Support Vector Machine (SVM):**
  - 7 câu hỏi lý thuyết (Siêu phẳng, Support Vectors, Hard vs Soft margin, Kernel trick, Tham số C, StandardScaler).
  - Phân loại hoa Iris: Đối sánh thực nghiệm 4 kernel (Linear, Poly, RBF, Sigmoid).
  - Nhận dạng chữ số viết tay Digits: RBF kernel, C=10 đạt 98.06% Test Accuracy.
  - Dự đoán tiểu đường Diabetes & Phân loại tình trạng động vật Animal Condition: Đạt hiệu năng phân lớp xuất sắc.
- **Mục 2.3: Bayes ngây thơ (Naive Bayes):**
  - 7 câu hỏi lý thuyết (Định lý Bayes, Giả định ngây thơ, 3 biến thể phân phối, Quy trình túi từ Bag-of-Words).
  - Phân loại tin nhắn rác SMS Spam: Pipeline CountVectorizer + MultinomialNB đạt 98.26% Accuracy, F1-score 0.9291.
  - Dự đoán mua hàng Customer Behaviour: GaussianNB đạt 87.50% Accuracy.
  - Phân loại nấm Mushroom: OneHotEncoder + MultinomialNB đạt 94.58% Accuracy, Precision 99.01% trên nấm độc.

---

## 3. CẤU TRÚC THƯ MỤC NỘP BÀI

```
Lab05_ModelTraining_LeVanHieu_3124411091/
├── Bao_Cao_Tong_Hop_Lab05_Phan_Lop.docx      # CUỐN BÁO CÁO TỔNG HỢP TOÀN BỘ LAB 05 (Bìa SGU, bảng số liệu & 19 charts)
├── Bao_cao_EDA_phan_1_3.docx                # Báo cáo chi tiết chuyên sâu Lab 1 EDA (219 đoạn, 7 bảng)
├── Lab_2_1_1_On_tap_ly_thuyet_Decision_Tree_Random_Forest.docx # Trả lời 9 câu hỏi lý thuyết Mục 2.1.1
├── Lab_2_3_1_On_tap_ly_thuyet_Naive_Bayes.docx # Trả lời 7 câu hỏi lý thuyết Mục 2.3.1
├── README.md                                # Tài liệu hướng dẫn tổng quan và mục lục tra cứu
│
├── code/                                    # TOÀN BỘ MÃ NGUỒN NOTEBOOK ĐÃ CHẠY ĐẦY ĐỦ 100% OUTPUTS
│   ├── lab1_3_PTKPDL.ipynb                  # Master Notebook Lab 1 (Penguins, Housing, Marketing, SweetViz, AutoViz)
│   ├── lab2_1_DecisionTree_RandomForest.ipynb # Master Notebook Lab 2.1 (Lý thuyết, 2.1.2, 2.1.3, 2.1.4, Overfitting)
│   ├── 01_CreditCard_DT_RF.ipynb            # Notebook độc lập Mục 2.1.2 (Credit Card Default)
│   ├── 02_Titanic_DT_RF.ipynb               # Notebook độc lập Mục 2.1.3 (Titanic Survival)
│   ├── 03_Diabetes_DT_RF.ipynb              # Notebook độc lập Mục 2.1.4 (Pima Indians Diabetes)
│   ├── 01-iris-svm.ipynb                    # Notebook độc lập Mục 2.2 (SVM Iris 4 kernels)
│   ├── 02-digits-svm.ipynb                  # Notebook độc lập Mục 2.2 (SVM Digits 8x8)
│   ├── 03-diabetes-svm.ipynb                # Notebook độc lập Mục 2.2 (SVM Diabetes 100k mẫu)
│   ├── 04-animal-svm.ipynb                  # Notebook độc lập Mục 2.2 (SVM Animal Condition)
│   ├── lab2_3_NaiveBayes.ipynb              # Notebook độc lập Mục 2.3 (Naive Bayes Spam, Customer, Mushroom)
│   ├── iris_confusion_matrix.png            # Biểu đồ ma trận nhầm lẫn Iris SVM
│   ├── iris_kernel_comparison.png           # Biểu đồ so sánh 4 kernel Iris SVM
│   ├── iris_evaluation.txt                  # Kết quả text đánh giá mô hình Iris
│   └── Reports/                             # Thư mục báo cáo HTML tương tác & tài liệu phụ trợ
│       ├── Lythuyet.docx                    # Lý thuyết bổ trợ SVM
│       ├── Lythuyet_2_1_DecisionTree_RandomForest.docx # Lý thuyết bổ trợ 2.1
│       ├── marketing_profile.html           # Báo cáo HTML tự động từ ydata-profiling
│       ├── marketing_sweetviz.html          # Báo cáo HTML tự động từ SweetViz
│       └── AutoViz/                         # Thư mục biểu đồ tự động từ AutoViz
│
├── data/                                    # TOÀN BỘ DỮ LIỆU THỰC NGHIỆM ĐỂ CHẠY NOTEBOOKS
│   ├── AnimalCondition.csv                  # Dữ liệu tình trạng động vật (SVM)
│   ├── Customer_Behaviour.csv               # Dữ liệu hành vi mua hàng (Naive Bayes)
│   ├── default_of_credit_card_clients.csv   # Dữ liệu vỡ nợ thẻ tín dụng 30k khách hàng (DT & RF)
│   ├── diabetes.csv                         # Dữ liệu tiểu đường Pima Indians 768 bệnh nhân (DT & RF)
│   ├── diabetes_prediction_dataset.csv      # Dữ liệu tiểu đường 100k mẫu (SVM)
│   ├── diabetes_prediction_dataset.csv.zip  # Tệp nén dự phòng
│   ├── HousingPrices-Amsterdam-August-2021.csv # Dữ liệu giá nhà Amsterdam (EDA)
│   ├── marketing_campaign.csv               # Dữ liệu chiến dịch tiếp thị 2.2k khách hàng (EDA)
│   ├── mushrooms.csv                        # Dữ liệu phân loại nấm 8.1k mẫu (Naive Bayes)
│   ├── penguins_size.csv                    # Dữ liệu kích thước chim cánh cụt (EDA)
│   ├── penguins_lter.csv                    # Dữ liệu sinh thái chim cánh cụt (EDA)
│   ├── spam.csv                             # Dữ liệu SMS Spam 5.5k tin nhắn (Naive Bayes)
│   ├── train.csv, test.csv                  # Dữ liệu Titanic hành khách (DT & RF)
│   ├── winequality-red.csv                  # Dữ liệu chất lượng rượu vang (EDA)
│   ├── covid-data.csv                       # Dữ liệu dịch bệnh COVID-19 (EDA)
│   └── Online Retail.xlsx                   # Dữ liệu giao dịch bán lẻ trực tuyến (EDA)
│
├── figures/                                 # TOÀN BỘ 19 HÌNH VẼ ĐỘ PHÂN GIẢI CAO XUẤT TỪ MÔ HÌNH
│   ├── 2_1_2_decision_tree_depth2.png       # Cấu trúc Cây quyết định depth=2 (Credit Card)
│   ├── 2_1_2_dt_max_depth_errorbar.png      # Errorbar Mean +- 1 SE theo max_depth (Credit Card)
│   ├── 2_1_2_rf_feature_importance.png      # Độ quan trọng đặc trưng Random Forest (Credit Card)
│   ├── 2_1_2_rf_n_estimators_tuning.png     # Thời gian và ROC-AUC theo n_estimators (Credit Card)
│   ├── 2_1_3_titanic_best_tree.png          # Cấu trúc Cây quyết định tối ưu (Titanic)
│   ├── 2_1_3_titanic_confusion_matrix.png   # Ma trận nhầm lẫn DT & RF (Titanic)
│   ├── 2_1_3_titanic_rf_feature_importance.png # Độ quan trọng đặc trưng (Titanic)
│   ├── 2_1_3_titanic_tuning.png             # Đường cong điều chỉnh GridSearchCV (Titanic)
│   ├── 2_1_4_diabetes_best_tree.png         # Cấu trúc Cây quyết định tối ưu (Diabetes)
│   ├── 2_1_4_diabetes_confusion_matrix.png  # Ma trận nhầm lẫn DT & RF (Diabetes)
│   ├── 2_1_4_diabetes_rf_feature_importance.png # Độ quan trọng đặc trưng (Diabetes)
│   ├── 2_1_4_diabetes_tuning.png            # Đường cong điều chỉnh GridSearchCV (Diabetes)
│   ├── 2_2_2_digits_cm.png                  # Ma trận nhầm lẫn 10 chữ số Digits (SVM)
│   ├── 2_2_4_animal_cm.png                  # Ma trận nhầm lẫn tình trạng động vật (SVM)
│   ├── 2_3_2_spam_cm.png                    # Ma trận nhầm lẫn phân loại tin nhắn rác Spam (NB)
│   ├── 2_3_3_customer_cm.png                # Ma trận nhầm lẫn dự đoán mua hàng (NB)
│   ├── 2_3_4_mushroom_cm.png                # Ma trận nhầm lẫn phân loại nấm (NB)
│   └── summary_metrics_2_1.csv              # Bảng chỉ số đối sánh mô hình 2.1
│
├── scripts/                                 # KỊCH BẢN THỰC THI & TỰ ĐỘNG HÓA BÁO CÁO
│   ├── build_full_report.py                 # Kịch bản biên dịch toàn bộ Báo cáo Word tổng hợp
│   ├── generate_theory_docx.py              # Kịch bản biên dịch báo cáo lý thuyết
│   └── execute_all_notebooks.py             # Kịch bản tự động chạy lại toàn bộ notebooks
│
├── 01_COVID_ThongKeMoTa.ipynb               # Notebook chuyên đề EDA: COVID-19
├── 02_MarketingCampaign_XuLyDuLieu.ipynb    # Notebook chuyên đề EDA: Marketing Campaign
├── 03_RedWine_ThongKeVaTrucQuan.ipynb       # Notebook chuyên đề EDA: Red Wine Quality
├── 04_PimaDiabetes_ThongKeVaTrucQuan.ipynb  # Notebook chuyên đề EDA: Pima Indians Diabetes
├── 05_AmsterdamHousing_TrucQuan.ipynb       # Notebook chuyên đề EDA: Amsterdam Housing
└── 06_OnlineRetail_EDA.ipynb                # Notebook chuyên đề EDA: Online Retail
```

---

## 4. HƯỚNG DẪN MỞ BÁO CÁO VÀ CHẠY CODE

### 4.1 Xem Báo cáo
- **Cuốn Báo cáo Tổng hợp chính:** Mở tệp `Bao_Cao_Tong_Hop_Lab05_Phan_Lop.docx` bằng Microsoft Word hoặc LibreOffice Writer.
- **Báo cáo chuyên biệt Lab 1 (EDA):** Mở tệp `Bao_cao_EDA_phan_1_3.docx`.
- **Báo cáo chuyên biệt Lý thuyết 2.1:** Mở tệp `Lab_2_1_1_On_tap_ly_thuyet_Decision_Tree_Random_Forest.docx`.
- **Báo cáo chuyên biệt Lý thuyết 2.3:** Mở tệp `Lab_2_3_1_On_tap_ly_thuyet_Naive_Bayes.docx`.

### 4.2 Chạy Notebooks
- Cài đặt các thư viện cần thiết:
  ```bash
  pip install numpy pandas matplotlib seaborn scikit-learn jupyter
  ```
- Khởi chạy JupyterLab hoặc Jupyter Notebook từ thư mục giải nén:
  ```bash
  jupyter notebook
  ```
- Mở thư mục `code/` và chạy tuần tự các notebook:
  - `lab1_3_PTKPDL.ipynb`
  - `lab2_1_DecisionTree_RandomForest.ipynb`
  - `01_CreditCard_DT_RF.ipynb`
  - `02_Titanic_DT_RF.ipynb`
  - `03_Diabetes_DT_RF.ipynb`
  - `01-iris-svm.ipynb`
  - `02-digits-svm.ipynb`
  - `03-diabetes-svm.ipynb`
  - `04-animal-svm.ipynb`
  - `lab2_3_NaiveBayes.ipynb`
- Tất cả đường dẫn nạp dữ liệu (`../data/...`) và xuất biểu đồ đều được cấu hình tương đối, đảm bảo chạy trơn tru 100% trên mọi hệ điều hành (Windows, Linux, macOS) mà không cần chỉnh sửa đường dẫn.
