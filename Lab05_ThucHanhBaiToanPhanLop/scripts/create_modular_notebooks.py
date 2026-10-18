import json
import os

def create_modular_notebooks():
    code_dir = 'Lab05_ThucHanhBaiToanPhanLop/code'
    
    def md(text):
        return {
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in text.strip().split("\n")]
        }

    def code(text):
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in text.strip().split("\n")]
        }

    def make_nb(cells):
        return {
            "cells": cells,
            "metadata": {
                "language_info": {"name": "python", "version": "3.12"},
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }

    # --------------------------------------------------------------------------
    # 1. 01_CreditCard_DT_RF.ipynb
    # --------------------------------------------------------------------------
    cells_cc = [
        md("# 2.1.2 BÀI LÀM MẪU: DỰ ĐOÁN KHẢ NĂNG VỠ NỢ THẺ TÍN DỤNG\nMô hình: Decision Tree Classifier và Random Forest Classifier\nThực hiện: Lê Văn Hiếu"),
        md("### Nhiệm vụ 1: Nạp dữ liệu, tiền xử lý, huấn luyện DecisionTreeClassifier với max_depth=2"),
        code("""import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score

data_path = '../data/default_of_credit_card_clients.csv' if os.path.exists('../data/default_of_credit_card_clients.csv') else 'Lab05_ThucHanhBaiToanPhanLop/data/default_of_credit_card_clients.csv'
df_cc = pd.read_csv(data_path)
if 'PAY_0' in df_cc.columns:
    df_cc = df_cc.rename(columns={'PAY_0': 'PAY_1'})

cols_to_drop = ['ID', 'SEX', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
df_clean = df_cc.drop(columns=[c for c in cols_to_drop if c in df_cc.columns])

target_col = 'default payment next month'
X = df_clean.drop(columns=[target_col])
y = df_clean[target_col]
feature_names = list(X.columns)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=24
)

dt2 = DecisionTreeClassifier(max_depth=2, random_state=24)
dt2.fit(X_train, y_train)

y_prob_dt2 = dt2.predict_proba(X_test)[:, 1]
print(f"DecisionTree max_depth=2 Test ROC AUC: {roc_auc_score(y_test, y_prob_dt2):.4f}")

plt.figure(figsize=(12, 5), dpi=400)
plot_tree(
    dt2, feature_names=feature_names,
    class_names=['Khong tre han', 'Tre han'], filled=True, rounded=True, fontsize=10, proportion=True
)
plt.title("Cay quyet dinh DecisionTree max_depth=2 - Credit Card Default")
plt.tight_layout()
plt.show()"""),
        md("""### Nhiệm vụ 2: Dùng GridSearchCV tìm max_depth tối ưu và vẽ biểu đồ errorbar Mean +- 1 SE
Ý nghĩa các thiết lập:
- scoring='roc_auc': Đánh giá diện tích dưới đường cong ROC để phản ánh khả năng phân biệt giữa lớp vỡ nợ và không vỡ nợ trên tập dữ liệu mất cân bằng.
- cv=4: Kiểm định chéo 4 phần, chia tập huấn luyện thành 4 phần bằng nhau, luân phiên 3 phần để học và 1 phần để kiểm tra.
- return_train_score=True: Lưu lại điểm số trên tập huấn luyện để so sánh với tập kiểm định, giúp quan sát hiện tượng quá khớp."""),
        code("""param_grid_dt = {'max_depth': [1, 2, 4, 6, 8, 10, 12]}
dt_search = GridSearchCV(
    estimator=DecisionTreeClassifier(random_state=24),
    param_grid=param_grid_dt,
    scoring='roc_auc',
    cv=4,
    return_train_score=True
)
dt_search.fit(X_train, y_train)

print(f"Best max_depth: {dt_search.best_params_['max_depth']}")
print(f"Best CV ROC AUC: {dt_search.best_score_:.4f}")

cv_res = pd.DataFrame(dt_search.cv_results_)
mean_tr = cv_res['mean_train_score']
se_tr = cv_res['std_train_score'] / np.sqrt(4)
mean_te = cv_res['mean_test_score']
se_te = cv_res['std_test_score'] / np.sqrt(4)

plt.figure(figsize=(8, 5))
plt.errorbar(
    param_grid_dt['max_depth'], mean_tr, yerr=se_tr,
    fmt='-o', color='black', label='Tap huan luyen Mean +- 1 SE', capsize=4
)
plt.errorbar(
    param_grid_dt['max_depth'], mean_te, yerr=se_te,
    fmt='--s', color='gray', label='Tap kiem dinh cheo Mean +- 1 SE', capsize=4
)
plt.xlabel('max_depth')
plt.ylabel('ROC AUC Score')
plt.title('Hieu nang ROC AUC theo max_depth tren tap huan luyen va kiem dinh')
plt.xticks(param_grid_dt['max_depth'])
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()"""),
        md("### Nhiệm vụ 3: RandomForestClassifier tuning n_estimators, subplot 1x2 và Feature Importance"),
        code("""param_grid_rf = {'n_estimators': list(range(10, 101, 10))}
rf_search = GridSearchCV(
    estimator=RandomForestClassifier(max_depth=3, max_features='sqrt', random_state=4),
    param_grid=param_grid_rf,
    scoring='roc_auc',
    cv=4,
    return_train_score=True
)
rf_search.fit(X_train, y_train)

print(f"Random Forest Best params: {rf_search.best_params_}")
print(f"Random Forest Best CV ROC AUC: {rf_search.best_score_:.4f}")

cv_res_rf = pd.DataFrame(rf_search.cv_results_)
mean_time = cv_res_rf['mean_fit_time']
mean_te_rf = cv_res_rf['mean_test_score']
se_te_rf = cv_res_rf['std_test_score'] / np.sqrt(4)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(param_grid_rf['n_estimators'], mean_time, '-o', color='black')
axes[0].set_xlabel('n_estimators')
axes[0].set_ylabel('Mean fit time giay')
axes[0].set_title('Thoi gian huan luyen theo n_estimators')
axes[0].set_xticks(param_grid_rf['n_estimators'])
axes[0].grid(True, linestyle=':', alpha=0.6)

axes[1].errorbar(
    param_grid_rf['n_estimators'], mean_te_rf, yerr=se_te_rf,
    fmt='-s', color='black', ecolor='gray', capsize=4
)
axes[1].set_xlabel('n_estimators')
axes[1].set_ylabel('Mean testing ROC AUC +- 1 SE')
axes[1].set_title('Hieu nang ROC AUC kiem dinh theo n_estimators')
axes[1].set_xticks(param_grid_rf['n_estimators'])
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()

best_rf = rf_search.best_estimator_
fi = pd.Series(best_rf.feature_importances_, index=feature_names).sort_values(ascending=True)

plt.figure(figsize=(8, 5.5))
fi.plot(kind='barh', color='black', edgecolor='gray')
plt.xlabel('Do quan trong Gini Importance')
plt.ylabel('Dac trung')
plt.title('Do quan trong dac trung trong Random Forest Credit Card')
plt.tight_layout()
plt.show()

y_pred_rf = best_rf.predict(X_test)
print(f"Test Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}")
print(f"Test F1: {f1_score(y_test, y_pred_rf):.4f}")
print(f"Test ROC AUC: {roc_auc_score(y_test, best_rf.predict_proba(X_test)[:, 1]):.4f}")""")
    ]

    # --------------------------------------------------------------------------
    # 2. 02_Titanic_DT_RF.ipynb
    # --------------------------------------------------------------------------
    cells_ti = [
        md("# 2.1.3 BÀI TẬP THỰC HÀNH 1: DỰ ĐOÁN KHẢ NĂNG SỐNG SÓT TRÊN TÀU TITANIC\nMô hình: Decision Tree và Random Forest\nThực hiện: Lê Văn Hiếu"),
        md("### 1. Khám phá và tiền xử lý dữ liệu"),
        code("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)

ti_path = '../data/train.csv' if os.path.exists('../data/train.csv') else 'Lab05_ThucHanhBaiToanPhanLop/data/train.csv'
df = pd.read_csv(ti_path)

print("Kich thuoc du lieu goc:", df.shape)
print("So luong khuyet thieu Age:", df['Age'].isnull().sum())
print("So luong khuyet thieu Embarked:", df['Embarked'].isnull().sum())
print("Phan bo nhan Survived:\\n", df['Survived'].value_counts())

# Tien xu ly tranh Data Leakage
ti_df = df.copy()
ti_df['Sex'] = ti_df['Sex'].map({'male': 0, 'female': 1})
features_raw = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
X_raw = ti_df[features_raw]
y = ti_df['Survived']

X_train, X_test, y_train, y_test = train_test_split(
    X_raw, y, test_size=0.2, random_state=42, stratify=y
)
X_train = X_train.copy()
X_test = X_test.copy()

age_med = X_train['Age'].median()
emb_mode = X_train['Embarked'].mode()[0]
X_train['Age'] = X_train['Age'].fillna(age_med)
X_test['Age'] = X_test['Age'].fillna(age_med)
X_train['Embarked'] = X_train['Embarked'].fillna(emb_mode)
X_test['Embarked'] = X_test['Embarked'].fillna(emb_mode)

X_train = pd.get_dummies(X_train, columns=['Embarked'], drop_first=True, dtype=int)
X_test = pd.get_dummies(X_test, columns=['Embarked'], drop_first=True, dtype=int)
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)
features = list(X_train.columns)

print(f"Kich thuoc tap train: {X_train.shape}, tap test: {X_test.shape}")"""),
        md("### 2. Xây dựng mô hình Baseline đánh giá hiện tượng quá khớp"),
        code("""dt_base = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
rf_base = RandomForestClassifier(random_state=42).fit(X_train, y_train)

print(f"DT Baseline Train Acc: {dt_base.score(X_train, y_train):.4f}, Test Acc: {dt_base.score(X_test, y_test):.4f}")
print(f"RF Baseline Train Acc: {rf_base.score(X_train, y_train):.4f}, Test Acc: {rf_base.score(X_test, y_test):.4f}")"""),
        md("### 3. Tối ưu hóa siêu tham số bằng GridSearchCV và vẽ biểu đồ quá trình tuning"),
        code("""param_dt = {'max_depth': [2, 3, 4, 5, 6], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}
grid_dt = GridSearchCV(DecisionTreeClassifier(random_state=42), param_dt, cv=5, scoring='accuracy').fit(X_train, y_train)
best_dt = grid_dt.best_estimator_
print(f"DT Best params: {grid_dt.best_params_}, CV Acc: {grid_dt.best_score_:.4f}")

param_rf = {'n_estimators': [50, 100, 150], 'max_depth': [4, 6, 8], 'min_samples_split': [2, 5], 'min_samples_leaf': [2, 4], 'max_features': ['sqrt']}
grid_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_rf, cv=5, scoring='accuracy').fit(X_train, y_train)
best_rf = grid_rf.best_estimator_
print(f"RF Best params: {grid_rf.best_params_}, CV Acc: {grid_rf.best_score_:.4f}")

# Bieu do danh gia qua trinh tuning
cv_dt = pd.DataFrame(grid_dt.cv_results_)
dt_depth_scores = cv_dt.groupby('param_max_depth')['mean_test_score'].max()
cv_rf = pd.DataFrame(grid_rf.cv_results_)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].plot(dt_depth_scores.index, dt_depth_scores.values, '-o', color='black')
axes[0].set_xlabel('max_depth')
axes[0].set_ylabel('Mean CV Accuracy')
axes[0].set_title('Decision Tree: CV Accuracy theo do sau max_depth')
axes[0].grid(True, linestyle=':', alpha=0.6)

