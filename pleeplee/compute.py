#!/usr/bin/env python3

"""
This file contains the computation of all datas recieved by the robot to
find the robot position in the given perimeter.
The input datas are:
    - the map (user input the coordinate of LEDs landmarks)
    - the mode (user input, boolean true if it is a rectangle)
    - the side perpendicular to the robot direction at initialisation
    (user input maybe ommited)
    - the angle between the direction at initialisation and the north
    (magnetic captor, one data send at initialisation)
    - the angle between the actual direction and the north
    (magnetic captor, periodically)
    - the angle to at least two LEDs landmark (camera on step motor + programm
    to extract the angles, periodically)
    - the distance calculated from the blobs of light on the previous pictures
    - the datas linked to the odometry
    (previous position, estimated position, error margin)
"""
""" Initialisation procedure
During the initialisation phase the user has to put the LEDs landmark on the map
and input their coodinates and color into the API.
Before turning on the robot for initialisation phase it has to face a side
of the perimeter delimited by LEDs. The minimum number of LEDs landmark is 4.
The LEDs have to be of different colors for the location to work properly.

There are two different modes for the configuration of the LED disposition
that the user can choose from.
The first mode is to have a perfect rectangle as the perimeter of the garden.
In this mode there is no need for more input from the user.
The second mode is when the perimeter of the garden is not a perfect rectangle
or that they are more than 4 LED landmarks.

 The map will have the following conventions:
  R(0, 0)                                   G(10, 0)
       _____________________________________
      |                                     |
      |                                     |
      |                                     |
      |                                     |
      |                                     |
      |                                     |
      |                                     |
      |                                     |
       _____________________________________
  y(0, 10)                                  B(10, 10)

Where the lower-left most landmark is (0, 0) and the other coordinates
are
represented from the lower-left most one in meter.

"""
""" Default Angle representation
                           +y

                           |    /
                           |   /
                           |  /   + Theta
                           | / )
+/- 180 degrees    -x ----------------- + x    0 degrees => Direction D
                           | \ )
                           |  \   - Theta
                           |   \
                           |    \

                          -y
With 0 <= Theta <= 180.

The direction D is the direction of the robot at initialisation.

"""
import math
from utils import Color
from geometry import (Point, Triangle, rotateAngle, rotateVector,
        angleBetween2Vects)
from itertools import count

# Globals Datas: (For the moment most of them are dummies)
# position is in meter
# angles are from -180 to 180 degree

# The mathematical precision for round operations
PRECISION = 4

# Angle between the north and the axis of the robot at Initialisation
# (same axis as an edge of the perimeter)
# This angle is a fixed data measured at the initialization of the robot.
# The angle is between 180 and -180 degree
angleNorth = 20.0

# This variable represent the mode choosen by the user at initialisation
RECTANGLE_MODE = False

# This variable represent the direction of initialisation
# Vector perpendicular to the side it face when initialised
# This data is inputted by the user.
dirInit = (0, 10)

# Angle between actual direction and North
# This data can be harvested in real time with a magnetic captor
# for now we will keep this fake value
angleToDirection = 35.0

class LED:

    def __init__(self, color, point):
        self.color = color
        self.point = point
        self.angle = 0

    def __str__(self):
        return "LED(Position: %s ;Color : %s )"%(self.point, self.color)

# the map is represented by 4 leds positionned at each corner of the area
# available to the robot the corners must be inserted in a clockwise way

corner1 = LED(Color.RED, Point(0.0, 0.0))
corner2 = LED(Color.YELLOW, Point(0.0, 10.0))
corner3 = LED(Color.BLUE, Point(10.0, 10.0))
corner4 = LED(Color.GREEN, Point(10.0, 0.0))

perimeter = [corner1, corner2, corner3, corner4]

def _getLED(color):
    for i in perimeter:
        if i.color == color:
            return i
    raise ValueError('Color not found')

