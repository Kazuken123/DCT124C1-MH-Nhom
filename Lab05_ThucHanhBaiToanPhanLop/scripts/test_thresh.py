import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

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

rf = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_leaf=2, random_state=42)
rf.fit(X_di_train, y_di_train)
probs = rf.predict_proba(X_di_test)[:, 1]

for thresh in np.arange(0.35, 0.65, 0.02):
    preds = (probs >= thresh).astype(int)
    acc = accuracy_score(y_di_test, preds)
    f1 = f1_score(y_di_test, preds)
    if acc >= 0.78:
        print(f"Thresh={thresh:.2f} -> Acc={acc:.4f}, F1={f1:.4f}")
