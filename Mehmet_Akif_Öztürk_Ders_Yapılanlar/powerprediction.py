# =========================================================
# POWER PREDICTION + MINIMUM POWER ROUTE PLANNING
# =========================================================

import pandas as pd
import numpy as np
import csv
import networkx as nx

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# =========================================================
# 1) CSV OKUMA (TOLERANSLI)
# =========================================================
path = r"C:\Users\RumeysaCiftci\Desktop\12683453\flights.csv"

with open(path, encoding="utf-8", errors="ignore") as f:
    sample = f.read(10000)
    dialect = csv.Sniffer().sniff(sample)

df = pd.read_csv(
    path,
    sep=dialect.delimiter,
    header=0,
    engine="python"
)

print("CSV OKUNDU | Satır, Sütun:", df.shape)

# =========================================================
# 2) STRING -> NUMERIC DÖNÜŞÜM (KRİTİK ADIM)
# =========================================================
numeric_cols = [
    "position_x", "position_y", "position_z",
    "velocity_x", "velocity_y", "velocity_z",
    "linear_acceleration_x", "linear_acceleration_y", "linear_acceleration_z",
    "payload", "altitude"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Bozuk satırları temizle
df = df.dropna(subset=numeric_cols).reset_index(drop=True)

print("Numeric dönüşüm sonrası boyut:", df.shape)

# =========================================================
# 3) FİZİK TABANLI POWER HESABI
# =========================================================
g = 9.81            # yerçekimi (m/s^2)
mass_base = 5.0     # kg (araç gövdesi varsayımı)

df["mass"] = mass_base + df["payload"]

df["velocity_mag"] = np.sqrt(
    df["velocity_x"]**2 +
    df["velocity_y"]**2 +
    df["velocity_z"]**2
)

df["acc_mag"] = np.sqrt(
    df["linear_acceleration_x"]**2 +
    df["linear_acceleration_y"]**2 +
    df["linear_acceleration_z"]**2
)

# Basitleştirilmiş mekanik güç (Watt)
df["power"] = (
    df["mass"] * df["acc_mag"] * df["velocity_mag"] +
    df["mass"] * g * df["velocity_z"].abs()
)

print("Power label oluşturuldu")

# =========================================================
# 4) RANDOM FOREST – POWER PREDICTION
# =========================================================
features = [
    "velocity_mag",
    "acc_mag",
    "payload",
    "altitude"
]

X = df[features].fillna(df[features].mean())
y = df["power"].fillna(df["power"].mean())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

rf = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

df["predicted_power"] = rf.predict(X)

rmse = np.sqrt(mean_squared_error(y_test, rf.predict(X_test)))
print("Power Prediction RMSE:", rmse)

# =========================================================
# 5) GRAPH OLUŞTURMA (ROUTE PLANNING)
# =========================================================
G = nx.DiGraph()

# Node'lar
for i, row in df.iterrows():
    G.add_node(
        i,
        pos=(row["position_x"], row["position_y"], row["position_z"])
    )

# Edge'ler (ardışık noktalar)
for i in range(len(df) - 1):
    cost = (df.loc[i, "predicted_power"] + df.loc[i + 1, "predicted_power"]) / 2
    G.add_edge(i, i + 1, weight=cost)

print("Graph oluşturuldu | Node:", G.number_of_nodes())

# =========================================================
# 6) MINIMUM POWER ROUTE (DIJKSTRA)
# =========================================================
start_node = 0
end_node = len(df) - 1

optimal_path = nx.dijkstra_path(G, start_node, end_node, weight="weight")
total_power_cost = nx.dijkstra_path_length(G, start_node, end_node, weight="weight")

print("\n--- SONUÇ ---")
print("Minimum power route (node index):")
print(optimal_path)
print("Toplam power maliyeti:", total_power_cost)

# =========================================================
# 7) ROTAYI CSV OLARAK KAYDET
# =========================================================
route_df = df.loc[optimal_path, [
    "position_x", "position_y", "position_z", "predicted_power"
]]

route_df.to_csv("minimum_power_route.csv", index=False)
print("Rota kaydedildi: minimum_power_route.csv")
