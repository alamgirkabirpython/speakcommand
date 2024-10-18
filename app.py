import streamlit as st
import datetime
import webbrowser
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
import langdetect

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

# Streamlit UI
st.title("Personal Assistant Jessica")

if 'greeting' not in st.session_state:
    st.session_state['greeting'] = wiseMe()

st.write(f"{st.session_state['greeting']} I am Jessica, sir. Please tell me how I may help you")

# JavaScript for voice recognition
st.markdown("""
<script>
    async function listenForCommand() {
        const recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            document.getElementById('status').innerText = 'Listening...';
        };

        recognition.onresult = function(event) {
            const command = event.results[0][0].transcript;
            document.getElementById('commandInput').value = command;
            document.getElementById('commandForm').submit();
        };

        recognition.onerror = function(event) {
            document.getElementById('status').innerText = 'Error occurred in recognition: ' + event.error;
        };

        recognition.start();
    }

    // Automatically start listening when the page loads
    window.onload = function() {
        listenForCommand();
    };
</script>
""", unsafe_allow_html=True)

# Display status
st.write('<div id="status"></div>', unsafe_allow_html=True)

# Hidden input form for commands
command = st.text_input("Say a command:", key="commandInput")

# Process command directly without a submit button
if command:
    query_lower = command.lower()

    # Stop listening and exit if the user says "stop" or "exit"
    if "stop" in query_lower or "exit" in query_lower:
        st.write("Stopping assistant.")
    # Check if the command is to play a song
    elif "play" in query_lower:
        search_term = query_lower.replace("play", "").strip()
        result = search_youtube(search_term)
        st.write(result)
    # Check if the command is to open a website
    elif "open" in query_lower:
        search_term = query_lower.replace("open", "").strip()
        webbrowser.open(f"https://{search_term}.com")
        st.write(f"Opening {search_term}.com")
    # Generate AI response using Google Generative AI (Gemini) for other commands
    else:
        chat = llm.start_chat()
        full_translation_prompt_text = command_speaker.format(text=query_lower)
        full_translation_response = chat.send_message(full_translation_prompt_text)
        ai_response = full_translation_response.candidates[0].content.parts[0].text.strip()

        if ai_response:
            st.write(f"AI Response: {ai_response}")

# Button to start listening
st.button("Start Listening", on_click=lambda: None)  # Placeholder button
