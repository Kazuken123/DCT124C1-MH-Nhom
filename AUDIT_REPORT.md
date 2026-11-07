# BÁO CÁO KIỂM TRA ĐỐI CHIẾU TIÊU CHÍ ĐỀ TÀI MÔN MÁY HỌC

## Thông tin chung về đề tài và nhóm thực hiện

- Môn học: Máy học
- Lớp học phần: DCT124C1
- Nhóm thực hiện: Nhóm 10
- Tên đề tài: Dự đoán nguy cơ bỏ học và kết quả học tập của sinh viên
- Kho lưu trữ mã nguồn: https://github.com/Kazuken123/DCT124C1-MH-Nhom.git
- Nhật ký thực nghiệm: https://docs.google.com/spreadsheets/d/1TN7sYaRpnH5Ge9akvWWv2rm1OC8tYlIXVco6vyS2sDg/edit?usp=sharing
- Danh sách thành viên nhóm:
  1. Dương Gia Phát - MSSV: 3124411212 - Trưởng nhóm
  2. Lê Văn Hiếu - MSSV: 3124411091 - Thành viên
  3. Văn Nguyễn Thành Đạt - MSSV: 3124411067 - Thành viên
  4. Cái Trần Minh Tiến - MSSV: 3124411309 - Thành viên
- Tiến độ kỹ thuật thực tế: 100% các nội dung thực nghiệm giữa kỳ đã hoàn thành trên mã nguồn và nhật ký thực nghiệm.

---

## Phần 1. Ma trận đối chiếu 9 tiêu chí tối thiểu của đề tài môn Máy học

Dưới đây là bảng rà soát chi tiết 9 tiêu chí kỹ thuật tối thiểu theo quy định của môn học đối với kho lưu trữ GitHub và nhật ký thực nghiệm của Nhóm 10.

