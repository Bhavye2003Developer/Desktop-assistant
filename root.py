#Importing all packages
from email.mime import audio
import os
import time
import speake3
import datetime
import webbrowser
from datetime import date
from googlesearch import search
import speech_recognition as sr

# os.popen("/usr/bin/firefox")  --> to open application

r = sr.Recognizer() #Initialise the recognizer
engine = speake3.Speake() #Initialise the speaker to speak

#configuring engine for speaking
engine.set("voice","en")
engine.set("speed","140")
engine.set("pitch","40")
engine.set("volume","20")

def take_input(): #Taking the input
    text = ""
    try:
        with sr.Microphone() as source:
            a = r.record(source,duration=3.5)
            text = r.recognize_google(a,language='en-US', show_all=False)
            return text
    except:
        return text


def speak(output): #To speak the output via speaker
    engine.say(output) #output --> what you want to say
    engine.talkback()


def app_open(query): #To open binaries
    print(query)
    bin_dir = os.listdir("/usr/bin")  #Binaries absolute path
    for i in bin_dir:
        binary = ""
        for j in i:
            binary+=(j.lower())
        
        flag = True # App exists
        for j in query:
            if (j not in binary):
                flag = False
        if (flag):
            a = os.popen(f"/usr/bin/{i}")
            print(a)
            speak(f"Opening {binary}")
            return 1
    return 0

def website_open(query):
    query = query[2:]
    to_be_searched = ""
    for i in query:
        to_be_searched+=i+"+"
    to_be_searched = to_be_searched[:-1]
    speak(f"opening {to_be_searched}")
    url = f"https://www.{to_be_searched}"
    # webbrowser.open_new_tab(url)
    webbrowser.open_new_tab(url) #opening browser new tab with that website


def google_search(query):
    query = query[1:]
    to_be_searched = "" #To format the query before searching
    for i in query:
        to_be_searched+=i+"+"
    to_be_searched = to_be_searched[:-1]
    url = f"https://www.google.com/search?client=firefox-b-d&q={to_be_searched}"
    speak(f"searching {to_be_searched}") 
    webbrowser.open_new_tab(url) #opening browser new tab with that website

def initialise():
    query = take_input()  #Taking input via microphone

    #Making record of all commands
    f = open("logs","a")

    if (query==""):
        print("No command given!!!")
        pass

    else:
        if query!="":
            log = f"{str(datetime.datetime.now())} : {query}" #to log that command with date and time
        else:
            log = f"{str(datetime.datetime.now())} : NOT HEARED"
        is_run = ""

        #Breaking command
        query = query.split(" ")
        l = []
        for i in query:
            l.append(i.lower())
        query = l

        if len(query)>=2:
            if (query[0]=='open' and query[1]=='website'):
                website_open(query)
                is_run = "RUN"

            elif (query[0]=="open"):
                app_condition = app_open(query[1:])

                if (app_condition==0):
                    speak("APPLICATION NOT FOUND") #if application not found
                    is_run = "NOT RUN"
                
                else:
                    is_run = "RUN"

            elif (query[0]=="search"):
                google_search(query) #searching google 
                is_run = "RUN"
        
        elif (query[0]=="shutdown"):
            speak("Shuting down...")
            is_run = "RUN"
            exit() #exit to the program
    
        log+=" : " + is_run
        f.write("\n")
        f.write(log)
        f.close()

while True:
    initialise() #while loop to run this program every 3.5 seconds  