import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice



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
    speak(f"I am {BOTNAME}. How may I assist you?")



def process(query):
    print(query)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 0.8
        r.energy_threshold = 300
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-us')
        if 'exit' in query:
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
    



