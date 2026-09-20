import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor


# ============================================================
# 1. ĐỌC DỮ LIỆU
# ============================================================

df = pd.read_csv(
    "/kaggle/input/competitions/house-prices-advanced-regression-techniques/train.csv"
)

print("Kích thước dữ liệu:", df.shape)

display(df.head())


# ============================================================
# 2. KIỂM TRA DỮ LIỆU
# ============================================================

if "SalePrice" not in df.columns:
    raise ValueError("Không tìm thấy cột SalePrice")

if df["SalePrice"].isna().any():
    raise ValueError("SalePrice có giá trị thiếu")

if (df["SalePrice"] < 0).any():
    raise ValueError("SalePrice có giá trị âm")


# ============================================================
# 3. TÁCH X VÀ y
# ============================================================

X = df.drop(
    columns=["SalePrice", "Id"],
    errors="ignore"
)

y = df["SalePrice"]


# ============================================================
# 4. CHIA TRAIN / VALIDATION
# ============================================================

Xtr, Xval, ytr, yval = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training:", Xtr.shape)
print("Validation:", Xval.shape)


# ============================================================
# 5. XÁC ĐỊNH CỘT NUMERIC / CATEGORICAL
# ============================================================

numeric = X.select_dtypes(
    include="number"
).columns.tolist()

categorical = X.select_dtypes(
    exclude="number"
).columns.tolist()

print("Số cột numeric:", len(numeric))
print("Số cột categorical:", len(categorical))


# ============================================================
# 6. TIỀN XỬ LÝ DỮ LIỆU
# ============================================================

prep = ColumnTransformer([

    (
        "num",

        SimpleImputer(
            strategy="median"
        ),

        numeric
    ),

    (
        "cat",

        Pipeline([

            (
                "fill",

                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "onehot",

                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            )

        ]),

        categorical
    )

])


# Fit trên training
A = prep.fit_transform(Xtr).astype("float32")

# Transform validation
B = prep.transform(Xval).astype("float32")


# Kiểm tra dữ liệu
if not np.isfinite(A).all():
    raise ValueError(
        "Training data sau tiền xử lý có giá trị không hợp lệ"
    )

if not np.isfinite(B).all():
    raise ValueError(
        "Validation data sau tiền xử lý có giá trị không hợp lệ"
    )


print(
    "Số feature sau One-Hot:",
    A.shape[1]
)


# ============================================================
# 7. HÀM ĐÁNH GIÁ MODEL
# ============================================================

def score(y_true, pred):

    pred = np.asarray(pred).ravel()

    # RMSLE không chấp nhận giá trị âm
    p = np.maximum(pred, 0)

    rmsle = np.sqrt(
        np.mean(
            (
                np.log1p(y_true)
                -
                np.log1p(p)
            ) ** 2
        )
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            pred
        )
    )

    mae = mean_absolute_error(
        y_true,
        pred
    )

    r2 = r2_score(
        y_true,
        pred
    )

    negative_predictions = np.sum(
        pred < 0
    )

    return {

        "RMSLE": rmsle,

        "RMSE": rmse,

        "MAE": mae,

        "R2": r2,

        "Negative Predictions":
            negative_predictions
    }


# ============================================================
# 8. TẠO MODEL
# ============================================================

models = {

    "Decision Tree":

        DecisionTreeRegressor(
            max_depth=8,
            min_samples_leaf=5,
            random_state=42
        ),


    "XGBoost":

        XGBRegressor(
            n_estimators=500,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            tree_method="hist",
            random_state=42,
            n_jobs=2
        )
}


# ============================================================
# 9. TRAIN DECISION TREE + XGBOOST
# ============================================================

results = {}

predictions = {}


for name, model in models.items():

    print()
    print("=" * 50)
    print("Đang train:", name)
    print("=" * 50)

    model.fit(
        A,
        ytr
    )

    pred = model.predict(
        B
    )

    predictions[name] = pred

    results[name] = score(
        yval.to_numpy(),
        pred
    )


# ============================================================
# 10. IMPORT TENSORFLOW
# ============================================================

import tensorflow as tf

# Đảm bảo TensorFlow chỉ dùng CPU
tf.config.set_visible_devices(
    [],
    "GPU"
)

print()
print("TensorFlow version:", tf.__version__)

print(
    "GPU TensorFlow:",
    tf.config.list_physical_devices("GPU")
)


# ============================================================
# 11. CHUẨN HÓA INPUT CHO ANN
# ============================================================

tf.keras.utils.set_random_seed(42)


scale = StandardScaler()

Atr = scale.fit_transform(A)

Bval = scale.transform(B)


