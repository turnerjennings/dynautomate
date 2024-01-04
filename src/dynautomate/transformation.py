import numpy as np

# define class to build node transformation operators
class Transformation:
    def __init__(self):
        self.matrix = np.eye(4)

    def scale(self, sx: float, sy: float, sz: float):
        scale_matrix = np.array(
            [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]]
        )
        self.matrix = scale_matrix @ self.matrix

    def translate(self, tx: float, ty: float, tz: float):
        translate_matrix = np.array(
            [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]]
        )
        self.matrix = translate_matrix @ self.matrix

    def rotate(self, p1: list[float], p2: list[float], angle):
        # convert angle to radians and calculate trig terms
        angle_rad = angle * 3.1415926535 / 180
        c = np.cos(angle_rad)
        s = np.sin(angle_rad)
        nc = 1 - c

        # define unit vector between p1 and p2
        omega = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]], dtype=float)
        omega /= np.linalg.norm(omega)

        # define matrix using rodrigues formula
        wx, wy, wz = omega

        rotate_matrix = np.array(
            [
                [c + (wx * wx) * nc, wx * wy * nc - wz * s, wy * s + wx * wz * nc, 0],
                [wz * s + wx * wy * nc, c + (wy * wy) * nc, -wx * s + wy * wz * nc, 0],
                [-wy * s + wx * wz * nc, wx * s + wy * wz * nc, c + (wz * wz) * nc, 0],
                [0, 0, 0, 1],
            ]
        )
        print(f"Rotate matrix:\n {rotate_matrix}")

        # clean small values
        rotate_matrix[np.abs(rotate_matrix) < 1e-9] = 0

        self.matrix = rotate_matrix @ self.matrix

    def info(self):
        print(f"Transformation matrix:\n{self.matrix}")