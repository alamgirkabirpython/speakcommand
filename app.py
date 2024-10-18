import os
import streamlit as st
import datetime
import webbrowser
import speech_recognition as sr
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
import re
import requests
from gtts import gTTS
import tempfile
import langdetect
import base64
from streamlit_audio_recorder import audio_recorder

# Google Generative AI setup
api_key = "AIzaSyARRfATt7eG3Kn5Ud4XPzDGflNRdiqlxBM"
genai.configure(api_key=api_key)

# Define ChatPromptTemplate
command_speaker = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. You follow the command that the user gives."),
        ("user", "Follow the command: {text}")
    ]
)

# Initialize Google Generative AI Model
llm = genai.GenerativeModel(model_name="gemini-1.0-pro")

# Function to create audio file using gTTS and provide download link
def create_audio_file(text, lang):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts = gTTS(text=text, lang=lang)
        tts.save(fp.name)
        return fp.name

# Function to provide download link for the generated audio file
def download_audio_file(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        b64_audio = base64.b64encode(audio_bytes).decode()
        audio_html = f'<a href="data:audio/mp3;base64,{b64_audio}" download="output.mp3">Download Audio</a>'
        st.markdown(audio_html, unsafe_allow_html=True)

# Function to detect language and return appropriate TTS response
def speak(text):
    # Detect the language of the text
    lang = langdetect.detect(text)
    
    # Create an audio file with gTTS
    audio_file = create_audio_file(text, lang)
    
    # Provide a download link for the audio file
    st.write("Audio generated.")
    download_audio_file(audio_file)

# Greeting based on the time of day
def wiseMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        greeting = "Good Morning!"
    elif hour >= 12 and hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    return greeting

# Function to listen for voice commands using Streamlit's audio_recorder
def listen():
    audio_bytes = audio_recorder()
    
    if audio_bytes:
        recognizer = sr.Recognizer()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_file:
            audio_file.write(audio_bytes)
            audio_file.flush()
            audio = sr.AudioFile(audio_file.name)
            with audio as source:
                recognizer.adjust_for_ambient_noise(source)
                audio_data = recognizer.record(source)
            try:
                command = recognizer.recognize_google(audio_data)
                st.write(f"You said: {command}")
                return command
            except sr.UnknownValueError:
                st.write("Sorry, I could not understand the audio.")
                return ""
            except sr.RequestError:
                st.write("Could not request results; check your network connection.")
                return ""

# Function to search for a YouTube video
def search_youtube(query):
    youtube_search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(youtube_search_url)
    return f"Opening YouTube and searching for {query}"

# Streamlit UI
st.title("Personal Assistant Jessica")

if 'greeting' not in st.session_state:
    st.session_state['greeting'] = wiseMe()

st.write(f"{st.session_state['greeting']} I am Jessica, sir. Please tell me how I may help you")

if st.button("Speak Command"):
    st.session_state['listening'] = True

    while st.session_state.get('listening', False):
        # Listen to user command
        query = listen()

        if query:
            query_lower = query.lower()

            # Stop listening and exit if the user says "stop" or "exit"
            if "stop" in query_lower or "exit" in query_lower:
                st.write("Stopping assistant.")
                speak("Goodbye, sir.")
                st.session_state['listening'] = False
                break

            # Check if the command is to play a song
            elif "play" in query_lower:
                search_term = query_lower.replace("play", "").strip()
                result = search_youtube(search_term)
                st.write(result)
                speak(result)

            # Check if the command is to open a website
            elif "open" in query_lower:
                search_term = query_lower.replace("open", "").strip()
                webbrowser.open(f"https://{search_term}.com")
                st.write(f"Opening {search_term}.com")
                speak(f"Opening {search_term}.com")

            # Generate AI response using Google Generative AI (Gemini) for other commands
            else:
                chat = llm.start_chat()
                full_translation_prompt_text = command_speaker.format(text=query)
                full_translation_response = chat.send_message(full_translation_prompt_text)
                ai_response = full_translation_response.candidates[0].content.parts[0].text.strip()

                if ai_response:
                    st.write(f"AI Response: {ai_response}")
                    speak(ai_response)
