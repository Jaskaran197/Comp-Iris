import cv2
import sys
import time
import pyautogui
import threading
import os

x=0
y=0
rx=0
ry=0
cy=0
cx=0

def move():
   while(True):
	global cy
	global ry
	
	
	print ' cy is '
	
	#print 'in thread'
	print cy
#	while(True):
	 #print x,y
	if(y<ry-5):
		
	 	
	   pyautogui.typewrite(['up'])
	   #time.sleep(1)
        elif(y>ry+5):
	   pyautogui.typewrite(['down'])
	    #var=var-4
        #if(y>ry-15):
	#elif(x<rx-5):
		
	 	
	 #  pyautogui.typewrite(['left'])
	   #time.sleep(1)
       # elif(x>rx+5):
	#   pyautogui.typewrite(['right'])
	
	
	


#print os.path.abspath(cv2.__file__)
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
#faceCascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)
print video_capture.get(3)
print video_capture.get(4)
video_capture.set(3,320)
video_capture.set(4,240)
#video_capture.set(6,20)

print video_capture.get(3)
print video_capture.get(4)



while(True): 
   # print 'i first'
   
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        
	print x
	print y
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rx=x
	ry=y
        
        print 'done reference' 
	break
    else:
	continue 
    print "Breaking out"
    break   
    # Display the resulting frame
    

t=threading.Thread(target=move,args=())
t.start()



while True: 
   # print 'in main'
   
  
    
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
	
	cy=y

	
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
	os.kill(os.getpid(), signal.SIGINT)      
	break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

