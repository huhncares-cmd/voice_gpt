from dotenv import load_dotenv

load_dotenv()

import os
import time
from gtts import gTTS
from pygame import mixer
import speech_recognition as sr
from revChatGPT.V1 import Chatbot

CONTEXT_FILE = "context.txt"

# https://chat.openai.com/api/auth/session
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def get_context(filename):
    with open(filename, "r+") as f:
        context = f.read()
        if len(context) >= 1000:
            context = ""
            os.remove(filename)
            open(filename, "w+")
    return context

def write_context(filename, response):
    with open(filename, "a+") as f:
        f.write(response)

def generate_prompt(question, context):
    return f"""
    Role: You're a smart speaker and you want to reply in short informative sentences if not asked differnetly. You answer in the language the question is formulated in.\n
    Context: {context}\n
    {question}"""

def ask_chatbot(chatbot, prompt):
    response = ""
    for data in chatbot.ask(prompt):
        response = data["message"]
    return response

def speak(text):
    # Enter any language you want
    tts = gTTS(text=text, lang='de', slow=False)

    filename = "audio.mp3"

    tts.save(filename)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    return
    
if __name__ == "__main__":
    #TODO: Fix speech recognition
    """r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print(text)"""

    chatbot = Chatbot(config={
        "access_token": ACCESS_TOKEN
    })
    prompt = generate_prompt(input("You: "), get_context(CONTEXT_FILE))
    response = ask_chatbot(chatbot, prompt)
    print(response)
    speak(response)
    write_context(CONTEXT_FILE, response)