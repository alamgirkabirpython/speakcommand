import streamlit as st

# Streamlit UI
st.title("Voice Input Example")

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

                recognition.onresult = function(e) {
                    var speech_to_text = e.results[0][0].transcript;
                    // Set the query parameter with the transcribed text
                    window.location.href = window.location.href.split('?')[0] + '?input_text=' + encodeURIComponent(speech_to_text);
                    recognition.stop();
                };

                recognition.onerror = function(e) {
                    console.error('Speech recognition error', e);
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
    st.write(f"Transcribed Text: {input_text}")
else:
    st.write("Please click the button and speak.")
