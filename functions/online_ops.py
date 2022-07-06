import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address

def search_wikipedia(query):
    print('-->',query)
    results = wikipedia.summary(query, sentences=3)
    return results

#print(search_wikipedia('batman'))