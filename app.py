import streamlit as st
import datetime
import webbrowser
import speech_recognition as sr
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from gtts import gTTS
import tempfile
import langdetect

# Initialize API Key for Google Generative AI
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

# Function to generate downloadable speech audio using gTTS
def speak(text):
    lang = langdetect.detect(text)
    tts = gTTS(text=text, lang=lang if lang in ['bn', 'hi', 'en'] else 'en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format='audio/mp3')
        st.download_button("Download Audio", data=open(fp.name, 'rb').read(), file_name=f"response_{lang}.mp3")

# Greeting based on the time of day
def wiseMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        return "Good Morning!"
    elif hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

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
                full_translation_prompt_text = command_speaker.format(text=query)
                full_translation_response = chat.send_message(full_translation_prompt_text)
                ai_response = full_translation_response.candidates[0].content.parts[0].text.strip()

                if ai_response:
                    st.write(f"AI Response: {ai_response}")
                    speak(ai_response)
