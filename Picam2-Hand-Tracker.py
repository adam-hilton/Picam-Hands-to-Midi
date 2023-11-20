#Import the necessary Packages for this software to run
import mediapipe
import cv2
from picamera2 import Picamera2

#setup what I think will be the thing picam will send to open cv

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
#picam2.configure("preview")
#picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()

#Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

#Use CV2 Functionality to create a Video stream and add some values
#cap = cv2.VideoCapture()
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
     while True:
           im = picam2.capture_array()
           #ret, frame = cap.read()
           #Unedit the below line if your live feed is produced upsidedown
           im = cv2.flip(im, flipCode = -1)
           
           #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
           #frame1 = im
           #cv2.resize(im, (640, 480))
           
           #produces the hand framework overlay ontop of the hand, you can choose the colour here too)
           results = hands.process(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
           
           #Incase the system sees multiple hands this if statment deals with that and produces another hand overlay
           if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                  drawingModule.draw_landmarks(im, handLandmarks, handsModule.HAND_CONNECTIONS)
                  
                  #   Added Code to find Location of Index Finger !!
                  #for point in handsModule.HandLandmark:
                      
                      #normalizedLandmark = handLandmarks.landmark[point]
                      #pixelCoordinatesLandmark= drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, 640, 480)
                      
                      #if point == 8:
                          #print(point)
                          #print(pixelCoordinatesLandmark)
                          #print(normalizedLandmark)
            
           #Below shows the current frame to the desktop 
           cv2.imshow("Frame", im);
           key = cv2.waitKey(1) & 0xFF
           
           #Below states that if the |q| is press on the keyboard it will stop the system
           if key == ord("q"):
              break

