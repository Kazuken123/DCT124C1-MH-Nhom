import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# 2. Diabetes
diabetes_raw = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/diabetes.csv')
features_di = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
X_raw_di = diabetes_raw[features_di]
y_di = diabetes_raw['Outcome']

X_di_train, X_di_test, y_di_train, y_di_test = train_test_split(
    X_raw_di, y_di, test_size=0.2, random_state=42, stratify=y_di
)
X_di_train = X_di_train.copy()
X_di_test = X_di_test.copy()

for col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
    X_di_train[col] = X_di_train[col].replace(0, np.nan)
    med = X_di_train[col].median()
    X_di_train[col] = X_di_train[col].fillna(med)
    X_di_test[col] = X_di_test[col].replace(0, np.nan)
    X_di_test[col] = X_di_test[col].fillna(med)

print("=== DIABETES BASELINES ===")
dt_di_b = DecisionTreeClassifier(random_state=42).fit(X_di_train, y_di_train)
rf_di_b = RandomForestClassifier(random_state=42).fit(X_di_train, y_di_train)
print(f"DT Base -> TrAcc={dt_di_b.score(X_di_train, y_di_train):.4f}, TeAcc={dt_di_b.score(X_di_test, y_di_test):.4f}, F1={f1_score(y_di_test, dt_di_b.predict(X_di_test)):.4f}, AUC={roc_auc_score(y_di_test, dt_di_b.predict_proba(X_di_test)[:,1]):.4f}")
print(f"RF Base -> TrAcc={rf_di_b.score(X_di_train, y_di_train):.4f}, TeAcc={rf_di_b.score(X_di_test, y_di_test):.4f}, F1={f1_score(y_di_test, rf_di_b.predict(X_di_test)):.4f}, AUC={roc_auc_score(y_di_test, rf_di_b.predict_proba(X_di_test)[:,1]):.4f}")

# DT Tuning:
param_dt_di = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [2, 3, 4, 5, 6],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
g_dt = GridSearchCV(DecisionTreeClassifier(random_state=42), param_dt_di, cv=5, scoring='f1').fit(X_di_train, y_di_train)
best_dt = g_dt.best_estimator_
print(f"DT Tuned (f1): best={g_dt.best_params_}, CV={g_dt.best_score_:.4f} -> TeAcc={best_dt.score(X_di_test, y_di_test):.4f}, F1={f1_score(y_di_test, best_dt.predict(X_di_test)):.4f}, AUC={roc_auc_score(y_di_test, best_dt.predict_proba(X_di_test)[:,1]):.4f}")

# RF Grid search testing different grids:
grids = [
    {
        'desc': 'Grid 1 (wide depth, accuracy scoring)',
        'scoring': 'accuracy',
        'params': {
            'n_estimators': [50, 100, 150],
            'criterion': ['gini', 'entropy'],
            'max_depth': [4, 6, 8, 10, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
    },
    {
        'desc': 'Grid 2 (wide depth, roc_auc scoring)',
        'scoring': 'roc_auc',
        'params': {
            'n_estimators': [50, 100, 150],
            'criterion': ['gini', 'entropy'],
            'max_depth': [4, 6, 8, 10, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
    },
    {
        'desc': 'Grid 3 (wide depth, f1 scoring)',
        'scoring': 'f1',
        'params': {
            'n_estimators': [50, 100, 150],
            'criterion': ['gini', 'entropy'],
            'max_depth': [4, 6, 8, 10, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
    }
]

for g_cfg in grids:
    g_rf = GridSearchCV(RandomForestClassifier(random_state=42), g_cfg['params'], cv=5, scoring=g_cfg['scoring']).fit(X_di_train, y_di_train)
    m = g_rf.best_estimator_
    te_acc = m.score(X_di_test, y_di_test)
    f1 = f1_score(y_di_test, m.predict(X_di_test))
    auc = roc_auc_score(y_di_test, m.predict_proba(X_di_test)[:, 1])
    print(f"\n{g_cfg['desc']}:")
    print(f"  Best params: {g_rf.best_params_}, CV Score: {g_rf.best_score_:.4f}")
    print(f"  Train Acc: {m.score(X_di_train, y_di_train):.4f}, Test Acc: {te_acc:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}")
