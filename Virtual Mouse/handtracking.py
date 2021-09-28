import cv2
import mediapipe as mp

# FOR CHECKING THE FRAME RATE
import time

# CREATE A VIDEOCAPTURE OBJECT
cap = cv2.VideoCapture(0);

#  TO DETECT HAND
mpHands = mp.solutions.hands

# WE HAVE CREATED A MEDIAPIPE 'HANDS' OBJECT, THUS DETECTING HAND WITH HELP OF THE 21 GIVEN POINTS)
# PARAMS :-
#  static_image_mode = false means  DETECTION + TRACKING (if tracking confidence is above some threshold)
# SINCE DEFAULT PARAMS USED, WE HAVE NOT PASSED ANYTHING TO Hands
hands = mpHands.Hands();

mpDraw = mp.solutions.drawing_utils

# NOW WE WILL CHECK FRAME RATE SO FOR THAT WE WILL DEFINE PTIME , CTIME
ptime = 0
ctime = 0

if not cap.isOpened():
    print("Camera is not started yet")
while True:
    # CAPTURE IMAGE FRAME BY FRAME
    # RETURNS BOOL AND FRAME , TRUE IF FRAME IS READ CORRECTLY IN BGR FORMAT
    success,img = cap.read();

    # CONVERT IMAGE TO RGB
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB);


    #  THIS METHOD PERFORMS HAND LANDMARK ESTIMATION AND THIS METHOD EXPECTS RGB  FORMAT IMAGE
    results = hands.process(imgRGB)

    #  IF WE WANT TO GET THE LANDMARK OF OUR  HANDS
    print(results.multi_hand_landmarks);

    # CHECK IF MULTIPLE HANDS ARE THERE ,AND IF YES, EXTRACT THEM
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            # HERE WE ARE LOCATING THE 21(0-20) POINTS OF OUR HAND WITH X AND Y COORDINATES FOR EACH HAND FRAME
            for id, lm in enumerate(handlms.landmark):
                # print(id,lm)

                # we are taking height, width and channel
                h, w, c= img.shape

                # Convert the different parameters into pixels
                cx , cy = int(lm.x* w), int(lm.y* h)

                # identify id with locations in pixels
                #print(id, cx, cy)

                # now we will draw a circle for id 0
                if id==8:
                     cv2.circle(img, (cx , cy), 20, (255,0,255), cv2.FILLED)

                # now we will draw a circle for id 4
                if id ==12:
                    cv2.circle(img, (cx, cy), 20, (255, 255, 0), cv2.FILLED)


            # FOR DRAWING LANDMARKS (HAND_CONNECTIONS HELP TO JOIN THE 21 POINTS TO THE RESPECTIVE POINTS)
            mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS);

    ctime = time.time()
    fps= 1/(ctime-ptime)
    ptime = ctime

    # HERE WE ARE DISPLAYING THE FPS ALONG WITH THE VIDEO
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    # TO DISPLAY THE FRAME
    cv2.imshow("Hand Detector WebCam",img);

    if not success:
        break;
    # IF USER PRESS  Q THEN WE HAVE TO QUIT
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break;

# When Everything Done Release the capture
cap.release()

# Destroy All the windows
cv2.destroyAllWindows()