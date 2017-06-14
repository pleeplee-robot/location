from pleeplee.geometry import (Point, Triangle, rotateAngle, rotateVector,
        angleBetween2Vects, PRECISION)
from pleeplee.utils import Color
from math import sqrt

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

# Test the Triangle class
def test_triangle_corner():
    point = Point(2.0, 4.5)
    angle = 24.56
    triangle = Triangle(angle, point, Color.RED)
    # The triangle must be rectangle. Sum of the angles of triangle = 180 degree
    assert triangle.angleP + triangle.cornerAngle() + 90 == 180

