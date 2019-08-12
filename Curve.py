import numpy as np


class Curve:
    def __init__(self, omega_x, omega_y):
        if omega_x < 0 or omega_y < 0:
            Exception("Angular Frequency must be positive")
        self.omega_x = omega_x
        self.omega_y = omega_y

    # x = a1*sin(omega_x*t) + b1*cos(omega_x*t)
    # y = a2*sin(omega_y*t) + b2*cos(omega_y*t)

    def start(self, x0, y0, vx0, vy0):
        a1 = vx0 / self.omega_x
        a2 = vy0 / self.omega_y
        b1 = x0
        b2 = y0
        return lambda t: np.array([
            a1 * np.sin(self.omega_x * t) + b1 * np.cos(self.omega_x * t),
            a2 * np.sin(self.omega_y * t) + b2 * np.cos(self.omega_y * t)
        ]), np.linalg.norm((a1, b1)), np.linalg.norm((a2, b2))


if __name__ == '__main__':
    curve = Curve(1, 1)
    f = curve.start(1, 0, 0, 1)
    print(f(np.linspace(0, 1, 100)))
