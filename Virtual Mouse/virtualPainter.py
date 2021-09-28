import cv2
import numpy as np
import time #for fps
import os # to acces this files
import handtrackingmodule as htm

folderPath= "header"
myList = os.listdir(folderPath)
print(myList)
overLayList=[]
for imPath in myList:
    image= cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)
print(len(overLayList))
header= overLayList[0]

# by default color chosen
drawColor = (255,0,255)

# brush thickness
brushThickness= 10
eraserThickness= 50

cap= cv2.VideoCapture(0)
cap.set(3,1280) # width
cap.set(4,720) # height
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
xp, yp=0,0
imgCanvas= np.zeros((720, 1280,3),np.uint8)


while True:
   # 1. Import image
   success, img= cap.read()
   img = cv2.flip(img, 1)

   # 2. Find Hand Landmarks
   img = detector.findHands(img)
   lmlist,bbox = detector.findPosition(img, draw=False) # to find the position of the landmarks

   if len(lmlist)!= 0:
       # print(lmlist)

       # tip of index and middle fingers
       x1,y1 = lmlist[8][1:]

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
           if y1< 125:
               if 255<x1<450:
                   header= overLayList[0]
                   drawColor= (255,0,255)
               elif 550 <x1 <750:
                   header= overLayList[1]
                   drawColor = (255, 0, 0)
               elif 800 <x1 < 950:
                   header= overLayList[2]
                   drawColor = (0, 255, 0)
               elif 1050 <x1 <1200:
                   header= overLayList[3]
                   drawColor = (0, 0, 0)

           cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
       # 5. If Drawing mode - Index finger is up
       if fingers[1] and fingers[2] == False:
           cv2.circle(img, (x1, y1), 15,drawColor, cv2.FILLED)
           print("Drawing mode")
           if xp==0 and yp==0:
               xp, yp= x1,y1

           if drawColor == (0,0,0):
               cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
               cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

           else:
               cv2.line(img, (xp,yp),(x1,y1), drawColor, brushThickness)
               cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

           xp,yp = x1,y1

   imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
   _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
   imgInv= cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
   img = cv2.bitwise_and(img, imgInv)
   img = cv2.bitwise_or(img, imgCanvas)

   img[0:125,0:1280]= header #to place the image at the top of the video frame
   # img= cv2.addWeighted(img, 0.5,imgCanvas,0.5,0)
   cv2.imshow("Image",img)
   cv2.imshow("Canvas", imgCanvas)
   cv2.waitKey(1)