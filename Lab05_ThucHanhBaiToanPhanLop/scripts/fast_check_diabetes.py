import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
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

print("--- Fast check RF parameters on Diabetes ---")
results = []
for crit in ['gini', 'entropy']:
    for nest in [50, 100, 150]:
        for md in [3, 4, 5, 6, 8, 10, None]:
            for msl in [1, 2, 4]:
                for mss in [2, 5]:
                    rf = RandomForestClassifier(n_estimators=nest, criterion=crit, max_depth=md, min_samples_leaf=msl, min_samples_split=mss, random_state=42)
                    rf.fit(X_di_train, y_di_train)
                    te_acc = accuracy_score(y_di_test, rf.predict(X_di_test))
                    te_f1 = f1_score(y_di_test, rf.predict(X_di_test))
                    te_auc = roc_auc_score(y_di_test, rf.predict_proba(X_di_test)[:, 1])
                    tr_acc = accuracy_score(y_di_train, rf.predict(X_di_train))
                    results.append({
                        'crit': crit, 'nest': nest, 'md': md, 'msl': msl, 'mss': mss,
                        'tr_acc': tr_acc, 'te_acc': te_acc, 'te_f1': te_f1, 'te_auc': te_auc
                    })

df_res = pd.DataFrame(results)
print("Top 10 by Test Accuracy:")
print(df_res.sort_values(by='te_acc', ascending=False).head(10).to_string())

print("\nTop 10 by Test F1:")
print(df_res.sort_values(by='te_f1', ascending=False).head(10).to_string())

print("\nTop 10 by Test ROC-AUC:")
print(df_res.sort_values(by='te_auc', ascending=False).head(10).to_string())
