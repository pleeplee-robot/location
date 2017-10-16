#!/usr/bin/env python3

import pytest
from pytest_mock import mocker

from pleeplee.geometry import Point
from pleeplee.location import Location, Odometry, filterOdometry
from pleeplee.utils import LED, Color, Data


def test_odometry():
    lastPos = Odometry(Point(2.0, 4.0), 1.2)
    assert lastPos.withinRange(Point(2.5, 4.2))


def test_filter_odometry(mocker):
    mocker.patch('pleeplee.location.Odometry._range', 0.03)
    lastPos = Odometry(Point(2.0, 4.0), 1.2)
    solutions = [Point(2.5, 4.2), Point(2.9, 4.9), Point(0.0, 0.0)]
    print(Point(2.0, 4.0).distance(Point(2.9, 4.9)))
    rest = filterOdometry(solutions, lastPos)
    assert len(rest) == 1


def test_location_compute_pos(mocker):
    mocker.patch('pleeplee.location.Odometry._range', 0.03)
    # Data set
    corner1 = LED(Color.RED, Point(3.0, 3.0))
    corner2 = LED(Color.YELLOW, Point(13.0, 5.0))
    corner3 = LED(Color.BLUE, Point(11.0, 9.0))
    corner4 = LED(Color.GREEN, Point(1.0, 10.0))
    perimeter = [corner1, corner2, corner3, corner4]

    dirInit = (-10.0, -10.0)
    angleNorth = -45.0
    angleToDirection = -90.0
    height = 0.0
    args = [angleNorth, angleToDirection, perimeter]

    data0 = Data(Color.RED, 134.0, *args)
    data1 = Data(Color.YELLOW, 19.0, *args)
    data2 = Data(Color.BLUE, -25.0, *args)
    datas = [data0, data1, data2]

    odometry = Odometry(Point(6.5, 6.7), 0.6)

    # Init & use of location
    loc = Location(angleNorth, dirInit, height, *perimeter)
    assert loc.computePos(angleToDirection, odometry, *datas) == Point(
        7.0, 7.0)
