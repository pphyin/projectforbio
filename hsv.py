from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse

max_value = 255
max_value_H = 360 // 2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H - 1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H + 1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S - 1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S + 1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V - 1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V + 1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)


# parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
# parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
# args = parser.parse_args()
# cap = cv.VideoCapture(args.camera)

image = cv.imread("color3.png")

cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)

# cv.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
# cv.createTrackbar(high_H_name, window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
# cv.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
# cv.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
# cv.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
# cv.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)

# Setting up blob detection
params = cv.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 100
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False

detector = cv.SimpleBlobDetector_create(params)

while True:

    # ret, frame = cap.read()
    if image is None:
        break
    frame_HSV = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(frame_HSV)
    white = 255 * np.ones_like(h)
    threshH = white - cv.inRange(h, 44, 126)
    threshS = cv.inRange(s, 44, 100)
    threshV = cv.inRange(v, 50, 100)
    frame_threshold = threshH & threshS & threshV
    frame_threshold = cv.medianBlur(frame_threshold, 5)

    key_points = detector.detect(255 - frame_threshold)


    im_with_key_points = cv.drawKeypoints(frame_threshold, key_points, np.array([]), (0, 0, 255),
                                          cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    x = 0.0
    y = 0.0
    s = 1.0
    try:
        x = key_points[0].pt[0]
        y = key_points[0].pt[1]
        s = key_points[0].size
        checkForBlack = True
        while checkForBlack:
            y = y + 1
            if frame_threshold.item(int(y), int(x)) == 0:
                checkForBlack = False
    except:
        print("")

    print(int(x), int(y))
    cv.circle(im_with_key_points, (int(x), int(y) - 1), 1, (0, 255, 0), -1)
    cv.imshow(window_capture_name, image)
    cv.imshow(window_detection_name, im_with_key_points)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break
