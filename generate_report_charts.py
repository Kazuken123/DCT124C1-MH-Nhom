import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('figures_report', exist_ok=True)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# -------------------------------------------------------------
# Hinh 1: Phan bo bien muc tieu Target
# -------------------------------------------------------------
def plot_target_distribution():
    classes = ['Graduate', 'Dropout', 'Enrolled']
    train_counts = [1767, 1137, 635]
    test_counts = [442, 284, 159]

    x = np.arange(len(classes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)
    bars1 = ax.bar(x - width/2, train_counts, width, label='Tap huan luyen: 3.539 mau', color='#4A6572')
    bars2 = ax.bar(x + width/2, test_counts, width, label='Tap kiem tra: 885 mau', color='#F9AA33')

    ax.set_ylabel('So luong sinh vien')
    ax.set_title('Phan bo so luong cac lop muc tieu Target')
    ax.set_xticks(x)
    ax.set_xticklabels(classes)
    ax.legend(frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in bars1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 20, f'{yval:,}', ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 20, f'{yval:,}', ha='center', va='bottom', fontsize=9)

    ax.set_ylim(0, 2100)
    plt.tight_layout()
    fig.savefig('figures_report/fig1_target_distribution.png')
    plt.close()
    print("Generated fig1_target_distribution.png")

# -------------------------------------------------------------
# Hinh 2: Ty le bo hoc theo cac dac trung then chot (EDA)
# -------------------------------------------------------------
def plot_eda_correlation():
    categories = [
        'Diem HK2 = 0', 'Diem HK2 > 0',
        'No hoc phi', 'Khong no\nhoc phi',
        'Khong co\nhoc bong', 'Co hoc bong'
    ]
    rates = [83.40, 19.37, 64.01, 28.19, 38.64, 12.86]
    colors = ['#D32F2F', '#388E3C', '#D32F2F', '#388E3C', '#E65100', '#1976D2']

    fig, ax = plt.subplots(figsize=(8.0, 4.3), dpi=300)
    bars = ax.bar(categories, rates, color=colors, width=0.52)

    ax.set_ylabel('Ty le sinh vien bo hoc: %')
    ax.set_title('Ty le bo hoc theo tinh trang diem so, no hoc phi va hoc bong')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1.8, f'{yval:.2f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    fig.savefig('figures_report/fig2_eda_correlation.png')
    plt.close()
    print("Generated fig2_eda_correlation.png")

# -------------------------------------------------------------
# Hinh 3: So sanh Macro-F1 giua 11 luot chay thuc nghiem
# -------------------------------------------------------------
def plot_model_comparison():
    models = [
        'DummyClassifier v1 - Da so',
        'DummyClassifier v2 - Phan tang',
        'Decision Tree v1 - Co dinh',
        'Decision Tree v2 - One-Hot',
        'LR Ablation B - Bo hoc ky 2',
        'Decision Tree v2 - Nested Tuned',
        'Random Forest v1 - 100 cay',
        'XGBoost v1 - 100 cay',
        'Logistic Regression v1 - Tieu chuan',
        'LR Ablation C - Them dac trung',
        'Logistic Regression v2 - Can bang lop'
    ]
    f1_scores = [0.2220, 0.3383, 0.6472, 0.6586, 0.6578, 0.6783, 0.6852, 0.6994, 0.6997, 0.7031, 0.7067]
    colors = [
        '#B0BEC5', '#90A4AE', '#78909C', '#607D8B', '#FF7043',
        '#4DB6AC', '#26A69A', '#42A5F5', '#1E88E5', '#1565C0', '#0D47A1'
    ]

    fig, ax = plt.subplots(figsize=(8.2, 5.2), dpi=300)
    y_pos = np.arange(len(models))
    bars = ax.barh(y_pos, f1_scores, color=colors, height=0.65)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(models, fontsize=9)
    ax.set_xlabel('Diem Macro-F1 kiem dinh cheo 5 fold')
    ax.set_title('So sanh Macro-F1 giua cac mo hinh hoc may tren tap huan luyen')
    ax.set_xlim(0, 0.85)
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.01, bar.get_y() + bar.get_height()/2.0, f'{w:.4f}', ha='left', va='center', fontsize=8.5, fontweight='bold')

    plt.tight_layout()
    fig.savefig('figures_report/fig3_model_macro_f1_comparison.png')
    plt.close()
    print("Generated fig3_model_macro_f1_comparison.png")

