import pygame
import time

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(1)

if __name__ == "__main__":
    audio_file = "/home/dell/Desktop/BabyMonitor/babymonitor/babymonitor/soft-lullaby-in-spanish-28361.wav"
    play_audio(audio_file)
