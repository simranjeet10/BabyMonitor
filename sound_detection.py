import pyaudio
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import vlc
import time

# Function to play audio
def play_audio(file_path):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(file_path)
    player.set_media(media)
    player.play()

    while player.get_state() != vlc.State.Ended:
        time.sleep(1)

# Set up the Firebase credentials and initialize the app
cred = credentials.Certificate(r'baby-data-update-firebase-adminsdk-xsff3-b6ee3dfddc.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testingdht11-default-rtdb.firebaseio.com/'
})

# Get a reference to the sound status node in the Realtime Database
sound_ref = db.reference('sound')

# Set up the audio recording parameters
RATE = 44100
BUFFER_SIZE = 1024

# Create a PyAudio object
pa = pyaudio.PyAudio()

# Open a stream for recording audio
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=BUFFER_SIZE)

def sound_check():
    while True:
        # Read a buffer of audio data from the stream
        data = np.frombuffer(stream.read(BUFFER_SIZE), dtype=np.int16)

        # Compute the FFT of the audio data
        fft = np.fft.fft(data)

        # Compute the power spectrum of the FFT
        power_spectrum = np.abs(fft) ** 2

        # Find the peak frequency of the power spectrum
        peak_freq = np.argmax(power_spectrum)

        # Convert the peak frequency to Hz
        freq_hz = peak_freq * RATE / BUFFER_SIZE

        # Check if the frequency is above a certain threshold (e.g., 1000 Hz)
        if freq_hz > 1000:
            print('High pitch sound detected!')
            sound_ref.set("sound detected!")
            # Play the audio file
            play_audio("/home/dell/Desktop/BabyMonitor/babymonitor/babymonitor/soft-lullaby-in-spanish-28361.wav")
        else:
            sound_ref.set("no sound detected")

        # You can add a sleep time if you want to reduce the frequency of checking sound
        # time.sleep(0.5)

# Run the sound check function
sound_check()
