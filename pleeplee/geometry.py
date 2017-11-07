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
    """Simple point representation.

    Contains utility functions for points manipulation.

    Attributes:
        X: x coordinate of the point.
        Y: y coordinate of the point.
    """

    # Thresold to determine that two points are similar (distance < 15cm)
    _threshold = 0.1

    def __init__(self, x, y):
        """Initialize point with coordinates x and y."""
        self.X = x
        self.Y = y

    def __str__(self):
        return "Point(%s,%s)" % (self.X, self.Y)

    def distance(self, other):
        """Compute distance between two points

        Performs the distance between the current point and the one given
        in parameters.

        Args:
            self: The current point.
            other: Another point.

        Returns:
            A floating point approximation of **PRECISION** digits.
        """
        dx = self.X - other.X
        dy = self.Y - other.Y
        return round(sqrt(dx**2 + dy**2), PRECISION)

    def __eq__(self, other):
        """Overload of the == operator to simplify point manipulations."""
        return (abs(self.X - other.X) < self._threshold
                and abs(self.Y - other.Y) < self._threshold)

    def minus(self, other):
        """Performs the substraction of two points.

        Args:
            self: The current point.
            other: Another point.

        Returns:
            A Point object.
        """
        return (self.X - other.X, self.Y - other.Y)

    def toShapely(self):
        """Converts the Point object to a Shapely Point object.

        This is usefull for using advanced mathematical functions from shapely.

        Args:
            self: The current Point.

        Returns:
            A Shapely Point object.
        """
        return shapely.geometry.point.Point(self.X, self.Y)


# Rotate a vector in a plane by an angle alpha in degree.
# The rotation is clockwise.
# The formula is obtained by multiplying the rotation matrix with
# the vector(x, y)
def rotateVector(vect, alpha):
    """Rotate a vector to with an angle.

    Args:
        vect: a vector composed of two values (x y).
        alpha: the angle.

    Returns:
        An updated vector (x y).
    """
    (x, y) = vect
    u = round(x * cos(radians(alpha)) + y * sin(radians(alpha)), PRECISION)
    v = round(y * cos(radians(alpha)) - x * sin(radians(alpha)), PRECISION)
    return (u, v)


# Function to get the angle beween two vectors.
# The angle obtained respect the angle convention detailled in compute.py
def angleBetween2Vects(vect1, vect2):
    """Get the angle between two vectors.

    Args:
        vect1: a vector composed of two values (x y).
        vect2: a vector composed of two values (x y).

    Returns:
        An angle (float).
    """
    (x1, y1) = vect1
    (x2, y2) = vect2
    angle = atan2(y2, x2) - atan2(y1, x1)
    return round(degrees(angle), PRECISION)
