import pyttsx3
import speech_recognition as sr
import wikipedia  as wikipedia
import webbrowser
import datetime as dt
import os
import requests
import json
import pyjokes

class voiceAssistant:
    def __init__(self,apiKey):
        ''' initializes internal windows voice already present on windows '''
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice',self.voices[0])
        self.apiKey = apiKey
        

    def speak(self,audio):
        '''takes audio as input as speaks the passed argument '''
        self.engine.say(audio)
        self.engine.runAndWait()

    def greet(self):
        '''greets the user according to the time '''
        hour = int(dt.datetime.now().hour)
        if hour >= 0 and hour <= 12 :
            self.speak('good morning , how can i help you')
        elif hour > 12 and hour < 18:
            self.speak('good evening , how can i help you')
        else:
            self.speak('how can i help you ')

    def take_command(self):
        ''' takes input from microphone and returns the query(input) received'''
        with sr.Microphone() as source:
            receive = sr.Recognizer()
            receive.pause_threshold = 1
            audio = receive.listen(source)
        try :
            print('Listining....')
            query  = receive.recognize_google(audio,language='en-in')
            print(query)
        except Exception as e:
            print('error occured please say again')
        
        return query


    def process_query(self):
        query = self.take_command()
        query = query.lower()               #converting query to small letters
        '''processing query based on type of query'''
        if 'wikipedia' in query:
            print('results from wikipedia...')
            answer = str(wikipedia.summary(query.replace('wikipedia',''),sentences=2))
            self.speak(answer)
            print(answer)

        elif 'weather' in query:
            base_url =  "http://api.openweathermap.org/data/2.5/weather?"
            city = query.replace("weather in","")
            complete_url = base_url + "appid" +self.apiKey + "&q" + city
            response = requests.get(complete_url)

            data = response.json()

            if data['cod'] != "404":
                info = data['main']    #the weather info is present in main
                temperature = info['temp']
                humidity    = info['humidity']
                climate     = info['weather'][0]['description']

                self.speak('the temperature is {0} the humidity in air is{1} and climate is {2}'.format(temperature,humidity,climate))
                
            else:
                self.speak('error occured please try again')
                print('error occurred please try again')


            

        elif 'send mail' in query:
            pass

        elif 'youtube' in query:
            print('opening youtube')
            self.speak('opening youtube')
            webbrowser.open('youtube.com')
        
        elif 'google' in query:
            print('opening google.com')
            self.speak('opening google in browser')
            webbrowser.open('google.com')

        elif 'open mail' in query:
            print('opening gmail in browser')
            self.speak('opening gmail in browser')
            webbrowser.open('gmail.com')

        elif 'current time' in query:
            hour  = str(dt.datatime.now().hour)
            minutes = str(dt.datetime.now().minute)
            self.speak('the time is '+ hour+ "hours" + minutes + "minutes")
            print('hours :' + hour + ' minutes :' + minutes)

        elif 'open notepad' in query:
            self.speak('opening note pad')
            os.system('notepad')

        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            self.speak(joke)
            print(joke)

        else :
            self.speak('opening in browser')
            print('opening in browser')
            webbrowser.open(query)


if __name__ == "__main__":
    apikey = input("enter apikey for myweather api for weather ")
    user = voiceAssistant(apikey)
    user.greet()
    user.process_query()
    
        


