import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    classification_report, confusion_matrix
)

def evaluate_model(model, X_train, y_train, X_test, y_test, name=""):
    y_tr_pred = model.predict(X_train)
    y_te_pred = model.predict(X_test)
    y_te_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    acc_tr = accuracy_score(y_train, y_tr_pred)
    acc_te = accuracy_score(y_test, y_te_pred)
    prec_te = precision_score(y_test, y_te_pred, zero_division=0)
    rec_te = recall_score(y_test, y_te_pred, zero_division=0)
    f1_te = f1_score(y_test, y_te_pred, zero_division=0)
    auc_te = roc_auc_score(y_test, y_te_prob) if y_te_prob is not None else 0.0
    
    print(f"\n--- {name} ---", flush=True)
    print(f"Train Accuracy: {acc_tr:.4f}", flush=True)
    print(f"Test Accuracy : {acc_te:.4f}", flush=True)
    print(f"Precision     : {prec_te:.4f}", flush=True)
    print(f"Recall        : {rec_te:.4f}", flush=True)
    print(f"F1-score      : {f1_te:.4f}", flush=True)
    print(f"ROC-AUC       : {auc_te:.4f}", flush=True)
    return {
        'Model': name,
        'Train Acc': acc_tr,
        'Test Acc': acc_te,
        'Precision': prec_te,
        'Recall': rec_te,
        'F1-Score': f1_te,
        'ROC-AUC': auc_te
    }

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    figures_dir = 'Lab05_ThucHanhBaiToanPhanLop/figures'
    os.makedirs(figures_dir, exist_ok=True)

    # ==============================================================================
    # 2.1.3: BÀI TẬP THỰC HÀNH 1 - TITANIC DATASET
    # ==============================================================================
    print("================== 2.1.3 TITANIC ==================", flush=True)
    titanic_raw = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/train.csv')
    print(f"Kich thuoc Titanic goc: {titanic_raw.shape}", flush=True)

    # Tien xu ly khong ro ri du lieu (Data Leakage Free)
    titanic_df = titanic_raw.copy()
    titanic_df['Sex'] = titanic_df['Sex'].map({'male': 0, 'female': 1})
    features_raw_ti = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    X_raw_ti = titanic_df[features_raw_ti]
    y_ti = titanic_df['Survived']

    # Chia tap train/test truoc khi impute
    X_ti_train, X_ti_test, y_ti_train, y_ti_test = train_test_split(
        X_raw_ti, y_ti, test_size=0.2, random_state=42, stratify=y_ti
    )
    X_ti_train = X_ti_train.copy()
    X_ti_test = X_ti_test.copy()

    # Tinh gia tri dien khuyet chi tu tap huan luyen X_ti_train
    age_median = X_ti_train['Age'].median()
    embarked_mode = X_ti_train['Embarked'].mode()[0]

    X_ti_train['Age'] = X_ti_train['Age'].fillna(age_median)
    X_ti_test['Age'] = X_ti_test['Age'].fillna(age_median)
    X_ti_train['Embarked'] = X_ti_train['Embarked'].fillna(embarked_mode)
    X_ti_test['Embarked'] = X_ti_test['Embarked'].fillna(embarked_mode)

    # Ma hoa One-Hot cho Embarked
    X_ti_train = pd.get_dummies(X_ti_train, columns=['Embarked'], drop_first=True, dtype=int)
    X_ti_test = pd.get_dummies(X_ti_test, columns=['Embarked'], drop_first=True, dtype=int)
    X_ti_test = X_ti_test.reindex(columns=X_ti_train.columns, fill_value=0)
    features_titanic = list(X_ti_train.columns)

    print(f"Titanic Train: {X_ti_train.shape}, Test: {X_ti_test.shape}", flush=True)

    # 1. Baseline Decision Tree
    dt_ti_base = DecisionTreeClassifier(random_state=42)
    dt_ti_base.fit(X_ti_train, y_ti_train)

    # 2. Baseline Random Forest
    rf_ti_base = RandomForestClassifier(random_state=42)
    rf_ti_base.fit(X_ti_train, y_ti_train)

    # 3. GridSearchCV Decision Tree
    param_grid_dt_ti = {
        'max_depth': [2, 3, 4, 5, 6],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_dt_ti = GridSearchCV(
        DecisionTreeClassifier(random_state=42),
        param_grid_dt_ti,
        scoring='accuracy',
        cv=5
    )
    grid_dt_ti.fit(X_ti_train, y_ti_train)
    best_dt_ti = grid_dt_ti.best_estimator_
    print(f"DT Titanic Best Params: {grid_dt_ti.best_params_}, CV Score: {grid_dt_ti.best_score_:.4f}", flush=True)

    # 4. GridSearchCV Random Forest
    param_grid_rf_ti = {
        'n_estimators': [50, 100, 150],
        'max_depth': [4, 6, 8],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [2, 4],
        'max_features': ['sqrt']
    }
    grid_rf_ti = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid_rf_ti,
        scoring='accuracy',
        cv=5
    )
    grid_rf_ti.fit(X_ti_train, y_ti_train)
    best_rf_ti = grid_rf_ti.best_estimator_
    print(f"RF Titanic Best Params: {grid_rf_ti.best_params_}, CV Score: {grid_rf_ti.best_score_:.4f}", flush=True)

    # Bieu do danh gia qua trinh tuning Titanic
    cv_dt_ti = pd.DataFrame(grid_dt_ti.cv_results_)
    dt_ti_depth_scores = cv_dt_ti.groupby('param_max_depth')['mean_test_score'].max()
    cv_rf_ti = pd.DataFrame(grid_rf_ti.cv_results_)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(dt_ti_depth_scores.index, dt_ti_depth_scores.values, '-o', color='black')
    axes[0].set_xlabel('max_depth')
    axes[0].set_ylabel('Mean CV Accuracy')
    axes[0].set_title('Decision Tree: CV Accuracy theo do sau max_depth')
    axes[0].grid(True, linestyle=':', alpha=0.6)
    
    for nest in [50, 100, 150]:
        sub = cv_rf_ti[cv_rf_ti['param_n_estimators'] == nest]
        sub_grouped = sub.groupby('param_max_depth')['mean_test_score'].max()
        axes[1].plot(sub_grouped.index, sub_grouped.values, '-o', label=f'n_estimators={nest}')
    axes[1].set_xlabel('max_depth')
    axes[1].set_ylabel('Mean CV Accuracy')
    axes[1].set_title('Random Forest: CV Accuracy theo max_depth va n_estimators')
    axes[1].legend()
    axes[1].grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    tuning_path_ti = os.path.join(figures_dir, '2_1_3_titanic_tuning.png')
    plt.savefig(tuning_path_ti, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Da luu Titanic Tuning: {tuning_path_ti}", flush=True)

    # 5. Danh gia ket qua
    res_dt_ti_base = evaluate_model(dt_ti_base, X_ti_train, y_ti_train, X_ti_test, y_ti_test, "DT Baseline (Titanic)")
    res_dt_ti_opt  = evaluate_model(best_dt_ti, X_ti_train, y_ti_train, X_ti_test, y_ti_test, "DT Tuned (Titanic)")
    res_rf_ti_base = evaluate_model(rf_ti_base, X_ti_train, y_ti_train, X_ti_test, y_ti_test, "RF Baseline (Titanic)")
    res_rf_ti_opt  = evaluate_model(best_rf_ti, X_ti_train, y_ti_train, X_ti_test, y_ti_test, "RF Tuned (Titanic)")

    # Confusion Matrix Titanic
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    cm_dt = confusion_matrix(y_ti_test, best_dt_ti.predict(X_ti_test))
    cm_rf = confusion_matrix(y_ti_test, best_rf_ti.predict(X_ti_test))

    sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False,
                xticklabels=['Tu vong', 'Song sot'], yticklabels=['Tu vong', 'Song sot'])
    axes[0].set_title(f"Confusion Matrix: Decision Tree (Tuned)\nAcc: {res_dt_ti_opt['Test Acc']:.4f}")
    axes[0].set_xlabel('Du doan')
    axes[0].set_ylabel('Thuc te')

    sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Greens', ax=axes[1], cbar=False,
                xticklabels=['Tu vong', 'Song sot'], yticklabels=['Tu vong', 'Song sot'])
    axes[1].set_title(f"Confusion Matrix: Random Forest (Tuned)\nAcc: {res_rf_ti_opt['Test Acc']:.4f}")
    axes[1].set_xlabel('Du doan')
    axes[1].set_ylabel('Thuc te')

    plt.tight_layout()
    cm_path_ti = os.path.join(figures_dir, '2_1_3_titanic_confusion_matrix.png')
    plt.savefig(cm_path_ti, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Da luu Titanic CM: {cm_path_ti}", flush=True)

    # Cay quyet dinh Titanic
    plt.figure(figsize=(16, 8), dpi=400)
    plot_tree(
        best_dt_ti,
        feature_names=features_titanic,
        class_names=['Tu vong', 'Song sot'],
        filled=True,
        rounded=True,
        fontsize=9
    )
    plt.title(f"Cay quyet dinh toi uu (Titanic) - max_depth={best_dt_ti.max_depth}")
    plt.tight_layout()
    tree_path_ti = os.path.join(figures_dir, '2_1_3_titanic_best_tree.png')
    plt.savefig(tree_path_ti, dpi=400, bbox_inches='tight')
    plt.close()
    print(f"Da luu Titanic Tree: {tree_path_ti}", flush=True)

    # Feature Importance Titanic
    fi_rf_ti = pd.Series(best_rf_ti.feature_importances_, index=features_titanic).sort_values(ascending=True)
    plt.figure(figsize=(8, 5))
    fi_rf_ti.plot(kind='barh', color='black', edgecolor='gray')
    plt.xlabel('Do quan trong (Gini Importance)')
    plt.ylabel('Dac trung')
    plt.title('Muc do quan trong cua dac trung trong Random Forest (Titanic)')
    plt.tight_layout()
    fi_path_ti = os.path.join(figures_dir, '2_1_3_titanic_rf_feature_importance.png')
    plt.savefig(fi_path_ti, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Da luu Titanic FI: {fi_path_ti}", flush=True)

    # ==============================================================================
    # 2.1.4: BÀI TẬP THỰC HÀNH 2 - DIABETES DATASET (PIMA INDIANS)
    # ==============================================================================
    print("\n================== 2.1.4 DIABETES ==================", flush=True)
    diabetes_raw = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/diabetes.csv')
    print(f"Kich thuoc Diabetes goc: {diabetes_raw.shape}", flush=True)

    # Chia train/test truoc de tranh Data Leakage
    features_diabetes = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    X_raw_di = diabetes_raw[features_diabetes]
    y_di = diabetes_raw['Outcome']

    X_di_train, X_di_test, y_di_train, y_di_test = train_test_split(
        X_raw_di, y_di, test_size=0.2, random_state=42, stratify=y_di
    )
    X_di_train = X_di_train.copy()
    X_di_test = X_di_test.copy()

    # Xu ly gia tri 0 bat thuong bang trung vi chi tinh tren tap train
    cols_with_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in cols_with_zero:
        X_di_train[col] = X_di_train[col].replace(0, np.nan)
        col_median = X_di_train[col].median()
        X_di_train[col] = X_di_train[col].fillna(col_median)
        
        X_di_test[col] = X_di_test[col].replace(0, np.nan)
        X_di_test[col] = X_di_test[col].fillna(col_median)

    print(f"Diabetes Train: {X_di_train.shape}, Test: {X_di_test.shape}", flush=True)

    # 1. Baseline Decision Tree
    dt_di_base = DecisionTreeClassifier(random_state=42)
    dt_di_base.fit(X_di_train, y_di_train)

    # 2. Baseline Random Forest
    rf_di_base = RandomForestClassifier(random_state=42)
    rf_di_base.fit(X_di_train, y_di_train)

    # 3. GridSearchCV Decision Tree
    param_grid_dt_di = {
        'max_depth': [2, 3, 4, 5, 6],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_dt_di = GridSearchCV(
        DecisionTreeClassifier(random_state=42),
        param_grid_dt_di,
        scoring='f1',
        cv=5
    )
    grid_dt_di.fit(X_di_train, y_di_train)
    best_dt_di = grid_dt_di.best_estimator_
    print(f"DT Diabetes Best Params: {grid_dt_di.best_params_}, CV Score: {grid_dt_di.best_score_:.4f}", flush=True)

    # 4. GridSearchCV Random Forest
    param_grid_rf_di = {
        'n_estimators': [50, 100, 150],
        'max_depth': [3, 5, 7],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [2, 4],
        'max_features': ['sqrt']
    }
    grid_rf_di = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid_rf_di,
        scoring='f1',
        cv=5
    )
    grid_rf_di.fit(X_di_train, y_di_train)
    best_rf_di = grid_rf_di.best_estimator_
    print(f"RF Diabetes Best Params: {grid_rf_di.best_params_}, CV Score: {grid_rf_di.best_score_:.4f}", flush=True)

    # Bieu do danh gia qua trinh tuning Diabetes
    cv_dt_di = pd.DataFrame(grid_dt_di.cv_results_)
    dt_di_depth_scores = cv_dt_di.groupby('param_max_depth')['mean_test_score'].max()
    cv_rf_di = pd.DataFrame(grid_rf_di.cv_results_)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(dt_di_depth_scores.index, dt_di_depth_scores.values, '-o', color='black')
    axes[0].set_xlabel('max_depth')
    axes[0].set_ylabel('Mean CV F1-score')
    axes[0].set_title('Decision Tree: CV F1 theo do sau max_depth')
    axes[0].grid(True, linestyle=':', alpha=0.6)
    
    for nest in [50, 100, 150]:
        sub = cv_rf_di[cv_rf_di['param_n_estimators'] == nest]
        sub_grouped = sub.groupby('param_max_depth')['mean_test_score'].max()
        axes[1].plot(sub_grouped.index, sub_grouped.values, '-o', label=f'n_estimators={nest}')
    axes[1].set_xlabel('max_depth')
    axes[1].set_ylabel('Mean CV F1-score')
    axes[1].set_title('Random Forest: CV F1 theo max_depth va n_estimators')
    axes[1].legend()
    axes[1].grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    tuning_path_di = os.path.join(figures_dir, '2_1_4_diabetes_tuning.png')
    plt.savefig(tuning_path_di, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Da luu Diabetes Tuning: {tuning_path_di}", flush=True)

    # 5. Danh gia ket qua
    res_dt_di_base = evaluate_model(dt_di_base, X_di_train, y_di_train, X_di_test, y_di_test, "DT Baseline (Diabetes)")
    res_dt_di_opt  = evaluate_model(best_dt_di, X_di_train, y_di_train, X_di_test, y_di_test, "DT Tuned (Diabetes)")
    res_rf_di_base = evaluate_model(rf_di_base, X_di_train, y_di_train, X_di_test, y_di_test, "RF Baseline (Diabetes)")
    res_rf_di_opt  = evaluate_model(best_rf_di, X_di_train, y_di_train, X_di_test, y_di_test, "RF Tuned (Diabetes)")

    # Confusion Matrix Diabetes
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    cm_dt_di = confusion_matrix(y_di_test, best_dt_di.predict(X_di_test))
    cm_rf_di = confusion_matrix(y_di_test, best_rf_di.predict(X_di_test))

    sns.heatmap(cm_dt_di, annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False,
                xticklabels=['Khong mac benh', 'Mac benh'], yticklabels=['Khong mac benh', 'Mac benh'])
    axes[0].set_title(f"Confusion Matrix: Decision Tree (Tuned)\nF1: {res_dt_di_opt['F1-Score']:.4f}")
    axes[0].set_xlabel('Du doan')
    axes[0].set_ylabel('Thuc te')

    sns.heatmap(cm_rf_di, annot=True, fmt='d', cmap='Greens', ax=axes[1], cbar=False,
                xticklabels=['Khong mac benh', 'Mac benh'], yticklabels=['Khong mac benh', 'Mac benh'])
    axes[1].set_title(f"Confusion Matrix: Random Forest (Tuned)\nF1: {res_rf_di_opt['F1-Score']:.4f}")
    axes[1].set_xlabel('Du doan')
    axes[1].set_ylabel('Thuc te')

    plt.tight_layout()
    cm_path_di = os.path.join(figures_dir, '2_1_4_diabetes_confusion_matrix.png')
    plt.savefig(cm_path_di, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Da luu Diabetes CM: {cm_path_di}", flush=True)

    # Cay quyet dinh Diabetes
    plt.figure(figsize=(16, 8), dpi=400)
    plot_tree(
        best_dt_di,
        feature_names=features_diabetes,
        class_names=['Khong tieu duong', 'Tieu duong'],
        filled=True,
        rounded=True,
        fontsize=9
    )
    plt.title(f"Cay quyet dinh toi uu (Diabetes) - max_depth={best_dt_di.max_depth}")
    plt.tight_layout()
    tree_path_di = os.path.join(figures_dir, '2_1_4_diabetes_best_tree.png')
    plt.savefig(tree_path_di, dpi=400, bbox_inches='tight')
    plt.close()
    print(f"Da luu Diabetes Tree: {tree_path_di}", flush=True)

    # Feature Importance Diabetes
    fi_rf_di = pd.Series(best_rf_di.feature_importances_, index=features_diabetes).sort_values(ascending=True)
    plt.figure(figsize=(8, 5))
    fi_rf_di.plot(kind='barh', color='black', edgecolor='gray')
    plt.xlabel('Do quan trong (Gini Importance)')
    plt.ylabel('Dac trung')
    plt.title('Muc do quan trong cua dac trung trong Random Forest (Diabetes)')
    plt.tight_layout()
    fi_path_di = os.path.join(figures_dir, '2_1_4_diabetes_rf_feature_importance.png')
    plt.savefig(fi_path_di, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Da luu Diabetes FI: {fi_path_di}", flush=True)

    # Bang tong hop ket qua
    summary_df = pd.DataFrame([
        res_dt_ti_base, res_dt_ti_opt, res_rf_ti_base, res_rf_ti_opt,
        res_dt_di_base, res_dt_di_opt, res_rf_di_base, res_rf_di_opt
    ])
    summary_path = os.path.join(figures_dir, 'summary_metrics_2_1.csv')
    summary_df.to_csv(summary_path, index=False)
    print(f"\nBang tong hop ket qua:\n{summary_df.to_string(index=False)}", flush=True)

if __name__ == '__main__':
    main()
