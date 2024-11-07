# utils.py
import pyttsx3
import speech_recognition as sr
from playsound import playsound

class Utils:
    
    active = 0
    listen_state = False
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, phrase_time_limit=5)
        try:
            command = self.recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Didn't recognize anything.")
            return 0

    def play_sound(self, file_path):
        playsound(file_path)

    def active_process(self):
        if self.active == 1:
            return True
        else:
            return False