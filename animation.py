import random
import colorsys
from time import time
from typing import Tuple


class Animation:
    def __init__(self):
        pass

    def __str__(self):
        return f"{type(self).__name__}"

    def update(self, index, count):
        return (0, 0, 0)

    def name(self):
        return "None"


class Off(Animation):
    def __init__(self):
        super(Off, self).__init__()

    def name(self):
        return "off"


class Steady(Animation):
    def __init__(self, color):
        super(Steady, self).__init__()
        (r, g, b) = color
        self.r = r
        self.g = g
        self.b = b

    def update(self, index, count):
        return (self.r, self.g, self.b)

    def __str__(self):
        return f"{type(self).__name__}({self.r}, {self.g}, {self.b})"

    def name(self):
        return "steady"


class RandomSingle(Animation):
    """
        by Max & Lightmoll (https://lght.ml)
        from 2022-06-08
    """

    def __init__(self, color):
        super().__init__()
        self.PERIOD = 4 * 30  # frames
        self.color = self._rand_color()
        self.last_colors = []
        self.frame_counter = 0

    def update(self, index: int, count: int) -> Tuple[int, int, int]:
        if index == 0:
            if ((self.frame_counter % self.PERIOD) == 0):
                self.last_colors = []
                for _ in range(count):
                    self.last_colors.append(self._rand_color())
            self.frame_counter += 1
        try:
            return self.last_colors[index]
        except IndexError:
            print("INDEX ERROR: ", index, len(self.last_colors))
            raise Exception(f"{index}, {len(self.last_colors)}")

    def _rand_color(self):
        return (
            round(random.random() * 255),
            round(random.random() * 255),
            round(random.random() * 255)
        )

    def __str__(self):
        return "randomsingle"

    def name(self):
        return str(self)


class TwoColor(Steady):
    """
        by Max & Lightmoll (https://lght.ml)
        from 2022-06-08
    """

    def __init__(self, color):
        super().__init__(color)
        self.start_time = time()
        self.PERIOD = 0.5  # s
        self.COL_1 = color  # input color

        self.COL_2 = (255 - self.r, 255 - self.g, 255 - self.b)  # compl. color

        # of lights

    def update(self, index: int, count: int) -> Tuple[int, int, int]:
        time_diff = time() - self.start_time
        # r,g,b
        color = (0, 0, 0)

        if (self.PERIOD / 2 > (time_diff % self.PERIOD)):
            color = self.COL_1
        else:
            color = self.COL_2
        return color

    def __str__(self):
        return "twocolor"

    def name(self):
        return str(self)


class Caramelldansen(Steady):
    """
        by Max & Lightmoll (https://lght.ml)
        from 2022-06-08
    """

    def __init__(self, color):
        super().__init__(color)
        self.start_time = time()
        self.PERIOD = int(0.42 * 30)  # frames
        self.COLORS = [
            (230, 50, 50),
            (255, 0, 0),
            (50, 230, 50),
            (0, 255, 0),
            (50, 50, 230),
            (0, 0, 255)
        ]
        """
        self.COLORS = [
            (255,0,0),
            (0,255,0),
            (0,0,255)
        ]
        """
        self.color_index = 0
        self.frame_counter = 0

    def update(self, index: int, count: int) -> Tuple[int, int, int]:
        time_diff = round(time() - self.start_time)
        # r,g,b
        if index == 0:
            self.frame_counter += 1

        if (((self.frame_counter % self.PERIOD) == 0) and index == 0):
            self.color_index += 1

        if (self.color_index == len(self.COLORS)):
            # self.frame_counter = 0 #prevent big numbers
            self.color_index = 0

        return self.COLORS[self.color_index]

    def __str__(self):
        # when is this endpoint called?
        return "caramelldansen"

    def name(self):
        return str(self)


class FadeTo(Steady):
    def __init__(self, color, t=2.0):
        super(FadeTo, self).__init__(color)
        self.t = t
        self.start = time()

    def update(self, index, count):
        h = (time() - self.start) / self.t
        h = min(h, 1.0)
        return (int(self.r * h), int(self.g * h), int(self.b * h))

    def __str__(self):
        return f"{type(self).__name__}({self.r}, {self.g}, {self.b}, {self.t:.2f})"

    def name(self):
        return "fadeTo"


