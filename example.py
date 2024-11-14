from zoneinfo import available_timezones

import cv2
import pickle
import numpy as np
import cvzone

width, height = 120,150
move_offset = 400

cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

car_classifier = cv2.CascadeClassifier("haarcascade_car.xml")

def checkParkingSpace(imgPro, imgGray):
    available_space = 0

    for pos in posList:
        x,y = pos
        imgCrop = imgPro[y:y+height, x:x+width]
        # cv2.imshow(str(x+y), imgCrop)
        count = cv2.countNonZero(imgCrop)

        cvzone.putTextRect(img, str(count), (x, y+height - 10), scale=1.5, thickness=2, offset=0)

        # cropGray = imgGray[y:y+height, x:x+width]
        # cars = car_classifier.detectMultiScale(cropGray, 1.4,2)
        # print(len(cars))
        if count < 1700:
            color = (0,255,0)
            thickness = 5
            available_space += 1

        else:
            color = (0,0,255)
            thickness = 2


        cv2.rectangle(img, pos, (pos[0]+width, pos[1] + height), color, thickness=thickness)


def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1,y1 = pos

            if x1 < x < x1+ width and y1 < y < y1+ width:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

running = True
while running:
    # img = cv2.imread("Parking2.jpg")

    # Capture frame-by-frame
    ret, img = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25,15)
    imgMedian = cv2.medianBlur(imgThreshold, 5)


    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)



    # cv2.rectangle(img,(200, 100), (550 ,500), (255,0,255), 2)
    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0]+width, pos[1] + height), (255,0,255), 2)

    checkParkingSpace(imgDilate, imgGray)

    cv2.imshow("Window", img)
    # cv2.imshow("Dilated", imgThreshold)

    cv2.setMouseCallback("Window", mouseClick)
    # cv2.imwrite("captured_image.jpg", img)
    cv2.waitKey(1)
    # cv2.destroyAllWindows()
    #
    # # Release the camera
    # cap.release()
    #
    # running = False