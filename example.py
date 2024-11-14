from zoneinfo import available_timezones

import cv2
import pickle
import numpy as np
import cvzone
import string
import random


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

# car_classifier = cv2.CascadeClassifier("haarcascade_car.xml")

def generate_random_string(length=3):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def checkParkingSpace(imgPro):
    available_space = 0
    available_slots_name = []

    for pos in posList:
        x,y,label, is_occupied = pos
        imgCrop = imgPro[y:y+height, x:x+width]
        # cv2.imshow(str(x+y), imgCrop)
        count = cv2.countNonZero(imgCrop)

        cvzone.putTextRect(img, str(label), (x, y+height - 10), scale=1.5, thickness=2, offset=0)
        if count < 1700:
            color = (0,255,0)
            thickness = 5
            available_space += 1
            available_slots_name.append(label)
        else:
            color = (0,0,255)
            thickness = 2

        cv2.rectangle(img, (pos[0],pos[1]), (pos[0]+width, pos[1] + height), color, thickness=thickness)

    with open('CarParkStatus', 'wb') as f:
        pickle.dump({
            "total": available_space,
            "slots": available_slots_name
        }, f)




def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y, generate_random_string(), False))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1,y1, label, is_occupied = pos

            if x1 < x < x1+ width and y1 < y < y1+ width:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


def preprocess_dark_areas(img):
    # Convert to HSV for color detection
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define a range for dark colors (e.g., black)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    # Create a mask where dark colors are detected
    black_mask = cv2.inRange(hsv_img, lower_black, upper_black)
    # Convert detected black areas to white
    img[black_mask > 0] = [255, 255, 255]
    return img

running = True
while running:
    # img = cv2.imread("Parking2.jpg")

    # Capture frame-by-frame
    ret, img = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    img_copy = img.copy()
    imgProcessed = preprocess_dark_areas(img_copy)
    imgGray = cv2.cvtColor(imgProcessed, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25,15)
    imgMedian = cv2.medianBlur(imgThreshold, 5)


    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)



    # cv2.rectangle(img,(200, 100), (550 ,500), (255,0,255), 2)
    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0]+width, pos[1] + height), (255,0,255), 2)

    checkParkingSpace(imgDilate)

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



