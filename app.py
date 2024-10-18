import speech_recognition as sr
import streamlit as st
# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Reading Microphone as source
# listening the speech and store in audio_text variable

with sr.Microphone() as source:
    st.write("Talk")
    audio_text = r.listen(source)
    st.write("Time over, thanks")
# recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    
    try:
        # using google speech recognition
        st.write("Text: "+r.recognize_google(audio_text))
    except:
         st.write("Sorry, I did not get that")
