import streamlit as st
import datetime
import webbrowser
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
    lang = langdetect.detect(text)  # Detect the language of the text
    
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

# Function to search for a YouTube video
def search_youtube(query):
    youtube_search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(youtube_search_url)
    return f"Opening YouTube and searching for {query}"

# JavaScript for voice recognition using the Web Speech API
st.write("""
    <script>
        var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        function startRecognition() {
            recognition.start();
            document.getElementById('output').innerHTML = 'Listening...';
        }

        recognition.onresult = function(event) {
            var result = event.results[0][0].transcript;
            document.getElementById('output').innerHTML = 'You said: ' + result;
            var input = document.getElementById('input_text');
            input.value = result;
            document.getElementById('submit_button').click();
        };

        recognition.onerror = function(event) {
            document.getElementById('output').innerHTML = 'Error occurred in recognition: ' + event.error;
        };
    </script>
""", unsafe_allow_html=True)

# UI in Streamlit
st.title("Personal Assistant Jessica")

# Show greeting on load
if 'greeting' not in st.session_state:
    st.session_state['greeting'] = wiseMe()

st.write(f"{st.session_state['greeting']} I am Jessica, sir. Please tell me how I may help you")

# Button to start voice recognition
st.write('<button onclick="startRecognition()">Speak Command</button>', unsafe_allow_html=True)
st.write('<p id="output">Click the button to start speaking...</p>', unsafe_allow_html=True)

# Hidden form input field to capture speech recognition result and submit it
st.text_input("Command", key="input_text", label_visibility="collapsed")
if st.button("Submit", key="submit_button"):
    query = st.session_state["input_text"]
    if query:
        query_lower = query.lower()

        # Stop listening and exit if the user says "stop" or "exit"
        if "stop" in query_lower or "exit" in query_lower:
            st.write("Stopping assistant.")
            audio_file = speak("Goodbye, sir.")
            st.audio(audio_file)  # Play the audio file in the browser

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
