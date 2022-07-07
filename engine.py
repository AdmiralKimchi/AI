import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
import functions.os_ops as ops
import functions.online_ops as web
import nlp

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
    if hour in range(4, 12):
        speak(f"Good Morning {USERNAME}")
    elif hour in range(12, 16):
        speak(f"Good afternoon {USERNAME}")
    elif hour in range(16, 23):
        speak(f"Good evening {USERNAME}")
    else:
        speak(f"Good night {USERNAME}")

    #speak(f"I am {BOTNAME}. How may I assist you?")




def is_question(query_class, tokenized):
    question_words = [ 
             "is", "do", "does", 
             "are", "could", "can", "would", 
             "should", "has", "have"
             ]

    if query_class[0] in ['whQuestion', 'ynQuestion']:
        return True
    elif query_class[0] == 'Statement':
        return any(x in tokenized[0] for x in question_words)

    

def process(query):
    proc = nlp.LanguageProcessor()
    query = query.casefold()
    clf = proc.load_question_model()
    vectorizer = proc.tf_idf_vect
    query_class = clf.predict(vectorizer.transform([query])) 
 
    if 'open' in query:
        ops.execute(query)

    if is_question(query_class, proc.strtok(query)):
        print(proc.find_nouns(query))
        web.search_google(query)
    



def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.adjust_for_ambient_noise(source, duration=0.3)
        r.pause_threshold = 0.8
        r.energy_threshold = 600
        try:
            audio = r.listen(source)
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
        speak('Sorry, I could not understand. say that again')
        query = 'None'
    take_command()
    return query
     

if __name__ == '__main__':
    engine.setProperty('rate', 190)
    engine.setProperty('volume', 1.5)
    set_voice('male')
    greet()
    take_command()
    



