import heapq
import matplotlib.pyplot as plt
import numpy as np

# Grid boyutu
GRID_SIZE = 20

# Başlangıç ve hedef
start = (0, 0)
goal = (19, 19)

# Manhattan heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* algoritması
def astar(start, goal):
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

        for neighbor in neighbors:
            nx, ny = neighbor
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

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
path = astar(start, goal)

# ---------- PLOT ----------
grid = np.zeros((GRID_SIZE, GRID_SIZE))

plt.figure(figsize=(6, 6))
plt.imshow(grid, cmap="gray_r")

# Grid çizgileri
plt.xticks(np.arange(-0.5, GRID_SIZE, 1))
plt.yticks(np.arange(-0.5, GRID_SIZE, 1))
plt.grid(True)

# Yol çizimi
if path:
    x_coords = [p[0] for p in path]
    y_coords = [p[1] for p in path]
    plt.plot(y_coords, x_coords, linewidth=3)  # yol
    plt.scatter(start[1], start[0], marker="o", s=100)  # başlangıç
    plt.scatter(goal[1], goal[0], marker="X", s=100)   # hedef

plt.title("A* Algoritması - 20x20 Engelsiz Grid")
plt.gca().invert_yaxis()
plt.show()
import heapq
import matplotlib.pyplot as plt
import numpy as np

# Grid boyutu
GRID_SIZE = 20

# Başlangıç ve hedef
start = (0, 0)
goal = (19, 19)

# Manhattan heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* algoritması
def astar(start, goal):
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

        for neighbor in neighbors:
            nx, ny = neighbor
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

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
path = astar(start, goal)

# ---------- PLOT ----------
grid = np.zeros((GRID_SIZE, GRID_SIZE))

plt.figure(figsize=(6, 6))
plt.imshow(grid, cmap="gray_r")

# Grid çizgileri
plt.xticks(np.arange(-0.5, GRID_SIZE, 1))
plt.yticks(np.arange(-0.5, GRID_SIZE, 1))
plt.grid(True)

# Yol çizimi
if path:
    x_coords = [p[0] for p in path]
    y_coords = [p[1] for p in path]
    plt.plot(y_coords, x_coords, linewidth=3)  # yol
    plt.scatter(start[1], start[0], marker="o", s=100)  # başlangıç
    plt.scatter(goal[1], goal[0], marker="X", s=100)   # hedef

plt.title("A* Algoritması - 20x20 Engelsiz Grid")
plt.gca().invert_yaxis()
plt.show()
