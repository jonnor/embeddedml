import math
import time

class FastAtan2:
    def __init__(self, size=10):
        self.NQ = size  # Size of quadrant I LUT
        self.lut = self._build_lut()

    def _build_lut(self):
        lut = [[0 for _ in range(self.NQ)] for _ in range(self.NQ)]
        for i in range(self.NQ):
            for j in range(self.NQ):
                y = i / (self.NQ - 1)
                x = j / (self.NQ - 1)
                if x == 0 and y == 0:
                    angle = 0.0
                else:
                    angle = math.degrees(math.atan2(y, x))
                lut[i][j] = int(round(angle * 10))  # store in degrees * 10
        return lut

    @micropython.native
    def compute(self, y : float, x : float):
        if x == 0 and y == 0:
            return 0  # 0° in fixed-point

        abs_y = abs(y)
        abs_x = abs(x)
        max_val = max(abs_y, abs_x, 1e-6)

        ny = abs_y / max_val
        nx = abs_x / max_val

        i = int(ny * (self.NQ - 1) + 0.5)
        j = int(nx * (self.NQ - 1) + 0.5)

        i = min(max(i, 0), self.NQ - 1)
        j = min(max(j, 0), self.NQ - 1)

        angle = self.lut[i][j]

        # Reflect based on quadrant
        if x >= 0 and y >= 0:      # Q1
            return angle
        elif x < 0 and y >= 0:     # Q2
            return 1800 - angle
        elif x < 0 and y < 0:      # Q3
            return -1800 + angle
        else:                      # Q4
            return -angle


if __name__ == "__main__":
    fast_atan = FastAtan2(size=10)

    # Example: simulate accelerometer values
    a_x = 0.55
    a_y = -0.607
    a_z = 0.907

    roll_ref = round(math.degrees(math.atan2(a_y, a_z)), 1)
    roll_fast = fast_atan.compute(a_y, a_z) / 10.0

    denominator = math.sqrt(a_y * a_y + a_z * a_z)
    pitch_ref = round(math.degrees(math.atan2(-a_x, denominator)), 1)
    pitch_fast = fast_atan.compute(-a_x, denominator) / 10.0

    print(roll_ref, roll_fast)
    print(pitch_ref, pitch_fast)


    repeats = 10000

    start = time.ticks_us()
    for n in range(repeats):
        f = round(math.degrees(math.atan2(a_x, a_y)))
    ref = time.ticks_diff(time.ticks_us(), start)


    start = time.ticks_us()
    for n in range(repeats):
        f = fast_atan.compute(a_x, a_y)
    lookup = time.ticks_diff(time.ticks_us(), start)

    # XXX: on x86 micropython unix, lookup is 10x slower!
    # probably because doing many more operations in Python, including floating point
    print(ref, lookup)
