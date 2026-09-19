# -*- coding: utf-8 -*-
"""
House Prices: Advanced Regression Techniques
Trích xuất toàn bộ mã nguồn từ tài liệu PDF: "House Prices: Advanced Regression Techniques - Rishabh Nimje"
Nguồn tham khảo: https://risx3.github.io/house-prices/
Cuộc thi Kaggle: https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques
"""

# ==========================================
# 1. IMPORT THƯ VIỆN CẦN THIẾT
# ==========================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Thư viện Machine Learning & Tuning
import xgboost
from sklearn.model_selection import RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier  # Lưu ý: Bài gốc dùng Classifier (trong hồi quy thường dùng DecisionTreeRegressor)

# Thư viện Deep Learning
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import backend as k


# ==========================================
# 2. TẢI DỮ LIỆU (LOAD DATA)
# ==========================================
print("=== 1. TẢI DỮ LIỆU ===")
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

print("Train Shape: ", train.shape)
print("Test Shape: ", test.shape)

print("\n--- Train Info ---")
train.info()

print("\n--- Test Info ---")
test.info()


# ==========================================
# 3. KIỂM TRA GIÁ TRỊ THIẾU (CHECK NULL VALUES)
# ==========================================
print("\n=== 2. KIỂM TRA DỮ LIỆU KHUYẾT (NULL VALUES) ===")
print("Train NULL values:")
print(train.isnull().sum())

# Vẽ Heatmap kiểm tra NULL (tùy chọn)
plt.figure(figsize=(12, 6))
sns.heatmap(train.isnull(), cbar=True, cmap='viridis')
plt.title("Train Missing Values Heatmap")
plt.show()

print("\nTest NULL values:")
print(test.isnull().sum())

plt.figure(figsize=(12, 6))
sns.heatmap(test.isnull(), cbar=True, cmap='viridis')
plt.title("Test Missing Values Heatmap")
plt.show()


# ==========================================
# 4. XỬ LÝ DỮ LIỆU KHUYẾT (HANDLING NULL DATA)
# ==========================================
print("\n=== 3. XỬ LÝ DỮ LIỆU KHUYẾT ===")
# Xử lý cho tập Train
cat_col_train = [
    'FireplaceQu', 'GarageType', 'GarageFinish', 'MasVnrType', 'BsmtQual',
    'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'FireplaceQu',
    'GarageQual', 'GarageCond'
]

ncat_col_train = ['LotFrontage', 'GarageYrBlt', 'MasVnrArea']

# Điền Mode (giá trị xuất hiện nhiều nhất) cho biến phân loại
for i in cat_col_train:
    train[i] = train[i].fillna(train[i].mode()[0])

# Điền Mean (trung bình) cho biến số
for j in ncat_col_train:
    train[j] = train[j].fillna(train[j].mean())

# Xử lý cho tập Test
cat_col_test = [
    'FireplaceQu', 'GarageType', 'GarageFinish', 'MasVnrType', 'BsmtQual',
    'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'FireplaceQu',
    'GarageQual', 'GarageCond', 'MSZoning', 'Utilities', 'Exterior1st',
    'Exterior2nd', 'KitchenQual', 'Functional', 'SaleType'
]

ncat_col_test = [
    'LotFrontage', 'GarageYrBlt', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2',
    'BsmtUnfSF', 'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath', 'GarageCars',
    'GarageArea'
]

for i in cat_col_test:
    test[i] = test[i].fillna(test[i].mode()[0])

for j in ncat_col_test:
    test[j] = test[j].fillna(test[j].mean())

# Xóa các cột có tỷ lệ rỗng > 70% và cột 'Id'
to_drop = ['Id', 'Alley', 'PoolQC', 'Fence', 'MiscFeature']

for k_col in to_drop:
    train.drop([k_col], axis=1, inplace=True)
    test.drop([k_col], axis=1, inplace=True)

print("Sau khi xử lý NULL:")
print("Train Shape: ", train.shape)
print("Test Shape: ", test.shape)


