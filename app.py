import streamlit as st
import google.generativeai as genai
import pyttsx3
import tempfile
import langdetect
from gtts import gTTS

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

# Streamlit UI
st.title("Personal Assistant Jessica")

# Embedding JavaScript for voice recognition
st.markdown("## Voice Assistant")
st.write("Click the button below and start speaking.")

# HTML + JavaScript for capturing voice input
html_code = """
    <script>
        function startDictation() {
            if (window.hasOwnProperty('webkitSpeechRecognition')) {
                var recognition = new webkitSpeechRecognition();
                
                recognition.continuous = false;
                recognition.interimResults = false;

                recognition.lang = "en-US";
                recognition.start();

                recognition.onresult = function(e) {
                    var speech_to_text = e.results[0][0].transcript;
                    document.getElementById('input_text').value = speech_to_text;
                    recognition.stop();
                    document.getElementById('submit_button').click();  // Automatically submit the form
                };

                recognition.onerror = function(e) {
                    recognition.stop();
                }
            }
        }
    </script>

    <button onclick="startDictation()">Click to Speak</button>
    <br>
    <form action="#" method="post">
        <input type="text" id="input_text" name="input_text">
        <input type="submit" id="submit_button" style="display: none;">
    </form>
"""

# Embedding the HTML into the Streamlit app
st.components.v1.html(html_code)

# Get the transcribed text (POST request from JavaScript)
if st.session_state.get("input_text") is None:
    st.session_state["input_text"] = ""

input_text = st.text_input("Transcribed Text:", st.session_state.get("input_text"))

if input_text:
    st.session_state["input_text"] = input_text

    # Reset the input after each submission
    if st.session_state["input_text"]:
        st.session_state["input_text"] = ""

    # Use Generative AI to respond
    if input_text:
        chat = llm.start_chat()
        ai_response = chat.send_message(input_text).candidates[0].content.parts[0].text.strip()
        st.write(f"AI Response: {ai_response}")
        speak(ai_response)
