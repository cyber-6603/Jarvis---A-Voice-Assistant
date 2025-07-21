import speech_recognition as sr
import webbrowser
import pyttsx3
import MusicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

newsapi = "4450921ae5e24789804e4e6cb7e6a05a"
openai_api_key = "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"

recognizer = sr.Recognizer()
pygame.mixer.init()

def speak(text):
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove('temp.mp3')
    except Exception as e:
        print("Speech error:", e)

def aiProcess(command):
    try:
        client = OpenAI(api_key=openai_api_key)
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis. Keep it short."},
                {"role": "user", "content": command}
            ]
        )
        return res.choices[0].message.content
    except Exception as e:
        print("AI error:", e)
        return "Sorry, I couldn't process that."

def processCommand(c):
    c = c.lower()
    print("Command:", c)

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif c.startswith("play "):
        song = c.split("play ")[-1]
        link = MusicLibrary.music.get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Song not found.")
    elif any(kw in c for kw in ["news", "headlines", "tell me the news"]):
        try:
            response = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "in", "apiKey": newsapi, "pageSize": 5}
            )
            data = response.json()
            print("🔹 NewsAPI JSON:", data)

            if data.get("status") != "ok":
                print("NewsAPI error:", data.get("code"), data.get("message"))
                speak("Sorry, the news service returned an error.")
                return

            if data.get("totalResults", 0) == 0 or not data.get("articles"):
                speak("I couldn't find any headlines right now.")
                return

            speak("Here are today's top headlines.")
            for art in data["articles"]:
                if title := art.get("title"):
                    speak(title)

        except Exception as e:
            print("Exception fetching news:", e)
            speak("Sorry, couldn't fetch the news.")
    else:
        speak(aiProcess(c))

def listen_command(timeout=10, phrase_time_limit=8):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, 0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            cmd = recognizer.recognize_google(audio)
            print("Heard:", cmd)
            return cmd
        except Exception as e:
            print("Listen error:", e)
            return None

if __name__ == "__main__":
    speak("Initializing Jarvis.")
    while True:
        tr = listen_command(timeout=8, phrase_time_limit=4)
        if tr and "jarvis" in tr.lower():
            speak("Yes?")
            cmd = listen_command(timeout=10, phrase_time_limit=8)
            if cmd:
                processCommand(cmd)