# ==========================================
# 5. MÃ HÓA ONE-HOT (ONE HOT ENCODING)
# ==========================================
print("\n=== 4. TIẾN HÀNH ONE-HOT ENCODING ===")
# Nối tạm thời tập train và test để đồng bộ danh sách danh mục
final_df = pd.concat([train, test], axis=0)
print("Final DF Shape ban đầu:", final_df.shape)

all_cat_col = [
    'MSZoning', 'Street', 'LotShape', 'LandContour', 'Utilities', 'LotConfig',
    'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType',
    'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd',
    'MasVnrType', 'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual',
    'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'Heating',
    'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual', 'Functional',
    'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond',
    'PavedDrive', 'SaleType', 'SaleCondition'
]

def cat_onehot_encoding(multicol):
    global final_df
    df_final = final_df
    i = 0
    for fields in multicol:
        print(f"Encoding: {fields}")
        df1 = pd.get_dummies(final_df[fields], drop_first=True)
        final_df.drop([fields], axis=1, inplace=True)
        if i == 0:
            df_final = df1.copy()
        else:
            df_final = pd.concat([df_final, df1], axis=1)
        i = i + 1
        
    df_final = pd.concat([final_df, df_final], axis=1)
    return df_final

final_df = cat_onehot_encoding(all_cat_col)
print("Shape sau khi One-Hot:", final_df.shape)

# Loại bỏ các cột trùng tên nếu có
final_df = final_df.loc[:, ~final_df.columns.duplicated()]
print("Shape sau khi loại bỏ cột trùng lặp:", final_df.shape)


# ==========================================
# 6. TÁCH LẠI TẬP TRAIN VÀ TEST
# ==========================================
print("\n=== 5. CHIA LẠI DỮ LIỆU HUẤN LUYỆN VÀ KIỂM THỬ ===")
df_train = final_df.iloc[:1460, :]
df_test = final_df.iloc[1460:, :]

# Xóa cột SalePrice khỏi tập test (vì tập test không có nhãn này)
df_test = df_test.drop(['SalePrice'], axis=1)

print("Train Shape: ", df_train.shape)
print("Test Shape: ", df_test.shape)

# Tách features (x_train) và target (y_train)
x_train = df_train.drop(['SalePrice'], axis=1)
y_train = df_train['SalePrice']


# ==========================================
# 7. MÔ HÌNH 1: XGBOOST REGRESSOR & HYPERPARAMETER TUNING
# ==========================================
print("\n=== 6. HUẤN LUYỆN MÔ HÌNH XGBOOST ===")
xgb_model = xgboost.XGBRegressor()
xgb_model.fit(x_train, y_train)

# Thiết lập không gian siêu tham số để tìm kiếm
param = {
    'n_estimators': [100, 500, 900, 1100, 1500],
    'max_depth': [2, 3, 5, 10, 15],
    'learning_rate': [0.05, 0.1, 0.15, 0.2],
    'min_child_weight': [1, 2, 3, 4],
    'booster': ['gbtree', 'gblinear'],
    'base_score': [0.25, 0.5, 0.75, 1]
}

print("Tìm kiếm siêu tham số tối ưu bằng RandomizedSearchCV...")
random_cv = RandomizedSearchCV(
    estimator=xgb_model,
    param_distributions=param,
    cv=5,
    n_iter=50,
    scoring='neg_mean_absolute_error',
    n_jobs=4,
    verbose=5,
    return_train_score=True,
    random_state=42
)

# Chạy tìm kiếm siêu tham số (uncomment khi muốn chạy lại)
# random_cv.fit(x_train, y_train)
# print("Best Estimator:", random_cv.best_estimator_)

