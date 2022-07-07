import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
from googlesearch import search
import webbrowser


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address

def search_wikipedia(query):
    results = wikipedia.summary(query, sentences=3)
    return results


def search_google(query):
    kit.search(query)

def open_website(query):
    print(query)
    webbrowser.open(query)
