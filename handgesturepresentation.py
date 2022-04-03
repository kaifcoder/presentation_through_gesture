from operator import index
from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

width = 1280
height = 720

folderPath = "presentation"

# camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get the list of the presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

imgNumber = 0
hs, ws = 120, 213
gestureThreshold = 350
buttonPressed = False
buttonCounter = 0
buttonDelay = 20
annotationNumber = -1
annotationStart = False
annotations = [[]]
# hand
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # import images
    success, img = cap.read()
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    img = cv2.flip(img, 1)
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)

    cv2.line(img, (0, gestureThreshold),
             (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        # constraint values of easier drawing
        xVal = int(np.interp(lmList[8][0], [width//2, w], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal
        # print(fingers)

        if cy <= gestureThreshold:
            # gesture 1 - left
            if fingers == [1, 0, 0, 0, 0]:
                print('left')
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotationNumber = -1
                    annotationStart = False
                    annotations = [[]]

            # gesture 2 - right
            if fingers == [0, 0, 0, 0, 1]:
                print('right')
                buttonPressed = True
                if imgNumber < len(pathImages)-1:
                    imgNumber += 1
                    annotationNumber = -1
                    annotationStart = False
                    annotations = [[]]

            # gesture 3 - pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        # gesture 4- draw
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True

    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent, annotations[i][j-1],
                         annotations[i][j], (0, 0, 200), 12)

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w-ws:w] = imgSmall
    # cv2.imshow("Image", img)
    cv2.imshow("slide", imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