# Sử dụng mô hình XGBoost với bộ tham số tối ưu nhất tìm được
xgb_best = xgboost.XGBRegressor(
    base_score=0.25,
    booster='gbtree',
    colsample_bylevel=1,
    colsample_bynode=1,
    colsample_bytree=1,
    gamma=0,
    gpu_id=-1,
    importance_type='gain',
    interaction_constraints='',
    learning_rate=0.1,
    max_delta_step=0,
    max_depth=2,
    min_child_weight=1,
    monotone_constraints='()',
    n_estimators=900,
    n_jobs=0,
    num_parallel_tree=1,
    objective='reg:squarederror',
    random_state=0,
    reg_alpha=0,
    reg_lambda=1,
    scale_pos_weight=1,
    subsample=1,
    tree_method='exact',
    validate_parameters=1,
    verbosity=None
)

xgb_best.fit(x_train, y_train)

# Lưu model XGBoost
with open("xgb_model.pkl", "wb") as f_out:
    pickle.dump(xgb_best, f_out)
print("Đã lưu: xgb_model.pkl")

# Dự đoán trên tập test và tạo file nộp
pred_xgb = xgb_best.predict(df_test)
print("Kích thước dự đoán XGBoost:", pred_xgb.shape)

try:
    sub_df = pd.read_csv('sample_submission.csv')
    sub_df['SalePrice'] = pred_xgb
    sub_df.to_csv('sample_sub_xgb.csv', index=False)
    print("Đã xuất file nộp: sample_sub_xgb.csv")
except Exception as e:
    print("Thông báo: Chưa tìm thấy sample_submission.csv để xuất trực tiếp.")


# ==========================================
# 8. MÔ HÌNH 2: DECISION TREE
# ==========================================
print("\n=== 7. HUẤN LUYỆN MÔ HÌNH DECISION TREE ===")
# Khởi tạo mô hình Decision Tree (theo code của tài liệu gốc)
dt_model = DecisionTreeClassifier()
dt_model.fit(x_train, y_train)

pred_dt = dt_model.predict(df_test)
print("Kích thước dự đoán Decision Tree:", pred_dt.shape)

try:
    sub_df = pd.read_csv('sample_submission.csv')
    sub_df['SalePrice'] = pred_dt
    sub_df.to_csv('sample_sub_dt.csv', index=False)
    print("Đã xuất file nộp: sample_sub_dt.csv")
except Exception as e:
    pass


# ==========================================
# 9. MÔ HÌNH 3: MẠNG NƠ-RON NHÂN TẠO (ANN)
# ==========================================
print("\n=== 8. HUẤN LUYỆN MẠNG NƠ-RON (ANN) ===")

# Hàm loss tùy chỉnh: Root Mean Squared Error
def root_mean_squared_error(y_true, y_pred):
    return k.sqrt(k.mean(k.square(y_pred - y_true)))

# Xây dựng kiến trúc ANN với Keras Sequential
nn_model = Sequential()
nn_model.add(Dense(50, kernel_initializer='he_uniform', activation='relu', input_dim=176))
nn_model.add(Dense(25, kernel_initializer='he_uniform', activation='relu'))
nn_model.add(Dense(50, kernel_initializer='he_uniform', activation='relu'))
nn_model.add(Dense(1, kernel_initializer='he_uniform'))

nn_model.compile(loss=root_mean_squared_error, optimizer='Adamax')

# Huấn luyện mô hình ANN (epochs=1000, batch_size=10)
nn_model.fit(
    x_train.values,
    y_train.values,
    validation_split=0.25,
    batch_size=10,
    epochs=1000,
    verbose=1
)

# Lưu mô hình ANN
nn_model.save('nn_model.h5')
print("Đã lưu mô hình: nn_model.h5")

# Dự đoán tập test và xuất submission
pred_nn = nn_model.predict(df_test).flatten()
print("Kích thước dự đoán ANN:", pred_nn.shape)

try:
    sub_df = pd.read_csv('sample_submission.csv')
    sub_df['SalePrice'] = pred_nn
    sub_df.to_csv('sample_sub_nn.csv', index=False)
    print("Đã xuất file nộp: sample_sub_nn.csv")
except Exception as e:
    pass

print("\n=== HOÀN TẤT TOÀN BỘ QUY TRÌNH ===")