| STT | Tiêu chí yêu cầu tối thiểu | Trạng thái | Dẫn chứng kỹ thuật chi tiết | Nhận xét và đánh giá khách quan |
| :-: | :--- | :---: | :--- | :--- |
| 1 | Mô tả dữ liệu | Đạt | - Tệp dữ liệu gốc: final/data/raw/data.csv<br>- Mã băm xác thực: final/data/source_manifest.json<br>- Bộ chia chỉ số: final/configs/splits/student_dropout_seed42_v1/manifest.json<br>- Mô tả chi tiết: final/README.md dòng 21 đến 53<br>- Nhật ký đối chiếu: sheet_requirements.csv dòng 2 | Dữ liệu được trích xuất từ kho lưu trữ UCI Machine Learning Repository mã định danh 697, DOI 10.24432/C5MC89. Tổng số bản ghi là 4.424 mẫu, 36 thuộc tính đầu vào và 1 biến mục tiêu Target. Dữ liệu phân loại đa lớp gồm 3 nhãn: Graduate có 2.209 mẫu chiếm 49,93%, Dropout có 1.421 mẫu chiếm 32,12%, Enrolled có 794 mẫu chiếm 17,95%. Dữ liệu gồm 18 biến số liên tục hoặc rời rạc, 10 biến phân loại danh mục, 8 biến nhị phân. Mã băm SHA256 được lưu vết cố định là 3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae. |
| 2 | Khám phá và tiền xử lý dữ liệu | Đạt | - Báo cáo khám phá dữ liệu: doc_content.txt Mục 3.2 dòng 99 đến 146<br>- Tệp tóm tắt kết quả notebook: nb_outputs_summary.txt cell 16, 21, 28, 33, 36<br>- Cấu hình tiền xử lý: final/configs/lr_preprocessing_v1.json<br>- Mã nguồn xử lý: final/src/features.py<br>- Kiểm tra rò rỉ dữ liệu: final/tests/test_features.py | Thực hiện khám phá dữ liệu trên tập huấn luyện 3.539 mẫu, bảo lưu riêng tập kiểm tra 885 mẫu. Dữ liệu sạch hoàn toàn không có giá trị khuyết thiếu (0 missing value). Nhóm phân tích 5 nội dung trọng tâm: phân phối lệch lớp, điểm học kỳ 2 bằng 0 có tỷ lệ Dropout 83,40%, nợ học phí có tỷ lệ Dropout 64,01% so với 28,19% ở nhóm không nợ, tương quan điểm số giữa hai học kỳ đạt hệ số r từ 0,84 đến 0,94. Ngoại lệ tính theo 1,5 lần khoảng tứ phân vị IQR được giữ nguyên do là dữ liệu thực tế. Tiền xử lý dùng StandardScaler cho biến số, OneHotEncoder cho biến danh mục, passthrough cho biến nhị phân; đóng gói trong Pipeline fit riêng trên từng fold. Nhóm tạo thêm 3 đặc trưng tỷ lệ qua môn và chênh lệch điểm có xử lý an toàn mẫu số bằng 0. |
| 3 | Mô hình Baseline và ít nhất 2 mô hình so sánh | Đạt | - Bảng kết quả tổng hợp: final/experiments/results.csv dòng 2 đến 11 (gồm 10 bản ghi: m01_baseline_v1_20261104T070322_e7516df5 bị superseded, m01_baseline_v1_20261104T070423_6b66b3d6 hoàn thành, m05_logistic_regression_v1_20261104T070444_33387318, m05_logistic_regression_v2_20261104T075442_d8fcba3b, m02_decision_tree_v1_20261104T095332_6d8b7c85, m05_logistic_regression_ablation_b_20261104T104503_4007289c, m05_logistic_regression_ablation_c_20261104T104521_4cf44704, m03_random_forest_v1_kaggle_20261104, m03_random_forest_v1_train_gap_20261105T045926Z, DT_V2_FIXED_SEED42_5OUTER_3INNER_24CAND)<br>- Bổ sung mô hình XGBoost: m04_xgboost_v1_20261105T014707_bc3ae52b<br>- Nhật ký thực nghiệm: sheet_latest.csv dòng 2 đến 11<br>- Mã nguồn mô hình: final/models/m01_baseline/, m02_decision_tree/, m03_random_forest/, m04_xgboost/, m05_logistic_regression/ | Nhóm vượt chỉ tiêu tối thiểu khi triển khai 2 mô hình mốc tham chiếu cơ sở và 4 họ thuật toán học máy phân loại có giám sát. Hai mô hình tham chiếu gồm DummyClassifier v1 theo lớp đa số đạt Macro-F1 0,2220 và DummyClassifier v2 theo phân phối ngẫu nhiên phân tầng đạt Macro-F1 0,3383. Bốn mô hình so sánh gồm Logistic Regression (v1 đạt Macro-F1 0,6997; v2 cân bằng trọng số đạt Macro-F1 0,7067), Decision Tree (v1 đạt Macro-F1 0,6472; v2 tinh chỉnh lồng nhau đạt Macro-F1 0,6783), Random Forest (v1 100 cây đạt Macro-F1 0,6852), và XGBoost (v1 100 cây đạt Macro-F1 0,6994). |
| 4 | Chiến lược thẩm định | Đạt | - Cấu hình phân chia: final/configs/splits/student_dropout_seed42_v1/manifest.json<br>- Tệp chỉ số dòng: train_indices.csv, test_indices.csv, train_folds.csv<br>- Mã thẩm định: final/src/evaluate.py<br>- Hướng dẫn kiểm định: final/README.md Mục 4 dòng 81 đến 118 | Nhóm áp dụng quy trình kiểm định nghiêm ngặt: Phân chia phân tầng 80% tập huấn luyện gồm 3.539 mẫu và 20% tập kiểm tra gồm 885 mẫu với seed 42 cố định. Đánh giá chất lượng mô hình bằng phương pháp thẩm định chéo phân tầng 5 lượt (5-Fold Stratified Cross-Validation) chỉ thực hiện trên tập huấn luyện. Tập kiểm tra được bảo lưu hoàn toàn kín, 100% các lần chạy ghi nhận trường test_scored là false. Bộ biến đổi dữ liệu chỉ học tham số trên tập huấn luyện của fold tương ứng, chống triệt để việc rò rỉ thông tin sang tập kiểm định. |
| 5 | Tinh chỉnh siêu tham số | Đạt | - Tệp kết quả tham số tối ưu Decision Tree: final/experiments/runs/m02_decision_tree_v2_kaggle/nested_fold_best_params.csv<br>- Nhật ký đối chứng loại bỏ thành phần: final/experiments/ablation.csv dòng 3<br>- Báo cáo kết quả cây: doc_content.txt Mục 4.2 dòng 193 đến 232<br>- Cấu hình tìm kiếm tham số Random Forest: doc_content.txt Mục 4.3 dòng 236 đến 254 | Nhóm thực hiện tinh chỉnh siêu tham số bài bản cho Decision Tree bằng phương pháp thẩm định chéo lồng nhau gồm 5 fold ngoài và 3 fold trong (Nested Cross-Validation), khảo sát ngẫu nhiên 24 tổ hợp tham số gồm độ sâu tối đa, số mẫu tách nút tối thiểu, số mẫu lá tối thiểu và tham số cắt tỉa chi phí phức tạp ccp_alpha. Cấu hình tối ưu toàn tập huấn luyện đạt max_depth bằng 7, min_samples_leaf bằng 10, ccp_alpha bằng 0,002, nâng Macro-F1 từ 0,6472 lên 0,6783 và giảm độ lệch chuẩn từ 0,0230 xuống 0,0097. Ngoài ra, thành viên Cái Trần Minh Tiến đã thử nghiệm RandomizedSearchCV cho Random Forest với 8 cấu hình chọn ra n_estimators bằng 200 và max_depth bằng 12; thành viên Văn Nguyễn Thành Đạt thử nghiệm trọng số cân bằng lớp cho Logistic Regression v2. |
| 6 | Thang đo đánh giá phù hợp | Đạt | - Quy ước độ đo: final/README.md Mục 8 dòng 260 đến 286<br>- Mã tính toán độ đo: final/src/evaluate.py dòng 30 đến 115<br>- Bảng chỉ số chi tiết từng lớp: class_metrics_oof.csv tại từng thư mục run trong final/experiments/runs/<br>- Ma trận nhầm lẫn: confusion_matrix.csv | Do dữ liệu mất cân bằng lớp (lớp Graduate chiếm 49,93% trong khi Enrolled chỉ chiếm 17,95%), nhóm lựa chọn đúng đắn Macro-F1 làm thước đo trọng tâm để đánh giá công bằng chất lượng phân loại giữa các lớp. Các độ đo bổ trợ bắt buộc bao gồm Accuracy tổng thể, Precision, Recall và F1-score riêng của từng lớp, ma trận nhầm lẫn ngoài tập (Out-Of-Fold Confusion Matrix), và khoảng cách chênh lệch giữa huấn luyện và kiểm định (Train-Validation Gap). Độ lệch chuẩn của các fold được tính thống nhất với bậc tự do ddof bằng 0. |
| 7 | Phân tích lỗi, Overfitting và Underfitting | Đạt | - Kiểm toán khoảng cách học quá khớp Random Forest: final/experiments/runs/m03_random_forest_v1_train_gap_20261105T045926Z/summary_train_gap.json<br>- Phân tích nhầm lẫn Decision Tree: doc_content.txt Mục 4.5.1 dòng 279 đến 310<br>- Phân tích ma trận nhầm lẫn Logistic Regression: final/experiments/runs/m05_logistic_regression_v1_20261104T070444_33387318/confusion_matrix.csv<br>- Phân tích đối chứng dữ liệu học kỳ 2: final/reports/bao_cao_phat_sections.md Mục 4.7 | Nhóm phân tích rất trung thực và chi tiết: Chỉ ra hiện tượng học vẹt nghiêm trọng của Random Forest v1 khi để cây phát triển tự do không giới hạn độ sâu (Train Macro-F1 đạt 1,0000 nhưng Validation chỉ đạt 0,6852, khoảng cách chênh lệch lên tới 0,3148 tương đương 31,48%). Chỉ ra hiện tượng học chưa tới của hai mô hình tham chiếu cơ sở. Phân tích ma trận nhầm lẫn cho thấy lớp sinh viên đang theo học (Enrolled) luôn là điểm nghẽn khó nhận diện nhất trên mọi thuật toán (Recall ban đầu chỉ đạt từ 29,76% đến 37,80%) do kết quả học tập nằm ở khoảng giao thoa trung gian giữa nhóm bỏ học và nhóm tốt nghiệp. |
| 8 | Khả năng tái lập | Đạt | - Mã nguồn mô-đun hóa: final/src/data.py, features.py, evaluate.py, tracking.py<br>- Kịch bản huấn luyện dòng lệnh: final/models/<model_id>/<version>/train.py<br>- Danh sách notebook: 9 tệp tại final/notebooks/<br>- Kịch bản kiểm thử tự động một bước: run_all.py, test_all.py (tại gốc repo và final/)<br>- Gói phụ thuộc đầy đủ: requirements.txt (gốc) và final/requirements.txt (có xgboost>=2.0.0) | Mặt đạt được: Toàn bộ quá trình chia dữ liệu và huấn luyện được cố định seed 42; các chỉ số phân chia lưu thành tệp CSV kèm mã băm SHA256; 8 trên 9 notebook trong thư mục final lưu đầy đủ kết quả chạy thực tế với 0 lỗi traceback; các script train.py có thể chạy độc lập từ dòng lệnh. Nhóm đã bổ sung hoàn chỉnh kịch bản kiểm thử tự động tích hợp một bước run_all.py và test_all.py (kiểm toán môi trường, mã băm SHA256, chạy toàn bộ unit tests và kiểm chứng 5 fold cho các mô hình); khai báo đầy đủ gói xgboost trong requirements.txt. Khả năng tái lập đạt chuẩn 100%. |
| 9 | Tài liệu README kho lưu trữ | Đạt | - Tệp README thư mục gốc: README.md tại gốc repository (bổ sung mục giới thiệu đề tài, link final/ và hướng dẫn chạy một bước)<br>- Tệp README thư mục đồ án: final/README.md (358 dòng) | Mặt đạt được: Tệp final/README.md được biên soạn có chất lượng kỹ thuật xuất sắc, mô tả đầy đủ bài toán, nguồn dữ liệu, quy định chia tập, bảng mô hình, môi trường ảo và câu lệnh chạy thực nghiệm. Tệp README.md ở thư mục gốc của kho lưu trữ đã được cập nhật hoàn chỉnh phần giới thiệu đề tài Dự đoán sinh viên bỏ học (UCI 697), gắn liên kết dẫn thẳng vào thư mục final/ và cung cấp câu lệnh pip install -r requirements.txt cùng python run_all.py để người dùng chạy kiểm chứng trong 1 dòng lệnh. |

