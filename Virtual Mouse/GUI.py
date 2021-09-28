# Import Required Libraries
from tkinter import *
import cv2
import mediapipe as mp
import numpy as np
import time
import math
import autopy
import handtrackingmodule as htm
import os



############################### Define a method for Mouse Controller  ###############################
def onClickForHandTrackingAndMouseControl():
    ###############  STEPS  #################
    # Step 1: Find the landmarks
    # Step 2: Get the tip of the index and middle finger
    # Step 3: Check which fingers are up
    # Step 4: Only Index finder : it means it in in moving mode
    # Step 5: Convert Coordinates:
    # Because resolution of each computer machine is different
    # We need to convert those coordinates to computer resolution
    # Step 6: Smoothen Values
    # Step 7: Move Mouse
    # Step 8: Check Whether we are in clicking mode
    # if index finger and middle finger are up
    # Step 9: Find dinstance between index finger and middle
    # if distance is less than a limited distance
    # Then perform click funtion
    # Step 10: Frame Rate

    #################################################################
    # create object of VideoCam
    cap = cv2.VideoCapture(0)

    # Change the width and height of camera
    # initialize width of cam as wCam and height of cam as hCam
    (wCam, hCam) = (1280, 720)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    smoothening = 7

    # Create the object of handTrackingModukle
    detector = htm.HandDetector(maxHands=1)

    # previous time
    pTime = 0
    # current time
    cTime = 0

    # Set Frame Reduction
    frameR = 60
    # Find Out size of screen
    wScreen, hScreen = autopy.screen.size()
    # print("Size of screen:",wScreen,hScreen)

    if not cap.isOpened():
        print("Camera is not started")
    while True:
        success, flip = cap.read()
        img = cv2.flip(flip, 1)

        # Step 1: Find the landmarks
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)

        # Step 2: Get the tip of the index and middle finger
        if len(lmlist) != 0:
            x1, y1 = lmlist[8][1:]
            x2, y2 = lmlist[12][1:]
            # print(x1,y1,x2,y2)

            # Step 3: Check which fingers are up
            fingers = detector.fingersUp()

            # print("Up Fingers:",fingers)

            # draw a rectange on screen for the reason when the hand will be in rectangle
            # the cursor will move if finger is at a corner of rectangle then cursor should be at corner of computer screen
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 3)
            # Step 4: Only Index finder : it means it in in moving mode

            if (fingers[1] == 1) & (fingers[2] == 0):
                # Step 5: Convert Coordinates:
                # Because resolution of each computer machine is different
                # We need to convert those coordinates to computer resolution
                # Convert the range from width of webCam to width of Computer Screen
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScreen))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScreen))
                print("mouse location is:", x3, y3)

                # Step 6: Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # Step 7: Move Mouse
                autopy.mouse.move(clocX, clocY)  # (wScreen-x3) because when i move left cursor moves to the right
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            # Step 8: Check Whether we are in clicking mode
            # if index finger and middle finger are up
            if (fingers[1] == 1) & (fingers[2] == 1):

                distance, img, info = detector.findDistance(p1=8, p2=12, img=img)
                print("Length is:", distance)

                # Step 9: Find dinstance between index finger and middle
                # if distance is less than a limited distance
                # Then perform click funtion
                if distance < 40:
                    cv2.circle(img, (info[4], info[5]), 15, (0, 255, 0), cv2.FILLED)
                    print("Click Mode")

                    # Perform click Function
                    autopy.mouse.click()

        # Step 10: Frame Rate

        # current time
        cTime = time.time()

        # Calculate Frame Rate
        fps = 1 / (cTime - pTime)
        pTime = cTime
        # Put Text on screen to show Frame Rate
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # Step 11: Dispay
        cv2.imshow("Mouse Controller VideoCam", img)
        if not success:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break;


    cap.release()
    cv2.destroyAllWindows()




#####################  Create a Method for paint  ###########################
def onClickForPaint():
    folderPath = "header"
    myList = os.listdir(folderPath)
    print(myList)
    overLayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overLayList.append(image)
    print(len(overLayList))
    header = overLayList[0]

    # by default color chosen
    drawColor = (255, 0, 255)

    # brush thickness
    brushThickness = 10
    eraserThickness = 50

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # width
    cap.set(4, 720)  # height
    # 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
    # 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
    # 2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
    # 3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
    # 4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
    # 5. CV_CAP_PROP_FPS Frame rate.
    # 6. CV_CAP_PROP_FOURCC 4-character code of codec.
    # 7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
    # 8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
    # 9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
    # 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
    # 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
    # 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
    # 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
    # 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
    # 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
    # 16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
    # 17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
    # 18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

    detector = htm.HandDetector(detectionCon=0.90)
    xp, yp = 0, 0
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    while True:
        # 1. Import imageq
        success, img = cap.read()
        img = cv2.flip(img, 1)

        # 2. Find Hand Landmarks
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img, draw=False)  # to find the position of the landmarks

        if len(lmlist) != 0:
            # print(lmlist)

            # tip of index and middle fingers
            x1, y1 = lmlist[8][1:]

            # tip of middle finger and middle fingers
            x2, y2 = lmlist[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            print(fingers)

            # 4. If selection mode - Two fingers are up
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                print("Selection mode")
                # checking for the click
                if y1 < 125:
                    if 255 < x1 < 450:
                        header = overLayList[0]
                        drawColor = (255, 0, 255)
                    elif 550 < x1 < 750:
                        header = overLayList[1]
                        drawColor = (255, 0, 0)
                    elif 800 < x1 < 950:
                        header = overLayList[2]
                        drawColor = (0, 255, 0)
                    elif 1050 < x1 < 1200:
                        header = overLayList[3]
                        drawColor = (0, 0, 0)

                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            # 5. If Drawing mode - Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                print("Drawing mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        img[0:125, 0:1280] = header  # to place the image at the top of the video frame
        # img= cv2.addWeighted(img, 0.5,imgCanvas,0.5,0)
        cv2.imshow("Image", img)
        cv2.imshow("Canvas", imgCanvas)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break;



def onClickForQuitOut():
    print("RightClick Pressed")


############################################    CREATE GUI WINDOW   ################################################
window=Tk()


# set window title
window.title("Hand Detector - Mouse Controller GUI")

# Set size of window
window.wm_minsize(800,400)

# Set Background color of window
#window.configure(bg="blue")
#window["bg"]="green"
window["bg"]="#8790ff"

# Set Label
label1=Label(window,text="Hand Detector - Virtual Mouse & Painter",font=("Times New Roman",55,"bold"),bg="#8790ff").pack(pady=60)

# Set Button
button1=Button(window,font=("Times New Roman",17,"bold"),text="Click me to start Video Camera and Mouse Function",bg="#AD1457",command=onClickForHandTrackingAndMouseControl).pack()
button2=Button(window,font=("Times New Roman",17,"bold"),text="Click me for Paint",bg="#6A1B9A",command=onClickForPaint).pack(pady=10)
button3=Button(window,font=("Times New Roman",17,"bold"),text="Quit Out",bg="#8E24AA",command=onClickForQuitOut).pack(pady=10)




window.mainloop()