# ============================================================
# 12. CHUẨN HÓA TARGET
# ============================================================

ym = float(
    ytr.mean()
)

ys = float(
    ytr.std()
)


ytr_scaled = (
    ytr.to_numpy() - ym
) / ys


# ============================================================
# 13. TẠO ANN
# ============================================================

network = tf.keras.Sequential([

    tf.keras.Input(
        shape=(Atr.shape[1],)
    ),

    tf.keras.layers.Dense(
        128,
        activation="relu"
    ),

    tf.keras.layers.Dropout(
        0.2
    ),

    tf.keras.layers.Dense(
        64,
        activation="relu"
    ),

    tf.keras.layers.Dense(
        1
    )
])


# ============================================================
# 14. COMPILE ANN
# ============================================================

network.compile(

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),

    loss="mse"
)


# ============================================================
# 15. TRAIN ANN
# ============================================================

print()
print("=" * 50)
print("Đang train: ANN")
print("=" * 50)


history = network.fit(

    Atr,

    ytr_scaled,

    validation_split=0.2,

    epochs=200,

    batch_size=32,

    verbose=1,

    callbacks=[

        tf.keras.callbacks.EarlyStopping(

            monitor="val_loss",

            patience=20,

            restore_best_weights=True
        )
    ]
)


# ============================================================
# 16. DỰ ĐOÁN ANN
# ============================================================

ann_pred = (

    network.predict(
        Bval,
        verbose=0
    ).ravel()

    * ys

    + ym
)


predictions["ANN"] = ann_pred


results["ANN"] = score(

    yval.to_numpy(),

    ann_pred
)


# ============================================================
# 17. BẢNG KẾT QUẢ
# ============================================================

results_df = pd.DataFrame(
    results
).T


print()
print("=" * 70)
print("KẾT QUẢ ĐÁNH GIÁ MODEL")
print("=" * 70)


display(
    results_df.style.format({

        "RMSLE": "{:.4f}",

        "RMSE": "{:,.2f}",

        "MAE": "{:,.2f}",

        "R2": "{:.4f}",

        "Negative Predictions":
            "{:.0f}"
    })
)


# ============================================================
# 18. BIỂU ĐỒ ANN TRAINING HISTORY
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.xlabel(
    "Epoch"
)

plt.ylabel(
    "MSE trên giá đã chuẩn hóa"
)

plt.title(
    "ANN Training History"
)

plt.legend()

plt.tight_layout()

plt.show()


# ============================================================
# 19. PREDICTED VS ACTUAL
# ============================================================

fig, axes = plt.subplots(

    1,

    3,

    figsize=(18, 5)
)


for ax, (name, pred) in zip(

    axes,

    predictions.items()
):

    ax.scatter(

        yval,

        pred,

        alpha=0.4,

        s=12
    )


    lim = max(

        np.max(yval),

        np.max(pred)
    )


    ax.plot(

        [0, lim],

        [0, lim],

        "r--"
    )


    ax.set_title(
        name
    )


    ax.set_xlabel(
        "Giá thực tế (USD)"
    )


    ax.set_ylabel(
        "Giá dự đoán (USD)"
    )


plt.tight_layout()

plt.show()


# ============================================================
# 20. RESIDUAL PLOT
# ============================================================

fig, axes = plt.subplots(

    1,

    3,

    figsize=(18, 5)
)


for ax, (name, pred) in zip(

    axes,

    predictions.items()
):

    residual = (

        yval.to_numpy()

        -

        pred
    )


    ax.hist(

        residual,

        bins=35
    )


    ax.axvline(

        0,

        color="red",

        linestyle="--"
    )


    ax.set_title(
        name
    )


    ax.set_xlabel(
        "Sai số: thực tế - dự đoán (USD)"
    )


    ax.set_ylabel(
        "Số căn nhà"
    )


plt.tight_layout()

plt.show()


# ============================================================
# 21. XGBOOST FEATURE IMPORTANCE
# ============================================================

feature_names = (

    prep.get_feature_names_out()
)


importance = pd.Series(

    models[
        "XGBoost"
    ].feature_importances_,

    index=feature_names

).sort_values(

    ascending=False
)


plt.figure(

    figsize=(10, 8)
)


importance.head(
    20
).sort_values().plot.barh()


plt.title(
    "Top 20 XGBoost Feature Importance"
)


plt.xlabel(
    "Importance"
)


plt.tight_layout()

plt.show()


# ============================================================
# 22. HIỂN THỊ TOP 20 FEATURE
# ============================================================

print()
print("=" * 50)
print("TOP 20 FEATURES")
print("=" * 50)


display(

    importance.head(
        20
    ).to_frame(
        "Importance"
    )
)
