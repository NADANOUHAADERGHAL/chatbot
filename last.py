import streamlit as st
from audio_recorder_streamlit import audio_recorder
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

google_API_key = 'AIzaSyArNjjHPuVtyDj9DmP9NlUXTTax2BiiRKI' 
genai.configure(api_key=google_API_key)
model = genai.GenerativeModel('gemini-1.5-pro-latest')
convo = model.start_chat()

# Speech recognition function
def recognize_speech(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_content = recognizer.record(source)
        text = recognizer.recognize_google(audio_content)
        st.markdown(f'<div class="user-bubble"> 🗣️You said: {text}</div>', unsafe_allow_html=True)
        return text
    except sr.UnknownValueError:
        st.write("Could not understand the audio.")
        return None
    except sr.RequestError as e:
        st.write(f"Could not request results; {e}")
        return None

# Response generation function
def generate_response(input_text):
    try:
        if "how are you" in input_text.lower():
            response_text = "I'm good, thank you!"
        elif "good morning" in input_text.lower():
            response_text = "Good morning, have a good day!"
        elif "good night" in input_text.lower():
            response_text = "Good night, have a sweet dream!"
        elif "good evening" in input_text.lower():
            response_text = "Good evening to you too!"
        elif "what is key box training and robotics school" in input_text.lower():
            response_text = "KEY BOX is a technological learning center specializing in robotics. Its goal is to popularize the field of robotics and make it more accessible to all enthusiasts and lovers of creation and invention."
        elif "what is key box" in input_text.lower():
            response_text = "KEY BOX is a technological learning center specializing in robotics. Its goal is to popularize the field of robotics and make it more accessible to all enthusiasts and lovers of creation and invention."
        elif "what is keybox" in input_text.lower():
            response_text = "KEY BOX is a technological learning center specializing in robotics. Its goal is to popularize the field of robotics and make it more accessible to all enthusiasts and lovers of creation and invention."
        elif "Qu'est-ce que Keybox" in input_text.lower():
            response_text = "KEYBOX est un centre d’apprentissage technologique spécialisé en robotique. Pour but de la vulgarisation du domaine de la robotique et le rendre plus accessible pour tt les amateurs et les amoureux de la création et d’invention."
        elif "À quoi sert Keybox ?" in input_text.lower():
            response_text = "KEYBOX est un centre d’apprentissage technologique spécialisé en robotique. Pour but de la vulgarisation du domaine de la robotique et le rendre plus accessible pour tt les amateurs et les amoureux de la création et d’invention."
        elif "Qu'est-ce que le système Keybox ?" in input_text.lower():
            response_text = "KEYBOX est un centre d’apprentissage technologique spécialisé en robotique. Pour but de la vulgarisation du domaine de la robotique et le rendre plus accessible pour tt les amateurs et les amoureux de la création et d’invention."
        elif "Comment fonctionne Keybox ?" in input_text.lower():
            response_text = "KEYBOX est un centre d’apprentissage technologique spécialisé en robotique. Pour but de la vulgarisation du domaine de la robotique et le rendre plus accessible pour tt les amateurs et les amoureux de la création et d’invention."
        elif "ماهو كيبوكس ?" in input_text.lower():
            response_text = "كيبوكس هو مركز تعليمي تكنولوجي متخصص في مجال الروبوتات. يهدف إلى تبسيط مجال الروبوتات وجعله أكثر سهولة لجميع الهواة وعشاق الابتكار والاختراع."
        elif "what is the capital of plastine" in input_text.lower():
            response_text = "the capital of plastine is el qods"
        elif "c'est quoi keybox" in input_text.lower():
            response_text = "KEYBOX est un centre d’apprentissage technologique spécialisé en robotique. Pour but de la vulgarisation du domaine de la robotique et le rendre plus accessible pour tt les amateurs et les amoureux de la création et d’invention"    
        else:
            response = convo.send_message(input_text)
            response_text = response.text
            response_text = response_text.replace("*", "").replace("😊", "").replace(" 💪", "").replace(" 🦗 ", "").replace(" ✨ ", "").replace(" ##", "").replace("  🤖✨ ", "").replace(" 🤖", "").replace(" ✨ ", "").replace(" 👋 ", "").replace("😄 ", "").replace(" 🕌❄️ ", "").replace(" 🎿", "").replace(" ❄️", "").replace(" 🐪🎿", "").replace("🤔  ", "").replace("  🕌", "").strip()
            print("My response:", response_text)
        
        return response_text
        
    except Exception as e:
        print("An error occurred while generating response: {}".format(e))
        return None

# Streamlit front-end UI design
st.markdown(
    '''
    <style>
        .main-heading {
            color: #2C3E50;
            text-align: center;
            font-family: 'Arial', sans-serif;
            margin-bottom: 20px;
            font-size: 36px;
            font-weight: bold;
        }
        .user-bubble {
            background-color: #D1E8E2;
            border-radius: 15px;
            padding: 10px;
            margin: 5px 0;
            text-align: left;
            width: fit-content;
            max-width: 70%;
            font-family: 'Arial', sans-serif;
            color: #2C3E50;
            box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
            align-self: flex-start;
        }
        .assistant-bubble {
            background-color: #E8F0FE;
            border-radius: 15px;
            padding: 10px;
            margin: 5px 0;
            text-align: left;
            width: fit-content;
            max-width: 70%;
            font-family: 'Arial', sans-serif;
            color: #2C3E50;
            box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
            align-self: flex-start;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: center; /* Center items horizontally */
        }
        .input-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center; /* Center the input field only */
        }
        .text-input {
            flex: 1;
            max-width: 400px; /* Optional: Set a maximum width for the input box */
        }
    </style>

    <h1 class="main-heading">Chat with your Keybox Assistant 🤖</h1>
    <div class="chat-container">
    ''',
    unsafe_allow_html=True
)

# Adding input field and microphone button in a single row
with st.container():
    # Centering the input box only
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input("Ask your Keybox Assistant:", key="user_input", label_visibility="collapsed", placeholder="Type your message here...")
    with col2:
        audio_data = audio_recorder(pause_threshold=0.5, key="audio_recorder")

# Process the input text
if user_input:
    response = generate_response(user_input)
    if response:
        st.markdown(f'<div class="assistant-bubble">🤖 {response}</div>', unsafe_allow_html=True)

# Process the audio input
if audio_data:
    st.audio(audio_data, format='audio/wav')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_data)
        temp_audio_file_path = temp_audio_file.name
    text = recognize_speech(temp_audio_file_path)

    if text:
        response = generate_response(text)
        if response:
            # Convert text response to speech
            tts = gTTS(response)
            temp_audio_response_path = tempfile.mktemp(suffix=".mp3")
            tts.save(temp_audio_response_path)

            # Display response text as a bubble
            st.markdown(f'<div class="assistant-bubble">🤖 {response}</div>', unsafe_allow_html=True)

            # Play the voice response
            st.audio(temp_audio_response_path)

            # Clean up the temporary file
            os.remove(temp_audio_response_path)

    os.remove(temp_audio_file_path)

# Close the chat-container div
st.markdown("</div>", unsafe_allow_html=True)
