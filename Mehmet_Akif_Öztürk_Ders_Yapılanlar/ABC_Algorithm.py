import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# =========================
# 1. DOSYA YOLU
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "flwights.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"CSV bulunamadı: {DATA_PATH}")

# =========================
# 2. CSV OKUMA
# =========================
df = pd.read_csv(DATA_PATH, sep=";", engine="python")

# sütun adlarını temizle
df.columns = df.columns.str.strip()

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# =========================
# 3. TÜM SÜTUNLARI SAYISALA ÇEVİR
# =========================
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

numeric_df = df.dropna()

# =========================
# 4. HEDEF SÜTUN
# =========================
target_col = "altitude"

if target_col not in numeric_df.columns:
    raise ValueError(
        f"Hedef sütun bulunamadı: {target_col}\n"
        f"Mevcut sütunlar: {numeric_df.columns.tolist()}"
    )

X = numeric_df.drop(columns=[target_col]).values
y = numeric_df[target_col].values

# =========================
# 5. ÖLÇEKLEME
# =========================
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

DIM = X_train.shape[1]

# =========================
# 6. FITNESS
# =========================
def fitness_function(weights):
    y_pred = X_train @ weights
    return np.mean((y_train - y_pred) ** 2)

# =========================
# 7. ABC PARAMETRELERİ
# =========================
NUM_BEES = 30
MAX_ITER = 100
LIMIT = 40
LB, UB = -5, 5

# =========================
# 8. BAŞLANGIÇ
# =========================
food = np.random.uniform(LB, UB, (NUM_BEES, DIM))
fit = np.array([fitness_function(f) for f in food])
trial = np.zeros(NUM_BEES)

best = food[np.argmin(fit)]
best_fit = np.min(fit)

# =========================
# 9. ABC DÖNGÜ
# =========================
for it in range(MAX_ITER):

    for i in range(NUM_BEES):
        k = np.random.choice([j for j in range(NUM_BEES) if j != i])
        phi = np.random.uniform(-1, 1, DIM)

        v = food[i] + phi * (food[i] - food[k])
        v = np.clip(v, LB, UB)

        f_v = fitness_function(v)

        if f_v < fit[i]:
            food[i], fit[i], trial[i] = v, f_v, 0
        else:
            trial[i] += 1

    for i in range(NUM_BEES):
        if trial[i] > LIMIT:
            food[i] = np.random.uniform(LB, UB, DIM)
            fit[i] = fitness_function(food[i])
            trial[i] = 0

    if np.min(fit) < best_fit:
        best_fit = np.min(fit)
        best = food[np.argmin(fit)]

    print(f"Iter {it+1}/{MAX_ITER} | Best MSE: {best_fit:.6f}")

# =========================
# 10. TEST
# =========================
test_mse = np.mean((y_test - X_test @ best) ** 2)
print("\nTEST MSE:", test_mse)
