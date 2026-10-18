import os
import sys
import numpy as np
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def evaluate(model, X_train, y_train, X_test, y_test, name):
    tr_pred = model.predict(X_train)
    te_pred = model.predict(X_test)
    te_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    acc_tr = accuracy_score(y_train, tr_pred)
    acc_te = accuracy_score(y_test, te_pred)
    prec_te = precision_score(y_test, te_pred, zero_division=0)
    rec_te = recall_score(y_test, te_pred, zero_division=0)
    f1_te = f1_score(y_test, te_pred, zero_division=0)
    auc_te = roc_auc_score(y_test, te_prob) if te_prob is not None else 0.0
    
    return {
        'Mô hình thử nghiệm': name,
        'Train Acc': f"{acc_tr:.4f}",
        'Test Acc': f"{acc_te:.4f}",
        'Precision': f"{prec_te:.4f}",
        'Recall': f"{rec_te:.4f}",
        'F1-Score': f"{f1_te:.4f}",
        'ROC-AUC': f"{auc_te:.4f}"
    }

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

dt_ti_base = DecisionTreeClassifier(random_state=42).fit(X_ti_train, y_ti_train)
rf_ti_base = RandomForestClassifier(random_state=42).fit(X_ti_train, y_ti_train)

grid_dt_ti = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    {'max_depth': [2, 3, 4, 5, 6], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]},
    scoring='accuracy', cv=5
).fit(X_ti_train, y_ti_train)

grid_rf_ti = GridSearchCV(
    RandomForestClassifier(random_state=42),
    {'n_estimators': [50, 100], 'max_depth': [4, 6, 8], 'min_samples_split': [2, 5], 'min_samples_leaf': [2, 4], 'max_features': ['sqrt']},
    scoring='accuracy', cv=5
).fit(X_ti_train, y_ti_train)

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

dt_di_base = DecisionTreeClassifier(random_state=42).fit(X_di_train, y_di_train)
rf_di_base = RandomForestClassifier(random_state=42).fit(X_di_train, y_di_train)

grid_dt_di = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    {'max_depth': [2, 3, 4, 5, 6], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]},
    scoring='f1', cv=5
).fit(X_di_train, y_di_train)

grid_rf_di = GridSearchCV(
    RandomForestClassifier(random_state=42),
    {'n_estimators': [50, 100], 'max_depth': [3, 5, 7], 'min_samples_split': [2, 5], 'min_samples_leaf': [2, 4], 'max_features': ['sqrt']},
    scoring='f1', cv=5
).fit(X_di_train, y_di_train)

table = [
    evaluate(dt_ti_base, X_ti_train, y_ti_train, X_ti_test, y_ti_test, "DT Baseline Titanic"),
    evaluate(grid_dt_ti.best_estimator_, X_ti_train, y_ti_train, X_ti_test, y_ti_test, "DT Tuned Titanic"),
    evaluate(rf_ti_base, X_ti_train, y_ti_train, X_ti_test, y_ti_test, "RF Baseline Titanic"),
    evaluate(grid_rf_ti.best_estimator_, X_ti_train, y_ti_train, X_ti_test, y_ti_test, "RF Tuned Titanic"),
    evaluate(dt_di_base, X_di_train, y_di_train, X_di_test, y_di_test, "DT Baseline Diabetes"),
    evaluate(grid_dt_di.best_estimator_, X_di_train, y_di_train, X_di_test, y_di_test, "DT Tuned Diabetes"),
    evaluate(rf_di_base, X_di_train, y_di_train, X_di_test, y_di_test, "RF Baseline Diabetes"),
    evaluate(grid_rf_di.best_estimator_, X_di_train, y_di_train, X_di_test, y_di_test, "RF Tuned Diabetes")
]

df_table = pd.DataFrame(table)
print(df_table.to_string(index=False))
print("\nDT Titanic Best Params:", grid_dt_ti.best_params_)
print("RF Titanic Best Params:", grid_rf_ti.best_params_)
print("DT Diabetes Best Params:", grid_dt_di.best_params_)
print("RF Diabetes Best Params:", grid_rf_di.best_params_)