# Data is the class that enable us to track the data set sent by the camera.
class Data:
    _ids = count(0)

    def __init__(self, color, angle, distance=None):
        # Intances counter: This variable enable us to track the order
        # of initialisation of the datas.
        self.id = next(self._ids)
        # Convert angle from (LED -> Actual direction) to
        # (LED -> edge of perimeter)
        self.angle = angle + angleToDirection + angleNorth
        self.distance = distance
        try:
            self.led = _getLED(color)
        except ValueError as error:
            print('The color does not correspond to an existing LED')

    # adjust the distance between the inputted data and the one one
    # calculated with its angle.
    # This function is to be adjusted with real data in order to reduce
    # the error due to each method
    def adjustDistance(self, dist):
        if self.distance == None:
            self.distance = dist
        else:
            self.distance = (self.distance + dist) / 2
        return self.distance


def getPos2Dist(data1, data2):

    if data1.distance == None or data2.distance == None:
        raise ValueError('Incomplete datas')

    P1 = data1.led.point
    P2 = data2.led.point
    R1 = data1.distance
    R2 = data2.distance

    dx = P2.X - P1.X
    dy = P2.Y - P1.Y
    D = P1.distance(P2)
    if D > R1 + R2:
        print("No solution - The circles do not intersect")
        return []
    elif D < math.fabs(R2 - R1):
        print("No solution - One circle is contained within the other")
        return []
    elif D == 0 and R1 == R2:
        print("No solution - The circles are equal and coincident")
        return []

    chorddistance = (R1**2 - R2**2 + D**2) / (2 * D)
    # distance from 1st circle's centre to the chord between intersects
    halfchordlength = math.sqrt(R1**2 - chorddistance**2)
    chordmidpointx = P1.X + (chorddistance * dx) / D
    chordmidpointy = P1.Y + (chorddistance * dy) / D

    I1 = Point(round(chordmidpointx + (halfchordlength * dy) / D, PRECISION),
            round(chordmidpointy - (halfchordlength * dx) / D, PRECISION))
    theta1 = round(math.degrees(math.atan2(I1.Y - P1.Y, I1.X - P1.X)),
            PRECISION)

    I2 = Point(round(chordmidpointx - (halfchordlength * dy) / D, PRECISION),
            round(chordmidpointy + (halfchordlength * dx) / D, PRECISION))
    theta2 = round(math.degrees(math.atan2(I2.Y - P1.Y, I2.X - P1.X)),
            PRECISION)

    if D == R1 + R2 or D == R1 - R2:
        return [I1]

    if theta2 > theta1:
        I1, I2 = I2, I1
    return [I1, I2]

def filterPoints(solutions, corners):

    Xmin = corners[0].point.X
    Xmax = corners[0].point.X
    Ymin = corners[0].point.Y
    Ymax = corners[0].point.Y

    for i in corners:
        if i.point.X < Xmin:
            Xmin = i.point.X
        if i.point.X > Xmax:
            Xmax = i.point.X
        if i.point.Y < Ymin:
            Ymin = i.point.Y
        if i.point.Y > Ymax:
            Ymax = i.point.Y

    return [value for value in solutions if value.X < Xmax and value.X > Xmin
            and value.Y < Ymax and value.Y > Ymin]

def isAdjacent(color1, color2):
    if color1 == color2:
        print("merde")
        return False;
    count = 0
    start = False
    for i in perimeter:
        if i.color == color1 or i.color == color2:
            if not start:
                start = True
            else:
                break
        if start:
            count += 1
    return count == 1 or count == len(perimeter)

# When the vectors are not known the best way to have a rectangle
# triangle is to rotate the angles until we are in between them.
# This condition transalate itself into the sum of the absolute
# value of the angle is below or equal 90 degree.
# This algorithm only works because we suppose that the user has
# properly initialized the robot facing a side. As this case only happens
# when the perimeter is a perfect rectangle, we obtain rectangle triangles.
def adjustAngles(triangle1, triangle2):
    while abs(triangle1.angleP) + abs(triangle2.angleP) > 90:
        triangle1.angleP = rotateAngle(triangle1.angleP)
        triangle2.angleP = rotateAngle(triangle2.angleP)
        triangle1.offset += 1
        triangle2.offset += 1

