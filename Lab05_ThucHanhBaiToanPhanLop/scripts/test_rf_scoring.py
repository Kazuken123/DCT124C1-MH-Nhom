import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

diabetes_raw = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/diabetes.csv')
features_diabetes = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
X_raw = diabetes_raw[features_diabetes]
y_di = diabetes_raw['Outcome']

X_di_train, X_di_test, y_di_train, y_di_test = train_test_split(
    X_raw, y_di, test_size=0.2, random_state=42, stratify=y_di
)
X_di_train = X_di_train.copy()
X_di_test = X_di_test.copy()

for col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
    X_di_train[col] = X_di_train[col].replace(0, np.nan)
    med = X_di_train[col].median()
    X_di_train[col] = X_di_train[col].fillna(med)
    X_di_test[col] = X_di_test[col].replace(0, np.nan)
    X_di_test[col] = X_di_test[col].fillna(med)

for scoring in ['accuracy', 'roc_auc', 'recall']:
    grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        {'n_estimators': [50, 100], 'max_depth': [3, 4, 5, 6], 'min_samples_split': [2, 5], 'min_samples_leaf': [1, 2, 4]},
        scoring=scoring, cv=5
    ).fit(X_di_train, y_di_train)
    m = grid.best_estimator_
    print(f"Scoring={scoring}, params={grid.best_params_} -> Acc={accuracy_score(y_di_test, m.predict(X_di_test)):.4f}, F1={f1_score(y_di_test, m.predict(X_di_test)):.4f}, AUC={roc_auc_score(y_di_test, m.predict_proba(X_di_test)[:,1]):.4f}")
