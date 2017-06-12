import numpy as np
import argparse
import cv2
import sys

def print_distance(real_size, focal, size):
    distance = real_size * focal / size
    print distance
    return distance

def print_focal(size, distance, real_size):
    focal = size * distance / real_size
    print focal
    return focal

def get_size_of_light(keypoints, bin_image, source_image):
    min_x = 5000
    for k in keypoints:
        center_x = int(k.pt[0])
        if center_x < min_x:
            min_x = center_x
            center_y = int(k.pt[1])
            x_left = 0
            x_right = 0
            y_down = 0
            y_up = 0
            height, width, chan = source_image.shape
            while (center_x - x_left > 0 and
               bin_image[center_y, center_x - x_left] == 255):
                source_image[center_y, center_x - x_left] = [32, 124, 63]
                x_left += 1
            while (center_x + x_right < width and
               bin_image[center_y, center_x + x_right] == 255):
                source_image[center_y, center_x + x_right] = [32, 124, 63]
                x_right += 1

            while (center_y - y_up > 0 and
               bin_image[center_y - y_up, center_x] == 255):
                source_image[center_y - y_up, center_x] = [32, 124, 63]
                y_up += 1
            while (center_y + y_down < height and
               bin_image[center_y + y_down, center_x] == 255):
                source_image[center_y + y_down, center_x] = [32, 124, 63]
                y_down += 1
            size = (x_left + x_right + y_down + y_up - 2) / 2.0
    print size
    return size

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

def binarize_image(source_image):
    # load the image, clone it for output, and then convert it to grayscale
    copy_image = source_image.copy()
    gray = cv2.cvtColor(copy_image, cv2.COLOR_BGR2GRAY)
    ret, binarized_image = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    return binarized_image

def show_and_wait(image):
    cv2.imshow("output", image)
    cv2.waitKey(0)

def process_size(image_path):
    name = image_path
    source_image = cv2.imread(name)
    show_and_wait(source_image)
    bin_image = binarize_image(source_image)
    show_and_wait(bin_image)
    keypoints = get_keypoints(source_image)
    key_image = get_keypoints_image(keypoints, source_image)
    show_and_wait(key_image)
    size_obj = get_size_of_light(keypoints, bin_image, key_image)
    show_and_wait(key_image)
    #cv2.imwrite("/tmp/" + image_path, key_image)
    return size_obj

def main(argv=None):
    if argv is None:
        argv = sys.argv
    size_obj_focal = process_size("../tests/calque/3m.jpg")
    focal = print_focal(size_obj_focal, 300, 3.5)
    print "EXPECTED 300 => "
    print_distance(3.5, focal, size_obj_focal)
    print focal

    size_obj2 = process_size("../tests/calque/5m.jpg")
    print "EXPECTED 500 => "
    print_distance(3.5, focal, size_obj2)

    size_obj3 = process_size("../tests/calque/6m.jpg")
    print "EXPECTED 600 => "
    print_distance(3.5, focal, size_obj3)

    size_obj4 = process_size("../tests/calque/7m.jpg")
    print "EXPECTED 700 => "
    print_distance(3.5, focal, size_obj4)

    size_obj5 = process_size("../tests/calque/8m.jpg")
    print "EXPECTED 800 => "
    print_distance(3.5, focal, size_obj5)

    size_obj6 = process_size("../tests/calque/9m.jpg")
    print "EXPECTED 900 => "
    print_distance(3.5, focal, size_obj6)

    size_obj7 = process_size("../tests/calque/10m.jpg")
    print "EXPECTED 1000 => "
    print_distance(3.5, focal, size_obj7)

    size_obj8 = process_size("../tests/calque/2m.jpg")
    print "EXPECTED 200 => "
    print_distance(3.5, focal, size_obj8)

    size_obj9 = process_size("../tests/calque/4m.jpg")
    print "EXPECTED 400 => "
    print_distance(3.5, focal, size_obj9)

    size_obj10 = process_size("../tests/calque/1m.jpg")
    print "EXPECTED 100 => "
    print_distance(3.5, focal, size_obj10)

if __name__ == "__main__":
    sys.exit(main())
