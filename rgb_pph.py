import cv2
import numpy as np
import imutils
import re
import matplotlib.pyplot as plt

all_expected_x = []
all_expected_y = []
all_actual_x = []
all_actual_y = []
all_files = ['X1small_Y0bigL_east.jpg', 'X2small_Y0bigL_east.jpg', 'X2small_Y0bigR_west.jpg', 'X3big_Y1smallR_north.jpg', 'X3big_Y2smallL_south.jpg',
    'X3big_Y3smallL_south.jpg', 'X7big_Y0smallR_south.jpg', 'X5big_Y0smallR_south.jpg', 'X5big_Y1smallL_south.jpg', 'X5big_Y1smallR_south.jpg',
    'X5big_Y2smallL_south.jpg', 'X5big_Y2smallR_south.jpg', 'X5big_Y4smallR_south.jpg', 'X5big_Y5smallR_south.jpg', 'X5big_Y6smallL_south.jpg',
    'X5small_Y1bigR_west.jpg', 'X7small_Y1bigR_west.jpg']

def equalize_img(image): #Split the images into different channel and merge and eualize them
    b,g,r = cv2.split(img)
    Red = cv2.equalizeHist(r)
    Green = cv2.equalizeHist(g)
    Blue = cv2.equalizeHist(b)
    eql_img = cv2.merge((Blue, Green, Red))
    cv2.imshow('equalized', eql_img)
    cv2.waitKey(0)
    return eql_img

def find_bounds(ini_image):      # find mostly red pixels, note that array is BGR
                                 # range based on which way it's facing
    if "north.jpg" in ini_image:
        lb = np.array([130, 90, 180])
        ub = np.array([165, 120, 220])
    elif ("east" in ini_image) | ("west" in ini_image):
        lb = np.array([60, 60, 250])
        ub = np.array([255, 255, 255])
    else:
        lb = np.array([50, 50, 250])
        ub = np.array([230, 230, 255])
    return lb, ub


i = 0 #for counting  
for ini_image in all_files:   #main loop   
    
    print("reading",ini_image,i)
    img = cv2.imread(ini_image)
    cv2.imshow('img', img)
    cv2.waitKey(0)      #wait till keyboard interrupt


    eql_img = equalize_img(img)

    
    lb, ub = find_bounds(ini_image)
    mask = cv2.inRange(eql_img,lb,ub)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)

    # find contour in mask image
    contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour  = imutils.grab_contours(contour)

    # use filename to find cones' size
    size = ini_image.split('_')
    # determine minimum threshold of contour shape to be used later based on size of cone
    if "small" in size[1]:
        MIN_THRESH = 10
    else:
        MIN_THRESH = 100

    # outline all contours found if area of contour > MIN_THRESH
    for c in contour:
        if cv2.contourArea(c) > MIN_THRESH:
            # draw red contour around cone
            cv2.drawContours(img, [c], -1, (0, 0, 0), 2)
            base = tuple(c[c[:, :, 1].argmax()][0])
            print("pixel(x,y): ", base)
            # draw green dot at base of cone
            cv2.circle(img, base, 2, (0, 0, 0), -1)
            cv2.imshow("Cone", img)
            cv2.waitKey(0)

    # convert pixel (x,y) coordinate to image(x,y)
    # 1 pixel = 1.12um
    i_y_p = float(base[0] * 1.12 * 10**-6)
    i_z_p = float(base[1] * 1.12 * 10**-6)

#*********************************************************************************************************
#*********************************************************************************************************

    # TO DO: FIX SCALING OF H, F HERE
    # compute c_x_p, c_y_p from image(x,y)
    # focal = 3040 um, height= 13.4cm
    h = 13.4 * 10**-2
    f = 3040 * 10**-6
    c_x_p = h * f / i_z_p
    c_y_p = h * i_y_p / i_z_p
    print("(c_x_p, c_y_p): ", c_x_p, ",", c_y_p)
    all_expected_x.append(c_x_p)
    all_expected_y.append(c_y_p)

    # compute actual x, y
    # extract number of tiles in x direction and what size (big vs small)
    segments = ini_image.split("_")
    x_dir = re.split("([0-9])", segments[0])
    small_tile = 40.5 * 10**-2
    big_tile = 92 * 10**-2
    if "big" in x_dir[2]:
        actual_x = (float(x_dir[1]) * big_tile)
    else:
        actual_x = (float(x_dir[1]) * small_tile)

    # same logic as above
    y_dir = re.split("([0-9])", segments[1])
    if "big" in y_dir[2]:
        actual_y = (float(y_dir[1]) * big_tile)
    else:
        actual_y = (float(y_dir[1]) * small_tile)

    print("(actual_x, actual_y): ", actual_x, ",", actual_y)
    all_actual_x.append(actual_x)
    all_actual_y.append(actual_y)
    
    print("\n")

    i += 1

# plot expected and actual (x,y)
plt.plot(all_expected_x, all_expected_y, 'ro')
plt.plot(all_actual_x, all_actual_y, 'b+')
plt.xlabel("x")
plt.ylabel("y")
plt.title('Expected locations in red circles, actuals in blue plus sign')
plt.show()





