import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)
engine.setProperty('volume',3.0)
engine.setProperty('rate',180)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    '''it takes commands from micropphone of the user and returns string output'''

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 600
        audio = r.listen(source)

    try:
       print("Recognizing....")
       query = r.recognize_google(audio, language="en-in")
       print(f"You said: {query}\n ")
    
    except Exception as e:
        # print(e)
        print("say that again please...")
        return "None"
    query = query.lower()   #if you enable this you can skip all the commanda like -- you can skip the lower 
    return query


