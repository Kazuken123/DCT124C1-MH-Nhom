import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn import datasets, svm
from sklearn.preprocessing import StandardScaler

figures_dir = 'Lab05_ThucHanhBaiToanPhanLop/figures'
os.makedirs(figures_dir, exist_ok=True)
data_dir = 'Lab05_ThucHanhBaiToanPhanLop/data'

# 1. Spam Naive Bayes
try:
    spam_data = pd.read_csv(os.path.join(data_dir, 'spam.csv'), encoding='latin-1')
    spam_data = spam_data[['v1', 'v2']].dropna().drop_duplicates(subset='v2')
    spam_data.columns = ['label', 'text']
    spam_data['label'] = spam_data['label'].map({'ham': 0, 'spam': 1})
    X_tr, X_te, y_tr, y_te = train_test_split(spam_data['text'], spam_data['label'], test_size=0.2, random_state=42, stratify=spam_data['label'])
    vec = CountVectorizer()
    X_tr_vec = vec.fit_transform(X_tr)
    X_te_vec = vec.transform(X_te)
    nb_spam = MultinomialNB().fit(X_tr_vec, y_tr)
    cm = confusion_matrix(y_te, nb_spam.predict(X_te_vec))
    
    plt.figure(figsize=(6, 4.5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
    plt.title('Ma tran nham lan: Phan loai Email Spam (MultinomialNB)')
    plt.xlabel('Du doan')
    plt.ylabel('Thuc te')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '2_3_2_spam_cm.png'), dpi=300)
    plt.close()
    print("Exported 2_3_2_spam_cm.png")
except Exception as e:
    print("Spam CM err:", e)

# 2. Customer Behaviour Naive Bayes
try:
    cust = pd.read_csv(os.path.join(data_dir, 'Customer_Behaviour.csv')).drop_duplicates()
    X = cust[['Age', 'EstimatedSalary', 'Gender']].copy()
    X['Age'] = X['Age'].fillna(X['Age'].median())
    X['EstimatedSalary'] = X['EstimatedSalary'].fillna(X['EstimatedSalary'].median())
    X['Gender'] = X['Gender'].fillna(X['Gender'].mode()[0])
    X = pd.get_dummies(X, columns=['Gender'], dtype=int)
    y = cust['Purchased']
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    nb_cust = GaussianNB().fit(X_tr, y_tr)
    cm = confusion_matrix(y_te, nb_cust.predict(X_te))
    
    plt.figure(figsize=(6, 4.5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', xticklabels=['Khong mua', 'Mua'], yticklabels=['Khong mua', 'Mua'])
    plt.title('Ma tran nham lan: Customer Behaviour (GaussianNB)')
    plt.xlabel('Du doan')
    plt.ylabel('Thuc te')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '2_3_3_customer_cm.png'), dpi=300)
    plt.close()
    print("Exported 2_3_3_customer_cm.png")
except Exception as e:
    print("Customer CM err:", e)

# 3. Mushrooms Naive Bayes
try:
    mush = pd.read_csv(os.path.join(data_dir, 'mushrooms.csv')).drop_duplicates()
    X = mush.drop(columns=['class']).copy()
    y = mush['class'].map({'e': 0, 'p': 1})
    X = X.fillna(X.mode().iloc[0])
    X = pd.get_dummies(X, dtype=int)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    nb_mush = MultinomialNB().fit(X_tr, y_tr)
    cm = confusion_matrix(y_te, nb_mush.predict(X_te))
    
    plt.figure(figsize=(6, 4.5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', xticklabels=['An duoc', 'Doc'], yticklabels=['An duoc', 'Doc'])
    plt.title('Ma tran nham lan: Mushroom Classification (MultinomialNB)')
    plt.xlabel('Du doan')
    plt.ylabel('Thuc te')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '2_3_4_mushroom_cm.png'), dpi=300)
    plt.close()
    print("Exported 2_3_4_mushroom_cm.png")
except Exception as e:
    print("Mushroom CM err:", e)

# 4. Digits SVM
try:
    digits = datasets.load_digits()
    X_tr, X_te, y_tr, y_te = train_test_split(digits.data, digits.target, test_size=0.2, random_state=42, stratify=digits.target)
    scaler = StandardScaler()
    X_tr = scaler.fit_transform(X_tr)
    X_te = scaler.transform(X_te)
    clf = svm.SVC(kernel='rbf', C=10, gamma='scale').fit(X_tr, y_tr)
    cm = confusion_matrix(y_te, clf.predict(X_te))
    
    plt.figure(figsize=(7, 5.5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=range(10), yticklabels=range(10))
    plt.title('Ma tran nham lan: Nhan dang chu so viet tay Digits (SVM RBF)')
    plt.xlabel('Du doan')
    plt.ylabel('Thuc te')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '2_2_2_digits_cm.png'), dpi=300)
    plt.close()
    print("Exported 2_2_2_digits_cm.png")
except Exception as e:
    print("Digits CM err:", e)

# 5. Animal Condition SVM
try:
    animal_df = pd.read_csv(os.path.join(data_dir, 'AnimalCondition.csv')).dropna()
    target_c = animal_df.columns[-1]
    X = animal_df.drop(columns=[target_c])
    X = pd.get_dummies(X, drop_first=True, dtype=int)
    y = animal_df[target_c]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_tr = scaler.fit_transform(X_tr)
    X_te = scaler.transform(X_te)
    clf = svm.SVC(kernel='rbf', C=10).fit(X_tr, y_tr)
    cm = confusion_matrix(y_te, clf.predict(X_te))
    
    plt.figure(figsize=(6, 4.5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Purples')
    plt.title('Ma tran nham lan: Animal Condition (SVM)')
    plt.xlabel('Du doan')
    plt.ylabel('Thuc te')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '2_2_4_animal_cm.png'), dpi=300)
    plt.close()
    print("Exported 2_2_4_animal_cm.png")
except Exception as e:
    print("Animal CM err:", e)
