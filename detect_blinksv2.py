# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from numpy import interp
import numpy as np
import argparse
import threading
import imutils
import time
import pyautogui
import dlib
import cv2

interp(256,[1,512],[5,10])


c=(0,0)
r=(0,0)
eucleft=0
eucright=0
euctop=0
eucbot=0
flag=True
firstval=0.0
ran=0.0

def move():
    speedx=0
    speedx1=0
    speedy=0
    speedy1=0
    while(True):
        if(eucleft<eucright-5 or eucright<eucleft-5 or ran<firstval-3 or firstval<ran-3):
            i=(eucleft+2)- eucright
            j=(ran+3)-firstval
            #print ran, firstval
            
            #print speed
            #i=(i+3)/(6)*20
            #j=(j+3)/(6)*20
            if(i<0):
                i=i-speedx
            if(i>0):
                i=i+speedx

            if(j<0):
                j=j-speedx1
            if(j>0):
                j=j+speedx1
            #print speed
            
            pyautogui.moveRel(i,j)
            
        #print ry
       # else:
        #    speed=0
    #

        else:
            speedy1=0
            speedx1=0
            speedx=0
            speedy=0
        

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=False,
	help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="",
	help="path to input video file")
args = vars(ap.parse_args())
 
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.23
EYE_AR_CONSEC_FRAMES = 2

# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("dl.dat")

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
#vs = FileVideoStream(args["video"]).start()
#fileStream = True
vs = VideoStream(src=0).start()

#fps = vs.get(cv2.CAP_PROP_FPS)
print ("Frames per second  : {0}".format(vs.__dict__.keys()))
     


# vs = VideoStream(usePiCamera=True).start()
fileStream = False
time.sleep(1.0)



t=threading.Thread(target=move,args=())
t.start()




# loop over frames from the video stream
while True:
	# if this is a file video stream, then we need to check if
	# there any more frames left in the buffer to process
	if fileStream and not vs.more():
		break

	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale
	# channels)
	frame = vs.read()
	frame = imutils.resize(frame, width=420)
	frame = frame[80:360,120:420]
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
			COUNTER += 1

		# otherwise, the eye aspect ratio is not below the blink
		# threshold
		else:
			# if the eyes were closed for a sufficient number of
			# then increment the total number of blinks
			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				TOTAL += 1
				pyautogui.click()
				
				
				

			# reset the eye frame counter
			COUNTER = 0

		# draw the total number of blinks on the frame along with
		# the computed eye aspect ratio for the frame
                #print(shape[2][0],shape[33][0])
                #print(dist.euclidean(shape[2][0], shape[13][0]))
		rx=(dist.euclidean(shape[2][0], shape[30][0]))
		rx1=(dist.euclidean(shape[30][0], shape[13][0]))
		ry=(dist.euclidean(shape[23][1], shape[33][1]))
		ry1=(dist.euclidean(shape[8][1], shape[33][1]))
		cv2.putText(frame, "EAR: {:}".format(ear), (30, 70),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                #cv2.putText(frame, "rx1: {:}".format(rx1), (90, 110),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                #cv2.putText(frame, "ry: {:}".format(ry), (90, 150),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                #cv2.putText(frame, "ry1: {:}".format(ry1), (90, 170),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                       # (x,y)=shape[2]
                        
                       # cv2.circle(frame,(x,y), 1, (0, 0, 255), -1)
                       # (x,y)=shape[14]
                       # cv2.circle(frame,(x,y), 1, (0, 0, 255), -1)
		(x,y)=(shape[2]+shape[15])/2
		r=(x,y)
				#cv2.circle(frame,(x,y), 1, (0, 0, 255), -1)
		(b1,b2)=shape[29]+(0,12)
		c=(b1,b2)
                        #cv2.circle(frame,(b1,b2), 1, (0, 0, 255), -1)
	#for (x,y) in shape:
                        #cv2.circle(frame,(x,y), 1, (0, 0, 255), -1)
		tx=0
		ty=0


		for (x,y) in shape:
				tx,ty=tx+x,ty+y

                #print tx
                #print ty
				avg=(shape[19]+shape[24])/2
				cv2.circle(frame,(int(avg[0]),int(avg[1])), 1, (0, 0, 255), -1)
				rightCenter = (shape[2]+shape[1]+shape[3])/3
				
				leftCenter  = (shape[14]+shape[13]+shape[15])/3
				


				calculatedCenter=(rightCenter+leftCenter)/2
				bottom=shape[8]
				

				
				cv2.circle(frame,(int(calculatedCenter[0]),int(calculatedCenter[1])), 1, (0, 0, 255), -1)
				cv2.circle(frame,(int(rightCenter[0]),int(rightCenter[1])), 1, (0, 0, 255), -1)
				cv2.circle(frame,(int(leftCenter[0]),int(leftCenter[1])), 1, (0, 0, 255), -1)
		#cv2.circle(frame,(tx/68,ty/68), 1, (0, 0, 255), -1)
				cv2.circle(frame,(int(shape[8][0]),int(shape[8][1])), 1, (255, 0, 0), -1)
				eucleft=(dist.euclidean(leftCenter[0],shape[33][0]))
				eucright=(dist.euclidean(rightCenter[0],shape[33][0]))
				cv2.putText(frame, "euLe: {}".format(eucleft), (170, 110),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "euri: {}".format(eucright), (130, 150),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

							   
		cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                #print(dist.euclidean(shape[8][1],(leftCenter+rightCenter)/2))
                #print(shape[8][1])
		#print(tx/68,ty/68)
		#print((leftCenter+rightCenter)/2)
		pivot=(leftCenter+rightCenter)/2
		cv2.circle(frame,(int(pivot[0]),int(pivot[1])), 1, (0, 255, 0), -1)
		
		euctop=dist.euclidean(pivot[1],(shape[8][1]))
		cv2.putText(frame, "eutop: {}".format(euctop), (140, 230),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		eucbot= dist.euclidean(avg[1],(pivot[1]))
		#cv2.putText(frame, "eubot: {}".format(eucbot), (140, 180),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		r=(tx/68,ty/68)
		if(flag is True):
			fi=euctop/eucbot
			firstval=interp(fi,[0,2],[1,100])
			flag=False
		ra=euctop/eucbot
		ran=interp(ra,[0,2],[1,100])
		cv2.putText(frame, "ran: {}".format(ran), (140, 180),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		
		#print(euctop-eucbot)
                #print(eucleft-eucright)
		#for(x,y) in shape:
                   #cv2.circle(frame,(x,y), 1, (0, 0, 255), -1)
                    
 
	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
