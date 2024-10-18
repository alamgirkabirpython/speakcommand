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

                    // Redirect to the same page with the transcribed text in the URL
                    window.location.href = window.location.href.split('?')[0] + "?input_text=" + encodeURIComponent(speech_to_text);
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

# Get the input text from the query parameters
input_text = st.experimental_get_query_params().get("input_text", [""])[0]

# Use session state to hold transcribed text
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

# Update the session state with the new input text if it exists
if input_text:
    st.session_state.transcribed_text = input_text

# Show the transcribed text in the placeholder
transcribed_text_placeholder.write(f"Transcribed Text: **{st.session_state.transcribed_text}**")
