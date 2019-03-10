import numpy as np  
import cv2  
import dlib  
from scipy.spatial import distance as dist 
import time 
import threading
import pyautogui
pyautogui.FAILSAFE=False
PREDICTOR_PATH = "learnt.dat"  
   
FULL_POINTS = list(range(0, 68))  
FACE_POINTS = list(range(17, 68))  
   
JAWLINE_POINTS = list(range(0, 17))  
RIGHT_EYEBROW_POINTS = list(range(17, 22))  
LEFT_EYEBROW_POINTS = list(range(22, 27))  
NOSE_POINTS = list(range(27, 36))  
RIGHT_EYE_POINTS = list(range(36, 42))  
LEFT_EYE_POINTS = list(range(42, 48))  
MOUTH_OUTLINE_POINTS = list(range(48, 61))  
MOUTH_INNER_POINTS = list(range(61, 68))  
   
EYE_AR_THRESH = 0.30 
EYE_AR_CONSEC_FRAMES = 3  
   
COUNTER_LEFT = 0  
TOTAL_LEFT = 0  
   
COUNTER_RIGHT = 0  
TOTAL_RIGHT = 0  
global time1
time1=10.0
global time2
time2=0.0
global newTime
newTime=14.0


global rx
global ry

rx=0
ry=0

global cx
global cy
cx=0
cy=0

def move():
   while(True):
	global cy
	global cx
	global ry
	global rx
	
	
	
	
	#print 'in thread'
	#print cy
	#print cx
	#print rx
	#print ry
#	while(True):
	 #print x,y
        if(cy<ry-5 or cy>ry+5 or cx>rx+7 or cx<rx-7):
		#s=dist.euclidean([ry,0],[y,0])
		s=-(((ry)-cy))
		i=-((cx-(rx)+2))
		pyautogui.moveRel(i,s)
		
		pass
	#elif(cy>ry+5):
		
                #pyautogui.moveRel(0,5)
	#	pyautogui.moveRel(0,(cy-(ry+5)))
	#	pass	
	#elif(cx>rx+8):
         #       #pyautogui.moveRel(-5,0)
	#	pyautogui.moveRel(-(cx-(rx+8)),0)		
	#	pass	
#	elif(cx<rx-8):
#		#pyautogui.moveRel(5,0)
## 		pass
		
	 	
	 #  pyautogui.typewrite(['left'])
	   #time.sleep(1)
       # elif(x>rx+5):
	#   pyautogui.typewrite(['right'])
	
	







def returnTime():
   global newTime
   global time1
   global time2
   while(True):
        global newTime
        global time1
        global time2
	#if (time1-time2<1.20):
		#print "yes"
	time1=newTime
	time2=time1
	
		
	
	
   
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
   
detector = dlib.get_frontal_face_detector()  
   
predictor = dlib.shape_predictor(PREDICTOR_PATH)  
   
 # Start capturing the WebCam  
video_capture = cv2.VideoCapture(0)  
video_capture.set(3,360)
video_capture.set(4,640)
   
t=threading.Thread(target=move,args=())
t.start()

