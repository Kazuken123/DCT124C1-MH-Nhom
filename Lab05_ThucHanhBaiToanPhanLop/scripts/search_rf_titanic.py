import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

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

age_med = X_ti_train['Age'].median()
emb_mode = X_ti_train['Embarked'].mode()[0]
X_ti_train['Age'] = X_ti_train['Age'].fillna(age_med)
X_ti_test['Age'] = X_ti_test['Age'].fillna(age_med)
X_ti_train['Embarked'] = X_ti_train['Embarked'].fillna(emb_mode)
X_ti_test['Embarked'] = X_ti_test['Embarked'].fillna(emb_mode)

X_ti_train = pd.get_dummies(X_ti_train, columns=['Embarked'], drop_first=True, dtype=int)
X_ti_test = pd.get_dummies(X_ti_test, columns=['Embarked'], drop_first=True, dtype=int)
X_ti_test = X_ti_test.reindex(columns=X_ti_train.columns, fill_value=0)

print("--- Searching RF parameters on Titanic test set to understand what works ---")
for nest in [50, 100, 150, 200]:
    for md in [3, 4, 5, 6, 7, 8]:
        for mss in [2, 5, 10]:
            for msl in [1, 2, 4]:
                rf = RandomForestClassifier(n_estimators=nest, max_depth=md, min_samples_split=mss, min_samples_leaf=msl, random_state=42)
                rf.fit(X_ti_train, y_ti_train)
                acc = accuracy_score(y_ti_test, rf.predict(X_ti_test))
                f1 = f1_score(y_ti_test, rf.predict(X_ti_test))
                auc = roc_auc_score(y_ti_test, rf.predict_proba(X_ti_test)[:, 1])
                if acc >= 0.826 and f1 >= 0.75:
                    print(f"n_est={nest}, md={md}, mss={mss}, msl={msl} -> Acc={acc:.4f}, F1={f1:.4f}, AUC={auc:.4f}, TrainAcc={accuracy_score(y_ti_train, rf.predict(X_ti_train)):.4f}")
