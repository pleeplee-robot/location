#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .compute import compute2Data, compute3Data, sortData


"""
This file contains a class emcompassing all the data transmitted by the robot
An instance of this class represents all the data we have access to compute
the location at a given time t.
Methods from the class are wrapping compute.py to make it easy for the user of
the api to call the compute functions.

The datas needed as parameters are:
    - the angle north (only at init)
    - direction at initialisation (only at init)
    - angle to direction
    - perimeter (with LED color and point coordinate for each corner)
        (only at init)
    - odometry (last position + distance traveled)
    - sets of data (angle + distance to a colored point)
    - TBD : height of LEDs (only at init)
"""


class Odometry:

    # For now the range of acceptable distance with odometry is 30cm
    # We need to test the fiability of the measured values to
    # decrease this value.
    _range = 0.3

    def __init__(self, lastPos, dist):
        self.lastPos = lastPos
        self.dist = dist

    def withinRange(self, point):
        return self.lastPos.distance(point) - self.dist < self._range


def filterOdometry(solutions, odometry):
    soluce = [value for value in solutions if odometry.withinRange(value)]
    return soluce


class Location:

    """ Datas:

    position is in meter
    angles are from -180 to 180 degree

    angleNorth:
        Angle between the north and the axis of the robot at
        Initialization. This angle is a fixed data measured only once
        at the initialization of the robot.

    dirInit:
        This variable represent the direction the robot is at initialization.
        This data is to be inputted by the user once. It is a vector.

    heightLEDs:
        Difference of height between the robot camera and the LEDs used as
        corners. Value is in meter.

    perimeter:
        List of LEDs. (LED class can be found in compute.py)
        Each element of the lsit represents a corner of the area.
        The corners MUST be sorted clockwise when inserted in the list.

    angleToDirection:
        Angle between actual direction and North.
        This data is to be harvested in real time with a magnetic captor.
        Data is needed everytime the location is computed.

    odometry:
        Instance of class Odometry.

    datas:
        List of Data. (The Data class can be found in compute.py)
        These values represents the data collected by the robot camera.
        (LEDs percieved, angle, estimated distance)

    """

    def __init__(self, angleNorth, dirInit, height, *args):
        self.angleNorth = angleNorth
        self.dirInit = dirInit
        self.heightLEDs = height
        self.perimeter = args
        # at each iteration
        self.angleToDirection = None
        self.odometry = None
        self.datas = None

    def refreshData(self, angleToDirection, odometry, *args):
        self.angleToDirection = angleToDirection
        self.odometry = odometry
        self.datas = args

    def computePos(self, *args):
        self.refreshData(*args)
        my_args = [self.dirInit, self.angleNorth, self.angleToDirection,
                   self.perimeter]
        points = []

        if len(self.datas) < 2:
            print("Not enough data")
            return None
        elif len(self.datas) == 2:
            points = compute2Data(*self.datas, *my_args)
        else:
            points = compute3Data(self.datas[0], self.datas[1],
                                  self.datas[2], *my_args)

        points = filterOdometry(points, self.odometry)
        if len(points) == 0:
            print("No good datas")
        return sortData(points)
