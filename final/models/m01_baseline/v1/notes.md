# Dummy v1 — mốc lớp phổ biến nhất

Người thực hiện: Lê Văn Hiếu — 3124411091.

Giữ strategy=most_frequent, không tuning. Mỗi fold chỉ xác định lớp phổ biến từ phần Train của fold. Dùng để cho thấy Accuracy gần 50% vẫn có thể bỏ sót hoàn toàn Dropout/Enrolled.

Kết quả từng lần chạy ở `experiments/runs/<run_id>/`, tìm bằng model_id=m01_baseline, version=v1 trong `experiments/results.csv`. Không chép metrics vào file phiên bản rồi ghi đè qua các lần chạy. Dummy không cần tạo nhiều version chỉ để đủ số lượng.