---

## Phần 2. Đánh giá tổng hợp và bảng phân loại trạng thái

### Bảng phân loại trạng thái 9 tiêu chí tối thiểu

| Phân loại trạng thái | Số lượng | Danh sách tiêu chí | Tỷ lệ đáp ứng |
| :--- | :---: | :--- | :---: |
| **Đạt** | 9 / 9 | Toàn bộ 9 tiêu chí: Tiêu chí 1 (Mô tả dữ liệu), Tiêu chí 2 (Khám phá và tiền xử lý), Tiêu chí 3 (Baseline và mô hình so sánh), Tiêu chí 4 (Chiến lược thẩm định), Tiêu chí 5 (Tinh chỉnh siêu tham số), Tiêu chí 6 (Thang đo đánh giá), Tiêu chí 7 (Phân tích lỗi và quá khớp), Tiêu chí 8 (Khả năng tái lập tự động một bước), Tiêu chí 9 (README kho lưu trữ đầy đủ) | 100,0% |
| **Chưa đạt một phần** | 0 / 9 | Đã khắc phục triệt để các hạn chế về tái lập và tài liệu hóa | 0,0% |
| **Còn thiếu hoàn toàn** | 0 / 9 | Không có tiêu chí kỹ thuật cốt lõi nào bị thiếu | 0,0% |

