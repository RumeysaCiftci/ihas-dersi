import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

# =========================
# 1. DATA OKUMA
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "flights.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"CSV bulunamadı: {DATA_PATH}")

df = pd.read_csv(DATA_PATH, sep=";", engine="python")
df.columns = df.columns.str.strip()

print("İlk satır sayısı:", len(df))

# =========================
# 2. SAYISALA ÇEVİR
# =========================
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# 3. GEREKLİ SÜTUNLARA GÖRE NaN TEMİZLİĞİ
# (payload = 0 korunur)
# =========================
required_cols = [
    "battery_voltage",
    "battery_current",
    "speed",
    "payload",
    "altitude"
]

df = df.dropna(subset=required_cols)

print("NaN temizliği sonrası satır:", len(df))
print("Payload = 0 satır sayısı:", (df["payload"] == 0).sum())

# =========================
# 4. POWER (TARGET)
# =========================
df["power"] = df["battery_voltage"] * df["battery_current"]

# =========================
# 5. GİRİŞ / ÇIKIŞ
# =========================
X = df.drop(columns=["power"]).values
y = df["power"].values

# =========================
# 6. ÖLÇEKLEME
# =========================
scaler = StandardScaler()
X = scaler.fit_transform(X)

# =========================
# 7. TRAIN / TEST (%80 - %20)
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train satır:", X_train.shape[0])
print("Test satır :", X_test.shape[0])

# =========================
# 8. DNN (MLPRegressor)
# =========================
model = MLPRegressor(
    hidden_layer_sizes=(64, 64, 32),
    activation="relu",
    solver="adam",
    learning_rate_init=0.001,
    max_iter=300,
    batch_size=256,
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
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("\nTEST MSE :", mse)
print("TEST RMSE:", rmse)
