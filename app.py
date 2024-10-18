import streamlit as st
import google.generativeai as genai
import pyttsx3
import tempfile
import langdetect
from gtts import gTTS

# API key for Google Generative AI
api_key ="AIzaSyARRfATt7eG3Kn5Ud4XPzDGflNRdiqlxBM"
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
                    // Set the query parameter with the transcribed text
                    window.location.href = window.location.href.split('?')[0] + '?input_text=' + encodeURIComponent(speech_to_text);
                    recognition.stop();
                };

                recognition.onerror = function(e) {
                    recognition.stop();
                }
            }
        }
    </script>

    <button onclick="startDictation()">Click to Speak</button>
"""

# Embedding the HTML into the Streamlit app
st.components.v1.html(html_code)

# Read the transcribed text from URL query parameters
query_params = st.experimental_get_query_params()
input_text = query_params.get("input_text", [""])[0]

if input_text:
    st.write(f"Transcribed Text: {input_text}")
    
    # Use Generative AI to respond
    chat = llm.start_chat()
    ai_response = chat.send_message(input_text).candidates[0].content.parts[0].text.strip()
    st.write(f"AI Response: {ai_response}")
    speak(ai_response)
