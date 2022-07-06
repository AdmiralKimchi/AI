import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
from nltk.corpus import wordnet
import functions.os_ops as ops



USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')


def set_voice(gender):
    if gender == 'female':
        index = 1
    elif gender == 'male':
        index = 0
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[index].id)
    


def speak(text):
    """Used to speak whatever text is passed to it"""
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.now().hour
    if hour in range(6, 12):
        speak(f"Good Morning {USERNAME}")
    elif hour in range(12, 16):
        speak(f"Good afternoon {USERNAME}")
    elif hour in range(16, 23):
        speak(f"Good evening {USERNAME}")
    #speak(f"I am {BOTNAME}. How may I assist you?")



def process(query):
    query = query.casefold()
    print(query)
    if 'cmd' in query:
        speak('cmd')
        ops.open_cmd()
    if 'calculator' in query:
        print('calculator')
        ops.open_app('calculator')
    if 'chrome' in query:
        ops.open_app('chrome')
    if 'code' in query:
        ops.open_app('vscode')
    if 'camera' in query:
        ops.open_camera()



    


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 0.8
        r.energy_threshold = 400
        try:
            audio = r.listen(source, timeout=10.0)
        except Exception:
            print('nothing was said')

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-us')
        exit_commands = ['exit', 'stop']
        if any(cmd in query for cmd in exit_commands):
            speak('take care sir, goodbye for now')
            exit()
        process(query)
       
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    take_command()
    return query
     

if __name__ == '__main__':
    engine.setProperty('rate', 190)
    engine.setProperty('volume', 1.5)
    set_voice('male')
    greet()
    take_command()
    



