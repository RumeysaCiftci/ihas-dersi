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

# =========================
# 2. SAYISALA ÇEVİR
# =========================
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# =========================
# 3. POWER HESABI (TARGET)
# =========================
df["power"] = df["battery_voltage"] * df["battery_current"]

# =========================
# 4. GİRİŞ / ÇIKIŞ
# =========================
X = df.drop(columns=["power"]).values
y = df["power"].values

# =========================
# 5. ÖLÇEKLEME
# =========================
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 6. DNN (MLP) MODELİ
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
# 7. EĞİTİM
# =========================
model.fit(X_train, y_train)

# =========================
# 8. TEST
# =========================
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("\nTEST MSE:", mse)
print("TEST RMSE:", rmse)
