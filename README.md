# The Project

PleePlee is a proof of concept of a mobile gardener robot.
This repository is about the location of the robot.

## Features

The PleePlee robot is able to:
- :seedling: :shower: Water plants.
- :car: Move in a straight line and turn in place.
- :bulb: :satellite: Localize itself in a small area delimited by luminous landmarks.
- :curly_loop: Avoid obstacles.
- :eyes: Log any changes to the garden. (Foreign object or person crossing).

## Location

This repositiory only contains the code for the location of the robot.
The robot is able to move in a predefined area delimited at each corner
by luminous landmark.
Each luminous landmark is built from LEDs and each corner will have a different
color.

The location is estimated with multiple datas:
  - the distance to each luminous landmark
  - the angle between the axis of the robot and each landmark
  - the position of the north
  - odometry

## Installation and requirements

To test or use the code you only need python 3.

To install the package:

```bash
$ git clone https://github.com/pleeplee-robot/location.git
```

Install using develop mode:

```bash
$ python setup.py develop
```

## Getting started


