# import required libraries
import cv2
import numpy as np
import handtrackingmodule as htm
import autopy
import time


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
cap=cv2.VideoCapture(0)

# Change the width and height of camera
# initialize width of cam as wCam and height of cam as hCam
(wCam,hCam)=(1280,720)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 7

# Create the object of handTrackingModukle
detector=htm.HandDetector(maxHands=1)

# previous time
pTime=0
# current time
cTime=0

# Set Frame Reduction
frameR=60
# Find Out size of screen
wScreen,hScreen=autopy.screen.size()
#print("Size of screen:",wScreen,hScreen)

if not cap.isOpened():
    print("Camera is not started")
while True:
    success,flip=cap.read()
    img = cv2.flip(flip, 1)

    # Step 1: Find the landmarks
    img=detector.findHands(img)
    lmlist,bbox=detector.findPosition(img)


    # Step 2: Get the tip of the index and middle finger
    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        #print(x1,y1,x2,y2)


    # Step 3: Check which fingers are up
        fingers=detector.fingersUp()

        #print("Up Fingers:",fingers)



        # draw a rectange on screen for the reason when the hand will be in rectangle
        # the cursor will move if finger is at a corner of rectangle then cursor should be at corner of computer screen
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),3)
    # Step 4: Only Index finder : it means it in in moving mode

        if (fingers[1]==1)&(fingers[2]==0):



   # Step 5: Convert Coordinates:
        # Because resolution of each computer machine is different
        # We need to convert those coordinates to computer resolution
        # Convert the range from width of webCam to width of Computer Screen
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScreen))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScreen))
            print("mouse location is:",x3,y3)


    # Step 6: Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening


    # Step 7: Move Mouse
            autopy.mouse.move(clocX, clocY)  # (wScreen-x3) because when i move left cursor moves to the right
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY


    # Step 8: Check Whether we are in clicking mode
              # if index finger and middle finger are up
        if (fingers[1]==1)&(fingers[2]==1):

            distance,img,info=detector.findDistance(p1=8,p2=12,img=img)
            print("Length is:",distance)


    # Step 9: Find dinstance between index finger and middle
            # if distance is less than a limited distance
            # Then perform click funtion
            if distance<40:
                cv2.circle(img,(info[4],info[5]),15,(0,255,0),cv2.FILLED)
                print("Click Mode")

                # Perform click Function
                autopy.mouse.click()







    # Step 10: Frame Rate


    # current time
    cTime=time.time()

    # Calculate Frame Rate
    fps=1/(cTime-pTime)
    pTime=cTime
    # Put Text on screen to show Frame Rate
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Step 11: Dispay
    cv2.imshow("Mouse Controller VideoCam",img)
    if not success:
        break
    c = cv2.waitKey(1)
    if c == 27:
        break
cap.release()
cv2.destroyAllWindows()