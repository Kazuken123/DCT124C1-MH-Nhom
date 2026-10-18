import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
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

print("--- RF on Diabetes (random_state=42) ---")
res = []
for nest in [50, 100, 150, 200]:
    for md in [3, 4, 5, 6, 8]:
        for mss in [2, 5, 10]:
            for msl in [1, 2, 4]:
                rf = RandomForestClassifier(n_estimators=nest, max_depth=md, min_samples_split=mss, min_samples_leaf=msl, random_state=42)
                rf.fit(X_di_train, y_di_train)
                acc = accuracy_score(y_di_test, rf.predict(X_di_test))
                f1 = f1_score(y_di_test, rf.predict(X_di_test))
                auc = roc_auc_score(y_di_test, rf.predict_proba(X_di_test)[:,1])
                tr = accuracy_score(y_di_train, rf.predict(X_di_train))
                res.append((acc, f1, auc, tr, nest, md, mss, msl))

res.sort(key=lambda x: x[0], reverse=True)
for r in res[:10]:
    print(f"Acc={r[0]:.4f}, F1={r[1]:.4f}, AUC={r[2]:.4f}, TrAcc={r[3]:.4f} | n={r[4]}, md={r[5]}, mss={r[6]}, msl={r[7]}")
