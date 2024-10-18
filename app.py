import streamlit as st
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
import langdetect 
import tempfile
from gtts import gTTS
import pygame
import base64

# Initialize Google Generative AI Model
api_key = "AIzaSyARRfATt7eG3Kn5Ud4XPzDGflNRdiqlxBM"
genai.configure(api_key=api_key)

# Initialize pygame for audio playback
pygame.mixer.init()

# Function to speak text using pyttsx3 or gTTS
def speak(text):
    lang = langdetect.detect(text)
    if lang == 'bn':
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts = gTTS(text=text, lang='bn')
            tts.save(f"{fp.name}.mp3")
            pygame.mixer.music.load(f"{fp.name}.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
    elif lang == 'hi':
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts = gTTS(text=text, lang='hi')
            tts.save(f"{fp.name}.mp3")
            pygame.mixer.music.load(f"{fp.name}.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
    else:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

# Greeting based on time of day
def wiseMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        return "Good Morning!"
    elif hour >= 12 and hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

# Function to process audio input and recognize speech
def listen(audio_data):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)
        try:
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Could not request results; check your network connection."

# Streamlit UI
st.title("Personal Assistant Jessica")

if 'greeting' not in st.session_state:
    st.session_state['greeting'] = wiseMe()

st.write(f"{st.session_state['greeting']} I am Jessica, sir. Please tell me how I may help you")

# JavaScript to capture audio from microphone
st.markdown("""
    <script>
    var my_div = document.getElementById("mic_streamlit")
    if (my_div) {
        var my_div_1 = document.createElement('div')
        my_div_1.setAttribute("id", "my_div_new")
        document.getElementById("mic_streamlit").appendChild(my_div_1);
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function(stream) {
                const mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                const audioChunks = [];
                mediaRecorder.addEventListener("dataavailable", function(event) {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener("stop", function() {
                    const audioBlob = new Blob(audioChunks);
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = function() {
                        const base64AudioMessage = reader.result.split(',')[1];
                        const xhr = new XMLHttpRequest();
                        xhr.open("POST", "/process_audio");
                        xhr.setRequestHeader("Content-Type", "application/json");
                        xhr.send(JSON.stringify({ "audio_data": base64AudioMessage }));
                    };
                });

                setTimeout(function() {
                    mediaRecorder.stop();
                }, 3000);
            });
    }
    </script>
    <div id="mic_streamlit"></div>
""", unsafe_allow_html=True)

# Placeholder for audio processing
audio_input = st.empty()

# Function to search YouTube
def search_youtube(query):
    youtube_search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(youtube_search_url)
    return f"Opening YouTube and searching for {query}"

if st.button("Speak Command"):
    # Capture and process voice commands
    st.write("Listening...")
    # The `listen()` function will be triggered by JavaScript and process audio directly

# Placeholder for command response
if 'command' in st.session_state:
    st.write(f"You said: {st.session_state['command']}")
    if "play" in st.session_state['command'].lower():
        search_term = st.session_state['command'].replace("play", "").strip()
        result = search_youtube(search_term)
        st.write(result)
        speak(result)
    elif "open" in st.session_state['command'].lower():
        search_term = st.session_state['command'].replace("open", "").strip()
        webbrowser.open(f"https://{search_term}.com")
        st.write(f"Opening {search_term}.com")
        speak(f"Opening {search_term}.com")
    else:
        chat = llm.start_chat()
        prompt_text = command_speaker.format(text=st.session_state['command'])
        full_translation_response = chat.send_message(prompt_text)
        ai_response = full_translation_response.candidates[0].content.parts[0].text.strip()
        if ai_response:
            st.write(f"AI Response: {ai_response}")
            speak(ai_response)