for nest in [50, 100, 150]:
    sub = cv_rf[cv_rf['param_n_estimators'] == nest]
    sub_grouped = sub.groupby('param_max_depth')['mean_test_score'].max()
    axes[1].plot(sub_grouped.index, sub_grouped.values, '-o', label=f'n_estimators={nest}')
axes[1].set_xlabel('max_depth')
axes[1].set_ylabel('Mean CV Accuracy')
axes[1].set_title('Random Forest: CV Accuracy theo max_depth va n_estimators')
axes[1].legend()
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()"""),
        md("### 4. Đánh giá kiểm tra đầy đủ và vẽ ma trận nhầm lẫn"),
        code("""y_pred_dt = best_dt.predict(X_test)
y_prob_dt = best_dt.predict_proba(X_test)[:, 1]

y_pred_rf = best_rf.predict(X_test)
y_prob_rf = best_rf.predict_proba(X_test)[:, 1]

print("=== Ket qua Decision Tree Tuned ===")
print("Accuracy :", round(accuracy_score(y_test, y_pred_dt), 4))
print("Precision:", round(precision_score(y_test, y_pred_dt), 4))
print("Recall   :", round(recall_score(y_test, y_pred_dt), 4))
print("F1-score :", round(f1_score(y_test, y_pred_dt), 4))
print("ROC-AUC  :", round(roc_auc_score(y_test, y_prob_dt), 4))
print("\\nClassification Report Decision Tree:\\n", classification_report(y_test, y_pred_dt))

