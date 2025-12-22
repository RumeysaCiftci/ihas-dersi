import heapq
import matplotlib.pyplot as plt
import numpy as np

# Grid boyutu
GRID_SIZE = 20

# Başlangıç ve hedef
start = (0, 0)
goal = (19, 19)

# 0 = boş, 1 = engel
grid = np.zeros((GRID_SIZE, GRID_SIZE))

# -------- ENGELLER --------
# Dikey duvar
grid[5:15, 8] = 1
grid[5:15, 19] = 1
# Yatay duvar
grid[12, 3:14] = 1
grid[3, 3:19] = 1
# Bir boşluk bırak (geçit)

offset = 6
for i in range(6, 14):
    if 0 <= i + offset < GRID_SIZE:
        grid[i, i + offset] = 1


grid[12, 10] = 0
# --------------------------

# Manhattan heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* algoritması
def astar(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        x, y = current
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for nx, ny in neighbors:
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx, ny] == 1:  # Engel kontrolü
                    continue

                tentative_g = g_score[current] + 1

                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    came_from[(nx, ny)] = current
                    g_score[(nx, ny)] = tentative_g
                    f_score[(nx, ny)] = tentative_g + heuristic((nx, ny), goal)
                    heapq.heappush(open_set, (f_score[(nx, ny)], (nx, ny)))

    return None

# Yolu geri oluştur
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# A* çalıştır
path = astar(start, goal, grid)

# ---------- PLOT ----------
plt.figure(figsize=(6, 6))
plt.imshow(grid, cmap="gray_r")

# Grid çizgileri
plt.xticks(np.arange(-0.5, GRID_SIZE, 1))
plt.yticks(np.arange(-0.5, GRID_SIZE, 1))
plt.grid(True)

# Yol
if path:
    x = [p[0] for p in path]
    y = [p[1] for p in path]
    plt.plot(y, x, linewidth=3, label="Yol")

# Başlangıç & hedef
plt.scatter(start[1], start[0], marker="o", s=120, label="Başlangıç")
plt.scatter(goal[1], goal[0], marker="X", s=120, label="Hedef")

plt.title("A* Algoritması - 20x20 Grid (Engelli)")
plt.legend()
plt.gca().invert_yaxis()
plt.show()
