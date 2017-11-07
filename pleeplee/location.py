#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .compute import compute2Data, compute3Data, sortData


class Odometry:
    """Class that represents an odometry.

    Combination of last position, range and distance traveled.

    Arguments:
        lastPos: Last position of the robot when the position was computed.

        dist: distance traveled since lastPos.
        Recieved through odometry captors.
    """

    # For now the range of acceptable distance with odometry is 30cm
    # We need to test the fiability of the measured values to
    # decrease this value.
    _range = 0.3

    def __init__(self, lastPos, dist):
        self.lastPos = lastPos
        self.dist = dist

    def withinRange(self, point):
        """Evaluates whether the point in parameter is close enough

        Args:
            point: A Point instance to test

        Returns:
            True if the point is close enough (within the range).
            False otherwise.
        """
        return self.lastPos.distance(point) - self.dist < self._range


def filterOdometry(solutions, odometry):
    """Filter the solutions by odometry.

    Removes solutions from the list if there are not within range
    of the odometry.

    Args:
        solutions: A set of points candidates to the final solution.
        odometry: Odometry instance.

    Returns:
        A list of candidates points filtered.
    """
    soluce = [value for value in solutions if odometry.withinRange(value)]
    return soluce


class Location:
    """A class encompassing all the datas used to compute the location.

    Position is in meter. Angles are from -180 to 180 degree.
    This file contains a class emcompassing all the data transmitted by the
    robot. An instance of this class represents all the data we have access to
    compute the location at a given time t. Methods from the class are
    wrapping compute.py to make it easy for the user of the api to call the
    compute functions.
    For a given robot a single instance of Location should be used.


    Attributes:
        angleNorth: Angle between the north and the axis of the robot at
        Initialization. This angle is a fixed data measured only once
        at the initialization of the robot.

        dirInit: This variable represent the direction the robot is at
        initialization. This data is to be inputted by the user once.
        It is a vector.

        heightLEDs: Difference of height between the robot camera and the
        LEDs used as corners. Value is in meter.

        perimeter: List of LEDs. (LED class can be found in compute.py)
        Each element of the lsit represents a corner of the area.
        The corners MUST be sorted clockwise when inserted in the list.

        angleToDirection: Angle between actual direction and North.
        This data is to be harvested in real time with a magnetic captor.
        Data is needed everytime the location is computed.

        odometry: Instance of class Odometry.

        datas: List of Data. (The Data class can be found in compute.py)
        These values represents the data collected by the robot camera.
        (LEDs percieved, angle, estimated distance)
    """

    def __init__(self, angleNorth, dirInit, height, *args):
        """Initialize a Location"""
        self.angleNorth = angleNorth
        self.dirInit = dirInit
        self.heightLEDs = height
        self.perimeter = args
        # at each iteration
        self.angleToDirection = None
        self.odometry = None
        self.datas = None

    def refreshData(self, angleToDirection, odometry, *args):
        """Refresh the Location instance with the datas from captors"""
        self.angleToDirection = angleToDirection
        self.odometry = odometry
        self.datas = args

    def computePos(self, *args):
        """Compute the current location of the robot from the datas.

        Args:
            angleToDirection: The angle between the direction of
            the robot and the North.

            odometry: An instance of Odometry class.

            datas: list of Data instances (see utils.Data).

        Returns:
            A single sets of coordiantes representing the current position
            of the robot.
        """
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
