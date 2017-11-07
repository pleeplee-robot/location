#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################################
# AUTHOR  : Loïc Banet                                  #
# SUMMARY : Contain computation logics of several data #
#           related to the robot location               #
#########################################################

import math

import shapely.geometry

from .geometry import Point, angleBetween2Vects, rotateVector

"""
This file contains the computation of all datas recieved by the robot to
find the robot position in the given perimeter.
The input datas are:
    - the map (user input the coordinate of LEDs landmarks)
    - the mode (user input, boolean true if it is a rectangle)
    - the side perpendicular to the robot direction at initialisation
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
During the initialisation phase the user has to put the LEDs landmark
on the map and input their coodinates and color into the API.
Before turning on the robot for initialisation phase it has to face a side
of the perimeter delimited by LEDs. The minimum number of LEDs landmark is 4.
The LEDs have to be of different colors for the location to work properly.

 The map has the following conventions:
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

# The mathematical precision for round operations
PRECISION = 4


def getPos2Dist(data1, data2):
    """Get a set of positions from two sets of datas.

    Based on mathematical computations for the intersections between two circles.

    Args:
        data1: Data instance.
        data2: Data instance.

    Returns:
        A set of points candidates to the location.
    """
    if data1.distance is None or data2.distance is None:
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

    I1 = Point(
        round(chordmidpointx + (halfchordlength * dy) / D, PRECISION),
        round(chordmidpointy - (halfchordlength * dx) / D, PRECISION))
    theta1 = round(
        math.degrees(math.atan2(I1.Y - P1.Y, I1.X - P1.X)), PRECISION)

    I2 = Point(
        round(chordmidpointx - (halfchordlength * dy) / D, PRECISION),
        round(chordmidpointy + (halfchordlength * dx) / D, PRECISION))
    theta2 = round(
        math.degrees(math.atan2(I2.Y - P1.Y, I2.X - P1.X)), PRECISION)

    if D == R1 + R2 or D == R1 - R2:
        return [I1]

    if theta2 > theta1:
        I1, I2 = I2, I1
    return [I1, I2]


def filterPoints(solutions, corners):
    """Remove solutions if they are not whithin the perimeter.

    This function use shapely as the mathematical computaions for non rectangular
    shapes are quite heavy.

    Args:
        solutions: A list of candidate points.

        corners: The perimeter of the garden (list of LEDs).

    Returns:
        A list of points filtered.
    """
    coords = []
    for i in corners:
        if i.inPerimeter:
            coords.append((i.point.X, i.point.Y))

    polygon = shapely.geometry.polygon.Polygon(coords)

    solutions_2 = [value.toShapely() for value in solutions
                   if polygon.contains(value.toShapely())]

    return [Point(v.x, v.y) for v in solutions_2]


def isAdjacent(color1, color2, perimeter):
    """Check if two colors are adjacents in the perimeter.

    The LEDs in the perimeter all have a unique color. This function takes color
    in parameters to simplify the computations.

    Args:
        color1: First color.
        color2: Second color.
        perimeter: The list of LEDs in the perimeter.

    Returns:
        True if the two colors are adjacents. False otherwise.
    """
    if color1 == color2:
        print('Bad datas, not possible')
        return False
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


def vectorFromColors(led1, led2, perimeter):
    """Get the clockwise vector from two LEDs color in the perimeter.

    The arguments should be given from left to right in the scope of the camera.

    Args:
        led1: The leftmost LED
        led2: The rightmost LED
        perimeter: The list of LEDs

    Returns:
        The vector from led1 to led2
    """
    if not isAdjacent(led1.color, led2.color, perimeter):
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
        firstColorInFirst = not firstColorInFirst
    return (led2.point.minus(led1.point)
            if firstColorInFirst else led1.point.minus(led2.point))


def distanceFromAngles(data1, data2, dirInit, angleNorth, angleToDirection,
                       perimeter):
    """Distance computation from angle

    This function is the compuation of the distance to the robot given
    the angle. We cannot do it Data per Data as it is not a computation
    possible if our only data is the angle. The principle here is to cross
    two datas and given the position of the two LEDs we have a triangle
    where we know two angles and a distance. With these datas we can calculate
    the two remaining distances.

    Implementation details:
    The computation is done with vectors.
    The minus before the angle of rotateVector is necessary because the
    angles are counter clockwise by convention however the rotation is clockwise
    in order to correctly compute non adjacent LEDs the order of the input
    datas is important. They must be in the order as seen by the camera
    from left to right. This ensure that the robot will always be on the
    adequate side of the area and the vectPerpendicular calculus will
    be correct.

    Args:
        data1: The first Data instance.

        data2: The second data instance.

        dirInit: The direction of the robot at initialisation.

        angleNorth: The angle of the robot from the North at initialisation.

        angleToDirection: The angle between the current axis of the robot.
        and the North

        perimeter: The perimeter of the garden (list of LEDs).

    Returns:
        A pair of distance (x y) from the robot to respectively (led1 led2).
    """

    vect1 = rotateVector(dirInit, data1.angle)
    vect2 = rotateVector(dirInit, data2.angle)
    # By convention we choose the vectors of the sides in a clockwise
    # way if they are adjacent. We will then only need a rotation in a counter
    # clockwise way to always have a vector facing the outside of the perimeter
    vectIni = vectorFromColors(data1.led, data2.led, perimeter)
    vectPerpendicular = rotateVector(vectIni, 90)
    angle1 = angleBetween2Vects(vect1, vectPerpendicular)
    angle2 = angleBetween2Vects(vect2, vectPerpendicular)

    if angle1 < angle2:
        angle1, angle2 = angle2, angle1
    distance = abs(data1.led.point.distance(data2.led.point))
    # if the two angles have different signs their product will be negative
    if angle1 * angle2 < 0:
        x = distance / (1 + math.tan(math.radians(abs(angle2))) /
                        math.tan(math.radians(abs(angle1))))
        y = distance - x
        d1 = x / math.sin(math.radians(abs(angle1)))
        d2 = y / math.sin(math.radians(abs(angle2)))
        return (d1, d2)
    else:
        diff = math.radians(abs(angle1) - abs(angle2))
        ret = math.sin(diff)
        if ret == 0.0:
            print("oooops")
            return (0, 0)
        x = distance * math.cos(math.radians(angle2)) / math.sin(diff)
        y = distance * math.cos(math.radians(angle1)) / math.sin(diff)
        return (x, y)


def compute2Data(data1, data2, *args):
    """Compute a set of position candidates from 2 datas

    Final synthetizing of all the datas related to 2 points and computing.

    Args:
        data1: first Data instance.

        data2: second Data instance.

        *args: dirInit, angleNorth, angleToDirection, perimeter.
        See distanceFromAngles.

    Returns:
        A list of candidate positions for the actual location
    """
    perimeter = args[-1]
    (dist1, dist2) = distanceFromAngles(data1, data2, *args)
    data1.adjustDistance(dist1)
    data2.adjustDistance(dist2)
    res = getPos2Dist(data1, data2)
    return filterPoints(res, perimeter)


def compute3Data(data1, data2, data3, *args):
    """Synthetize the position computations for 3 Datas instances.

    See **Compute2Data** for the arguments and return value.
    """
    res1 = compute2Data(data1, data2, *args)
    res2 = compute2Data(data2, data3, *args)
    res3 = compute2Data(data1, data3, *args)
    res = res1 + res2 + res3
    return res


def hasManyOccurencies(elt, listx):
    """Find if a point has many similar occurences in a list.

    This function is based on a threshold by default it is 80%.

    Args:
        elt: One element of the list.
        listx: The list of elements

    Returns:
        True if it is a very frequent element, False otherwise.
    """
    _threshold = 80.0
    count = 0
    for i in listx:
        if elt == i:
            count += 1
    goodPercent = count * 100 / len(listx)
    print(goodPercent)
    return goodPercent >= _threshold


def sortData(data_array):
    """Filter the datas in given in parameter if they appear often.

    Args:
        data_array: A list of Points candidates to be the actual
        location of the robot.

    Returns:
        The mean of the most frequent elements in the list.
    """
    data_array = [x for x in data_array if hasManyOccurencies(x, data_array)]
    x = 0.0
    y = 0.0
    for i in data_array:
        x += i.X
        y += i.Y
    return Point(x / len(data_array), y / len(data_array))
