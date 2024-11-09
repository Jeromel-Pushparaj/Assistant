# utils.py
import pyttsx3
import speech_recognition as sr
from playsound import playsound
import webbrowser
import requests
import time
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
    
    def open_link(self, text_data):
        # Create a dictionary with the text data 
        server_url = "http://127.0.0.1:5000"
        # Send a POST request to the server with the text data 
        response = requests.post(f"{server_url}/submit", data={"text": text_data})
        
        time.sleep(1)
        # Open URL in a new tab, if a browser window is already open
        webbrowser.open_new_tab(server_url)
        # Open URL in a new window, if no browser window is open
        webbrowser.open_new(server_url)

    def active_process(self):
        if self.active == 1:
            return True
        else:
            return False