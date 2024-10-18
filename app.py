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

                    // Send the transcribed text to Streamlit using a hidden input field
                    const hiddenInput = document.getElementById("hiddenInput");
                    hiddenInput.value = speech_to_text;
                    hiddenInput.dispatchEvent(new Event('change'));
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
    <input type="hidden" id="hiddenInput" onchange="updateStreamlit()">
    <h2>Transcribed Text:</h2>
    <p id="result"></p>
"""

# Function to update Streamlit with the transcribed text
def update_streamlit():
    if 'input_text' in st.session_state:
        st.session_state.input_text = st.session_state.hidden_input
    else:
        st.session_state.input_text = ""

# Embedding the HTML into the Streamlit app
st.components.v1.html(html_code)

# Update Streamlit state when the hidden input changes
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Display the transcribed text
transcribed_text_placeholder.write(f"Transcribed Text: **{st.session_state.input_text}**")

# Capture the value from hidden input field
hidden_input_value = st.text_input("Hidden Input", key="hidden_input", label_visibility="collapsed")
if hidden_input_value:
    st.session_state.input_text = hidden_input_value  # Store in session state
