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
proc = nlp.LanguageProcessor()


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

def is_imperative(query):
    tagged = proc.pos_tag(query)
    print('----->', tagged)
    if tagged[0][1] == 'VB':
        return True
    else: return False

    

def process(query):
    query = query.casefold()
    clf = proc.load_question_model()
    vectorizer = proc.tf_idf_vect
    query_class = clf.predict(vectorizer.transform([query])) 
    print('test')

    if any(cmd in query for cmd in ['exit', 'stop', 'goodbye']):
        speak('take care sir, goodbye for now')
        exit()
 
    elif ('open' in query) or ('start' in query):
        if 'website' in query:
            web.open_website(query)
        else:
            ops.execute(query)

    elif is_question(query_class, proc.strtok(query)):
        noun_list = proc.find_nouns(query) 
        print(noun_list)
        web.search_google(query)

    elif is_imperative(query):
        print('yes') #TODO

    



def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.adjust_for_ambient_noise(source, duration=0.06)
        r.pause_threshold = 0.8
        r.energy_threshold = 1000
        try:
            audio = r.listen(source)
        except Exception:
            print('nothing was said')

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-us')
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
    



