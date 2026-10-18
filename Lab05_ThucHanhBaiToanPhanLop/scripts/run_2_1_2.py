import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, classification_report, confusion_matrix

sys.stdout.reconfigure(encoding='utf-8')
figures_dir = 'Lab05_ThucHanhBaiToanPhanLop/figures'
os.makedirs(figures_dir, exist_ok=True)

# -------------------------------------------------------------
# NHIỆM VỤ 1: Nạp dữ liệu, tiền xử lý, huấn luyện DT max_depth=2
# -------------------------------------------------------------
print("=== NHIỆM VỤ 1 ===")
df = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/default_of_credit_card_clients.csv')
print(f"Du lieu goc: {df.shape}")

# Chuan hoa ten cot PAY_0 thanh PAY_1 neu co
if 'PAY_0' in df.columns:
    df = df.rename(columns={'PAY_0': 'PAY_1'})

# Loai bo cac cot khong lien quan
cols_to_drop = ['ID', 'SEX', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
df_clean = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

# Xu ly bien muc tieu
target_col = 'default payment next month'
X = df_clean.drop(columns=[target_col])
y = df_clean[target_col]
feature_names = list(X.columns)
print(f"Tap dac trung ({len(feature_names)}): {feature_names}")

# Chia train/test voi test_size=0.2, random_state=24
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=24
)
print(f"X_train: {X_train.shape}, X_test: {X_test.shape}")

# Huan luyen DecisionTreeClassifier(max_depth=2)
dt2 = DecisionTreeClassifier(max_depth=2, random_state=24)
dt2.fit(X_train, y_train)

# Tinh ROC AUC tren test
y_pred_proba_dt2 = dt2.predict_proba(X_test)[:, 1]
auc_dt2 = roc_auc_score(y_test, y_pred_proba_dt2)
print(f"DecisionTree (max_depth=2) Test ROC AUC: {auc_dt2:.4f}")

# Xuat do thi cay quyet dinh (graphviz va fallback plot_tree voi dpi=400)
dt2_fig_path = os.path.join(figures_dir, '2_1_2_decision_tree_depth2.png')
try:
    import graphviz
    dot_data = export_graphviz(
        dt2,
        out_file=None,
        feature_names=feature_names,
        class_names=['Khong tre han', 'Tre han'],
        filled=True,
        rounded=True,
        special_characters=True,
        proportion=True
    )
    src = graphviz.Source(dot_data)
    src.render(os.path.join(figures_dir, '2_1_2_decision_tree_depth2'), format='png', cleanup=True)
    print("Xuat do thi cay bang graphviz thanh cong.")
except Exception as e:
    print(f"Graphviz fallback: {e}")
    plt.figure(figsize=(12, 6), dpi=400)
    plot_tree(
        dt2,
        feature_names=feature_names,
        class_names=['Khong tre han', 'Tre han'],
        filled=True,
        rounded=True,
        fontsize=10,
        proportion=True
    )
    plt.title("Cay quyet dinh DecisionTree (max_depth=2) - Credit Card Default")
    plt.tight_layout()
    plt.savefig(dt2_fig_path, dpi=400, bbox_inches='tight')
    plt.close()
    print("Xuat do thi cay bang plot_tree dpi=400 thanh cong.")

# -------------------------------------------------------------
# NHIỆM VỤ 2: GridSearchCV tim max_depth trong [1, 2, 4, 6, 8, 10, 12]
# -------------------------------------------------------------
print("\n=== NHIỆM VỤ 2 ===")
param_grid_dt = {'max_depth': [1, 2, 4, 6, 8, 10, 12]}
dt_grid = DecisionTreeClassifier(random_state=24)
grid_cv_dt = GridSearchCV(
    estimator=dt_grid,
    param_grid=param_grid_dt,
    scoring='roc_auc',
    cv=4,
    return_train_score=True
)
grid_cv_dt.fit(X_train, y_train)

best_depth = grid_cv_dt.best_params_['max_depth']
print(f"Best max_depth: {best_depth}, Best ROC AUC CV: {grid_cv_dt.best_score_:.4f}")

cv_res_dt = pd.DataFrame(grid_cv_dt.cv_results_)
mean_train = cv_res_dt['mean_train_score']
std_train = cv_res_dt['std_train_score']
se_train = std_train / np.sqrt(4)

mean_test = cv_res_dt['mean_test_score']
std_test = cv_res_dt['std_test_score']
se_test = std_test / np.sqrt(4)

