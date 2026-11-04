# NỘI DUNG BÁO CÁO PHẦN ĐƯỢC PHÂN CÔNG — DƯƠNG GIA PHÁT (MSSV: 3124411212)

---

## CHƯƠNG 1. GIỚI THIỆU BÀI TOÁN VÀ MỤC TIÊU NGHIÊN CỨU

### 1.1. Bối cảnh và ý nghĩa thực tiễn
Hiện tượng sinh viên bỏ học hoặc chậm tiến độ tốt nghiệp gây tổn thất lớn về nguồn lực đào tạo của nhà trường và ảnh hưởng trực tiếp đến tương lai của người học. Nếu nhà trường có thể nhận diện sớm các sinh viên gặp khó khăn ngay từ năm thứ nhất, các phòng ban cố vấn học tập có thể can thiệp kịp thời bằng các biện pháp trợ cấp, tư vấn tâm lý hoặc định hướng lộ trình học tập phù hợp.

### 1.2. Xác định bài toán học máy
- Loại bài toán: Học có giám sát, cụ thể là phân loại đa lớp.
- Đầu vào: 36 đặc trưng thu thập từ hồ sơ tuyển sinh, hoàn cảnh kinh tế xã hội và kết quả học tập tích lũy.
- Đầu ra: Một trong ba trạng thái học tập của sinh viên tại thời điểm khảo sát:
  1. `Dropout`: Sinh viên đã bỏ học hoặc thôi học.
  2. `Enrolled`: Sinh viên còn đang theo học tại trường.
  3. `Graduate`: Sinh viên đã hoàn thành chương trình và tốt nghiệp.

### 1.3. Mục tiêu nghiên cứu và phạm vi thời điểm dự đoán
Nghiên cứu tập trung vào hai câu hỏi kỹ thuật:
1. Đánh giá mức độ phụ thuộc của mô hình dự đoán vào kết quả học tập học kỳ 2: So sánh hiệu năng khi có và không có dữ liệu học kỳ 2 để xác định tính khả thi của việc cảnh báo sớm ở từng thời điểm trong năm học.
2. Đánh giá giá trị thực tế của việc xây dựng thêm các đặc trưng tỷ lệ qua môn và xu hướng điểm số so với việc chỉ sử dụng các thuộc tính số lượng gốc.

---

## CHƯƠNG 2. CƠ SỞ LÝ THUYẾT (MỤC 2.1 VÀ 2.5)

### 2.1. Tổng quan các hướng tiếp cận liên quan
Các nghiên cứu dự đoán kết quả học tập của sinh viên trên thế giới thường tiếp cận theo hai hướng chính:
- Hướng tiếp cận dựa trên hồ sơ tĩnh trước nhập học: Sử dụng điểm xét tuyển, trình độ học vấn của cha mẹ và hoàn cảnh kinh tế gia đình. Ưu điểm là có thể dự đoán ngay khi sinh viên nộp hồ sơ, nhưng nhược điểm là độ chính xác thường không cao do thiếu dữ liệu phản ánh sự thích nghi thực tế của sinh viên với môi trường đại học.
- Hướng tiếp cận dựa trên kết quả học tập tích lũy theo từng học kỳ: Kết hợp hồ sơ ban đầu với số tín chỉ đăng ký, số tín chỉ đạt và điểm trung bình tích lũy. Hướng tiếp cận này đem lại độ chính xác cao hơn rõ rệt nhưng phụ thuộc chặt chẽ vào thời điểm thu thập dữ liệu sau mỗi kỳ thi.

### 2.5. Cơ sở lý thuyết về Xây dựng đặc trưng và Nghiên cứu loại bỏ thành phần
- **Xây dựng đặc trưng:** Là quá trình áp dụng kiến thức chuyên môn miền bài toán để tạo ra các biến mới từ các biến gốc nhằm cung cấp tín hiệu phân loại trực tiếp cho thuật toán. Trong bài toán đào tạo tín chỉ, số môn sinh viên vượt qua trên tổng số môn đăng ký thể hiện trực tiếp năng lực hoàn thành khối lượng học tập, trong khi sự thay đổi điểm số giữa hai học kỳ thể hiện xu hướng tiến bộ hay sa sút của sinh viên.
- **Nghiên cứu loại bỏ thành phần:** Là phương pháp thực nghiệm khoa học trong đó người làm lần lượt cô lập, thêm hoặc bớt một nhóm đặc trưng hay một thành phần trong hệ thống, trong khi giữ cố định hoàn toàn mô hình, siêu tham số, dữ liệu huấn luyện và các tập fold kiểm định. Phương pháp này cho phép đo đạc chính xác mức đóng góp biên thực sự của từng thành phần dữ liệu, tránh việc gán nhầm cải thiện hiệu năng cho thuật toán phân loại.

---

## CHƯƠNG 3. THIẾT KẾ PHƯƠNG PHÁP VÀ ĐẶC TRƯNG (MỤC 3.4 VÀ 3.5)

