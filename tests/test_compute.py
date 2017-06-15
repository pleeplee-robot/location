import pytest
import math
from pleeplee.compute import (LED, Data, getPos2Dist, perimeter, filterPoints,
        isAdjacent)
from pleeplee.geometry import Point
from pleeplee.utils import Color

def test_data_adjust_distance():
    data1 = Data(Color.RED, 38.45, 12.4)
    data2 = Data(Color.RED, 38.45)
    assert data1.adjustDistance(6.8) == 9.6
    assert data2.adjustDistance(6.8) == 6.8

def test_pos_2_dist_none():
    data1 = Data(Color.RED, 38.45, 12.4)
    data2 = Data(Color.RED, 38.45)
    with pytest.raises(ValueError):
        getPos2Dist(data1, data2)

def test_pos_2_dist_no_solution():
    corner1 = perimeter[0]
    corner2 = perimeter[1]
    distance = math.sqrt((corner1.point.X - corner2.point.X)**2 +
                         (corner1.point.Y - corner2.point.Y)**2)
    d1 = 1.4
    data1 = Data(corner1.color, 55.0, d1)
    data2 = Data(corner2.color, -35.0, distance - d1 - 0.2)
    data3 = Data(corner2.color, 67.3, distance + d1 + 4.0)
    assert getPos2Dist(data1, data2) == []
    assert getPos2Dist(data1, data3) == []

# Only works with the current map, In order to improve the tests the map
# has to be mocked
def test_pos_2_dist_easy():
    data1 = Data(Color.RED, 55.0, 3.8)
    data2 = Data(Color.GREEN, -35.0, 9.4)
    res = getPos2Dist(data1, data2)
    assert len(res) == 2
    assert Point(1.3, 3.5) in res

# same here with mocks
def test_filter_point():
    data1 = Data(Color.RED, 55.0, 3.8)
    data2 = Data(Color.GREEN, -35.0, 9.4)
    res = filterPoints(getPos2Dist(data1, data2), perimeter)
    assert len(res) == 1
    assert Point(1.3, 3.5) == res[0]

def test_is_adjacent():
    assert not isAdjacent(Color.RED, Color.RED)
    assert isAdjacent(perimeter[0].color, perimeter[1].color)
    assert not isAdjacent(perimeter[0].color, perimeter[2].color)

def test_adjust_angles():
    pass # TODO

def test_compute_dist_from_angles():
    pass # TODO

def test_vector_from_colors():
    pass # TODO

def test_dist_from_angles_no_rectangle():
    pass # TODO

def test_compute_2_data():
    pass # TODO
