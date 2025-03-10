
import subprocess
import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import time
import datetime
import smtplib
import requests
import psutil
import socket
import re
import cv2
from dotenv import load_dotenv
from PIL import Image
import io
import speedtest
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import pywhatkit

# Load environment variables from .env file
load_dotenv()
DREAMSTUDIO_API = os.getenv('DREAMSTUDIO_API')
# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()
mic = sr.Microphone()

command_keywords = {
    'shutdown': ['shutdown', 'power down', 'turn off'],
    'open chrome': ['chrome', 'google chrome', 'open chrome'],
    'open edge': ['edge', 'microsoft edge', 'open edge'],
    'open store': ['store', 'microsoft store', 'open store'],
    'open linkedin': ['linkedin', 'open linkedin'],
    'open file manager': ['file manager', 'explorer', 'open file manager'],
    'open vs code': ['visual studio code', 'vs code', 'open vs code'],
    'open youtube': ['youtube', 'open youtube'],
    'google search': ['google', 'search', 'search google'],
    'play music on youtube': ['music', 'play music', 'youtube music'],
    'what time is it': ['time', 'current time', 'what time'],
    'make a phone call': ['phone call', 'call', 'make a call'],
    'send email': ['email', 'send email'],
    'search youtube': ['search youtube', 'on youtube'],
    'make a note': ['note', 'make a note', 'write down'],
    'weather': ['weather', 'what is the weather'],
    'reminder': ['reminder', 'set a reminder'],
    'joke': ['joke', 'tell me a joke'],
    'system info': ['system info', 'system information'],
    'movies':['trending movies','movies','popular movies'],
    'news': ['news', 'latest news','current news'],
    'calendar': ['calendar', 'check calendar'],
    'check IP address': ['ip address', 'check ip', 'what is my ip', 'check IP address', 'IP address'],
    'navigate': ['navigate', 'directions', 'navigate to'],
    'open camera': ['camera', 'open camera', 'start camera'],
    'speed test': ['speedtest', 'network speed', 'check speed', 'speed test', 'check the internet speed'],
    'generate image': ['generate image', 'create image', 'make picture', 'generate a picture']
}

def listen_for_wake_word():
    with mic as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        wake_word = recognizer.recognize_google(audio, language='en-IN').lower()
        print(f"Recognized wake word: {wake_word}")
        if wake_word in ["hi windows", "hello windows", "hey windows"]:
            speak("Yes, how can I assist you?")
            return True
        else:
            print("Wake word not recognized correctly.")
            return False
    except sr.UnknownValueError:
        print("Didn't recognize the wake word.")
    except sr.RequestError as e:
        print(f"Request error: {e}")

    return False

def listen_and_respond():
    with mic as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for your command...")
        audio = recognizer.listen(source)
        print("Recording complete.")

    try:
        print("Recognizing speech...")
        command = recognizer.recognize_google(audio, language='en-IN')
        print(f"Recognized command: {command}")
        speak(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        error_message = "I didn't quite catch that. Please repeat."
        print(error_message)
        speak(error_message)
        return ""
    except sr.RequestError as e:
        error_message = f"Request error: {e}"
        print(error_message)
        speak(error_message)
        return ""

def shutdown_computer():
    speak("Shutting down the computer.")
    subprocess.call(["shutdown", "/s", "/t", "1"])

def main():
    while True:
        if listen_for_wake_word():
            command = listen_and_respond()
            if not command:
                continue

            if any(keyword in command for keyword in command_keywords['shutdown']):
                shutdown_computer()

if __name__ == "__main__":
    main()
