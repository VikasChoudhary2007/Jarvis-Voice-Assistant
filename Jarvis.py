import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = ""

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(api_key="")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant. Give short responses."
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content

def processCommand(command):
    command = command.lower()

    if "stop" in command or "exit" in command or "quit" in command or "shutdown" in command:
        speak("Signing off")
        return False

    elif "open google" in command:
        webbrowser.open("https://google.com")

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")

    elif command.startswith("play"):
        song = command.split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in command:
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            for article in articles:
                speak(article["title"])

    else:
        output = aiProcess(command)
        speak(output)

    return True


if __name__ == "__main__":
    speak("Initializing Jarvis....")

    while True:
        recognizer = sr.Recognizer()

        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(
                    source,
                    timeout=2,
                    phrase_time_limit=1
                )

            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Ya")

                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                if not processCommand(command):
                    break

        except Exception as e:
            print(f"Error: {e}")