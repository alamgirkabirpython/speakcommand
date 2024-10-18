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

# JavaScript for voice recognition
st.markdown("""
<script>
    function startRecognition() {
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.onstart = function() {
            document.getElementById("status").innerHTML = "Listening...";
        };
        recognition.onresult = function(event) {
            var transcript = event.results[0][0].transcript;
            document.getElementById("output").innerHTML = transcript;
            // Trigger submit with the recognized command
            const command = transcript;
            fetch(`/execute_command?command=${encodeURIComponent(command)}`)
                .then(response => response.text())
                .then(data => {
                    document.getElementById("status").innerHTML = data;
                });
        };
        recognition.onerror = function(event) {
            document.getElementById("status").innerHTML = "Error occurred in recognition: " + event.error;
        };
        recognition.start();
    }
</script>
""", unsafe_allow_html=True)

# Button to start voice recognition
if st.button("Start Listening"):
    st.markdown('<script>startRecognition();</script>', unsafe_allow_html=True)

# Placeholder for displaying the command
st.write("Command: ")
output = st.empty()
output.text("Say something...")

# Streamlit's command execution handling
command = st.experimental_get_query_params().get("command", [None])[0]

if command:
    command_lower = command.lower()

    # Stop listening and exit if the user says "stop" or "exit"
    if "stop" in command_lower or "exit" in command_lower:
        st.write("Stopping assistant.")
        audio_file = speak("Goodbye, sir.")
        st.markdown(play_audio(audio_file), unsafe_allow_html=True)

    # Check if the command is to play a song
    elif "play" in command_lower:
        search_term = command_lower.replace("play", "").strip()
        result = f"Opening YouTube and searching for {search_term}."
        search_youtube(search_term)
        st.write(result)
        audio_file = speak(result)
        st.markdown(play_audio(audio_file), unsafe_allow_html=True)

    # Check if the command is to open a website
    elif "open" in command_lower:
        search_term = command_lower.replace("open", "").strip()
        webbrowser.open(f"https://{search_term}.com")
        st.write(f"Opening {search_term}.com")
        audio_file = speak(f"Opening {search_term}.com")
        st.markdown(play_audio(audio_file), unsafe_allow_html=True)

    # Generate AI response using Google Generative AI (Gemini) for other commands
    else:
        chat = llm.start_chat()
        full_translation_prompt_text = command_speaker.format(text=command)
        full_translation_response = chat.send_message(full_translation_prompt_text)
        ai_response = full_translation_response.candidates[0].content.parts[0].text.strip()

        if ai_response:
            st.write(f"AI Response: {ai_response}")
            audio_file = speak(ai_response)
            st.markdown(play_audio(audio_file), unsafe_allow_html=True)
