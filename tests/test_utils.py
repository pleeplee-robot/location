#!/usr/bin/env python3

import pytest
from pleeplee.geometry import Point
from pleeplee.utils import Color, Data, LED


# Data:

corner1 = LED(Color.RED, Point(0.0, 0.0))
corner2 = LED(Color.YELLOW, Point(0.0, 10.0))
corner3 = LED(Color.BLUE, Point(10.0, 10.0))
corner4 = LED(Color.GREEN, Point(10.0, 0.0))

testPerimeter1 = [corner1, corner2, corner3, corner4]

# Test function:

def test_data_adjust_distance():
    perimeter = testPerimeter1
    angleNorth = 20.0
    angleToDirection = 35.0
    args = [angleNorth, angleToDirection, perimeter]

    data1 = Data(Color.RED, 38.45, *args, 12.4)
    data2 = Data(Color.RED, 38.45, *args)
    assert data1.adjustDistance(6.8) == 9.6
    assert data2.adjustDistance(6.8) == 6.8
