import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

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

print("=== TITANIC BASELINES ===")
dt_ti_b = DecisionTreeClassifier(random_state=42).fit(X_ti_train, y_ti_train)
rf_ti_b = RandomForestClassifier(random_state=42).fit(X_ti_train, y_ti_train)
print(f"DT Base -> TrAcc={dt_ti_b.score(X_ti_train, y_ti_train):.4f}, TeAcc={dt_ti_b.score(X_ti_test, y_ti_test):.4f}, F1={f1_score(y_ti_test, dt_ti_b.predict(X_ti_test)):.4f}, AUC={roc_auc_score(y_ti_test, dt_ti_b.predict_proba(X_ti_test)[:,1]):.4f}")
print(f"RF Base -> TrAcc={rf_ti_b.score(X_ti_train, y_ti_train):.4f}, TeAcc={rf_ti_b.score(X_ti_test, y_ti_test):.4f}, F1={f1_score(y_ti_test, rf_ti_b.predict(X_ti_test)):.4f}, AUC={roc_auc_score(y_ti_test, rf_ti_b.predict_proba(X_ti_test)[:,1]):.4f}")

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

print("\n=== DIABETES BASELINES ===")
dt_di_b = DecisionTreeClassifier(random_state=42).fit(X_di_train, y_di_train)
rf_di_b = RandomForestClassifier(random_state=42).fit(X_di_train, y_di_train)
print(f"DT Base -> TrAcc={dt_di_b.score(X_di_train, y_di_train):.4f}, TeAcc={dt_di_b.score(X_di_test, y_di_test):.4f}, F1={f1_score(y_di_test, dt_di_b.predict(X_di_test)):.4f}, AUC={roc_auc_score(y_di_test, dt_di_b.predict_proba(X_di_test)[:,1]):.4f}")
print(f"RF Base -> TrAcc={rf_di_b.score(X_di_train, y_di_train):.4f}, TeAcc={rf_di_b.score(X_di_test, y_di_test):.4f}, F1={f1_score(y_di_test, rf_di_b.predict(X_di_test)):.4f}, AUC={roc_auc_score(y_di_test, rf_di_b.predict_proba(X_di_test)[:,1]):.4f}")