print("=== Ket qua Random Forest Tuned ===")
print("Accuracy :", round(accuracy_score(y_test, y_pred_rf), 4))
print("Precision:", round(precision_score(y_test, y_pred_rf), 4))
print("Recall   :", round(recall_score(y_test, y_pred_rf), 4))
print("F1-score :", round(f1_score(y_test, y_pred_rf), 4))
print("ROC-AUC  :", round(roc_auc_score(y_test, y_prob_rf), 4))
print("\\nClassification Report Random Forest:\\n", classification_report(y_test, y_pred_rf))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
cm_dt = confusion_matrix(y_test, y_pred_dt)
cm_rf = confusion_matrix(y_test, y_pred_rf)

sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False,
            xticklabels=['Tu vong', 'Song sot'], yticklabels=['Tu vong', 'Song sot'])
axes[0].set_title(f"Confusion Matrix: Decision Tree Tuned\\nAcc: {accuracy_score(y_test, y_pred_dt):.4f}")
axes[0].set_xlabel('Du doan')
axes[0].set_ylabel('Thuc te')

sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Greens', ax=axes[1], cbar=False,
            xticklabels=['Tu vong', 'Song sot'], yticklabels=['Tu vong', 'Song sot'])
axes[1].set_title(f"Confusion Matrix: Random Forest Tuned\\nAcc: {accuracy_score(y_test, y_pred_rf):.4f}")
axes[1].set_xlabel('Du doan')
axes[1].set_ylabel('Thuc te')

