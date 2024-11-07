import pywhatkit as pwk
import pyautogui
import time

# Function to send a WhatsApp message
def send_whatsapp_message(phone_number, message, hour, minute):
    pwk.sendwhatmsg(phone_number, message, hour, minute)
    time.sleep(20)  # Wait for the message to be sent

# Function to attach a file
def attach_file(file_path):
    time.sleep(5)  # Wait for WhatsApp Web to load
    pyautogui.click(x=100, y=200)  # Click on the attachment icon (adjust coordinates as needed)
    time.sleep(2)
    pyautogui.click(x=150, y=250)  # Click on the file option (adjust coordinates as needed)
    time.sleep(2)
    pyautogui.write(file_path)  # Type the file path
    pyautogui.press('enter')  # Press Enter to attach the file
    time.sleep(2)
    pyautogui.press('enter')  # Press Enter to send the file

# Example usage
phone_number = "+919345743018"  # Replace with the recipient's phone number
message = "Hello, this is a test message with an attachment."
file_path = r"F:\Project LIGHT Your  Desktop assistant\system-notification-199277.mp3"  # Replace with the path to your file
hour = 16  # 24-hour format
minute = 17

send_whatsapp_message(phone_number, message, hour, minute)
attach_file(file_path)