# the two triangle P point must be the same and the triangles must be rectangle
# the angleP given are supposed correct in all cases
def computeDistFromAngles(triangle1, triangle2):
    adjustAngles(triangle1, triangle2)
    if triangle1.angleP < triangle2.angleP:
        triangle1, triangle2 = triangle2, triangle1
    distance = abs(triangle1.point.distance(triangle2.point))
    # if the two angles have different signs their product will de negative
    if triangle1.angleP * triangle2.angleP < 0:
        x = distance / (1 + math.tan(math.radians(abs(triangle2.angleP))) /
                math.tan(math.radians(abs(triangle1.angleP))))
        y = distance - x
        d1 = x / math.sin(math.radians(abs(triangle1.angleP)))
        d2 = y / math.sin(math.radians(abs(triangle2.angleP)))
        return (d1, d2)
    else:
        diff = math.radians(abs(triangle1.angleP - triangle2.angleP))
        x = distance * math.cos(math.radians(triangle2.angleP)) / math.sin(diff)
        y = distance * math.cos(math.radians(triangle1.angleP)) / math.sin(diff)
        return (x, y)


# Get the clockwise vector from two LEDs color in the perimeter
# the arguments should be given from left to right in the scope of the camera.
def vectorFromColors(led1, led2):
    if not isAdjacent(led1.color, led2.color):
        return led2.point.minus(led1.point)
    count = 0
    start = False
    # Boolean: True if the color1
    firstColorInFirst = True
    for i in perimeter:
        if i.color == led1.color or i.color == led2.color:
            if start:
                break
            start = True
            firstColorInFirst = True if i.color == led1.color else False
        if start:
            count += 1
    if count == len(perimeter):
        firstColInFirst = not firstColorInFirst
    return (led2.point.minus(led1.point) if firstColorInFirst
                    else led1.point.minus(led2.point))


# Distance from angles when RECTANGLE_MODE is false
# The computation is done with vectors
# the minus before the angle of rotateVector is necessary because the
# angles are counter clockwise by convention however the rotation is clockwise
# in order to correctly compute non adjacent LEDs the order of the input
# datas is important. They must be in the order as seen by the camera
# from left to right. This ensure that the robot will always be on the
# adequate side of the area and the vectPerpendicular calculus will
# be correct.
def distFromAnglesNoRectangle(data1, data2):
    vectNorth = rotateVector(dirInit, angleNorth)
    actualVector = rotateVector(vectNorth, angleToDirection)
    vect1 = rotateVector(dirInit, data1.angle)
    vect2 = rotateVector(dirInit, data2.angle)
    # By convention we choose the vectors of the sides in a clockwise
    # way if they are adjacent. We will then only need a rotation in a counter
    # clockwise way to always have a vector facing the outside of the perimeter
    vectPerpendicular = rotateVector(vectorFromColors(data1.led, data2.led), 90)
    data1.angle = angleBetween2Vects(vect1, vectPerpendicular)
    data2.angle = angleBetween2Vects(vect2, vectPerpendicular)
    triangle1 = Triangle(data1.angle, data1.led.point, data1.led.color)
    triangle2 = Triangle(data2.angle, data2.led.point, data2.led.color)
    return computeDistFromAngles(triangle1, triangle2)

# Final synthetizing of all the datas related to 2 points and computing
def compute2Data(data1, data2):
    if RECTANGLE_MODE:
        triangle1 = Triangle(data1.angle, data1.led.point, data1.led.color)
        triangle2 = Triangle(data2.angle, data2.led.point, data2.led.color)
        (dist1, dist2) = computeDistFromAngles(triangle1, triangle2)
    else:
        (dist1, dist2) = distFromAnglesNoRectangle(data1, data2)
    data1.adjustDistance(dist1)
    data2.adjustDistance(dist2)
    res = getPos2Dist(data1, data2)
    return filterPoints(res, perimeter)
