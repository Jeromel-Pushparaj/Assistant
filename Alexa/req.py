import requests
import webbrowser
import time

# Define the server URL
server_url = "http://127.0.0.1:5000"

# Text data to send in the POST request
text_data = '''
John 3:16

For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.
'''

# Send POST request to the server
response = requests.post(f"{server_url}/submit", data={"text": text_data})

# Check if the request was successful
if response.status_code == 200:
    print("Text sent successfully")

    # Give the server a moment to process before opening the browser
    time.sleep(1)
    
    # Open the display page in a new tab of the default browser
    webbrowser.open_new_tab(server_url)
else:
    print("Failed to send text")
