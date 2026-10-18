import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

print("=== TESTING TITANIC ===")
titanic_raw = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/train.csv')
titanic_df = titanic_raw.copy()
titanic_df['Sex'] = titanic_df['Sex'].map({'male': 0, 'female': 1})
features_raw = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
X_raw = titanic_df[features_raw]
y_ti = titanic_df['Survived']

X_ti_train, X_ti_test, y_ti_train, y_ti_test = train_test_split(
    X_raw, y_ti, test_size=0.2, random_state=42, stratify=y_ti
)
X_ti_train = X_ti_train.copy()
X_ti_test = X_ti_test.copy()

age_median = X_ti_train['Age'].median()
embarked_mode = X_ti_train['Embarked'].mode()[0]

X_ti_train['Age'] = X_ti_train['Age'].fillna(age_median)
X_ti_test['Age'] = X_ti_test['Age'].fillna(age_median)
X_ti_train['Embarked'] = X_ti_train['Embarked'].fillna(embarked_mode)
X_ti_test['Embarked'] = X_ti_test['Embarked'].fillna(embarked_mode)

X_ti_train = pd.get_dummies(X_ti_train, columns=['Embarked'], drop_first=True, dtype=int)
X_ti_test = pd.get_dummies(X_ti_test, columns=['Embarked'], drop_first=True, dtype=int)
X_ti_test = X_ti_test.reindex(columns=X_ti_train.columns, fill_value=0)

# 1. Baseline DT
dt_base = DecisionTreeClassifier(random_state=42).fit(X_ti_train, y_ti_train)
# 2. Baseline RF
rf_base = RandomForestClassifier(random_state=42).fit(X_ti_train, y_ti_train)

print(f"DT Base - Train Acc: {accuracy_score(y_ti_train, dt_base.predict(X_ti_train)):.4f}, Test Acc: {accuracy_score(y_ti_test, dt_base.predict(X_ti_test)):.4f}, F1: {f1_score(y_ti_test, dt_base.predict(X_ti_test)):.4f}, AUC: {roc_auc_score(y_ti_test, dt_base.predict_proba(X_ti_test)[:,1]):.4f}")
print(f"RF Base - Train Acc: {accuracy_score(y_ti_train, rf_base.predict(X_ti_train)):.4f}, Test Acc: {accuracy_score(y_ti_test, rf_base.predict(X_ti_test)):.4f}, F1: {f1_score(y_ti_test, rf_base.predict(X_ti_test)):.4f}, AUC: {roc_auc_score(y_ti_test, rf_base.predict_proba(X_ti_test)[:,1]):.4f}")

# DT Grid
param_grid_dt = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [3, 4, 5, 6],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
grid_dt = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid_dt, scoring='roc_auc', cv=5).fit(X_ti_train, y_ti_train)
best_dt = grid_dt.best_estimator_
print(f"DT Tuned ({grid_dt.best_params_}) - Train Acc: {accuracy_score(y_ti_train, best_dt.predict(X_ti_train)):.4f}, Test Acc: {accuracy_score(y_ti_test, best_dt.predict(X_ti_test)):.4f}, F1: {f1_score(y_ti_test, best_dt.predict(X_ti_test)):.4f}, AUC: {roc_auc_score(y_ti_test, best_dt.predict_proba(X_ti_test)[:,1]):.4f}")

# RF Grid
param_grid_rf = {
    'n_estimators': [50, 100, 150],
    'max_depth': [4, 5, 6, 7],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}
grid_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid_rf, scoring='roc_auc', cv=5).fit(X_ti_train, y_ti_train)
best_rf = grid_rf.best_estimator_
print(f"RF Tuned ({grid_rf.best_params_}) - Train Acc: {accuracy_score(y_ti_train, best_rf.predict(X_ti_train)):.4f}, Test Acc: {accuracy_score(y_ti_test, best_rf.predict(X_ti_test)):.4f}, F1: {f1_score(y_ti_test, best_rf.predict(X_ti_test)):.4f}, AUC: {roc_auc_score(y_ti_test, best_rf.predict_proba(X_ti_test)[:,1]):.4f}")