### 3.4. Thiết kế các bộ đặc trưng đối chứng A, B, C
Để trả lời độc lập hai câu hỏi nghiên cứu, nhóm thiết lập ba cấu hình đặc trưng đối chứng:

| Cấu hình | Tên gọi | Số lượng thuộc tính | Thành phần đặc trưng | Ý nghĩa thực nghiệm |
| :--- | :--- | :---: | :--- | :--- |
| **A** | Dữ liệu gốc | 36 | 18 biến số liên tục, 10 biến phân loại, 8 biến nhị phân | Mốc đối chứng chuẩn của bộ dữ liệu UCI 697 |
| **B** | Bỏ học kỳ 2 | 30 | Loại bỏ 6 biến học kỳ 2, còn lại 12 biến số liên tục, 10 biến phân loại, 8 biến nhị phân | Đo lường hiệu năng khi chỉ có dữ liệu đến hết học kỳ 1 |
| **C** | Bổ sung đặc trưng mới | 39 | 36 biến gốc cộng thêm 3 biến đặc trưng tỷ lệ và xu hướng điểm số | Đo lường giá trị bổ sung của kỹ thuật xây dựng đặc trưng |

#### Công thức tính toán các đặc trưng tạo mới trong Cấu hình C:
1. **Tỷ lệ môn đạt học kỳ 1:**
   $$\text{Tỷ lệ đạt HK1} = \begin{cases} \frac{\text{Số môn đạt HK1}}{\text{Số môn đăng ký HK1}} & \text{nếu Số môn đăng ký HK1} > 0 \\ 0 & \text{nếu Số môn đăng ký HK1} = 0 \end{cases}$$
2. **Tỷ lệ môn đạt học kỳ 2:**
   $$\text{Tỷ lệ đạt HK2} = \begin{cases} \frac{\text{Số môn đạt HK2}}{\text{Số môn đăng ký HK2}} & \text{nếu Số môn đăng ký HK2} > 0 \\ 0 & \text{nếu Số môn đăng ký HK2} = 0 \end{cases}$$
3. **Chênh lệch điểm trung bình giữa hai học kỳ:**
   $$\text{Chênh lệch điểm} = \text{Điểm trung bình HK2} - \text{Điểm trung bình HK1}$$

#### Xử lý mẫu số bằng 0 và tính an toàn dữ liệu:
Trong tập dữ liệu khảo sát có 180 sinh viên đăng ký 0 tín chỉ ở học kỳ 1 và 180 sinh viên đăng ký 0 tín chỉ ở học kỳ 2. Nếu áp dụng phép chia trực tiếp sẽ gây ra lỗi chia cho 0 hoặc sinh giá trị vô cùng. Thuật toán kiểm tra điều kiện mẫu số lớn hơn 0 trước khi thực hiện phép chia; nếu mẫu số bằng 0, tỷ lệ được gán mặc định là 0.0. Toàn bộ các phép biến đổi được tính toán cục bộ theo từng dòng dữ liệu của từng sinh viên, không phụ thuộc vào bất kỳ giá trị trung bình hay độ lệch chuẩn toàn cục nào, đảm bảo không gây rò rỉ dữ liệu giữa các tập con.

### 3.5. Thiết kế đường ống xử lý và kiểm soát rò rỉ dữ liệu
Mọi thao tác tiền xử lý và tính toán đặc trưng được đóng gói trọn vẹn bên trong một Pipeline của thư viện Scikit-learn:
- Bước 1: `FeatureEngineer` tính toán thêm 3 đặc trưng mới trên tập con huấn luyện.
- Bước 2: `ColumnTransformer` áp dụng `StandardScaler` cho toàn bộ các biến số liên tục, `OneHotEncoder` cho các biến danh mục và `passthrough` cho các biến nhị phân.
- Bước 3: Đưa ma trận đặc trưng sau biến đổi vào bộ phân loại `LogisticRegression`.

Toàn bộ quá trình ước lượng giá trị trung bình và độ lệch chuẩn của bộ chuẩn hóa chỉ được thực hiện trên các chỉ số thuộc tập huấn luyện của fold tương ứng, sau đó áp dụng phép chuyển đổi lên fold kiểm định. Phép kiểm tra độc lập tại mỗi fold xác nhận số mẫu nhìn thấy của bộ chuẩn hóa luôn bằng đúng độ dài tập huấn luyện và phần bù tập kiểm định không có bất kỳ phần tử chung nào.

---

## CHƯƠNG 4. THỰC NGHIỆM ĐỐI CHỨNG VÀ THẢO LUẬN (MỤC 4.6)

### 4.6. Kết quả thực nghiệm đối chứng A/B/C
Thực nghiệm sử dụng mô hình Logistic Regression cố định từ cấu hình v1 do Lê Văn Hiếu bàn giao: chuẩn tắc hóa L2, hệ số nghịch đảo C bằng 1.0, thuật toán tối ưu lbfgs, số vòng lặp tối đa 2000, ngưỡng dừng 0.0001, seed 42 và không áp dụng trọng số lớp. Cả ba cấu hình đều chạy trên cùng 5 fold kiểm định phân tầng cố định từ mã chia `student_dropout_seed42_v1` trên 3.539 mẫu huấn luyện.

