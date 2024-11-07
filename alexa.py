import speech_recognition as li
import pywhatkit
import pyttsx3
import datetime
import os
import time
import pyjokes
from playsound import playsound
import google.generativeai as genai

converter = pyttsx3.init()

voices = converter.getProperty('voices')
  
for voice in voices:
    # to get the info. about various voices in our PC 
    print("Voice:")
    print("ID: %s" %voice.id)
    print("Name: %s" %voice.name)
    print("Age: %s" %voice.age)
    print("Gender: %s" %voice.gender)
    print("Languages Known: %s" %voice.languages)



listner = li.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice',voice[1].id)
engine.setProperty('rate', 150)

# Set up the Google Gemini API
genai.configure(api_key="AIzaSyCU9mAQIM_YO6uYgQ_LjpXAQ8B6WSyZy6M")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]


# Customizing The output voice
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])

def get_response(user_input):
    convo.send_message(user_input)
    gemini_reply = convo.last.text
    print(gemini_reply)
    return gemini_reply

def AI():
    # Initializing pyttsx3
    listening = True
    sending_to_gemini = True
    exit_words = ["exit", "disconnect","stop", "quit", "bye", "goodbye"]  # Add your exit words here
    wake_word = "buddy"  # Set your wake word here

    while listening:
        with li.Microphone() as source:
            recognizer = li.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            recognizer.dynamic_energy_threshold = 3000

            try:
                print("AI Listening...")
                audio = recognizer.listen(source, timeout=5.0)
                response = recognizer.recognize_google(audio)
                print(response)

                if any(exit_word in response.lower() for exit_word in exit_words):
                    sending_to_gemini = False
                    print("Stopped sending responses to Gemini.")
                    listening = False
                    continue

                if wake_word in response.lower() and not sending_to_gemini:
                    sending_to_gemini = True
                    print("Resumed sending responses to Gemini.")

                if sending_to_gemini:
                    response_from_gemini = get_response(response)
                    engine.setProperty('rate', 200)
                    engine.setProperty('volume', volume)
                    engine.setProperty('voice', 'greek')
                    engine.say(response_from_gemini)
                    engine.runAndWait()

            except li.UnknownValueError:
                print("Didn't recognize anything.")

active = 0
listen_state = False

def talk(text):
    engine.say(text)
    engine.runAndWait()

#funtion for wish you 
def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        talk("Hello sir,Good Morning")
        print("Hello sir,Good Morning")
    elif hour>=12 and hour<18:
        talk("Hello sir,Good Afternoon")
        print("Hello sir,Good Afternoon")
    else:
        talk("Hello sir,Good Evening")
        print("Hello sir,Good Evening")

#function for opening application
def open_app():
    if 'davinci resolve' in command:
            davinci = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\Resolve.exe"
            talk("opening davinci......")
            print("opening danvi")
            os.startfile(davinci)
    elif 'notion' in command:
            Notion = "C:\\Users\\Jeromel Pushparaj\\AppData\\Local\\Programs\\Notion\\Notion.exe"
            talk("opening notion......")
            print("opening notion")
            os.startfile(Notion)
    elif 'vs code''i need to code' in command:
            vscode = "C:\\Users\\Jeromel Pushparaj\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            talk("you are ready to code sir......")
            print("opening Vs code")
            os.startfile(vscode)




def take_command():
    
	rObject = li.Recognizer()
	audio = ''
 
	with li.Microphone() as source:
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
    

    
wishMe()
while 1:     
    command = take_command()
    if command is 0:
        active = 0
        print("hi")
        active_state = active_process()
        if listen_state is True and active_state is False:
            playsound(r"F:\Project LIGHT Your  Desktop assistant\bottle-205353.mp3")
            listen_state = False
        continue

    if "buddy" in command and active != 1:
        playsound(r"F:\Project LIGHT Your  Desktop assistant\system-notification-199277.mp3")
        listen_state = True
        active = 1
        print("Activated:")
  
    if "goodbye" in command or "ok bye" in command or "stop" in command and active == 1:
        talk('Good bye sir,see you again')
        print('Good bye sir,see you again')
        break    
        
    if 'good morning' in command and active == 1:
        plan = command.replace('good morning', '')
        talk('sir what is the plan today, How can i help you?')
    if 'good evening' in command and active == 1:
        plan = command.replace('good evening', '')
        talk('what about your todays day sir, what the work to done sir?')
                
    if 'play' in command and active == 1:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'search' in command and active == 1:   
        search = command.replace('please search','')
        talk('give  a  second  sir')
        pywhatkit.search(search)
        talk(search)
        print ("searching.....")
    elif 'time' in command and active == 1:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('current time is ' + time)
    elif 'joke' in command and active == 1:
        My_joke = pyjokes.get_joke(language="en", category="neutral") 
        talk('Here is my joke for you................ ' + My_joke)
    elif 'ask' in command:
        AI()
    




    elif 'open' in command and active == 1:
        talk('give a second sir')
        open_app()