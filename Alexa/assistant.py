# assistant.py
import datetime
import pywhatkit
import pyjokes
from utils import Utils
import config
import google.generativeai as genai
import os
import streamlit

class Assistant:
    def __init__(self):
        self.utils = Utils()
        genai.configure(api_key=config.GENAI_API_KEY)
        self.convo = None
        self.init_gemini()

    def init_gemini(self):
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        self.convo = model.start_chat(history=[])

    def get_gemini_response(self, user_input):
        self.convo.send_message(user_input)
        return self.convo.last.text

    def greet(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            self.utils.talk("Good Morning, sir")
        elif hour < 18:
            self.utils.talk("Good Afternoon, sir")
        else:
            self.utils.talk("Good Evening, sir")

    def open_application(self, command):
        if 'davinci' in command:
            app_path = config.APPS['davinci']
            self.utils.talk("Opening DaVinci Resolve")
            os.startfile(app_path)
        elif 'notion' in command:
            app_path = config.APPS['notion']
            self.utils.talk("Opening Notion")
            os.startfile(app_path)
        elif 'vs code' in command:
            app_path = config.APPS['vscode']
            self.utils.talk("Opening VS Code")
            os.startfile(app_path)

    def play_song(self, command):
        song = command.replace('play', '')
        self.utils.talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.utils.talk(joke)

    def ask_ai(self):
        chat = 1
        while chat:
            print("AI Activated:")
            prompt = self.utils.take_command()
            if prompt != 0:
                if "give input" in prompt:
                    print("Enter your Input (type 'END' on a new line to finish):")
                    paragraph = []
                    while True:
                        line = input()
                        if line.strip().upper() == 'END':
                            break
                        paragraph.append(line)

                    paragraph_text = "\n".join(paragraph)
                    response = self.get_gemini_response(paragraph_text)
                    print(response)
                    if len(response) > 10:
                        self.utils.open_link(response)
                    else:
                        self.utils.talk(response)
                    continue
            if prompt != 0:
                response = self.get_gemini_response(prompt)
                print(response)
                if len(response) > 10:
                    self.utils.open_link(response)
                else:
                    self.utils.talk(response)
            else:
                print("AI deactivated: ")
                chat = 0

