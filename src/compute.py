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

    def eq(self, other):
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

data1 = Data(Color.RED, -92.48, 7.3)
data2 = Data(Color.GREEN, 3.67, 5.7)
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
    res2 = getPos2Dist(data2, data3)
    res2 = filterPoints(res2, map)
    if len(res) == 0:
        return None
    if len(res) == 1:
        return res[0]
    for i in res:
        for j in res2:
            if i.eq(j):
                return i;
    return None



if __name__ == '__main__':
    print(getPos3Dist(data1, data2, data3))
