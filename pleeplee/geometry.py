"""
This file contains the geometry concepts needed for the computations.
"""
from math import sqrt, radians, cos, sin, degrees, acos

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
        return round(sqrt(dx**2 + dy**2), PRECISION)

    def __eq__(self, other):
        return self.distance(other) < self._threshold

    def minus(self, other):
        return (self.X - other.X, self.Y - other.Y)

# Rectangle triangle
class Triangle:

    def __init__(self, angle, point, color):
        # angle from the point we try to find the location
        self.angleP = angle
        # corner of the perimeter
        self.point = point
        self.color = color
        # offset to the standard direction
        self.offset = 0

    # angle from the led at a corner of the perimeter
    def cornerAngle(self):
        return 90.0 - self.angleP

    def __str__(self):
        return "TRIANGLE(%s ;%s)"%(self.angleP, self.cornerAngle())

# Rotate the angle in a counter-clockwise way in degree for angles between
# -180 and 180 degree.
def rotateAngle(alpha):
    if alpha + 45 > 180:
        alpha -= 360
    return alpha + 45

# Rotate a vector in a plane by an angle alpha in degree.
# The formula is obtained by multiplying the rotation matrix with
# the vector(x, y)
def rotateVector(vect, alpha):
    (x, y) = vect
    u = x * cos(radians(alpha)) + y * sin(radians(alpha))
    v = y * cos(radians(alpha)) - x * sin(radians(alpha))
    return (u, v)

# Function to get the angle beween two vectors
def angleBetween2Vects(vect1, vect2):
    (x1, y1) = vect1
    (x2, y2) = vect2
    dotprod = x1 * x2 + y1 * y2
    length1 = sqrt(x1 * x1 + y1 * y1)
    length2 = sqrt(x2 * x2 + y2 * y2)
    cosAngle = dotprod / (length1 * length2)
    return degrees(acos(cosAngle))
