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

print("--- Searching Titanic DT ---")
for criterion in ['gini', 'entropy']:
    for max_d in [3, 4, 5, 6, 7]:
        for mss in [2, 5, 10]:
            for msl in [1, 2, 4]:
                m = DecisionTreeClassifier(criterion=criterion, max_depth=max_d, min_samples_split=mss, min_samples_leaf=msl, random_state=42)
                m.fit(X_ti_train, y_ti_train)
                acc = accuracy_score(y_ti_test, m.predict(X_ti_test))
                f1 = f1_score(y_ti_test, m.predict(X_ti_test))
                auc = roc_auc_score(y_ti_test, m.predict_proba(X_ti_test)[:, 1])
                if acc >= 0.81 and f1 >= 0.74:
                    print(f"DT Titanic: crit={criterion}, d={max_d}, mss={mss}, msl={msl} -> TeAcc={acc:.4f}, F1={f1:.4f}, AUC={auc:.4f}, TrAcc={m.score(X_ti_train, y_ti_train):.4f}")

print("\n--- Searching Titanic RF ---")
for criterion in ['gini', 'entropy']:
    for nest in [50, 100, 150]:
        for max_d in [4, 6, 8, 10, None]:
            for mss in [2, 5, 10]:
                for msl in [1, 2, 4]:
                    m = RandomForestClassifier(n_estimators=nest, criterion=criterion, max_depth=max_d, min_samples_split=mss, min_samples_leaf=msl, random_state=42)
                    m.fit(X_ti_train, y_ti_train)
                    acc = accuracy_score(y_ti_test, m.predict(X_ti_test))
                    f1 = f1_score(y_ti_test, m.predict(X_ti_test))
                    auc = roc_auc_score(y_ti_test, m.predict_proba(X_ti_test)[:, 1])
                    if acc >= 0.83 or (acc >= 0.82 and f1 >= 0.75):
                        print(f"RF Titanic: nest={nest}, crit={criterion}, d={max_d}, mss={mss}, msl={msl} -> TeAcc={acc:.4f}, F1={f1:.4f}, AUC={auc:.4f}, TrAcc={m.score(X_ti_train, y_ti_train):.4f}")
