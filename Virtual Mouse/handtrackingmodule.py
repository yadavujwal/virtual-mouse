import cv2
import mediapipe as mp
import math
# FOR CHECKING THE FRAME RATE
import time
import numpy as np


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # TO DETECT HAND
        self.mpHands = mp.solutions.hands

        # WE HAVE CREATED A MEDIAPIPE 'HANDS' OBJECT, THUS DETECTING HAND WITH HELP OF THE 21 GIVEN POINTS)
        # PARAMS :-
        #  static_image_mode = false means  DETECTION + TRACKING (if tracking confidence is above some threshold)
        # SINCE DEFAULT PARAMS USED, WE HAVE NOT PASSED ANYTHING TO Hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]
    def findHands(self, img, draw=True):

        # CONVERT IMAGE TO RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # THIS METHOD PERFORMS HAND LANDMARK ESTIMATION AND THIS METHOD EXPECTS RGB  FORMAT IMAGE
        self.results = self.hands.process(imgRGB)

        # IF WE WANT TO GET THE LANDMARK OF OUR  HANDS
        # print(self.results.multi_hand_landmarks);

        # CHECK IF MULTIPLE HANDS ARE THERE ,AND IF YES, EXTRACT THEM
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    # FOR DRAWING LANDMARKS (HAND_CONNECTIONS HELP TO JOIN THE 21 POINTS TO THE RESPECTIVE POINTS)
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS);

        return img


    def findPosition(self,img, handNo=0, draw=True):

        xList=[]
        yList=[]
        bbox=[]

        # Initialize a List to append id with location of landmarks
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myhand= self.results.multi_hand_landmarks[handNo]
        # HERE WE ARE LOCATING THE 21(0-20) POINTS OF OUR HAND WITH X AND Y COORDINATES FOR EACH HAND FRAME
            for id, lm in enumerate(myhand.landmark):

                # By default the landmarks given by WebCam contains height, Width and Channel that is ratio of Image
                # But We Need Location in Pixel
                # Get The shape
                h, w, c= img.shape

                # we are taking height, width and channel so that we can convert the landmark which was in ratio to pixles
                cx , cy = int(lm.x* w), int(lm.y* h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id,cx,cy])



                # now we will draw a circle for id 8
                # if id == 8:
                if id==8:
                   cv2.circle(img, (cx , cy), 10, (255,0,0), cv2.FILLED)
                if id==12:
                    cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
            xmin,xmax=min(xList),max(xList)
            ymin,ymax=min(yList),max(yList)
            bbox=xmin,ymin,xmax,ymax

        return self.lmList,bbox


    def fingersUp(self):

        fingers=[]

        #Thumb
        #print(self.lmList,self.tipIds)
        if self.lmList[self.tipIds[0]][1]>self.lmList[self.tipIds[0]-1][1]:
           fingers.append(1)
        else:
           fingers.append(0)


        # Fingers
        for id in range(1,5):

            if self.lmList[self.tipIds[id]][2]<self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers



# Define a Method to find the distanv=ce between two landmarks
    def findDistance(self,p1,p2,img,draw=True,r=15,t=3):
        x1,y1=self.lmList[p1][1:]
        x2,y2=self.lmList[p2][1:]
        cx=(x1+x2)//2
        cy=(y1+y2)//2
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),t)
            cv2.circle(img,(x1,y1),r,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),r,(255,0,255),cv2.FILLED)
            cv2.circle(img,(cx,cy),r,(0,0,255),cv2.FILLED)
            length=math.hypot(x2-x1,y2-y1)

        return length,img,[x1,y1,x2,y2,cx,cy]
def main():
    # NOW WE WILL CHECK FRAME RATE SO FOR THAT WE WILL DEFINE PTIME , CTIME
    ptime = 0
    ctime = 0

    # CREATE A VIDEOCAPTURE OBJECT
    cap = cv2.VideoCapture(0)

    # in case camera is not open
    if not cap.isOpened():
        print("Camera is not started")

    # Create object of class HandDetector
    detector = HandDetector()

    # Apply Infinite For Loop
    while True:
        # CAPTURE IMAGE FRAME BY FRAME
        # RETURNS BOOL AND FRAME , TRUE IF FRAME IS READ CORRECTLY IN BGR FORMAT
        success, img = cap.read()

        # call findHands method to get hand drawn
        img = detector.findHands(img)



        # Call findPosition() method to get different landmarks of hand
        lmlist,bbox = detector.findPosition(img)
        #print("Hello lmlist:",lmlist)
        if len(lmlist) !=0:
            print(lmlist[8])
        else:
            print("No Hand Detected")



        #Call FingersUp() method to know which finger is up
        # it will return a list containing 0m and 1
        # 0 indicates the finger is down
        # 1 indicates finger is up
        # if len(lmlist)!=0:
        #    fingers=detector.fingersUp()
        #    print("Finger Up:",fingers)
        # else:
        #     print("No Hand Detected")





        #Call findDistance() funtion to cross check whether it is working or not
        # it will return distance between two fingers, image and some info
        #if len(lmlist)!=0:

         #  distance,img,info=detector.findDistance(p1=8,p2=12,img=img)
          # print("Distance between index finger and middle finger",distance)
           #print("Info",info)
        #else:
         #   print("No Hand Found")






        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        # HERE WE ARE DISPLAYING THE FPS ALONG WITH THE VIDEO
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # TO DISPLAY THE FRAME
        cv2.imshow("Hand Ditector WebCame", img);

        # if succcess is false
        if not success:
            break

        # IF USER PRESS  Q THEN WE HAVE TO QUIT
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break


if __name__ == "__main__":
    main()
