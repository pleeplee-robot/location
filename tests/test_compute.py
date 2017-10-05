#!/usr/bin/env python3

import pytest
import math
from pytest_mock import mocker
from pleeplee.compute import *
from pleeplee.geometry import (Point, Triangle)
from pleeplee.utils import Color


# Data needed for Mocks:
# Test data set 1
corner1 = LED(Color.RED, Point(0.0, 0.0))
corner2 = LED(Color.YELLOW, Point(0.0, 10.0))
corner3 = LED(Color.BLUE, Point(10.0, 10.0))
corner4 = LED(Color.GREEN, Point(10.0, 0.0))

testPerimeter1 = [corner1, corner2, corner3, corner4]

# Test data set 2
corner1_t2 = LED(Color.RED, Point(3.0, 3.0))
corner2_t2 = LED(Color.YELLOW, Point(13.0, 5.0))
corner3_t2 = LED(Color.BLUE, Point(11.0, 9.0))
corner4_t2 = LED(Color.GREEN, Point(1.0, 10.0))

testPerimeter2 = [corner1_t2, corner2_t2, corner3_t2, corner4_t2]


# Test functions:

def test_data_adjust_distance():
    perimeter = testPerimeter1
    angleNorth = 20.0
    angleToDirection = 35.0
    args = [angleNorth, angleToDirection, perimeter]

    data1 = Data(Color.RED, 38.45, *args, 12.4)
    data2 = Data(Color.RED, 38.45, *args)
    assert data1.adjustDistance(6.8) == 9.6
    assert data2.adjustDistance(6.8) == 6.8


def test_pos_2_dist_none():
    perimeter = testPerimeter1
    angleNorth = 20.0
    angleToDirection = 35.0
    args = [angleNorth, angleToDirection, perimeter]

    data1 = Data(Color.RED, 38.45, *args, 12.4)
    data2 = Data(Color.RED, 38.45, *args)
    with pytest.raises(ValueError):
        getPos2Dist(data1, data2)


def test_pos_2_dist_no_solution():
    perimeter = testPerimeter1
    angleNorth = 20.0
    angleToDirection = 35.0
    args = [angleNorth, angleToDirection, perimeter]
    corner1 = perimeter[0]
    corner2 = perimeter[1]
    distance = math.sqrt((corner1.point.X - corner2.point.X)**2 +
                         (corner1.point.Y - corner2.point.Y)**2)
    d1 = 1.4

    data1 = Data(corner1.color, 55.0, *args, d1)
    data2 = Data(corner2.color, -35.0, *args, distance - d1 - 0.2)
    data3 = Data(corner2.color, 67.3, *args, distance + d1 + 4.0)

    assert getPos2Dist(data1, data2) == []
    assert getPos2Dist(data1, data3) == []


def test_pos_2_dist_easy():
    perimeter = testPerimeter1
    angleNorth = 20.0
    angleToDirection = 35.0
    args = [angleNorth, angleToDirection, perimeter]

    data1 = Data(Color.RED, 55.0, *args, 3.8)
    data2 = Data(Color.GREEN, -35.0, *args, 9.4)

    res = getPos2Dist(data1, data2)
    assert len(res) == 2
    assert Point(1.3, 3.5) in res


def test_filter_point():
    perimeter = testPerimeter1
    res = filterPoints([Point(1.3, 3.5), Point(1.3, -3.5)], perimeter)
    assert len(res) == 1
    assert Point(1.3, 3.5) == res[0]


def test_is_adjacent():
    perimeter = testPerimeter1
    assert not isAdjacent(Color.RED, Color.RED, perimeter)
    assert isAdjacent(perimeter[0].color, perimeter[1].color, perimeter)
    assert not isAdjacent(perimeter[0].color, perimeter[2].color, perimeter)


def test_vector_from_colors():
    perimeter = testPerimeter1
    assert (vectorFromColors(perimeter[0], perimeter[1], perimeter) ==
            vectorFromColors(perimeter[1], perimeter[0], perimeter))
    assert vectorFromColors(perimeter[2], perimeter[3], perimeter) == (0.0, -10.0)


def test_dist_from_angles_no_rectangle():
    perimeter = testPerimeter1
    dirInit = (10.0, 0.0)
    angleNorth = 20.0
    angleToDirection = 35.0
    args = [angleNorth, angleToDirection, perimeter]
    data1 = Data(Color.RED, 55.0, *args)
    data2 = Data(Color.GREEN, -35.0, *args)

    (x, y) = distanceFromAngles(data1, data2, dirInit, angleNorth,
            angleToDirection, perimeter)
    errorMargin = 0.3 # 30cm

    assert abs(x - 3.7) < errorMargin
    assert abs(y - 9.2) < errorMargin


def test_dist_from_angles_no_rectangle_2():
    perimeter = testPerimeter2
    dirInit = (-10.0, -10.0)
    angleNorth = -45.0
    angleToDirection = -90.0
    args = [angleNorth, angleToDirection, perimeter]
    data1_t2 = Data(Color.YELLOW, 19.0, *args)
    data2_t2 = Data(Color.BLUE, -25.0, *args)

    (x, y) = distanceFromAngles(data1_t2, data2_t2, dirInit, angleNorth,
            angleToDirection, perimeter)
    errorMargin = 0.04 # 4cm

    assert abs(x - 6.4) < errorMargin
    assert abs(y - 4.5) < errorMargin


def test_compute_2_data_1():
    perimeter = testPerimeter2
    dirInit = (-10.0, -10.0)
    angleNorth = -45.0
    angleToDirection = -90.0
    args = [angleNorth, angleToDirection, perimeter]
    data1_t2 = Data(Color.YELLOW, 19.0, *args)
    data2_t2 = Data(Color.BLUE, -25.0, *args)

    res = compute2Data(data1_t2, data2_t2, dirInit, angleNorth,
            angleToDirection, perimeter)

    assert len(res) == 1
    errorMargin = 0.1 # 10cm
    assert abs(res[0].X - 7.0) < errorMargin
    assert abs(res[0].Y - 7.0) < errorMargin


def test_compute_3_data():
    perimeter = testPerimeter2
    dirInit = (-10.0, -10.0)
    angleNorth = -45.0
    angleToDirection = -90.0
    args = [angleNorth, angleToDirection, perimeter]

    data0_t2 = Data(Color.RED, 134.0, *args)
    data1_t2 = Data(Color.YELLOW, 19.0, *args)
    data2_t2 = Data(Color.BLUE, -25.0, *args)

    res = compute3Data(data0_t2, data1_t2, data2_t2, dirInit, angleNorth,
            angleToDirection, perimeter)

    errorMargin = 0.1 # 10cm
    assert abs(res[0].X - 7.0) < errorMargin
    assert abs(res[0].Y - 7.0) < errorMargin


def test_has_many_occurencies():
    my_list = [ Point(6.92, 5.78), Point(6.99, 5.81), Point(6.96, 5.80) ]
    ref = Point(7.0, 5.8)
    assert hasManyOccurencies(ref, my_list)


def test_sort_data():
    my_list = [ Point(6.92, 5.78), Point(6.99, 5.81), Point(6.96, 5.80) ]
    ref = Point(7.0, 5.8)
    assert sortData(my_list) == ref