while rx is 0: 
   ret, frame = video_capture.read()  
   
   if ret:  
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
   
     rects = detector(gray, 0)  
   
     for rect in rects:  
       x = rect.left()  
       y = rect.top()  
       x1 = rect.right()  
       y1 = rect.bottom()  
          
       landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])  
   
       left_eye = landmarks[LEFT_EYE_POINTS]  
       right_eye = landmarks[RIGHT_EYE_POINTS]  
   
       left_eye_hull = cv2.convexHull(left_eye)  
       right_eye_hull = cv2.convexHull(right_eye)  
       #cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)  
       #cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)  
       #g=left_eye[0]
       #rx=g[0]
       #ry=g[0][0]
       g=(np.array(left_eye)[0].tolist())
       rx=g[0]
       ry=g[1] 
       
       break
       ear_left = eye_aspect_ratio(left_eye)  
       ear_right = eye_aspect_ratio(right_eye)  
   
       #cv2.putText(frame, "ear l : {:.2f}".format(ear_left), (160, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  
       #cv2.putText(frame, "ear r: {:.2f}".format(ear_right), (160, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  
   
       if ear_left < EYE_AR_THRESH:  
         COUNTER_LEFT += 1  
         
       else:  
         if COUNTER_LEFT >= EYE_AR_CONSEC_FRAMES:  
           

           TOTAL_LEFT += 1  
           print("Left eye winked")
           #newTime=time.time() 
          
          
         COUNTER_LEFT = 0  
   
       if ear_right < EYE_AR_THRESH:  
         COUNTER_RIGHT += 1  
       else:  
         if COUNTER_RIGHT >= EYE_AR_CONSEC_FRAMES:  
           TOTAL_RIGHT += 1  
           print("Right eye winked")  
	   newTime=time.time()
         COUNTER_RIGHT = 0  
   
     #cv2.putText(frame, "Left : {}".format(TOTAL_LEFT), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  
     #cv2.putText(frame, "Right: {}".format(TOTAL_RIGHT), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  
   
     #cv2.imshow("Faces found", frame)  
   
   ch = 0xFF & cv2.waitKey(1)  
   
   if ch == ord('q'):  
     break  
   
cv2.destroyAllWindows()     


print rx
print ry
#rx=np.nditer(rx)[0]

while True: 
   global newTime 
   ret, frame = video_capture.read()  
   
   if ret:  
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
   
     rects = detector(gray, 0)  
   
     for rect in rects:  
       x = rect.left()  
       y = rect.top()  
       x1 = rect.right()  
       y1 = rect.bottom()  
   
       landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])  
   
       left_eye = landmarks[LEFT_EYE_POINTS]  
       right_eye = landmarks[RIGHT_EYE_POINTS]  
   
       left_eye_hull = cv2.convexHull(left_eye)  
       right_eye_hull = cv2.convexHull(right_eye)  
       cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)  
       cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)  
       #cx=left_eye[0]
       #cy=left_eye[1]
       g=(np.array(left_eye)[0].tolist())
       cx=g[0]
       cy=g[1] 
       ear_left = eye_aspect_ratio(left_eye)  
       ear_right = eye_aspect_ratio(right_eye)  
   
       cv2.putText(frame, "ear l : {:.2f}".format(ear_left), (160, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  
       cv2.putText(frame, "ear r: {:.2f}".format(ear_right), (160, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  
   
       if ear_left < EYE_AR_THRESH:  
         COUNTER_LEFT += 1  
         
       else:  
         if COUNTER_LEFT >= EYE_AR_CONSEC_FRAMES:  
           global newTime
           global time1
           global time2

           TOTAL_LEFT += 1  
           print("Left eye winked")
           newTime=time.time() 
          
           if(time1-time2<1.2):
	    print 'double click invoked'
            print 'time 1'
	    print time1
	    print 'time2'
            print time2
	    print 'Double click' 
	    pyautogui.click()
	   time2=time1
           time1=newTime 
           print newTime 
         COUNTER_LEFT = 0  
   
       if ear_right < EYE_AR_THRESH:  
         COUNTER_RIGHT += 1  
       else:  
         if COUNTER_RIGHT >= EYE_AR_CONSEC_FRAMES:  
           TOTAL_RIGHT += 1  
           print("Right eye winked") 
	   newTime=time.time() 
           if(time1-time2<1.2):
	    print 'double click invoked'
            print 'time 1'
	    print time1
	    print 'time2'
            print time2
	    print 'Double click' 
	    pyautogui.click()
	   time2=time1
           time1=newTime 
           print newTime 
         COUNTER_RIGHT = 0  
   
     cv2.putText(frame, "Left : {}".format(TOTAL_LEFT), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  
     cv2.putText(frame, "Right: {}".format(TOTAL_RIGHT), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)  
   
     cv2.imshow("Faces found", frame)  
   
   ch = 0xFF & cv2.waitKey(1)  
   
   if ch == ord('q'):  
     break  
   
cv2.destroyAllWindows()  
