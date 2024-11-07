import speech_recognition as sr
import time
from playsound import playsound

active = 0
listen_state = False
def get_audio():
    
	rObject = sr.Recognizer()
	audio = ''
 
	with sr.Microphone() as source:
		print("Speak...")	
		# recording the audio using speech recognition
		audio = rObject.listen(source, phrase_time_limit = 5) 
	print("Stop.") # limit 5 secs

	try:

		text = rObject.recognize_google(audio, language ='en-US')
		print("You : ", text)
		return text

	except:
		return 0

def active_process():
    global active
    if active is 1:
        return True
    else:
        return False

def checkForCommands(text):
    if "I want to know" in text:
        print("activating wiki")
    

while(1):
    
    text = get_audio()
    if text is 0:
        active = 0
        print("hi")
        active_state = active_process()
        if listen_state is True and active_state is False:
            playsound(r"F:\Project LIGHT Your  Desktop assistant\bottle-205353.mp3")
            listen_state = False
        continue

    if "buddy" in text and active != 1:
        playsound(r"F:\Project LIGHT Your  Desktop assistant\system-notification-199277.mp3")
        listen_state = True
        active = 1
        print("Activated:")
    
    if active == 1:
        checkForCommands(text)