# Bieu do errorbar so sanh Mean +- 1 SE train va test
plt.figure(figsize=(8, 5))
plt.errorbar(
    param_grid_dt['max_depth'], mean_train, yerr=se_train,
    fmt='-o', color='black', label='Tap huan luyen (Mean +- 1 SE)', capsize=4
)
plt.errorbar(
    param_grid_dt['max_depth'], mean_test, yerr=se_test,
    fmt='--s', color='gray', label='Tap kiem dinh chéo (Mean +- 1 SE)', capsize=4
)
plt.xlabel('max_depth')
plt.ylabel('ROC AUC Score')
plt.title('Hieu nang ROC AUC theo max_depth tren tap huan luyen va kiem dinh')
plt.xticks(param_grid_dt['max_depth'])
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()
dt_errorbar_path = os.path.join(figures_dir, '2_1_2_dt_max_depth_errorbar.png')
plt.savefig(dt_errorbar_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Da luu bieu do errorbar: {dt_errorbar_path}")

# -------------------------------------------------------------
# NHIỆM VỤ 3: RandomForestClassifier(max_depth=3, max_features='sqrt')
# -------------------------------------------------------------
print("\n=== NHIỆM VỤ 3 ===")
param_grid_rf = {'n_estimators': list(range(10, 101, 10))}
rf_base = RandomForestClassifier(max_depth=3, max_features='sqrt', random_state=4)
grid_cv_rf = GridSearchCV(
    estimator=rf_base,
    param_grid=param_grid_rf,
    scoring='roc_auc',
    cv=4,
    return_train_score=True
)
grid_cv_rf.fit(X_train, y_train)

best_n_estimators = grid_cv_rf.best_params_['n_estimators']
print(f"Random Forest Best params: {grid_cv_rf.best_params_}")
print(f"Random Forest Best CV ROC AUC: {grid_cv_rf.best_score_:.4f}")

cv_res_rf = pd.DataFrame(grid_cv_rf.cv_results_)
mean_fit_time = cv_res_rf['mean_fit_time']
mean_test_rf = cv_res_rf['mean_test_score']
std_test_rf = cv_res_rf['std_test_score']
se_test_rf = std_test_rf / np.sqrt(4)

# Subplot 1x2
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(param_grid_rf['n_estimators'], mean_fit_time, '-o', color='black')
axes[0].set_xlabel('n_estimators')
axes[0].set_ylabel('Mean fit time (giay)')
axes[0].set_title('Thoi gian huan luyen theo n_estimators')
axes[0].set_xticks(param_grid_rf['n_estimators'])
axes[0].grid(True, linestyle=':', alpha=0.6)

axes[1].errorbar(
    param_grid_rf['n_estimators'], mean_test_rf, yerr=se_test_rf,
    fmt='-s', color='black', ecolor='gray', capsize=4
)
axes[1].set_xlabel('n_estimators')
axes[1].set_ylabel('Mean testing ROC AUC +- 1 SE')
axes[1].set_title('Hieu nang ROC AUC kiem dinh theo n_estimators')
axes[1].set_xticks(param_grid_rf['n_estimators'])
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
rf_tuning_path = os.path.join(figures_dir, '2_1_2_rf_n_estimators_tuning.png')
plt.savefig(rf_tuning_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Da luu bieu do RF tuning: {rf_tuning_path}")

# Feature Importance barh
best_rf = grid_cv_rf.best_estimator_
importances = pd.Series(best_rf.feature_importances_, index=feature_names).sort_values(ascending=True)

print("\nDo quan trong dac trung (Top giam dan):")
print((importances.sort_values(ascending=False) * 100).round(2).to_string())

plt.figure(figsize=(9, 6))
importances.plot(kind='barh', color='black', edgecolor='gray')
plt.xlabel('Do quan trong (Gini Importance)')
plt.ylabel('Dac trung')
plt.title('Do quan trong cua cac dac trung trong Random Forest (Credit Card)')
plt.tight_layout()
rf_fi_path = os.path.join(figures_dir, '2_1_2_rf_feature_importance.png')
plt.savefig(rf_fi_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Da luu bieu do Feature Importance: {rf_fi_path}")

# Danh gia tren tap test cuoi cung
y_pred_rf = best_rf.predict(X_test)
y_pred_proba_rf = best_rf.predict_proba(X_test)[:, 1]
test_acc_rf = accuracy_score(y_test, y_pred_rf)
test_f1_rf = f1_score(y_test, y_pred_rf)
test_auc_rf = roc_auc_score(y_test, y_pred_proba_rf)
print(f"Random Forest Best Test Accuracy: {test_acc_rf:.4f}")
print(f"Random Forest Best Test F1: {test_f1_rf:.4f}")
print(f"Random Forest Best Test ROC AUC: {test_auc_rf:.4f}")
