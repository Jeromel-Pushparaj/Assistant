import pyaudio
import wave
import speech_recognition as sr


# Parameters
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1              # Number of channels
RATE = 44100              # Sample rate
CHUNK = 1024              # Chunk size
RECORD_SECONDS = 5        # Duration of recording
OUTPUT_FILENAME = "output.wav"  # Output file name

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Record data
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()


# Save the recorded data as a WAV file
wf = wave.open(OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

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

while(1):
    text = get_audio()
    if text is 0:
        continue
    if "buddy" in text:
        print("Activated:")
    