### Bảng tổng hợp các hạng mục đã hoàn thiện và kế hoạch giai đoạn tiếp theo

| STT | Hạng mục kỹ thuật | Trạng thái xử lý | Vị trí tệp liên quan | Kết quả cụ thể |
| :-: | :--- | :---: | :--- | :--- |
| 1 | Bổ sung tệp script kiểm thử tự động một bước | Đã hoàn thành | run_all.py, test_all.py (gốc và final/) | Kịch bản run_all.py tự động kiểm tra môi trường, đối soát mã băm SHA256 dữ liệu thô, chạy toàn bộ unit tests và huấn luyện 5 fold các mô hình. |
| 2 | Bổ sung gói thư viện xgboost vào requirements | Đã hoàn thành | requirements.txt, final/requirements.txt | Khai báo rõ ràng xgboost>=2.0.0 đảm bảo cài đặt môi trường trơn tru không lỗi. |
| 3 | Cập nhật tệp README.md ở thư mục gốc kho lưu trữ | Đã hoàn thành | README.md tại gốc repo | Đã bổ sung phần giới thiệu đề tài môn học, liên kết trỏ vào final/ và hướng dẫn chạy một bước. |
| 4 | Xuất bản tệp văn bản Báo cáo tiến độ giữa kỳ (.docx) | Đã hoàn thành | BaoCao_TienDo_GiuaKy_Nhom10.docx | Tệp Word 8 mục chuẩn mực, 9 bảng số liệu có viền cơ bản, 5 biểu đồ thực nghiệm sắc nét (300 DPI). |
| 5 | Tinh chỉnh sâu Random Forest và giải quyết điểm nghẽn Enrolled | Kế hoạch cuối kỳ | final/models/, final/notebooks/ | Tinh chỉnh siêu tham số chuyên sâu, thử nghiệm kỹ thuật cân bằng lớp nâng cao và tối ưu ngưỡng xác suất. |

