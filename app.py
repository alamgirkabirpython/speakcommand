import streamlit as st
import datetime
import webbrowser
import speech_recognition as sr
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
import tempfile
import langdetect
from gtts import gTTS
import base64

# Replace with your actual API key
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
    lang = langdetect.detect(text)  # Detect the language of the text
    audio_file = create_audio_file(text, lang)  # Create audio file
    st.write("Audio generated.")
    download_audio_file(audio_file)  # Provide download link

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

# Upload audio file
uploaded_file = st.file_uploader("Upload your audio command", type=["wav", "mp3"])

if uploaded_file is not None:
    # Use SpeechRecognition to convert audio to text
    r = sr.Recognizer()
    with sr.AudioFile(uploaded_file) as source:
        audio = r.record(source)  # Read the entire audio file
        try:
            command = r.recognize_google(audio)
            st.write(f"You said: {command}")
            query_lower = command.lower()

            # Stop listening and exit if the user says "stop" or "exit"
            if "stop" in query_lower or "exit" in query_lower:
                st.write("Stopping assistant.")
                speak("Goodbye, sir.")

            else:
                # Check if the command is to play a song
                if "play" in query_lower:
                    search_term = query_lower.replace("play", "").strip()
                    search_youtube(search_term)

                # Check if the command is to open a website
                elif "open" in query_lower:
                    search_term = query_lower.replace("open", "").strip()
                    webbrowser.open(f"https://{search_term}.com")
                    st.write(f"Opening {search_term}.com")
                    speak(f"Opening {search_term}.com")

                # Generate AI response using Google Generative AI (Gemini) for other commands
                else:
                    chat = llm.start_chat()
                    full_translation_prompt_text = command_speaker.format(text=query_lower)
                    full_translation_response = chat.send_message(full_translation_prompt_text)
                    ai_response = full_translation_response.candidates[0].content.parts[0].text.strip()

                    if ai_response:
                        st.write(f"AI Response: {ai_response}")
                        speak(ai_response)

        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.write("Could not request results; check your network connection.")

# Function to search for a YouTube video
def search_youtube(query):
    youtube_search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(youtube_search_url)
    return f"Opening YouTube and searching for {query}"
