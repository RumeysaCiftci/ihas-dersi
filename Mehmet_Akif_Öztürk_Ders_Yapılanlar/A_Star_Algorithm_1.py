import heapq
import matplotlib.pyplot as plt
import numpy as np

# =============================
# GRID & PARAMETRELER
# =============================
GRID_SIZE = 20

start = (0, 0)
goal = (19, 19)

# 0 = boş, 1 = engel
grid = np.zeros((GRID_SIZE, GRID_SIZE))

# =============================
# ENGELLER
# =============================

# Dikey duvarlar
grid[5:15, 8] = 1
grid[5:15, 19] = 1

# Yatay duvarlar
grid[12, 3:14] = 1
grid[3, 3:19] = 1

# Çapraz engel (6–13 arası, sağa offset)
offset = 6
for i in range(6, 14):
    if 0 <= i + offset < GRID_SIZE:
        grid[i, i + offset] = 1

# Geçit
grid[12, 10] = 0

# =============================
# HEURISTIC (Octile Distance)
# =============================
def heuristic(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return (dx + dy) + (np.sqrt(2) - 2) * min(dx, dy)

# =============================
# A* ALGORİTMASI (8 YÖNLÜ)
# =============================
def astar(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        x, y = current

        neighbors = [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1),
            (x+1, y+1), (x+1, y-1),
            (x-1, y+1), (x-1, y-1)
        ]

        for nx, ny in neighbors:
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx, ny] == 1:
                    continue

                # Çapraz hareket kontrolü
                if nx != x and ny != y:
                    # köşe kesme engeli
                    if grid[nx, y] == 1 or grid[x, ny] == 1:
                        continue
                    step_cost = np.sqrt(2)
                else:
                    step_cost = 1

                tentative_g = g_score[current] + step_cost

                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    came_from[(nx, ny)] = current
                    g_score[(nx, ny)] = tentative_g
                    f = tentative_g + heuristic((nx, ny), goal)
                    heapq.heappush(open_set, (f, (nx, ny)))

    return None

# =============================
# PATH GERİ OLUŞTURMA
# =============================
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

# =============================
# ÇALIŞTIR
# =============================
path = astar(start, goal, grid)

# =============================
# PLOT
# =============================
plt.figure(figsize=(6, 6))
plt.imshow(grid, cmap="gray_r")

plt.xticks(np.arange(-0.5, GRID_SIZE, 1))
plt.yticks(np.arange(-0.5, GRID_SIZE, 1))
plt.grid(True)

if path:
    x = [p[0] for p in path]
    y = [p[1] for p in path]
    plt.plot(y, x, linewidth=3, label="A* Yolu")

plt.scatter(start[1], start[0], s=120, label="Başlangıç")
plt.scatter(goal[1], goal[0], s=120, label="Hedef")

plt.title("A* Algoritması (8 Yönlü + Çapraz Engel)")
plt.legend()
plt.gca().invert_yaxis()
plt.show()
