import streamlit as st

# Streamlit UI
st.title("Simple Voice Input App")

# Display instructions
st.write("Click the button below and start speaking.")

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
                    // Send the text back to Streamlit
                    const queryString = "?input_text=" + encodeURIComponent(speech_to_text);
                    window.location.href = window.location.href.split('?')[0] + queryString;
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

# Retrieve the transcribed text from the URL parameters
input_text = st.experimental_get_query_params().get("input_text", [""])[0]

# Display the transcribed text if it exists
if input_text:
    st.write(f"Transcribed Text: **{input_text}**")
else:
    st.write("Please click the button and speak.")
