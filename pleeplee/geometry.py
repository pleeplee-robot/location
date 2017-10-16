#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# AUTHOR  : Loïc Banet                                   #
# SUMMARY : Contain the geometry concepts needed for the #
#           computations                                 #
##########################################################

import shapely.geometry

from math import atan2, cos, degrees, radians, sin, sqrt

PRECISION = 3


class Point:

    # Thresold to determine that two points are similar (distance < 15cm)
    _threshold = 0.1

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __str__(self):
        return "Point(%s,%s)" % (self.X, self.Y)

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return round(sqrt(dx**2 + dy**2), PRECISION)

    def __eq__(self, other):
        return (abs(self.X - other.X) < self._threshold
                and abs(self.Y - other.Y) < self._threshold)

    def minus(self, other):
        return (self.X - other.X, self.Y - other.Y)

    def toShapely(self):
        return shapely.geometry.point.Point(self.X, self.Y)


# Rotate a vector in a plane by an angle alpha in degree.
# The rotation is clockwise.
# The formula is obtained by multiplying the rotation matrix with
# the vector(x, y)
def rotateVector(vect, alpha):
    (x, y) = vect
    u = round(x * cos(radians(alpha)) + y * sin(radians(alpha)), PRECISION)
    v = round(y * cos(radians(alpha)) - x * sin(radians(alpha)), PRECISION)
    return (u, v)


# Function to get the angle beween two vectors.
# The angle obtained respect the angle convention detailled in compute.py
def angleBetween2Vects(vect1, vect2):
    (x1, y1) = vect1
    (x2, y2) = vect2
    angle = atan2(y2, x2) - atan2(y1, x1)
    return round(degrees(angle), PRECISION)
