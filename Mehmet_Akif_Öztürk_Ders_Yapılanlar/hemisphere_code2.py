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
    theta_step_deg,
    phi_step_deg
):
    """
    Yarım küre (hemisphere) üzerinde spiral waypoint üretimi
    """

    waypoints = []

    phi = 0.0  # tepe noktasından başlar (z yukarı)

    while phi <= math.pi / 2:  # yarım küre
        for theta_deg in range(0, 360, theta_step_deg):
            theta = math.radians(theta_deg)

            x = center_x + radius * math.sin(phi) * math.cos(theta)
            y = center_y + radius * math.sin(phi) * math.sin(theta)
            z = center_z + radius * math.cos(phi)

            waypoints.append((x, y, z))

        phi += math.radians(phi_step_deg)

    return waypoints


# ==============================
# MAIN
# ==============================
def main():

    # 🔧 GÖREV PARAMETRELERİ
    CENTER_X = 0.0
    CENTER_Y = 0.0
    CENTER_Z = 0.0

    RADIUS = 30.0           # yarım küre yarıçapı (m)

    THETA_STEP = 10         # yatay çözünürlük
    PHI_STEP = 5            # dikey çözünürlük

    # 📍 WAYPOINT ÜRET
    waypoints = hemispherical_spiral(
        CENTER_X,
        CENTER_Y,
        CENTER_Z,
        RADIUS,
        THETA_STEP,
        PHI_STEP
    )

    # 🖨️ KOORDİNATLAR
    print("Hemispherical Spiral Waypoints:\n")
    for i, (x, y, z) in enumerate(waypoints):
        print(f"{i+1:03d} -> X:{x:7.2f} | Y:{y:7.2f} | Z:{z:7.2f}")

    # 📊 3D GÖRSEL
    x_vals = [p[0] for p in waypoints]
    y_vals = [p[1] for p in waypoints]
    z_vals = [p[2] for p in waypoints]

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_vals, y_vals, z_vals, marker='o')

    ax.set_title("Hemispherical Spiral Drone Path")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")

    plt.show()


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    main()
