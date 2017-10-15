#######################################################
# AUTHOR  : Ashkan Kiaie-Sandjie                      #
# SUMMARY : Contain the logic to compute the angle    #
#           between an object and the center of the   #
#           image                                     #
#######################################################

import numpy as np
import argparse
import cv2
import sys
import math

fov_horizontal = 53.50
width_res = 1024
height_res = 768


def get_angle_from(source_image):
    keypoints = get_keypoints(source_image)
    pixel_in_width = math.sqrt(math.pow(width_res, 2) + math.pow(width_res, 2))
    pixel_degree = fov_horizontal / pixel_in_width

    for k in keypoints:
        center_x = int(k.pt[0])
        return center_x * pixel_degree

    return 0.0

def print_distance(real_size, focal, size):
    distance = real_size * focal / size
    print(distance)
    return distance

def get_keypoints_image(keypoints, source_image):
    image_keypoints = cv2.drawKeypoints(
        source_image, keypoints, np.array([]),
        (0,0,255),
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return image_keypoints

def get_keypoints(source_image):
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 150
    params.maxThreshold = 255
    params.minArea = 40
    params.maxArea = 20000
    params.filterByArea = 1
    params.filterByColor = 1
    params.filterByConvexity = 1
    params.minConvexity = 0.60
    params.filterByInertia = 1
    params.filterByCircularity = 1
    params.minCircularity = 0.6
    params.minInertiaRatio = 0.6
    params.blobColor = 255
    detector = cv2.SimpleBlobDetector(params)
    keypoints = detector.detect(source_image)
    return keypoints

def show_and_wait(image):
    cv2.imshow("output", image)
    cv2.waitKey(0)

def process_size(image_path):
    name = image_path
    source_image = cv2.imread(name)
    angle = get_angle_from(source_image)
    return angle

def main(argv=None):
    if argv is None:
        argv = sys.argv
    angle = process_size("../tests/calque/3m.jpg")
    print angle

    angle = process_size("../tests/calque/5m.jpg")
    print angle

    angle = process_size("../tests/calque/6m.jpg")
    print angle

    angle = process_size("../tests/calque/7m.jpg")
    print angle

    angle = process_size("../tests/calque/8m.jpg")
    print angle

    angle = process_size("../tests/calque/9m.jpg")
    print angle


if __name__ == "__main__":
    sys.exit(main())
