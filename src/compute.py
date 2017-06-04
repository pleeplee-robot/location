import math
from enum import Enum

# position is in meter
# angles are from -180 to 180 degree

PRECISION = 4
class Point:

    # Thresold to determine that two points are similar (distance < 15cm)
    _threshold = 0.15

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y)

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return round(math.sqrt(dx**2 + dy**2), PRECISION)

    def __eq__(self, other):
        return self.distance(other) < self._threshold

class Color(Enum):
    NONE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

class LED:

    def __init__(self, color, point):
        self.color = color
        self.point = point
        self.angle = 0

    def __str__(self):
        return "LED(Position: %s ;Color : %s )"%(self.point, self.color)

# the map is represented by 4 leds positionned at each corner of the area
# available to the robot

corner1 = LED(Color.RED, Point(0.0, 0.0))
corner2 = LED(Color.GREEN, Point(10.0, 0.0))
corner3 = LED(Color.BLUE, Point(0.0, 10.0))
corner4 = LED(Color.YELLOW, Point(10.0, 10.0))

map = [corner1, corner2, corner3, corner4]

def _getLED(color):
    for i in map:
        if i.color == color:
            return i
    raise ValueError('Color not found')

class Data:

    def __init__(self, color, angle, distance=None):
        self.angle = angle
        self.distance = distance
        try:
            self.led = _getLED(color)
        except ValueError as error:
            print('The color does not correspond to an existing LED')

data1 = Data(Color.RED, 55.0, 3.8)
data2 = Data(Color.GREEN, -35.0, 9.4)
data3 = Data(Color.YELLOW, 115.58, 7.0)

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


def getPos3Dist(data1, data2, data3):
    res = getPos2Dist(data1, data2)
    res = filterPoints(res, map)
    if len(res) == 0:
        return None
    if len(res) == 1:
        return res[0]
    res2 = getPos2Dist(data2, data3)
    res2 = filterPoints(res2, map)
    for i in res:
        if i in res2:
            return i;
    return None

# Angle between the north and the axis of the robot at Initialisation
# (same axis as an edge of the perimeter)
# This angle is a fixed data measured at the initialization of the robot.
# The angle is between 180 and -180 degree
# We can imagine that an option will make available the last angle measured if
# the map hasn't changed.
# The instruction is for the user to put the robot parralel to an edge of the
# perimeter of the garden to enable easier computations.
# We can also suppose that if our datas are sufficient this constraint can be
# an option left to the user in order to improve the location
angleNorth = 20.0

# Before the initialisation the user will input the map with each color
# corresponding to each corner of the map. He will also have to input the
# direction where the robot is initialized.
# The following vector is the direction it is initialized.
# This data may not be needed

# dirInit = (0, 10)

# The map will have the following conventions:
#  R(0, 0)                                  G(10, 0)
#       _____________________________________
#      |                                     |
#      |                                     |
#      |                                     |
#      |                                     |
#      |                                     |
#      |                                     |
#      |                                     |
#      |                                     |
#       _____________________________________
#  Y(0, 10)                                  B(10, 10)
# For now as we don't have yet the map representation these fake datas
# will represent the order of the corners
mapCorners = {Color.RED: 0, Color.GREEN: 1,
        Color.BLUE: 2, Color.YELLOW: 3}

def isAdjacent(color1, color2):
    if color1 == color2:
        return false;
    val = abs(mapCorners[color1] - mapCorners[color2])
    return val == 1 or val == 3

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

# Angle between actual direction and North
# This data can be harvested in real time with a magnetic captor
# for now we will keep this fake value
angleToDirection = 35.0

# Convert angle from (LED -> Actual direction) to (LED -> edge of perimeter)
def convertAngle(alpha):
    return alpha + angleToDirection + angleNorth

# Rotate the angle in a counter-clockwise way
def rotateAngle(alpha):
    if alpha + 45 > 180:
        alpha -= 360
    return alpha + 45

# Rectangle triangle to ease computations
class Triangle:

    # with alph the angle from actual direction to LED
    def __init__(self, data):
        # angle from the point we try to find the location
        self.angleP = convertAngle(data.angle)
        # corner of the perimeter
        self.point = data.led.point
        self.color = data.led.color
        # offset to the standard direction
        self.offset = 0

    # angle from the led at a corner of the perimeter
    def cornerAngle(self):
        return 90.0 - self.angleP

    def __str__(self):
        return "TRIANGLE(%s ;%s)"%(self.angleP, self.cornerAngle())

def adjustAngles(triangle1, triangle2):
    while abs(triangle1.angleP) + abs(triangle2.angleP) > 90:
        triangle1.angleP = rotateAngle(triangle1.angleP)
        triangle2.angleP = rotateAngle(triangle2.angleP)
        triangle1.offset += 1
        triangle2.offset += 1

# the two triangle P point must be the same
def computeDistFromAngles(triangle1, triangle2):
    if not isAdjacent(triangle1.color, triangle2.color):
        # TODO Opposite sides algorithm
        pass
    adjustAngles(triangle1, triangle2)
    distance = abs(triangle1.point.distance(triangle2.point))
    x = distance / (1 + math.tan(math.radians(abs(triangle2.angleP))) /
            math.tan(math.radians(abs(triangle1.angleP))))
    y = distance - x
    d1 = x / math.sin(math.radians(abs(triangle1.angleP)))
    d2 = y / math.sin(math.radians(abs(triangle2.angleP)))
    return (d1, d2)

def compute2Data(data1, data2):
    (dist1, dist2) = computeDistFromAngles(Triangle(data1), Triangle(data2))
    # TODO : Complete this function
    print("1: {}, 2: {}".format(dist1, dist2))

if __name__ == '__main__':
    print(getPos3Dist(data1, data2, data3))
    compute2Data(data1, data2)
