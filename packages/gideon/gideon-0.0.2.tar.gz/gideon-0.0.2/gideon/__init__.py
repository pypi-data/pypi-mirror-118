
from typing import Mapping
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import os,sys,time
import random
from pyttsx3 import *
from datetime import *

def init():


    recognizer = speech_recognition.Recognizer()

    speaker = tts.init()
    speaker.setProperty('rate', 150)



# def timetraffel():
#     global recognizer

#     speaker.say("to what year do you want to go captain?")
#     speaker.runAndWait()

#     done = False
#     while not done:
#         try:
#             with speech_recognition.Microphone() as mic:
#                 recognizer.adjust_for_ambient_noise(mic, duration=0.2)
#                 audio = recognizer.listen(mic)

#                 year = recognizer.recognize_google(audio)
#                 year = year.lower()
#         except speech_recognition.UnknownValueError:
#             recognizer = speech_recognition.Recognizer()
#             speaker.say("i did not get that captain")
#             speaker.runAndWait()

def voices():
    speaker = tts.init()
    speaker.setProperty('rate', 150)
    for voice in speaker.getProperty('voices'):
        print(voice)


def assistant(file):
    recognizer = speech_recognition.Recognizer()

    speaker = tts.init()
    speaker.setProperty('rate', 150)
    assistant = GenericAssistant(file)
    assistant.train_model()
    # assistant.request("gideon")
    os.system("cls")
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                message = recognizer.recognize_google(audio)
                message = message.lower()

                assistant.request(message)

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
