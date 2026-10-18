import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

sys.stdout.reconfigure(encoding='utf-8')

# 1. Titanic
titanic_raw = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/train.csv')
titanic_df = titanic_raw.copy()
titanic_df['Sex'] = titanic_df['Sex'].map({'male': 0, 'female': 1})
features_raw = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
X_raw_ti = titanic_df[features_raw]
y_ti = titanic_df['Survived']

X_ti_train, X_ti_test, y_ti_train, y_ti_test = train_test_split(
    X_raw_ti, y_ti, test_size=0.2, random_state=42, stratify=y_ti
)
X_ti_train = X_ti_train.copy()
X_ti_test = X_ti_test.copy()

age_med = X_ti_train['Age'].median()
emb_mode = X_ti_train['Embarked'].mode()[0]
X_ti_train['Age'] = X_ti_train['Age'].fillna(age_med)
X_ti_test['Age'] = X_ti_test['Age'].fillna(age_med)
X_ti_train['Embarked'] = X_ti_train['Embarked'].fillna(emb_mode)
X_ti_test['Embarked'] = X_ti_test['Embarked'].fillna(emb_mode)

X_ti_train = pd.get_dummies(X_ti_train, columns=['Embarked'], drop_first=True, dtype=int)
X_ti_test = pd.get_dummies(X_ti_test, columns=['Embarked'], drop_first=True, dtype=int)
X_ti_test = X_ti_test.reindex(columns=X_ti_train.columns, fill_value=0)

print("=== TITANIC BASELINES ===", flush=True)
dt_base = DecisionTreeClassifier(random_state=42).fit(X_ti_train, y_ti_train)
rf_base = RandomForestClassifier(random_state=42).fit(X_ti_train, y_ti_train)
print(f"DT Base -> TrAcc={dt_base.score(X_ti_train, y_ti_train):.4f}, TeAcc={dt_base.score(X_ti_test, y_ti_test):.4f}, F1={f1_score(y_ti_test, dt_base.predict(X_ti_test)):.4f}, AUC={roc_auc_score(y_ti_test, dt_base.predict_proba(X_ti_test)[:,1]):.4f}", flush=True)
print(f"RF Base -> TrAcc={rf_base.score(X_ti_train, y_ti_train):.4f}, TeAcc={rf_base.score(X_ti_test, y_ti_test):.4f}, F1={f1_score(y_ti_test, rf_base.predict(X_ti_test)):.4f}, AUC={roc_auc_score(y_ti_test, rf_base.predict_proba(X_ti_test)[:,1]):.4f}", flush=True)

param_dt_ti = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [3, 4, 5, 6],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

param_rf_ti = {
    'n_estimators': [50, 100, 150],
    'criterion': ['gini', 'entropy'],
    'max_depth': [4, 6, 8, 10],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt']
}

for scoring in ['accuracy', 'roc_auc', 'f1']:
    print(f"\n--- Testing scoring='{scoring}' on Titanic ---", flush=True)
    g_dt = GridSearchCV(DecisionTreeClassifier(random_state=42), param_dt_ti, cv=5, scoring=scoring).fit(X_ti_train, y_ti_train)
    m_dt = g_dt.best_estimator_
    print(f"DT Best ({g_dt.best_params_}), CV={g_dt.best_score_:.4f} -> TrAcc={m_dt.score(X_ti_train, y_ti_train):.4f}, TeAcc={m_dt.score(X_ti_test, y_ti_test):.4f}, F1={f1_score(y_ti_test, m_dt.predict(X_ti_test)):.4f}, AUC={roc_auc_score(y_ti_test, m_dt.predict_proba(X_ti_test)[:,1]):.4f}", flush=True)
    
    g_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_rf_ti, cv=5, scoring=scoring).fit(X_ti_train, y_ti_train)
    m_rf = g_rf.best_estimator_
    print(f"RF Best ({g_rf.best_params_}), CV={g_rf.best_score_:.4f} -> TrAcc={m_rf.score(X_ti_train, y_ti_train):.4f}, TeAcc={m_rf.score(X_ti_test, y_ti_test):.4f}, F1={f1_score(y_ti_test, m_rf.predict(X_ti_test)):.4f}, AUC={roc_auc_score(y_ti_test, m_rf.predict_proba(X_ti_test)[:,1]):.4f}", flush=True)
