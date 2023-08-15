import speech_recognition as sr
import os
import win32com.client
import webbrowser
import openai
import subprocess
import datetime
from config import apikey
import random


chatcom = ""

def say(s):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(s)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occurred"

def openaicode(prompt):
    openai.api_key = apikey
    text = f"OpenAi result of the prompt: {prompt}\n*********************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response["choices"][0]["text"])

    if not os.path.exists("openairesults"):
        os.mkdir("openairesults")

    # with open(f"openairesults\\{''.join(prompt.split('ai')[1:]) }.txt", "w") as f:
    with open(f"openairesults\\{''.join(prompt.split('ai')[1:])}.txt", "w") as f:
        f.write(text)


def chat(query):
    global chatcom
    print(chatcom)
    openai.api_key = apikey
    chatcom += f"Anu: {query}\n Veda: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatcom,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatcom += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]



if __name__ == '__main__':
    say("Hello I am Veda A.I. How can I help you")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.org/"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        winapps = ["cmd", "calc", "notepad", "camera"]

        for winapp in winapps:
            if f"open {winapp}".lower() in query.lower():
                try:
                    if winapp == "camera":
                        os.system(f"start microsoft.windows.camera:")
                    else:
                        subprocess.call(f'{winapp}.exe')
                except Exception as e:
                    say("Sorry sir can't open right now")


        if "open music" in query.lower():
            musicPath = "C:\\Users\\anubh\\Downloads\\WaterFountain.mp3"
            say("Playing music...")
            os.system(f"start {musicPath}")

        elif"the time" in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M")
            strfTime = strfTime.split(":")
            say(f"its{strfTime[0]} hours {strfTime[1]} minutes")

        elif "using ai".lower() in query.lower():
            openaicode(prompt=query.lower())

        elif "Veda quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatcom = ""

        else:
            print("Chatting...")
            chat(query)






