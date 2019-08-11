import math

class Vector:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.length = math.sqrt(x * x + y * y)
        self.angle = math.atan2(y, x)

    def __sub__(self, other):
        return Vector(self.X - other.X, self.Y - other.Y)

    def __add__(self, other):
        return Vector(self.X + other.X, self.Y + other.Y)
