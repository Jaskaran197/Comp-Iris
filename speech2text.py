import speech_recognition as sr
import webbrowser
import pyautogui
import os
new=2
f=0
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

        elif("start typing" in s):
             #os.system('gedit a.txt')
	     f=1

        elif("quit typing" in s):
             
	     f=0



    except:
        pass
