import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ==============================
# HEMISPHERICAL SPIRAL
# ==============================
def hemispherical_spiral(
    center_x,
    center_y,
    center_z,
    radius,
    total_turns,
    points_per_turn
):
    """
    total_turns     : yarım küre boyunca kaç tam dönüş (360°)
    points_per_turn : her dönüşte kaç waypoint
    """

    waypoints = []

    total_points = total_turns * points_per_turn

    for i in range(total_points + 1):

        # 0 → 1 arası normalize
        t = i / total_points

        # Açılar
        theta = 2 * math.pi * total_turns * t     # yatay dönüş
        phi = (math.pi / 2) * t                   # 0 → 90° (yarım küre)

        # Küresel → Kartezyen
        x = center_x + radius * math.sin(phi) * math.cos(theta)
        y = center_y + radius * math.sin(phi) * math.sin(theta)
        z = center_z + radius * math.cos(phi)

        waypoints.append((x, y, z))

    return waypoints


# ==============================
# MAIN
# ==============================
def main():

    # 🔧 SENİN KONTROLÜNDE
    CENTER_X = 0.0
    CENTER_Y = 0.0
    CENTER_Z = 0.0

    RADIUS = 30.0

    TOTAL_TURNS = 5        # 🔁 KAÇ TUR ATSIN
    POINTS_PER_TURN = 40   # çözünürlük

    waypoints = hemispherical_spiral(
        CENTER_X,
        CENTER_Y,
        CENTER_Z,
        RADIUS,
        TOTAL_TURNS,
        POINTS_PER_TURN
    )

    # 🖨️ Yazdır
    print(f"Hemispherical Spiral ({TOTAL_TURNS} turns):\n")
    for i, (x, y, z) in enumerate(waypoints):
        print(f"{i+1:03d} -> X:{x:7.2f} | Y:{y:7.2f} | Z:{z:7.2f}")

    # 📊 3D Çizim
    x_vals = [p[0] for p in waypoints]
    y_vals = [p[1] for p in waypoints]
    z_vals = [p[2] for p in waypoints]

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_vals, y_vals, z_vals, marker='o')

    ax.set_title(f"Hemispherical Spiral – {TOTAL_TURNS} Turns")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    plt.show()


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    main()
