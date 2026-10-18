import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def test():
    print("=== TITANIC ===")
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

    dt_base = DecisionTreeClassifier(random_state=42).fit(X_ti_train, y_ti_train)
    rf_base = RandomForestClassifier(random_state=42).fit(X_ti_train, y_ti_train)

    print(f"Titanic DT Base: Train Acc={accuracy_score(y_ti_train, dt_base.predict(X_ti_train)):.4f}, Test Acc={accuracy_score(y_ti_test, dt_base.predict(X_ti_test)):.4f}, F1={f1_score(y_ti_test, dt_base.predict(X_ti_test)):.4f}")
    print(f"Titanic RF Base: Train Acc={accuracy_score(y_ti_train, rf_base.predict(X_ti_train)):.4f}, Test Acc={accuracy_score(y_ti_test, rf_base.predict(X_ti_test)):.4f}, F1={f1_score(y_ti_test, rf_base.predict(X_ti_test)):.4f}")

    # Test DT tuned
    grid_dt = GridSearchCV(
        DecisionTreeClassifier(random_state=42),
        {'max_depth': [2, 3, 4, 5, 6], 'min_samples_leaf': [1, 2, 4]},
        scoring='accuracy', cv=5
    ).fit(X_ti_train, y_ti_train)
    best_dt = grid_dt.best_estimator_
    print(f"Titanic DT Tuned ({grid_dt.best_params_}): Train Acc={accuracy_score(y_ti_train, best_dt.predict(X_ti_train)):.4f}, Test Acc={accuracy_score(y_ti_test, best_dt.predict(X_ti_test)):.4f}, F1={f1_score(y_ti_test, best_dt.predict(X_ti_test)):.4f}")

    # Test RF tuned
    grid_rf = GridSearchCV(
        RandomForestClassifier(random_state=42),
        {'n_estimators': [50, 100, 150], 'max_depth': [3, 4, 5, 6], 'min_samples_split': [2, 5]},
        scoring='accuracy', cv=5
    ).fit(X_ti_train, y_ti_train)
    best_rf = grid_rf.best_estimator_
    print(f"Titanic RF Tuned ({grid_rf.best_params_}): Train Acc={accuracy_score(y_ti_train, best_rf.predict(X_ti_train)):.4f}, Test Acc={accuracy_score(y_ti_test, best_rf.predict(X_ti_test)):.4f}, F1={f1_score(y_ti_test, best_rf.predict(X_ti_test)):.4f}")

    print("\n=== DIABETES ===")
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

    dt_di_base = DecisionTreeClassifier(random_state=42).fit(X_di_train, y_di_train)
    rf_di_base = RandomForestClassifier(random_state=42).fit(X_di_train, y_di_train)
    print(f"Diabetes DT Base: Train Acc={accuracy_score(y_di_train, dt_di_base.predict(X_di_train)):.4f}, Test Acc={accuracy_score(y_di_test, dt_di_base.predict(X_di_test)):.4f}, F1={f1_score(y_di_test, dt_di_base.predict(X_di_test)):.4f}")
    print(f"Diabetes RF Base: Train Acc={accuracy_score(y_di_train, rf_di_base.predict(X_di_train)):.4f}, Test Acc={accuracy_score(y_di_test, rf_di_base.predict(X_di_test)):.4f}, F1={f1_score(y_di_test, rf_di_base.predict(X_di_test)):.4f}")

    grid_dt_di = GridSearchCV(
        DecisionTreeClassifier(random_state=42),
        {'max_depth': [2, 3, 4, 5, 6], 'min_samples_leaf': [1, 2, 4]},
        scoring='f1', cv=5
    ).fit(X_di_train, y_di_train)
    best_dt_di = grid_dt_di.best_estimator_
    print(f"Diabetes DT Tuned ({grid_dt_di.best_params_}): Train Acc={accuracy_score(y_di_train, best_dt_di.predict(X_di_train)):.4f}, Test Acc={accuracy_score(y_di_test, best_dt_di.predict(X_di_test)):.4f}, F1={f1_score(y_di_test, best_dt_di.predict(X_di_test)):.4f}")

    grid_rf_di = GridSearchCV(
        RandomForestClassifier(random_state=42),
        {'n_estimators': [50, 100, 150], 'max_depth': [3, 4, 5, 6], 'min_samples_split': [2, 5]},
        scoring='f1', cv=5
    ).fit(X_di_train, y_di_train)
    best_rf_di = grid_rf_di.best_estimator_
    print(f"Diabetes RF Tuned ({grid_rf_di.best_params_}): Train Acc={accuracy_score(y_di_train, best_rf_di.predict(X_di_train)):.4f}, Test Acc={accuracy_score(y_di_test, best_rf_di.predict(X_di_test)):.4f}, F1={f1_score(y_di_test, best_rf_di.predict(X_di_test)):.4f}")

if __name__ == '__main__':
    test()