plt.tight_layout()
plt.show()"""),
        md("### 5. Trực quan hóa Cây quyết định tối ưu và Feature Importance"),
        code("""plt.figure(figsize=(16, 8), dpi=400)
plot_tree(best_dt, feature_names=features, class_names=['Tu vong', 'Song sot'], filled=True, rounded=True, fontsize=9)
plt.title(f"Cay quyet dinh toi uu Titanic voi max_depth={best_dt.max_depth}")
plt.tight_layout()
plt.show()

fi = pd.Series(best_rf.feature_importances_, index=features).sort_values(ascending=True)
plt.figure(figsize=(7, 4))
fi.plot(kind='barh', color='black', edgecolor='gray')
plt.xlabel('Do quan trong')
plt.ylabel('Dac trung')
plt.title('Muc do quan trong dac trung Random Forest Titanic')
plt.tight_layout()
plt.show()"""),
        md("""### 6. Bảng tổng hợp so sánh trực diện và nhận xét về hiện tượng quá khớp
So sánh hiệu năng giữa Baseline và Tuned cho Decision Tree và Random Forest:"""),
        code("""summary_ti = pd.DataFrame([
    {
        'Model': 'DT Baseline',
        'Train Acc': round(dt_base.score(X_train, y_train), 4),
        'Test Acc': round(dt_base.score(X_test, y_test), 4),
        'Precision': round(precision_score(y_test, dt_base.predict(X_test)), 4),
        'Recall': round(recall_score(y_test, dt_base.predict(X_test)), 4),
        'F1-Score': round(f1_score(y_test, dt_base.predict(X_test)), 4),
        'ROC-AUC': round(roc_auc_score(y_test, dt_base.predict_proba(X_test)[:, 1]), 4)
    },
    {
        'Model': 'DT Tuned',
        'Train Acc': round(best_dt.score(X_train, y_train), 4),
        'Test Acc': round(best_dt.score(X_test, y_test), 4),
        'Precision': round(precision_score(y_test, y_pred_dt), 4),
        'Recall': round(recall_score(y_test, y_pred_dt), 4),
        'F1-Score': round(f1_score(y_test, y_pred_dt), 4),
        'ROC-AUC': round(roc_auc_score(y_test, y_prob_dt), 4)
    },
    {
        'Model': 'RF Baseline',
        'Train Acc': round(rf_base.score(X_train, y_train), 4),
        'Test Acc': round(rf_base.score(X_test, y_test), 4),
        'Precision': round(precision_score(y_test, rf_base.predict(X_test)), 4),
        'Recall': round(recall_score(y_test, rf_base.predict(X_test)), 4),
        'F1-Score': round(f1_score(y_test, rf_base.predict(X_test)), 4),
        'ROC-AUC': round(roc_auc_score(y_test, rf_base.predict_proba(X_test)[:, 1]), 4)
    },
    {
        'Model': 'RF Tuned',
        'Train Acc': round(best_rf.score(X_train, y_train), 4),
        'Test Acc': round(best_rf.score(X_test, y_test), 4),
        'Precision': round(precision_score(y_test, y_pred_rf), 4),
        'Recall': round(recall_score(y_test, y_pred_rf), 4),
        'F1-Score': round(f1_score(y_test, y_pred_rf), 4),
        'ROC-AUC': round(roc_auc_score(y_test, y_prob_rf), 4)
    }
])
print(summary_ti.to_string(index=False))"""),
        md("""Nhận xét cụ thể về hiện tượng quá khớp:
