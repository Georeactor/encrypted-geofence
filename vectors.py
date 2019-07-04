import math


class Vec2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2(self.x * other, self.y * other)
        elif isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        else:
            raise(TypeError("Can only multiply by a scalar (int or float) or another Vec2"))

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2(self.x / other, self.y / other)
        elif isinstance(other, Vec2):
            return Vec2(self.x / other.x, self.y / other.y)
        else:
            raise(TypeError("Can only divide by a scalar (int or float) or another Vec2"))

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        return self/(abs(self))

    def translate(self, vec):
        return self + vec

    def rotate(self, angle):
        return Vec2(
            self.x * math.cos(angle) - self.y * math.sin(angle),
            self.x * math.sin(angle) + self.y * math.cos(angle)
        )

    def rotate_neg(self, angle):
        return Vec2(
            self.x * math.cos(angle) + self.y * math.sin(angle),
            self.x * (-math.sin(angle)) + self.y * math.cos(angle)
        )

    def rotate_around(self, pivot, angle, neg=False):
        translated_vec = self.translate(-pivot)
        if neg is False:
            rotated_vec = translated_vec.rotate(angle)
        else:
            rotated_vec = translated_vec.rotate_neg(angle)
        return rotated_vec.translate(pivot)

    def __str__(self):
        return "(" + str(self.x) + "|" + str(self.y) + ")"


def dot_product(vec_a, vec_b):
    if not isinstance(vec_a, Vec2) or not isinstance(vec_b, Vec2):
        raise TypeError("Dot product can only be calculated with two Vec2")
    return vec_a.x * vec_b.x + vec_a.y * vec_b.y


def get_angle(vec_a, vec_b):
    if not isinstance(vec_a, Vec2) or not isinstance(vec_b, Vec2):
        raise TypeError("Angle calculation can only be done with two Vec2")
    vec_a = vec_a.normalize()
    vec_b = vec_b.normalize()
    return math.acos(dot_product(vec_a, vec_b) / (abs(vec_a) * abs(vec_b)))
