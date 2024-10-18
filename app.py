import streamlit as st

# Streamlit UI
st.title("Simple Voice Input App")

# Display instructions
st.write("Click the button below and start speaking.")

# Create a placeholder for displaying the transcribed text
transcribed_text_placeholder = st.empty()

# HTML + JavaScript for capturing voice input
html_code = """
    <script>
        function startDictation() {
            if (window.hasOwnProperty('webkitSpeechRecognition')) {
                var recognition = new webkitSpeechRecognition();
                
                recognition.continuous = false;  // Stop after a single recognition
                recognition.interimResults = false;  // No intermediate results
                recognition.lang = "en-US";  // Set the language

                recognition.onresult = function(e) {
                    var speech_to_text = e.results[0][0].transcript;  // Get the transcribed text
                    // Update the page with the recognized text
                    document.getElementById("result").innerText = speech_to_text;

                    // Send the transcribed text to Streamlit
                    const xhr = new XMLHttpRequest();
                    xhr.open("POST", "/update_transcribed_text", true);
                    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                    xhr.send(JSON.stringify({ text: speech_to_text }));
                };

                recognition.onerror = function(e) {
                    console.error('Speech recognition error', e);
                    alert('Error occurred: ' + e.error);
                };

                recognition.start();  // Start the speech recognition
            } else {
                alert("Sorry, your browser does not support speech recognition.");
            }
        }
    </script>

    <button onclick="startDictation()">Click to Speak</button>
    <h2>Transcribed Text:</h2>
    <p id="result"></p>
"""

# Embedding the HTML into the Streamlit app
st.components.v1.html(html_code)

# Streamlit's server-side to handle the transcribed text
def update_transcribed_text():
    if st.session_state.get("input_text"):
        st.session_state.transcribed_text = st.session_state.input_text
    else:
        st.session_state.transcribed_text = ""

# Use a callback route to receive the transcribed text from JavaScript
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

# Handle the input from JavaScript
if st.button("Get Transcribed Text"):
    update_transcribed_text()

# Show the transcribed text in the placeholder
transcribed_text_placeholder.write(f"Transcribed Text: **{st.session_state.transcribed_text}**")