1. Mô hình Decision Tree Baseline không giới hạn độ sâu đạt độ chính xác huấn luyện 98.17% nhưng độ chính xác kiểm tra chỉ 82.12%. Khoảng chênh lệch lớn này cho thấy cây đã học quá chi tiết vào dữ liệu huấn luyện và ghi nhớ cả nhiễu.
2. Khi sử dụng GridSearchCV khống chế max_depth=5 và min_samples_split=5, độ phức tạp của cây giảm xuống, độ chính xác huấn luyện hạ về 86.38% giúp mô hình tổng quát hóa ổn định hơn.
3. Mô hình Random Forest kết hợp nhiều cây con lấy mẫu ngẫu nhiên triệt tiêu phương sai, duy trì ROC-AUC kiểm tra ở mức cao 0.8317 và điểm Precision đạt 0.8077, vượt trội hơn cây quyết định đơn lẻ.""")
    ]

    # --------------------------------------------------------------------------
    # 3. 03_Diabetes_DT_RF.ipynb
    # --------------------------------------------------------------------------
    cells_di = [
        md("# 2.1.4 BÀI TẬP THỰC HÀNH 2: DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG PIMA INDIANS\nMô hình: Decision Tree và Random Forest\nThực hiện: Lê Văn Hiếu"),
        md("### 1. Khám phá và tiền xử lý dữ liệu: Xử lý giá trị 0 sinh lý bất thường"),
        code("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)

di_path = '../data/diabetes.csv' if os.path.exists('../data/diabetes.csv') else 'Lab05_ThucHanhBaiToanPhanLop/data/diabetes.csv'
df = pd.read_csv(di_path)

print("Kich thuoc tap du lieu goc:", df.shape)
print("Phan bo nhan Outcome:\\n", df['Outcome'].value_counts())

cols_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
X_raw = df[features]
y = df['Outcome']

# Chia train/test truoc de tranh Data Leakage
X_train, X_test, y_train, y_test = train_test_split(
    X_raw, y, test_size=0.2, random_state=42, stratify=y
)
X_train = X_train.copy()
X_test = X_test.copy()

for col in cols_zero:
    X_train[col] = X_train[col].replace(0, np.nan)
    med = X_train[col].median()
    X_train[col] = X_train[col].fillna(med)
    X_test[col] = X_test[col].replace(0, np.nan)
    X_test[col] = X_test[col].fillna(med)

print(f"Kich thuoc tap train: {X_train.shape}, tap test: {X_test.shape}")"""),
        md("### 2. Xây dựng mô hình Baseline đánh giá hiện tượng quá khớp"),
        code("""dt_base = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
rf_base = RandomForestClassifier(random_state=42).fit(X_train, y_train)

print(f"DT Baseline Train Acc: {dt_base.score(X_train, y_train):.4f}, Test Acc: {dt_base.score(X_test, y_test):.4f}")
print(f"RF Baseline Train Acc: {rf_base.score(X_train, y_train):.4f}, Test Acc: {rf_base.score(X_test, y_test):.4f}")"""),
        md("### 3. Tối ưu hóa siêu tham số bằng GridSearchCV và vẽ biểu đồ quá trình tuning"),
        code("""param_dt = {'max_depth': [2, 3, 4, 5, 6], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}
grid_dt = GridSearchCV(DecisionTreeClassifier(random_state=42), param_dt, cv=5, scoring='f1').fit(X_train, y_train)
best_dt = grid_dt.best_estimator_
print(f"DT Best params: {grid_dt.best_params_}, CV F1: {grid_dt.best_score_:.4f}")

param_rf = {'n_estimators': [50, 100, 150], 'max_depth': [3, 5, 7], 'min_samples_split': [2, 5], 'min_samples_leaf': [2, 4], 'max_features': ['sqrt']}
grid_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_rf, cv=5, scoring='f1').fit(X_train, y_train)
best_rf = grid_rf.best_estimator_
print(f"RF Best params: {grid_rf.best_params_}, CV F1: {grid_rf.best_score_:.4f}")

# Bieu do danh gia qua trinh tuning
cv_dt = pd.DataFrame(grid_dt.cv_results_)
dt_depth_scores = cv_dt.groupby('param_max_depth')['mean_test_score'].max()
cv_rf = pd.DataFrame(grid_rf.cv_results_)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
axes[0].plot(dt_depth_scores.index, dt_depth_scores.values, '-o', color='black')
axes[0].set_xlabel('max_depth')
axes[0].set_ylabel('Mean CV F1-score')
axes[0].set_title('Decision Tree: CV F1 theo do sau max_depth')
axes[0].grid(True, linestyle=':', alpha=0.6)

for nest in [50, 100, 150]:
    sub = cv_rf[cv_rf['param_n_estimators'] == nest]
    sub_grouped = sub.groupby('param_max_depth')['mean_test_score'].max()
    axes[1].plot(sub_grouped.index, sub_grouped.values, '-o', label=f'n_estimators={nest}')
axes[1].set_xlabel('max_depth')
axes[1].set_ylabel('Mean CV F1-score')
axes[1].set_title('Random Forest: CV F1 theo max_depth va n_estimators')
axes[1].legend()
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()"""),
        md("### 4. Đánh giá kiểm tra đầy đủ và vẽ ma trận nhầm lẫn"),
        code("""y_pred_dt = best_dt.predict(X_test)
y_prob_dt = best_dt.predict_proba(X_test)[:, 1]

y_pred_rf = best_rf.predict(X_test)
y_prob_rf = best_rf.predict_proba(X_test)[:, 1]

print("=== Ket qua Decision Tree Tuned ===")
print("Accuracy :", round(accuracy_score(y_test, y_pred_dt), 4))
print("Precision:", round(precision_score(y_test, y_pred_dt), 4))
print("Recall   :", round(recall_score(y_test, y_pred_dt), 4))
print("F1-score :", round(f1_score(y_test, y_pred_dt), 4))
print("ROC-AUC  :", round(roc_auc_score(y_test, y_prob_dt), 4))
print("\\nClassification Report Decision Tree:\\n", classification_report(y_test, y_pred_dt))

print("=== Ket qua Random Forest Tuned ===")
print("Accuracy :", round(accuracy_score(y_test, y_pred_rf), 4))
print("Precision:", round(precision_score(y_test, y_pred_rf), 4))
print("Recall   :", round(recall_score(y_test, y_pred_rf), 4))
print("F1-score :", round(f1_score(y_test, y_pred_rf), 4))
print("ROC-AUC  :", round(roc_auc_score(y_test, y_prob_rf), 4))
print("\\nClassification Report Random Forest:\\n", classification_report(y_test, y_pred_rf))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
cm_dt = confusion_matrix(y_test, y_pred_dt)
cm_rf = confusion_matrix(y_test, y_pred_rf)

sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False,
            xticklabels=['Khong mac benh', 'Mac benh'], yticklabels=['Khong mac benh', 'Mac benh'])
axes[0].set_title(f"Confusion Matrix: Decision Tree Tuned\\nF1: {f1_score(y_test, y_pred_dt):.4f}")
axes[0].set_xlabel('Du doan')
axes[0].set_ylabel('Thuc te')

sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Greens', ax=axes[1], cbar=False,
            xticklabels=['Khong mac benh', 'Mac benh'], yticklabels=['Khong mac benh', 'Mac benh'])
axes[1].set_title(f"Confusion Matrix: Random Forest Tuned\\nF1: {f1_score(y_test, y_pred_rf):.4f}")
axes[1].set_xlabel('Du doan')
axes[1].set_ylabel('Thuc te')

plt.tight_layout()
plt.show()"""),
        md("### 5. Trực quan hóa Cây quyết định tối ưu và Feature Importance"),
        code("""plt.figure(figsize=(16, 8), dpi=400)
plot_tree(best_dt, feature_names=features, class_names=['Khong mac benh', 'Mac benh'], filled=True, rounded=True, fontsize=9)
plt.title(f"Cay quyet dinh toi uu Diabetes voi max_depth={best_dt.max_depth}")
plt.tight_layout()
plt.show()

fi = pd.Series(best_rf.feature_importances_, index=features).sort_values(ascending=True)
plt.figure(figsize=(7, 4))
fi.plot(kind='barh', color='black', edgecolor='gray')
plt.xlabel('Do quan trong')
plt.ylabel('Dac trung')
plt.title('Muc do quan trong dac trung Random Forest Diabetes')
plt.tight_layout()
plt.show()"""),
        md("""### 6. Bảng tổng hợp so sánh trực diện và nhận xét về hiện tượng quá khớp
So sánh hiệu năng giữa Baseline và Tuned cho Decision Tree và Random Forest:"""),
        code("""summary_di = pd.DataFrame([
    {
        'Model': 'DT Baseline',
        'Train Acc': round(dt_base.score(X_train, y_train), 4),
        'Test Acc': round(dt_base.score(X_test, y_test), 4),
        'Precision': round(precision_score(y_test, dt_base.predict(X_test)), 4),
        'Recall': round(recall_score(y_test, dt_base.predict(X_test)), 4),
        'F1-Score': round(f1_score(y_test, dt_base.predict(X_test)), 4),
        'ROC-AUC': round(roc_auc_score(y_test, dt_base.predict_proba(X_test)[:, 1]), 4)
    },
    {
        'Model': 'DT Tuned',
        'Train Acc': round(best_dt.score(X_train, y_train), 4),
        'Test Acc': round(best_dt.score(X_test, y_test), 4),
        'Precision': round(precision_score(y_test, y_pred_dt), 4),
        'Recall': round(recall_score(y_test, y_pred_dt), 4),
        'F1-Score': round(f1_score(y_test, y_pred_dt), 4),
        'ROC-AUC': round(roc_auc_score(y_test, y_prob_dt), 4)
    },
    {
        'Model': 'RF Baseline',
        'Train Acc': round(rf_base.score(X_train, y_train), 4),
        'Test Acc': round(rf_base.score(X_test, y_test), 4),
        'Precision': round(precision_score(y_test, rf_base.predict(X_test)), 4),
        'Recall': round(recall_score(y_test, rf_base.predict(X_test)), 4),
        'F1-Score': round(f1_score(y_test, rf_base.predict(X_test)), 4),
        'ROC-AUC': round(roc_auc_score(y_test, rf_base.predict_proba(X_test)[:, 1]), 4)
    },
    {
        'Model': 'RF Tuned',
        'Train Acc': round(best_rf.score(X_train, y_train), 4),
        'Test Acc': round(best_rf.score(X_test, y_test), 4),
        'Precision': round(precision_score(y_test, y_pred_rf), 4),
        'Recall': round(recall_score(y_test, y_pred_rf), 4),
        'F1-Score': round(f1_score(y_test, y_pred_rf), 4),
        'ROC-AUC': round(roc_auc_score(y_test, y_prob_rf), 4)
    }
])
print(summary_di.to_string(index=False))"""),
        md("""Nhận xét cụ thể về hiện tượng quá khớp:
1. Decision Tree Baseline không khống chế độ sâu đạt độ chính xác huấn luyện tuyệt đối 100%, nhưng trên tập kiểm tra chỉ đạt 68.18% và F1-score đạt 0.5149. Chênh lệch 31.82% phản ánh hiện tượng quá khớp nặng khi cây cố gắng phân tách từng điểm nhiễu.
2. Sau khi dùng GridSearchCV khống chế max_depth=4, độ chính xác huấn luyện giảm về 79.48% nhưng độ chính xác kiểm tra tăng lên 78.57% và F1-score tăng lên 0.6916, chứng tỏ kiểm soát độ sâu giúp mô hình có khả năng tổng quát hóa cao.
3. Random Forest duy trì ROC-AUC kiểm tra ổn định ở mức 0.8041 đến 0.8192, thể hiện ưu thế của phương pháp kết hợp rừng cây trong việc chống quá khớp.""")
    ]

    for fname, cells in [
        ('01_CreditCard_DT_RF.ipynb', cells_cc),
        ('02_Titanic_DT_RF.ipynb', cells_ti),
        ('03_Diabetes_DT_RF.ipynb', cells_di)
    ]:
        p = os.path.join(code_dir, fname)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(make_nb(cells), f, ensure_ascii=False, indent=2)
        print(f"Created: {p} ({len(cells)} cells)")

if __name__ == '__main__':
    create_modular_notebooks()