#### Bảng tổng hợp kết quả đối chứng qua 5 Fold Cross-Validation:

| Cấu hình | Số biến | Macro-F1 CV | Độ lệch chuẩn (ddof=0) | Chênh lệch F1 so với A | Accuracy CV | Recall Dropout | Recall Enrolled | Recall Graduate | Chênh lệch Train-Validation |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **B (Bỏ HK2)** | 30 | 0,6578 | 0,0149 | -0,0420 | 74,62% | 75,28% | 29,92% | 90,26% | 0,0492 |
| **A (Gốc)** | 36 | 0,6997 | 0,0099 | 0,0000 | 77,54% | 77,48% | 37,80% | 91,85% | 0,0559 |
| **C (Tạo mới)** | 39 | 0,7031 | 0,0110 | +0,0033 | 77,71% | 77,74% | 38,43% | 91,79% | 0,0563 |

#### Bảng chi tiết Macro-F1 theo từng Fold kiểm định:

| Fold kiểm định | Cấu hình B (Bỏ HK2) | Cấu hình A (Gốc) | Cấu hình C (Tạo mới) | Chênh lệch A trừ B | Chênh lệch C trừ A |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Fold 1 | 0,6784 | 0,7190 | 0,7249 | +0,0406 | +0,0059 |
| Fold 2 | 0,6576 | 0,6946 | 0,6984 | +0,0370 | +0,0037 |
| Fold 3 | 0,6457 | 0,6919 | 0,6996 | +0,0462 | +0,0077 |
| Fold 4 | 0,6694 | 0,6995 | 0,6957 | +0,0301 | -0,0039 |
| Fold 5 | 0,6377 | 0,6937 | 0,6967 | +0,0559 | +0,0031 |
| **Trung bình** | **0,6578** | **0,6997** | **0,7031** | **+0,0420** | **+0,0033** |

### 4.7. Thảo luận và diễn giải kết quả chuyên môn

#### 1. Đóng góp của thông tin học kỳ 2 (So sánh A và B):
- Khi loại bỏ nhóm thông tin học kỳ 2, Macro-F1 trung bình giảm mạnh từ 0,6997 xuống 0,6578, tương đương mức sụt giảm 0,0420 điểm F1 (-6,0%). Độ chính xác tổng thể giảm từ 77,54% xuống 74,62%.
- Sự sụt giảm thể hiện rõ nét nhất ở lớp sinh viên còn theo học (`Enrolled`): Recall giảm từ 37,80% xuống 29,92% (giảm 7,88 điểm phần trăm). Điều này chứng minh số tín chỉ đạt được ở học kỳ 2 là ranh giới quyết định để phân biệt giữa sinh viên kiên trì theo học và sinh viên chuẩn bị rời trường.
- Độ ổn định của mô hình khi thiếu dữ liệu HK2 kém hơn: độ lệch chuẩn tăng từ 0,0099 lên 0,0149.
- **Kết luận về giới hạn triển khai:** Mô hình đạt hiệu năng xấp xỉ 70% Macro-F1 chỉ khả thi khi triển khai tại thời điểm sinh viên đã hoàn thành toàn bộ năm thứ nhất. Nếu cơ sở đào tạo yêu cầu cảnh báo sớm ở giai đoạn đầu năm học, hệ thống bắt buộc phải chấp nhận giới hạn nhận diện của cấu hình B với Macro-F1 khoảng 65,78%.

#### 2. Giá trị của kỹ thuật xây dựng đặc trưng mới (So sánh C và A):
- Việc bổ sung 3 đặc trưng tỷ lệ qua môn và chênh lệch điểm giúp Macro-F1 tăng từ 0,6997 lên 0,7031, cải thiện +0,0033 điểm F1. Xu hướng cải thiện ghi nhận được ở 4 trên 5 fold kiểm định.
- Khả năng nhận diện sinh viên bỏ học (`Dropout`) tăng từ 77,48% lên 77,74% (+0,26%); khả năng nhận diện sinh viên đang học (`Enrolled`) tăng từ 37,80% lên 38,43% (+0,63%).
- **Đánh giá kỹ thuật khách quan:** Mức tăng +0,0033 trên mô hình Logistic Regression là khiêm tốn. Lý do kỹ thuật là thuật toán Logistic Regression với bộ chuẩn hóa đã khai thác tốt mối quan hệ tuyến tính giữa số môn đạt và số môn đăng ký. Tuy vậy, việc biến đổi tỷ lệ phi tuyến vẫn cung cấp thêm một lượng thông tin biên hữu ích giúp mô hình cải thiện khả năng phân định ở các trường hợp biên mà không làm gia tăng khoảng cách học vẹt giữa tập huấn luyện và tập kiểm định.
