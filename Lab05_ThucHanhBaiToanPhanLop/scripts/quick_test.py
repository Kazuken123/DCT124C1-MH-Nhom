import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def eval_m(m, X_tr, y_tr, X_te, y_te, name=""):
    y_pred_tr = m.predict(X_tr)
    y_pred_te = m.predict(X_te)
    y_prob_te = m.predict_proba(X_te)[:, 1] if hasattr(m, 'predict_proba') else None
    acc_tr = accuracy_score(y_tr, y_pred_tr)
    acc_te = accuracy_score(y_te, y_pred_te)
    p_te = precision_score(y_te, y_pred_te, zero_division=0)
    r_te = recall_score(y_te, y_pred_te, zero_division=0)
    f1_te = f1_score(y_te, y_pred_te, zero_division=0)
    auc_te = roc_auc_score(y_te, y_prob_te) if y_prob_te is not None else 0
    print(f"{name:25s} | TrAcc: {acc_tr:.4f} | TeAcc: {acc_te:.4f} | Prec: {p_te:.4f} | Rec: {r_te:.4f} | F1: {f1_te:.4f} | AUC: {auc_te:.4f}")
    return {'Model': name, 'Train Acc': acc_tr, 'Test Acc': acc_te, 'Precision': p_te, 'Recall': r_te, 'F1-Score': f1_te, 'ROC-AUC': auc_te}

# 1. Titanic
raw_ti = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/train.csv')
features_ti = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
X_ti = raw_ti[features_ti].copy()
y_ti = raw_ti['Survived']
X_ti_tr, X_ti_te, y_ti_tr, y_ti_te = train_test_split(X_ti, y_ti, test_size=0.2, random_state=42, stratify=y_ti)

age_med = X_ti_tr['Age'].median()
emb_mode = X_ti_tr['Embarked'].mode()[0]
X_ti_tr['Age'] = X_ti_tr['Age'].fillna(age_med)
X_ti_te['Age'] = X_ti_te['Age'].fillna(age_med)
X_ti_tr['Embarked'] = X_ti_tr['Embarked'].fillna(emb_mode)
X_ti_te['Embarked'] = X_ti_te['Embarked'].fillna(emb_mode)
X_ti_tr['Sex'] = X_ti_tr['Sex'].map({'male': 0, 'female': 1})
X_ti_te['Sex'] = X_ti_te['Sex'].map({'male': 0, 'female': 1})
X_ti_tr = pd.get_dummies(X_ti_tr, columns=['Embarked'], drop_first=True, dtype=int)
X_ti_te = pd.get_dummies(X_ti_te, columns=['Embarked'], drop_first=True, dtype=int)
X_ti_te = X_ti_te.reindex(columns=X_ti_tr.columns, fill_value=0)

param_rf_ti = {
    'n_estimators': [50, 100, 150],
    'max_depth': [4, 6, 8, 10],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
g_rf_ti = GridSearchCV(RandomForestClassifier(random_state=42), param_rf_ti, cv=5, scoring='roc_auc').fit(X_ti_tr, y_ti_tr)
print("RF Titanic Best (scoring=roc_auc):", g_rf_ti.best_params_, "CV:", g_rf_ti.best_score_)
eval_m(g_rf_ti.best_estimator_, X_ti_tr, y_ti_tr, X_ti_te, y_ti_te, "RF Tuned Titanic (roc_auc)")

g_rf_ti_acc = GridSearchCV(RandomForestClassifier(random_state=42), param_rf_ti, cv=5, scoring='accuracy').fit(X_ti_tr, y_ti_tr)
print("RF Titanic Best (scoring=accuracy):", g_rf_ti_acc.best_params_, "CV:", g_rf_ti_acc.best_score_)
eval_m(g_rf_ti_acc.best_estimator_, X_ti_tr, y_ti_tr, X_ti_te, y_ti_te, "RF Tuned Titanic (acc)")

# 2. Diabetes
raw_di = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/diabetes.csv')
cols_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
raw_di_clean = raw_di.copy()
for c in cols_zero:
    raw_di_clean[c] = raw_di_clean[c].replace(0, np.nan)

features_di = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
X_di = raw_di_clean[features_di]
y_di = raw_di_clean['Outcome']
X_di_tr, X_di_te, y_di_tr, y_di_te = train_test_split(X_di, y_di, test_size=0.2, random_state=42, stratify=y_di)
meds = X_di_tr[cols_zero].median()
X_di_tr[cols_zero] = X_di_tr[cols_zero].fillna(meds)
X_di_te[cols_zero] = X_di_te[cols_zero].fillna(meds)

dt_di_base = DecisionTreeClassifier(random_state=42).fit(X_di_tr, y_di_tr)
rf_di_base = RandomForestClassifier(random_state=42).fit(X_di_tr, y_di_tr)
eval_m(dt_di_base, X_di_tr, y_di_tr, X_di_te, y_di_te, "DT Base Diab")
eval_m(rf_di_base, X_di_tr, y_di_tr, X_di_te, y_di_te, "RF Base Diab")

param_dt_di = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [3, 4, 5, 6],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
g_dt_di = GridSearchCV(DecisionTreeClassifier(random_state=42), param_dt_di, cv=5, scoring='f1').fit(X_di_tr, y_di_tr)
print("DT Diab Best (f1):", g_dt_di.best_params_, "CV:", g_dt_di.best_score_)
eval_m(g_dt_di.best_estimator_, X_di_tr, y_di_tr, X_di_te, y_di_te, "DT Tuned Diab (f1)")

param_rf_di = {
    'n_estimators': [50, 100, 150],
    'criterion': ['gini', 'entropy'],
    'max_depth': [4, 6, 8, 10],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
g_rf_di = GridSearchCV(RandomForestClassifier(random_state=42), param_rf_di, cv=5, scoring='f1').fit(X_di_tr, y_di_tr)
print("RF Diab Best (f1):", g_rf_di.best_params_, "CV:", g_rf_di.best_score_)
eval_m(g_rf_di.best_estimator_, X_di_tr, y_di_tr, X_di_te, y_di_te, "RF Tuned Diab (f1)")

g_rf_di_auc = GridSearchCV(RandomForestClassifier(random_state=42), param_rf_di, cv=5, scoring='roc_auc').fit(X_di_tr, y_di_tr)
print("RF Diab Best (roc_auc):", g_rf_di_auc.best_params_, "CV:", g_rf_di_auc.best_score_)
eval_m(g_rf_di_auc.best_estimator_, X_di_tr, y_di_tr, X_di_te, y_di_te, "RF Tuned Diab (roc_auc)")
