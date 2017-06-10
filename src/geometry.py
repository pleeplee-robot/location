"""
This file contains the geometry concepts needed for the computations.
"""
import math

PRECISION = 4
class Point:

    # Thresold to determine that two points are similar (distance < 15cm)
    _threshold = 0.15

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y)

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return round(math.sqrt(dx**2 + dy**2), PRECISION)

    def __eq__(self, other):
        return self.distance(other) < self._threshold

# Rectangle triangle to ease computations
class Triangle:

    # with alph the angle from actual direction to LED
    def __init__(self, data):
        # angle from the point we try to find the location
        self.angleP = data.angle
        # corner of the perimeter
        self.point = data.led.point
        self.color = data.led.color
        # offset to the standard direction
        self.offset = 0

    # angle from the led at a corner of the perimeter
    def cornerAngle(self):
        return 90.0 - self.angleP

    def __str__(self):
        return "TRIANGLE(%s ;%s)"%(self.angleP, self.cornerAngle())


