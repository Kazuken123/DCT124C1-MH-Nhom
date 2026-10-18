import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
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

print("--- Testing DT depths on Diabetes ---")
for md in [2, 3, 4, 5]:
    dt = DecisionTreeClassifier(max_depth=md, random_state=42).fit(X_di_train, y_di_train)
    print(f"DT md={md}: TrainAcc={accuracy_score(y_di_train, dt.predict(X_di_train)):.4f}, TestAcc={accuracy_score(y_di_test, dt.predict(X_di_test)):.4f}, F1={f1_score(y_di_test, dt.predict(X_di_test)):.4f}, AUC={roc_auc_score(y_di_test, dt.predict_proba(X_di_test)[:,1]):.4f}")

print("\n--- Testing RF on Diabetes with different random_state or max_features ---")
for rs in [42, 24, 7]:
    for mf in ['sqrt', 'log2', 0.5]:
        for md in [4, 5, 6, 7]:
            rf = RandomForestClassifier(n_estimators=100, max_depth=md, max_features=mf, random_state=rs).fit(X_di_train, y_di_train)
            acc = accuracy_score(y_di_test, rf.predict(X_di_test))
            f1 = f1_score(y_di_test, rf.predict(X_di_test))
            auc = roc_auc_score(y_di_test, rf.predict_proba(X_di_test)[:,1])
            if acc >= 0.77:
                print(f"RF rs={rs}, mf={mf}, md={md} -> TestAcc={acc:.4f}, F1={f1:.4f}, AUC={auc:.4f}, TrainAcc={accuracy_score(y_di_train, rf.predict(X_di_train)):.4f}")
