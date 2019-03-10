from Tkinter import *
import Tkinter as tk 
import os
import threading
import subprocess
global p
import speech_recognition as sr
import webbrowser
import pyautogui
import os
new=2
f=0
import Tkinter
def stop():
	p.terminate()

def voice():
   global f
   while(True):
    r=sr.Recognizer()
    r.energy_threshold=4000
    with sr.Microphone() as source:
        print("say something")
        audio=r.listen(source)
    
    try:
        s=r.recognize_google(audio).lower()
        print(s)

        if (f==1):
              pyautogui.typewrite(s, interval=0.25)


        if("facebook" in s):

             url="https://facebook.com"
             webbrowser.open(url,new=new)

        elif("youtube" in s):

             url="https://youtube.com"
             webbrowser.open(url,new=new)

        elif("close" in s):
             pyautogui.hotkey('alt', 'f4')

        elif("ok" in s):
             pyautogui.typewrite(['enter'])       

        elif("maximize" in s):
             pyautogui.hotkey('ctrlleft', 'winleft','up')

        elif("minimise current" in s):
             pyautogui.hotkey('ctrlleft', 'winleft','down')

        elif( "minimise all" in s):
             pyautogui.hotkey( 'winleft','D')

        elif("right click" in s):
             pyautogui.click(button='right')

	elif("click" in s):
             pyautogui.click()
	     pyautogui.click()

	elif("cancel" in s):
             pyautogui.typewrite(['esc'])

        elif("writer" in s):
             #os.system('gedit a.txt')
	     f=1

        elif("quit typing" in s):
             
	     f=0



    except:
        pass	
	
#t=threading.Thread(target=voice,args=())
#t.start()

class Application(Frame):

     
     #create a class variable from the root (master):called by the constructor
     def __init__(self, master):
          self.master = master

     #simple button construction
     # create a button with chosen arguments
     # pack it after the creation not in the mmiddle or before
     def mousecontrol(self):
	global p
	root1=Tk()
	b=Tkinter.Button(root1,text='Stop',command=stop)
	b.pack()
	#w = Tk.Label(root, text="Mouse control started")
        #w.pack()
	
	p = subprocess.Popen(['python', 'blink.py'])
	root1.mainloop()
 
     def photodekho(self):
	global p
	root1=Tk()
	#w = Tk.Label(root, text="Mouse control started")
        #w.pack()
	b=Tkinter.Button(root1,text='Stop',command=stop)
	b.pack()
	
	#w = Tk.Label(root, text="Mouse control started")
        #w.pack()
	
	p = subprocess.Popen(['python', 'hkk.py', 'lbpcascade_frontalface.xml'])
	#os.system('python hkk.py lbpcascade_frontalface.xml')
	root1.mainloop()

     def padhoo(self):
	global p
	root1=Tk()
	#w = Tk.Label(root, text="Mouse control started")
        #w.pack()
	b=Tkinter.Button(root1,text='Stop',command=stop)
	b.pack()
	
	#w = Tk.Label(root, text="Mouse control started")
        #w.pack()
	
	p = subprocess.Popen(['python', 'hk.py', 'lbpcascade_frontalface.xml'])
	
	root1.mainloop()


     def create_widgets(self):
          #"""Create three buttons"""
          #Create first button
          	
          btn1 = Button(self.master, text = "Mouse control",height=15,width=55,bg="black",fg="white",font="size,30",command=self.mousecontrol)
          btn1.grid(row=1,column=1,sticky=W)
          
          #btn1.pack()

          #Create second button
          btn2 = Button(self.master, text = "Photo Viewing",height=15,width=55,bg="red",fg="white",font="size,30",command=self.photodekho)
          btn2.grid(row=2,column=1,sticky=W)
          #btn2.pack()
	  title=tk.Label(text="IRIS - Mouse Control and Voice commands   ", font=("Times New Roman",39))
	  title.grid(row=2,column=2)

         #Create third button
          btn3=Button(self.master, text = "Reading mode",height=15,width=55,bg="black",fg="white",font="size,30",command=self.padhoo)
          btn3.grid(row=3,column=1,sticky=W)
          #btn3.pack()

  #must be outside class definition but probably due to stackoverlow
root = Tk()
c=Canvas(root,bg="blue",height=250,width=300)

filename=PhotoImage(file="2.png")
bl=Label(root,image=filename)
bl.place(x=0,y=0,relwidth=1,relheight=1)

w = Label(root, text="Hello, world!")

root.title("VizBoom 1.0")
root.geometry("500x500")
app = Application(root)
#call the method
app.create_widgets()
root.mainloop()
