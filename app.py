import streamlit as st
import datetime
import webbrowser
import os
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from gtts import gTTS
import tempfile
import langdetect
import base64

# Your Google API Key (ensure you set this in your environment)
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

# Function to generate audio and create a playable link
def speak(text):
    lang = langdetect.detect(text)
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name  # Return the path of the saved audio file

# Function to play the audio
def play_audio(file_path):
    audio_file = open(file_path, "rb").read()
    audio_b64 = base64.b64encode(audio_file).decode()
    return f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'

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

# Streamlit UI
st.title("Personal Assistant Jessica")

if 'greeting' not in st.session_state:
    st.session_state['greeting'] = wiseMe()

st.write(f"{st.session_state['greeting']} I am Jessica, sir. Please tell me how I may help you")

# JavaScript to capture voice input
st.markdown(
    """
    <script>
    const recordButton = document.getElementById("record");
    const audioPlayer = document.getElementById("audioPlayer");
    
    recordButton.onclick = function() {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            const audioChunks = [];
            
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks);
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayer.src = audioUrl;
                audioPlayer.play();

                // Send audio blob to server for speech recognition
                const formData = new FormData();
                formData.append('audio', audioBlob);

                fetch('/process_audio', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("result").innerText = "You said: " + data.transcript;
                    // Process command here if needed
                });
            };
            
            mediaRecorder.start();
            setTimeout(() => {
                mediaRecorder.stop();
            }, 3000); // Record for 3 seconds
        });
    };
    </script>
    """,
    unsafe_allow_html=True
)

# Button to start recording
st.button("Start Recording", key="record")

# Audio player for playback
st.markdown('<audio id="audioPlayer" controls></audio>', unsafe_allow_html=True)

# Placeholder for displaying results
st.markdown('<div id="result"></div>', unsafe_allow_html=True)

# Add your command processing logic here
if st.button("Stop Recording"):
    st.write("Recording stopped. Please analyze the command.")

