#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################
# AUTHOR  : Loïc Banet                           #
# SUMMARY : Contain enum class that define color #
##################################################

import math
from enum import Enum
from itertools import count


"""
There are only 7 colors available to simplify the image processing at
the camera level. The maximum number of LEDs available for a garden
is 7.
"""


class Color(Enum):
    NONE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    PURPLE = 5
    ORANGE = 6
    WHITE = 7


"""
The LED class represents a colored landmark to be put in the garden.
These landmarks are mandatory for the robot to locate itself.
The parameters of the class are the following:
    - color : The color of the LED, it must be unique
    - point : The position of the LED in the plan
    - perimeter : True if the LED is on the perimeter.
                False otherwise. By default this value is true.
                If the LED is on the perimeter an additionnal filter
                of the possible location's solution is applied
    - height : the difference of height between the robot's camera and the LED
"""


class LED:
    def __init__(self, color, point, inPerimeter=True, height=0.0):
        self.color = color
        self.point = point
        self.inPerimeter = inPerimeter
        self.height = height

    def __str__(self):
        return "LED(Position: %s ;Color : %s )" % (self.point, self.color)


def _getLED(color, perimeter):
    for i in perimeter:
        if i.color == color:
            return i
    raise ValueError('Color not found')


# Data is the class that enable us to track the data set sent by the camera.
class Data:
    _ids = count(0)

    def __init__(self,
                 color,
                 angle,
                 angleNorth,
                 angleToDirection,
                 perimeter,
                 distance=None):
        # Intances counter: This variable enable us to track the order
        # of initialisation of the datas.
        self.id = next(self._ids)
        # Convert angle from (LED -> Actual direction) to
        # (LED -> edge of perimeter)
        self.angle = angle + angleToDirection + angleNorth
        self.distance = distance
        try:
            self.led = _getLED(color, perimeter)
        except ValueError as error:
            print('The color does not correspond to an existing LED')

    # adjust the distance between the inputted data and the one one
    # calculated with its angle.
    # This function is to be adjusted with real data in order to reduce
    # the error due to each method
    def adjustDistance(self, dist):
        if self.distance is None:
            self.distance = dist
        else:
            theta = math.asin(self.led.height / self.distance)
            adjustedDist = math.cos(theta) * self.distance
            self.distance = (adjustedDist + dist) / 2
        return self.distance
