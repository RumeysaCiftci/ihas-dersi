import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# =========================
# 1. DATA OKUMA
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "flights.csv")

df = pd.read_csv(DATA_PATH, sep=";", engine="python")
df.columns = df.columns.str.strip()

print("İlk satır sayısı:", len(df))

# =========================
# 2. SAYISALA ÇEVİR
# =========================
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("Toplam NaN sayısı:", df.isna().sum().sum())

# =========================
# 3. POWER (TARGET)
# =========================
df["power"] = df["battery_voltage"] * df["battery_current"]

# =========================
# 4. GİRİŞ / ÇIKIŞ
# =========================
X = df.drop(columns=["power"]).values
y = df["power"].values.reshape(-1, 1)

# =========================
# 5. NaN DOLDURMA (SATIR SİLME YOK)
# =========================
imputer_X = SimpleImputer(strategy="median")
imputer_y = SimpleImputer(strategy="median")

X = imputer_X.fit_transform(X)
y = imputer_y.fit_transform(y).ravel()

print("NaN sonrası satır:", X.shape[0])
print("Payload = 0 satır sayısı:", (df["payload"] == 0).sum())

# =========================
# 6. ÖLÇEKLEME
# =========================
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X = scaler_X.fit_transform(X)
y = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

# =========================
# 7. TRAIN / TEST
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train satır:", X_train.shape[0])
print("Test satır :", X_test.shape[0])

# =========================
# 8. DNN (MLP)
# =========================
model = MLPRegressor(
    hidden_layer_sizes=(64, 64, 32),
    activation="relu",
    solver="adam",
    learning_rate_init=0.0005,
    max_iter=200,
    batch_size=512,
    random_state=42,
    verbose=True
)

# =========================
# 9. EĞİTİM
# =========================
model.fit(X_train, y_train)

# =========================
# 10. TEST
# =========================
y_pred_scaled = model.predict(X_test)

# Ölçeği geri al
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
y_test_real = scaler_y.inverse_transform(y_test.reshape(-1, 1))

mse = mean_squared_error(y_test_real, y_pred)
rmse = np.sqrt(mse)

print("\nTEST MSE :", mse)
print("TEST RMSE:", rmse)
