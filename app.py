import streamlit as st
import google.generativeai as genai
import pyttsx3
import tempfile
import langdetect
from gtts import gTTS

# API key for Google Generative AI
api_key = "AIzaSyARRfATt7eG3Kn5Ud4XPzDGflNRdiqlxBM"  # Replace with your actual API key
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

# Display instructions
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

                recognition.onstart = function() {
                    console.log("Speech recognition service has started");
                    alert('Please start speaking...');
                };

                recognition.onresult = function(e) {
                    var speech_to_text = e.results[0][0].transcript;
                    // Set the query parameter with the transcribed text
                    window.location.href = window.location.href.split('?')[0] + '?input_text=' + encodeURIComponent(speech_to_text);
                    recognition.stop();
                };

                recognition.onerror = function(e) {
                    console.error('Speech recognition error', e);
                    alert('Error occurred in recognition: ' + e.error);
                    recognition.stop();
                };

                recognition.onend = function() {
                    console.log("Speech recognition service has stopped");
                    alert('Speech recognition has ended. Please click the button to try again.');
                };

                recognition.start();
            } else {
                alert("Sorry, your browser does not support speech recognition.");
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

# Check if input_text is provided
if input_text:
    # Display the transcribed text (query you said)
    st.write(f"Transcribed Text (Query): {input_text}")
    
    # Print the query in the Streamlit logs (useful for debugging)
    st.write(f"Log (Query You Said): {input_text}")
    
    # Use Generative AI to respond to the query
    chat = llm.start_chat()
    response = chat.send_message(input_text).candidates[0].content.parts[0].text.strip()
    
    # Display the AI response
    st.write(f"AI Response: {response}")
    
    # Print the AI response in the logs (for debugging)
    st.write(f"Log (AI Response): {response}")
    
    # Speak the AI response
    speak(response)

else:
    # This message will help with debugging if the input_text is empty or not captured
    st.write("No transcribed text found. Please try again.")
