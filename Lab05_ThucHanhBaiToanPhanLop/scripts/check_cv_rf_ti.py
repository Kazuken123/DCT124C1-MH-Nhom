import sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier

titanic_raw = pd.read_csv('Lab05_ThucHanhBaiToanPhanLop/data/train.csv')
titanic_df = titanic_raw.copy()
titanic_df['Sex'] = titanic_df['Sex'].map({'male': 0, 'female': 1})
X_raw_ti = titanic_df[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]
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

for md in [4, 6, 8]:
    for msl in [2, 4]:
        rf = RandomForestClassifier(n_estimators=100, max_depth=md, min_samples_leaf=msl, random_state=42)
        cv = cross_val_score(rf, X_ti_train, y_ti_train, cv=5, scoring='accuracy').mean()
        rf.fit(X_ti_train, y_ti_train)
        print(f"md={md}, msl={msl} -> CV Acc={cv:.4f}, Test Acc={rf.score(X_ti_test, y_ti_test):.4f}")
