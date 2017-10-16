#!/usr/bin/env python

from math import sqrt

from pleeplee.geometry import (PRECISION, Point, angleBetween2Vects,
                               rotateVector)
from pleeplee.utils import Color


# Test the Point class
def test_point_distance():
    point1 = Point(2.0, 4.5)
    point2 = Point(3.4, 6.7)
    assert point1.distance(point2) == point2.distance(point1)
    assert point1.distance(point2) == round(sqrt(6.8), PRECISION)


def test_point_eq():
    point1 = Point(2.05, 4.3)
    x = point1.X + point1._threshold - 0.01
    point2 = Point(x, 4.3)
    assert point1 == point2


def test_point_not_eq():
    point1 = Point(2.05, 4.3)
    x = point1.X + point1._threshold + 0.01
    point2 = Point(x, 4.3)
    assert not point1 == point2


def test_point_minus():
    point1 = Point(2.0, 4.5)
    point2 = Point(3.4, 6.7)
    assert point1.minus(point2) == (-1.4, -2.2)


def test_rotate_vector_simple():
    assert rotateVector((10.0, 0.0), -90) == (0, 10)
    val = round(5 * sqrt(2), PRECISION)
    assert rotateVector((10.0, 0.0), -45) == (val, val)
    assert rotateVector((10.0, 0.0), 45) == (val, -val)


def test_angle_two_vects():
    assert angleBetween2Vects((10, 0), (0, 10)) == 90
    val = round(5 * sqrt(2), PRECISION)
    assert angleBetween2Vects((10, 0), (val, -val)) == -45
