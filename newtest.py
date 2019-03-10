import speech_recognition as sr
#import webbrowser
#import pyautogui
import os

while(True):
	r=sr.Recognizer()
	r.energy_threshold=2000
	with sr.Microphone() as source:
		print("say something")
		audio=r.listen(source)
	s=r.recognize_sphinx(audio).lower()
	print(s)
