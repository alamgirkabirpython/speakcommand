import streamlit as st
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import tempfile
import langdetect
from gtts import gTTS
import os

# API key for Google Generative AI
api_key = "AIzaSyARRfATt7eG3Kn5Ud4XPzDGflNRdiqlxBM"
genai.configure(api_key=api_key)

# Initialize Google Generative AI Model
llm = genai.GenerativeModel(model_name="gemini-1.0-pro")

# Function to speak text using pyttsx3 (for English) or gTTS (for Bangla, Hindi)
def speak(text):
    lang = langdetect.detect(text)
    
    if lang == 'bn':  # Bangla
        tts = gTTS(text=text, lang='bn')
        temp_file_path = save_tts_to_temp(tts)
        st.audio(temp_file_path)
        
    elif lang == 'hi':  # Hindi
        tts = gTTS(text=text, lang='hi')
        temp_file_path = save_tts_to_temp(tts)
        st.audio(temp_file_path)
        
    else:  # English
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

# Function to save TTS output to a temporary file
def save_tts_to_temp(tts):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file_path = temp_file.name
    tts.save(temp_file_path)
    temp_file.close()
    return temp_file_path

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

# Function to listen for voice commands (using Google Web Speech API)
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)  # Use Google Web Speech API for recognition
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
        query = listen()

        if query:
            query_lower = query.lower()

            if "stop" in query_lower or "exit" in query_lower:
                st.write("Stopping assistant.")
                speak("Goodbye, sir.")
                st.session_state['listening'] = False
                break

            elif "play" in query_lower:
                search_term = query_lower.replace("play", "").strip()
                result = search_youtube(search_term)
                st.write(result)
                speak(result)

            elif "open" in query_lower:
                search_term = query_lower.replace("open", "").strip()
                webbrowser.open(f"https://{search_term}.com")
                st.write(f"Opening {search_term}.com")
                speak(f"Opening {search_term}.com")

            else:
                chat = llm.start_chat()
                ai_response = chat.send_message(query).candidates[0].content.parts[0].text.strip()

                if ai_response:
                    st.write(f"AI Response: {ai_response}")
                    speak(ai_response)
