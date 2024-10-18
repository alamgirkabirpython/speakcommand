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
                    // Set the transcribed text to a hidden input field
                    document.getElementById("hiddenInput").value = speech_to_text;
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
    <input type="hidden" id="hiddenInput" value="">
"""

# Embedding the HTML into the Streamlit app
st.components.v1.html(html_code)

# Retrieve the transcribed text from the hidden input using JavaScript
st.write('<script>document.getElementById("hiddenInput").value</script>')

# Use session state to hold transcribed text
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

# Check if the hidden input has been updated and update the session state
input_text = st.experimental_get_query_params().get("input_text", [""])[0]
if input_text:
    st.session_state.transcribed_text = input_text

# Show the transcribed text in the placeholder
transcribed_text_placeholder.write(f"Transcribed Text: **{st.session_state.transcribed_text}**")
