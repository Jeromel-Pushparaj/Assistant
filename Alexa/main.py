# main.py
from assistant import Assistant
from utils import Utils
import config
import pywhatkit
import datetime

def main():
    assistant = Assistant()
    utils = Utils()

    assistant.greet()
    
    while True:
        command = utils.take_command()
        if command == 0:
            utils.active = 0
            active_state = utils.active_process()
            if utils.listen_state is True and active_state is False:
                utils.play_sound(r"F:\Project LIGHT Your  Desktop assistant\bottle-205353.mp3")
                utils.listen_state = False
            continue
        
        if "buddy" in command and utils.active != 1:
            utils.play_sound(r"F:\Project LIGHT Your  Desktop assistant\system-notification-199277.mp3")
            utils.listen_state = True
            utils.active = 1
            print("Activated:")
        elif "goodbye" in command and utils.active == 1:
            utils.talk("Goodbye, sir.")
            break
        elif "play" in command and utils.active == 1:
            assistant.play_song(command)
            utils.active = 0
        elif "search" in command and utils.active == 1:
            query = command.replace("search", "")
            pywhatkit.search(query)
            utils.talk(f"Searching {query}")
            utils.active = 0

        elif "time" in command and utils.active == 1:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            utils.talk(f"The time is {current_time}")
            utils.active = 0
        elif "joke" in command and utils.active == 1:
            assistant.tell_joke()
            utils.active = 0
        elif "open" in command and utils.active == 1:
            query = command.replace("open", "")
            assistant.open_application(command)
            utils.active = 0
        elif "ask" in command and utils.active == 1:
            assistant.ask_ai()
            utils.active = 0

if __name__ == "__main__":
    main()