# -------------------------------------------------------------
# Hinh 4: So sanh ma tran nham lan OOF: LR v1 vs LR v2
# -------------------------------------------------------------
def plot_confusion_matrices():
    cm_v1 = np.array([
        [881, 102, 154],
        [155, 240, 240],
        [68, 76, 1623]
    ])
    cm_v2 = np.array([
        [837, 204, 96],
        [107, 377, 151],
        [83, 249, 1435]
    ])
    labels = ['Dropout', 'Enrolled', 'Graduate']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 4.2), dpi=300)

    # Subplot 1: LR v1
    im1 = ax1.imshow(cm_v1, interpolation='nearest', cmap=plt.cm.Blues)
    ax1.set_title('Logistic Regression v1\nKhong ap dung can bang lop')
    ax1.set_xticks(np.arange(len(labels)))
    ax1.set_yticks(np.arange(len(labels)))
    ax1.set_xticklabels(labels)
    ax1.set_yticklabels(labels)
    ax1.set_xlabel('Du doan')
    ax1.set_ylabel('Thuc te')
    for i in range(len(labels)):
        for j in range(len(labels)):
            val = cm_v1[i, j]
            color = 'white' if val > 800 else 'black'
            ax1.text(j, i, f'{val}', ha='center', va='center', color=color, fontweight='bold')

    # Subplot 2: LR v2
    im2 = ax2.imshow(cm_v2, interpolation='nearest', cmap=plt.cm.Blues)
    ax2.set_title('Logistic Regression v2\nCo ap dung can bang lop balanced')
    ax2.set_xticks(np.arange(len(labels)))
    ax2.set_yticks(np.arange(len(labels)))
    ax2.set_xticklabels(labels)
    ax2.set_yticklabels(labels)
    ax2.set_xlabel('Du doan')
    ax2.set_ylabel('Thuc te')
    for i in range(len(labels)):
        for j in range(len(labels)):
            val = cm_v2[i, j]
            color = 'white' if val > 800 else 'black'
            ax2.text(j, i, f'{val}', ha='center', va='center', color=color, fontweight='bold')

    plt.tight_layout()
    fig.savefig('figures_report/fig4_confusion_matrix_lr_v1_v2.png')
    plt.close()
    print("Generated fig4_confusion_matrix_lr_v1_v2.png")

# -------------------------------------------------------------
# Hinh 5: Kiem toan qua khop: Train-Validation Gap
# -------------------------------------------------------------
def plot_overfitting_audit():
    models = ['Random Forest v1', 'Decision Tree v2 - Tuned', 'Logistic Regression v1']
    train_scores = [1.0000, 0.7088, 0.7556]
    val_scores = [0.6852, 0.6783, 0.6997]
    gaps = [0.3148, 0.0305, 0.0559]

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    b1 = ax.bar(x - width/2, train_scores, width, label='Train Macro-F1', color='#E53935')
    b2 = ax.bar(x + width/2, val_scores, width, label='Validation Macro-F1', color='#1E88E5')

    ax.set_ylabel('Diem Macro-F1')
    ax.set_title('Kiem toan hien tuong hoc qua khop giua Tap huan luyen va Kiem dinh')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylim(0, 1.28)
    ax.legend(loc='upper right', frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for i, bar in enumerate(b1):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, h + 0.02, f'{h:.4f}', ha='center', va='bottom', fontsize=8.5)
    for i, bar in enumerate(b2):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, h + 0.02, f'{h:.4f}', ha='center', va='bottom', fontsize=8.5)
        gap_val = gaps[i]
        ax.text(x[i], max(train_scores[i], val_scores[i]) + 0.07, f'Gap: {gap_val:.4f}\n{gap_val*100:.1f}%', ha='center', va='bottom', fontsize=8, color='#B71C1C', fontweight='bold')

    plt.tight_layout()
    fig.savefig('figures_report/fig5_train_val_gap_overfitting.png')
    plt.close()
    print("Generated fig5_train_val_gap_overfitting.png")

if __name__ == '__main__':
    plot_target_distribution()
    plot_eda_correlation()
    plot_model_comparison()
    plot_confusion_matrices()
    plot_overfitting_audit()
