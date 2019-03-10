import speech_recognition as sr
r=sr.Recognizer()
mic=sr.Microphone()
sr.Microphone.list_microphone_names()
mic=sr.Microphone(device_index=1)
with mic as source:
	r.adjust_for_ambient_noise(source)
	print("Say something")
	audio = r.listen(source)
	s=r.recognize_sphinx(audio).lower()
	print(s)
