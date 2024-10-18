import streamlit as st
import datetime
import webbrowser
import speech_recognition as sr
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
import langdetect
from gtts import gTTS
import tempfile

# Google Generative AI API Key configuration
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

# Function to generate text-to-speech audio file using gTTS
def speak(text):
    # Detect the language of the text
    lang = langdetect.detect(text)
    
    # Use gTTS to convert text to speech and save it as a file
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name  # Return the file path for the generated speech

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

# Function to listen for voice commands
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
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

# Show greeting on load
if 'greeting' not in st.session_state:
    st.session_state['greeting'] = wiseMe()

st.write(f"{st.session_state['greeting']} I am Jessica, sir. Please tell me how I may help you")

# Voice command button
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
                audio_file = speak("Goodbye, sir.")
                st.session_state['listening'] = False
                st.audio(audio_file)  # Play the audio file in the browser
                break

            # Check if the command is to play a song
            elif "play" in query_lower:
                search_term = query_lower.replace("play", "").strip()
                result = search_youtube(search_term)
                st.write(result)
                audio_file = speak(result)
                st.audio(audio_file)  # Play the audio file in the browser

            # Check if the command is to open a website
            elif "open" in query_lower:
                search_term = query_lower.replace("open", "").strip()
                webbrowser.open(f"https://{search_term}.com")
                st.write(f"Opening {search_term}.com")
                audio_file = speak(f"Opening {search_term}.com")
                st.audio(audio_file)  # Play the audio file in the browser

            # Generate AI response using Google Generative AI (Gemini) for other commands
            else:
                chat = llm.start_chat()
                full_translation_prompt_text = command_speaker.format(text=query)
                full_translation_response = chat.send_message(full_translation_prompt_text)
                ai_response = full_translation_response.candidates[0].content.parts[0].text.strip()

                if ai_response:
                    st.write(f"AI Response: {ai_response}")
                    audio_file = speak(ai_response)
                    st.audio(audio_file)  # Play the audio file in the browser
