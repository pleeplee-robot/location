# The Project

We are three students soon-to-be system and embeded engineers.
PleePlee is a small gardener robot we are building for our master's project.

## Location

This repository is about the location of the robot. The robot will be able to
move in a predefined area delimited at each corner by luminous landmark.
Each luminous landmark is built from LEDs and each corner will have a different
color.

The location is estimated with multiple datas:
  - the distance to each luminous landmark
  - the angle between the axis of the robot and each landmark
  - the position of the north
  - odometry

## TODO

* Compute location
  * [X] Complete the algorithm for non adjacent points
  * [X] Calculation of the angles with the vectors
  * [X] Synthetize the computations for 3 and 4 points
  * [X] Odometry
  * [X] Height parameter for the LEDs
  * [ ] Clean code : replace geometry by shapely
  * [X] Clean code : make if PEP8 compliant (yapf, flake8, isort)
  * [X] Clean code : refactor utils
  * [ ] Add Documentation
