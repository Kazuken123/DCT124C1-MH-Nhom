# Decision Tree V2 — kết quả train-only

Không dùng Test để tuning hoặc đánh giá. V2 tuned đánh giá theo nested CV (5 outer × 3 inner).

             model  cv_macro_f1_mean  cv_macro_f1_std_ddof0  cv_accuracy_mean  cv_dropout_recall_mean  cv_train_macro_f1_mean  cv_gap_mean  oof_macro_f1  oof_accuracy  oof_dropout_recall  oof_enrolled_f1
   DT_V1_raw_fixed            0.6472                 0.0230            0.7369                  0.7010                  0.6877       0.0405        0.6488        0.7369              0.7010           0.3607
DT_V2_onehot_fixed            0.6586                 0.0186            0.7409                  0.6983                  0.6933       0.0346        0.6598        0.7409              0.6983           0.3922
DT_V2_nested_tuned            0.6783                 0.0097            0.7358                  0.6965                  0.7088       0.0305        0.6792        0.7358              0.6966           0.4513

## Lưu ý
Kết quả CV theo fold khác OOF gộp. Mô hình đã chọn cần đánh giá trên một holdout độc lập trong giai đoạn tiếp theo nếu quy trình nhóm cho phép.
Permutation importance chỉ phản ánh quan hệ dự đoán, không phải nhân quả.