class RotatingRainbow(Animation):
    def __init__(self, looptime=10.0):
        super(RotatingRainbow, self).__init__()
        self.looptime = looptime
        pass

    def update(self, index, count):
        """
        One full round takes self.looptime seconds, each RGB is offset in a circle
        :param index:
        :param count:
        :return:
        """
        hue = (time() / self.looptime + (index + 0.0) / count) % 1.0
        rgb = hsv_to_rgb(hue, 1, 1)
        return rgb

    def __str__(self):
        return f"{type(self).__name__}"

    def name(self):
        return "rainbow"


class Chase(Steady):
    def __init__(self, color, looptime=1.0):
        super(Chase, self).__init__(color)
        self.looptime = looptime

    def update(self, index, count):
        angle = (time() / self.looptime + (index + 0.0) / count) % 1.0
        l = 1 - min(abs(angle - 1 / count) * .9, 1.0 / count) * count
        # print(f"f({index}, {angle:.2f}) -> {l:.2f}")
        return (int(self.r * l), int(self.g * l), int(self.b * l))

    def __str__(self):
        return f"{type(self).__name__}({self.r}, {self.g}, {self.b}, {self.looptime:.2f})"

    def name(self):
        return "chase"


class ChaseRandom(Animation):
    def __init__(self, color, looptime=1.0):
        super(Chase, self).__init__(color)
        self.looptime = looptime

    def update(self, index, count):
        angle = (time() / self.looptime + (index + 0.0) / count) % 1.0
        l = 1 - min(abs(angle - 1 / count) * .9, 1.0 / count) * count
        # print(f"f({index}, {angle:.2f}) -> {l:.2f}")
        return (int(self.r * l), int(self.g * l), int(self.b * l))

    def __str__(self):
        return f"{type(self).__name__}({self.r}, {self.g}, {self.b}, {self.looptime:.2f})"

    def name(self):
        return "chase"


class Numbers(Animation):
    def __init__(self, digits, color):
        super(Numbers, self).__init__()
        available = "0123456789abcdef -A"
        if type(digits) == str:
            self.digits = []
            digits = digits[:11]
            for d in digits.lower()[::-1]:
                c = available.find(d)
                self.digits.append(c if c != -1 else 10)
        else:
            self.digits = digits
        self.color = color
        self.segments_for_digits = [
            # 1, 2, 3, 4, 5, 6, 7
            [1, 1, 1, 1, 1, 1, 0, 0],  # 0
            [0, 0, 0, 1, 1, 0, 0, 0],  # 1
            [1, 0, 1, 1, 0, 1, 1, 0],  # 2
            [0, 0, 1, 1, 1, 1, 1, 0],  # 3
            [0, 1, 0, 1, 1, 0, 1, 0],  # 4
            [0, 1, 1, 0, 1, 1, 1, 0],  # 5
            [1, 1, 1, 0, 1, 1, 1, 0],  # 6
            [0, 0, 1, 1, 1, 0, 0, 0],  # 7
            [1, 1, 1, 1, 1, 1, 1, 0],  # 8
            [0, 1, 1, 1, 1, 1, 1, 0],  # 9
            [1, 1, 1, 1, 1, 0, 1, 0],  # 10 A
            [1, 1, 0, 0, 1, 1, 1, 0],  # 11 b
            [1, 1, 1, 0, 0, 1, 0, 0],  # 12 C
            [1, 0, 0, 1, 1, 1, 1, 0],  # 13 d
            [1, 1, 1, 0, 0, 1, 1, 0],  # 14 e
            [1, 1, 1, 0, 0, 0, 1, 0],  # 15 f
            [0, 0, 0, 0, 0, 0, 0, 0],  # 16 " "
            [0, 0, 0, 0, 0, 0, 1, 0],  # 17 -
        ]

    def update(self, index, count):
        if index / 8 >= len(self.digits):
            return (0, 0, 0)
        n = self.digits[int(index / 8)]
        s = self.segments_for_digits[n][index % 8]
        return self.color if s != 0 else (0, 0, 0)


def hsv_to_rgb(h, s, v):
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    return [int(r * 255), int(g * 255), int(b * 255)]


def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