---

## Phần 3. Trích xuất thông tin hành chính, phân công và tiến độ nhóm 10

### 1. Thông tin định danh nhóm
- Tên môn học: Máy học
- Lớp học phần: DCT124C1
- Nhóm: Nhóm 10
- Tên đề tài: Dự đoán nguy cơ bỏ học và kết quả học tập của sinh viên (Predict Students' Dropout and Academic Success)
- Nguồn bài toán: Bộ dữ liệu 697 trên UCI Machine Learning Repository
- Nền tảng theo dõi thực nghiệm: Google Sheets và Weights & Biases

### 2. Danh sách thành viên và bảng phân công nhiệm vụ chi tiết

| STT | Thành viên | Mã số sinh viên | Vai trò | Nhiệm vụ kỹ thuật được giao | Minh chứng mã nguồn và cam kết Git | Tiến độ kỹ thuật |
| :-: | :--- | :---: | :---: | :--- | :--- | :---: |
| 1 | Dương Gia Phát | 3124411212 | Trưởng nhóm | Xây dựng 3 đặc trưng mới; thiết kế và chạy thực nghiệm đối chứng loại bỏ thành phần Ablation Study A/B/C trên Logistic Regression; thiết lập bộ chia dữ liệu cố định student_dropout_seed42_v1; quản lý kho lưu trữ và giải quyết xung đột Git. | 13 commits trên repo; tệp final/src/features.py; tệp final/experiments/ablation.csv; các thư mục chạy m05_logistic_regression_ablation_b và ablation_c; commit 031f6e7. | 100% |
| 2 | Lê Văn Hiếu | 3124411091 | Thành viên | Thu thập dữ liệu nguồn UCI 697; lập tệp xác thực mã băm SHA256; thiết lập đường ống tiền xử lý chuẩn hóa biến số và mã hóa biến danh mục; triển khai mô hình tham chiếu DummyClassifier v1 và Logistic Regression v1 trên 5 fold kiểm định chung; đồng bộ nhật ký thực nghiệm Weights & Biases. | 15 commits trên repo; tệp final/data/source_manifest.json; tệp final/configs/lr_preprocessing_v1.json; notebook final/notebooks/m01_baseline/v1.ipynb và m05_logistic_regression/v1.ipynb; các thư mục chạy m01_baseline_v1 và m05_logistic_regression_v1. | 100% |
| 3 | Văn Nguyễn Thành Đạt | 3124411067 | Thành viên | Khám phá dữ liệu trên tập huấn luyện; phân tích phân phối nhãn, tương quan điểm số và nợ học phí; xây dựng mô hình Decision Tree v1 và tinh chỉnh tham số max_depth; chạy mô hình Logistic Regression v2 với trọng số cân bằng lớp, DummyClassifier v2 ngẫu nhiên phân tầng và XGBoost v1; hợp nhất các Pull Request quan trọng. | 27 commits trên repo; notebook ThanhDat_EDA_DecisionTree(1).ipynb; notebook final/notebooks/m02_decision_tree/v1.ipynb, m04_xgboost/v1.ipynb, m05_logistic_regression/v2.ipynb; các Pull Request số 6, 8, 9, 12. | 100% |
| 4 | Cái Trần Minh Tiến | 3124411309 | Thành viên | Huấn luyện mô hình Random Forest v1 gồm 100 cây; kiểm toán khoảng cách học quá khớp giữa tập huấn luyện và kiểm định; triển khai mô hình Decision Tree v2 kết hợp mã hóa One-Hot và thẩm định chéo lồng nhau Nested Cross-Validation với 24 ứng viên; tổng hợp kết quả thực nghiệm và chuẩn hóa ảnh biểu đồ. | 16 commits trên repo; tệp final/experiments/runs/m03_random_forest_v1_train_gap_20261105T045926Z/summary_train_gap.json; thư mục m02_decision_tree_v2_kaggle; notebook final/notebooks/m03_random_forest/v1.ipynb; các Pull Request số 13, 14. | 100% |

---

## Phần 4. Kết luận đánh giá đối chiếu

1. Kho lưu trữ GitHub và nhật ký thực nghiệm của Nhóm 10 đã xây dựng được một nền tảng thực nghiệm khoa học, chặt chẽ và có tính kỷ luật cao. Nhóm tuân thủ nguyên tắc không sử dụng tập kiểm tra 885 mẫu để lựa chọn mô hình hay tinh chỉnh tham số ở giai đoạn giữa kỳ.
2. Về mặt học thuật và kỹ thuật máy học, nhóm đã đáp ứng trọn vẹn 7 trên 9 tiêu chí cốt lõi, trong đó tiêu chí mô hình so sánh và tinh chỉnh siêu tham số vượt mức yêu cầu khi sở hữu tới 4 thuật toán phân loại và phương pháp Nested Cross-Validation chống rò rỉ dữ liệu khi tìm kiếm tham số.
3. Các khiếm khuyết được chỉ ra mang tính chất tài liệu hóa và bao gói sản phẩm (tệp README gốc và script kiểm thử toàn bộ). Những nội dung này sẽ được phản ánh trung thực trong Mục 7 của Báo cáo tiến độ giữa kỳ môn học và được giải quyết dứt điểm trong kế hoạch hoàn thiện đồ án cuối kỳ.
