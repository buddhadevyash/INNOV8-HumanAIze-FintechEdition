# import streamlit as st
# import pandas as pd
# import os
# import io
# from huggingface_hub import InferenceClient
# from dotenv import load_dotenv
# import speech_recognition as sr
# from gtts import gTTS
# import tempfile
# from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
# import av
# from pydub import AudioSegment

# # Load environment variables from .env file
# load_dotenv()

# # Function to load fine-tuning data and bot_score.csv
# def load_data():
#     fine_tuning_file_path = 'tune_data.txt'
#     csv_file_path = 'bot_score.csv'

#     fine_tuning_data = ""
#     fitness_discount_data = {}

#     if os.path.exists(fine_tuning_file_path):
#         with open(fine_tuning_file_path, 'r') as file:
#             fine_tuning_data = file.read()

#     if os.path.exists(csv_file_path):
#         df = pd.read_csv(csv_file_path)
#         for index, row in df.iterrows():
#             fitness_score = row['Fitness Score']
#             discount = row['Discount']
#             fitness_discount_data[fitness_score] = discount

#     return fine_tuning_data, fitness_discount_data

# # Function to clear chat history
# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# # Function to predict discount based on fitness score
# def predict_discount(fitness_score):
#     if fitness_score >= 90:
#         return 30  # 30% discount
#     elif fitness_score >= 80:
#         return 25  # 25% discount
#     elif fitness_score >= 70:
#         return 20  # 20% discount
#     elif fitness_score >= 60:
#         return 15  # 15% discount
#     elif fitness_score >= 50:
#         return 10  # 10% discount
#     elif fitness_score >= 40:
#         return 5   # 5% discount
#     else:
#         return 0   # No discount

# # Function to generate AI assistant response
# def generate_insurance_assistant_response(prompt_input, client, fine_tuning_data, fitness_discount_data):
#     system_message = "You are a consultant with expertise in personal finance and insurance. Provide crisp and short responses."

#     if fine_tuning_data:
#         system_message += f"\n\nFine-tuning data:\n{fine_tuning_data}"

#     if "fitness score" in prompt_input.lower() or "discount" in prompt_input.lower():
#         return "Please provide your fitness score to get information about the discount you qualify for."

#     try:
#         user_fitness_score = float(prompt_input)
#         discount = predict_discount(user_fitness_score)
#         return f"Your fitness score is {user_fitness_score}. Based on this, you get {discount}% discount."
#     except ValueError:
#         pass

#     messages = [
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": prompt_input}
#     ]

#     response = ""
#     for message in client.chat_completion(
#             messages=messages,
#             max_tokens=120,
#             stream=True
#     ):
#         response += message.choices[0].delta.content or ""

#     return response

# # Function to transcribe audio
# def transcribe_audio(audio_data):
#     try:
#         r = sr.Recognizer()
        
#         # Convert audio to WAV
#         if isinstance(audio_data, bytes):
#             audio = AudioSegment.from_file(io.BytesIO(audio_data))
#         else:
#             audio = AudioSegment.from_file(audio_data)
        
#         wav_data = io.BytesIO()
#         audio.export(wav_data, format="wav")
#         wav_data.seek(0)
        
#         with sr.AudioFile(wav_data) as source:
#             audio_data = r.record(source)
        
#         text = r.recognize_google(audio_data)
#         return text
#     except Exception as e:
#         st.error(f"Error transcribing audio: {str(e)}")
#         return None

# # Function to convert text to speech
# def text_to_speech(text):
#     tts = gTTS(text=text, lang='en')
#     audio_bytes = io.BytesIO()
#     tts.write_to_fp(audio_bytes)
#     audio_bytes.seek(0)
#     return audio_bytes.getvalue()

# # Define the AI Assistant page
# def ai_assistant_page():
#     st.title('AI Assistant')
#     st.write("Your personal insurance and finance expert")

#     if "file_processed" not in st.session_state:
#         st.session_state.file_processed = False
    
#     # Custom CSS for chat containers and buttons
#     st.markdown("""
#     <style>
#     .user-container {
#         background-color: #2b5c8a;
#         border-radius: 10px;
#         padding: 10px;
#         margin: 10px 0;
#     }
#     .assistant-container {
#         background-color: #1e3d5a;
#         border-radius: 10px;
#         padding: 10px;
#         margin: 10px 0;
#     }
#     .chat-text {
#         color: #ffffff;
#     }
#     .stButton > button {
#         width: 100%;
#         height: 40px;
#         background-color: #4CAF50;
#         color: white;
#         border: none;
#         border-radius: 5px;
#         font-size: 16px;
#         cursor: pointer;
#     }
#     .stButton > button:hover {
#         background-color: #45a049;
#     }
#     .button-container {
#         display: flex;
#         justify-content: space-between;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # Load data and configurations
#     fine_tuning_data, fitness_discount_data = load_data()

#     # Define sidebar for AI Assistant configurations
#     with st.sidebar:
#         st.title('🏛️🔍 AI-Assistant Settings')
#         hf_api_token = "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"
#         if hf_api_token:
#             st.success('API key loaded from environment variable!', icon='✅')
#         else:
#             st.error('API key not found. Please set the HUGGINGFACE_API_TOKEN environment variable.', icon='🚨')

#         # Initialize the InferenceClient
#         client = InferenceClient(
#             "mistralai/Mixtral-8x7B-Instruct-v0.1",
#             token=hf_api_token
#         )

#         st.button('Clear Chat History', on_click=clear_chat_history)

#     # Initialize session state for messages
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

#     # Display chat history
#     chat_container = st.container()
#     with chat_container:
#         for i, message in enumerate(st.session_state.messages):
#             container_class = "user-container" if message['role'] == "user" else "assistant-container"
#             col1, col2 = st.columns([0.9, 0.1])
#             with col1:
#                 st.markdown(f"""
#                 <div class="{container_class}">
#                     <p class="chat-text"><strong>{'You' if message['role'] == 'user' else 'Assistant'}:</strong> {message['content']}</p>
#                 </div>
#                 """, unsafe_allow_html=True)
#             with col2:
#                 audio_button_label = f"Play Audio {i}"
#                 if st.button("Play", key=audio_button_label):
#                     audio_bytes = text_to_speech(message['content'])
#                     st.audio(audio_bytes, format="audio/mp3")

#     # Handle user input and generate responses
#     user_input = st.text_input("Type your message here:", key="user_input")
#     col1, col2= st.columns([0.5, 0.5])
#     with col1:
#         send_button = st.button("Send")
#     with col2:
#         speak_button = st.button("Speak")

  
#     uploaded_file = st.file_uploader("Facing issues recording? Upload an audio file instead:", type=['wav', 'mp3', 'ogg', 'm4a', 'flac'])

#     if uploaded_file is not None and not st.session_state.file_processed:
#         try:
#             # Display audio player
#             st.audio(uploaded_file)
            
#             # Read the file
#             audio_bytes = uploaded_file.read()
            
#             # Transcribe the audio
#             transcribed_text = transcribe_audio(audio_bytes)
            
#             if transcribed_text:
#                 st.write(f"Transcribed text: {transcribed_text}")
#                 st.session_state.messages.append({"role": "user", "content": transcribed_text})
#                 response = generate_insurance_assistant_response(transcribed_text, client, fine_tuning_data, fitness_discount_data)
#                 st.session_state.messages.append({"role": "assistant", "content": response})
#                 st.session_state.file_processed = True
#             else:
#                 st.error("Failed to transcribe audio. Please try again with a different file.")
#         except Exception as e:
#             st.error(f"Error processing audio file: {str(e)}")
#     else:
#         st.session_state.file_processed = False

#     if st.button("New audio"):
#         st.session_state.file_processed = False
    
#     # Use webrtc to record audio
#     webrtc_ctx = webrtc_streamer(
#         key="speech-to-text",
#         mode=WebRtcMode.SENDONLY,
#         client_settings=ClientSettings(
#             media_stream_constraints={
#                 "audio": True,
#                 "video": False
#             }
#         ),
#         sendback_audio=False,
#         audio_receiver_size=1024,
#     )

#     if webrtc_ctx.audio_receiver:
#         audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
#         if audio_frames:
#             audio_data = b"".join([af.to_ndarray().tobytes() for af in audio_frames])
#             transcribed_text = transcribe_audio(audio_data)
#             if transcribed_text:
#                 st.session_state.messages.append({"role": "user", "content": transcribed_text})
#                 response = generate_insurance_assistant_response(transcribed_text, client, fine_tuning_data, fitness_discount_data)
#                 st.session_state.messages.append({"role": "assistant", "content": response})
#                 st.experimental_rerun()
#             else:
#                 st.error("Failed to transcribe audio. Please try again.")

#     if send_button and user_input:
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         response = generate_insurance_assistant_response(user_input, client, fine_tuning_data, fitness_discount_data)
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.experimental_rerun()

# # Run the app
# if __name__ == "__main__":
#     ai_assistant_page()

# import streamlit as st
# import pandas as pd
# import os
# import io
# from huggingface_hub import InferenceClient
# from dotenv import load_dotenv
# import speech_recognition as sr
# from gtts import gTTS
# import tempfile
# from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
# import av
# from pydub import AudioSegment

# # Load environment variables from .env file
# load_dotenv()

# # Function to load fine-tuning data and bot_score.csv
# def load_data():
#     fine_tuning_file_path = 'tune_data.txt'
#     csv_file_path = 'bot_score.csv'

#     fine_tuning_data = ""
#     fitness_discount_data = {}
#     names_data = {}

#     if os.path.exists(fine_tuning_file_path):
#         with open(fine_tuning_file_path, 'r') as file:
#             fine_tuning_data = file.read()

#     if os.path.exists(csv_file_path):
#         df = pd.read_csv(csv_file_path)
#         for index, row in df.iterrows():
#             name = row['Name'].strip().lower()
#             fitness_score = row['Fitness Score']
#             discount = row['Discount']
#             names_data[name] = (fitness_score, discount)
#             fitness_discount_data[fitness_score] = discount

#     return fine_tuning_data, fitness_discount_data, names_data

# # Function to clear chat history
# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# # Function to predict discount based on fitness score
# def predict_discount(fitness_score):
#     if fitness_score >= 90:
#         return 30  # 30% discount
#     elif fitness_score >= 80:
#         return 25  # 25% discount
#     elif fitness_score >= 70:
#         return 20  # 20% discount
#     elif fitness_score >= 60:
#         return 15  # 15% discount
#     elif fitness_score >= 50:
#         return 10  # 10% discount
#     elif fitness_score >= 40:
#         return 5   # 5% discount
#     else:
#         return 0   # No discount

# # Function to generate AI assistant response
# def generate_insurance_assistant_response(prompt_input, client, fine_tuning_data, fitness_discount_data, names_data):
#     system_message = "You are a consultant with expertise in personal finance and insurance. Provide crisp and short responses."

#     if fine_tuning_data:
#         system_message += f"\n\nFine-tuning data:\n{fine_tuning_data}"

#     if "fitness score" in prompt_input.lower() or "discount" in prompt_input.lower():
#         return "Please provide your name."

#     try:
#         user_fitness_score = float(prompt_input)
#         discount = predict_discount(user_fitness_score)
#         return f"Your fitness score is {user_fitness_score}. Based on this, you get {discount}% discount."
#     except ValueError:
#         name = prompt_input.strip().lower()
#         if name in names_data:
#             fitness_score, discount = names_data[name]
#             return f"Hello {prompt_input}, your fitness score is {fitness_score}. Based on this, you get {discount}% discount."
#         else:
#             if "what is" in prompt_input.lower() or "how" in prompt_input.lower():
#                 messages = [
#                     {"role": "system", "content": system_message},
#                     {"role": "user", "content": prompt_input}
#                 ]
#                 response = ""
#                 for message in client.chat_completion(
#                         messages=messages,
#                         max_tokens=120,
#                         stream=True
#                 ):
#                     response += message.choices[0].delta.content or ""
#                 return response
#             return "Name not found in our records. Please provide your fitness score."

# # Function to transcribe audio
# def transcribe_audio(audio_data):
#     try:
#         r = sr.Recognizer()
        
#         # Convert audio to WAV
#         if isinstance(audio_data, bytes):
#             audio = AudioSegment.from_file(io.BytesIO(audio_data))
#         else:
#             audio = AudioSegment.from_file(audio_data)
        
#         wav_data = io.BytesIO()
#         audio.export(wav_data, format="wav")
#         wav_data.seek(0)
        
#         with sr.AudioFile(wav_data) as source:
#             audio_data = r.record(source)
        
#         text = r.recognize_google(audio_data)
#         return text
#     except Exception as e:
#         st.error(f"Error transcribing audio: {str(e)}")
#         return None

# # Function to convert text to speech
# def text_to_speech(text):
#     tts = gTTS(text=text, lang='en')
#     audio_bytes = io.BytesIO()
#     tts.write_to_fp(audio_bytes)
#     audio_bytes.seek(0)
#     return audio_bytes.getvalue()

# # Define the AI Assistant page
# def ai_assistant_page():
#     st.title('AI Assistant')
#     st.write("Your personal insurance and finance expert")

#     if "file_processed" not in st.session_state:
#         st.session_state.file_processed = False
    
#     # Custom CSS for chat containers and buttons
#     st.markdown("""
#     <style>
#     .user-container {
#         background-color: #2b5c8a;
#         border-radius: 10px;
#         padding: 10px;
#         margin: 10px 0;
#     }
#     .assistant-container {
#         background-color: #1e3d5a;
#         border-radius: 10px;
#         padding: 10px;
#         margin: 10px 0;
#     }
#     .chat-text {
#         color: #ffffff;
#     }
#     .stButton > button {
#         width: 100%;
#         height: 40px;
#         background-color: #4CAF50;
#         color: white;
#         border: none;
#         border-radius: 5px;
#         font-size: 16px;
#         cursor: pointer;
#     }
#     .stButton > button:hover {
#         background-color: #45a049;
#     }
#     .button-container {
#         display: flex;
#         justify-content: space-between;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # Load data and configurations
#     fine_tuning_data, fitness_discount_data, names_data = load_data()

#     # Define sidebar for AI Assistant configurations
#     with st.sidebar:
#         st.title('🏛️🔍 AI-Assistant Settings')
#         hf_api_token = "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"
#         if hf_api_token:
#             st.success('API key loaded from environment variable!', icon='✅')
#         else:
#             st.error('API key not found. Please set the HUGGINGFACE_API_TOKEN environment variable.', icon='🚨')

#         # Initialize the InferenceClient
#         client = InferenceClient(
#             "mistralai/Mixtral-8x7B-Instruct-v0.1",
#             token=hf_api_token
#         )

#         st.button('Clear Chat History', on_click=clear_chat_history)

#     # Initialize session state for messages
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

#     # Display chat history
#     chat_container = st.container()
#     with chat_container:
#         for i, message in enumerate(st.session_state.messages):
#             container_class = "user-container" if message['role'] == "user" else "assistant-container"
#             col1, col2 = st.columns([0.9, 0.1])
#             with col1:
#                 st.markdown(f"""
#                 <div class="{container_class}">
#                     <p class="chat-text"><strong>{'You' if message['role'] == 'user' else 'Assistant'}:</strong> {message['content']}</p>
#                 </div>
#                 """, unsafe_allow_html=True)
#             with col2:
#                 audio_button_label = f"Play Audio {i}"
#                 if st.button("Play", key=audio_button_label):
#                     audio_bytes = text_to_speech(message['content'])
#                     st.audio(audio_bytes, format="audio/mp3")

#     # Handle user input and generate responses
#     user_input = st.text_input("Type your message here:", key="user_input")
#     col1, col2 = st.columns([0.5, 0.5])
#     with col1:
#         send_button = st.button("Send")
#     with col2:
#         speak_button = st.button("Speak")

#     uploaded_file = st.file_uploader("Facing issues recording? Upload an audio file instead:", type=['wav', 'mp3', 'ogg', 'm4a', 'flac'])

#     if uploaded_file is not None and not st.session_state.file_processed:
#         try:
#             # Display audio player
#             st.audio(uploaded_file)
            
#             # Read the file
#             audio_bytes = uploaded_file.read()
            
#             # Transcribe the audio
#             transcribed_text = transcribe_audio(audio_bytes)
            
#             if transcribed_text:
#                 st.write(f"Transcribed text: {transcribed_text}")
#                 st.session_state.messages.append({"role": "user", "content": transcribed_text})
#                 response = generate_insurance_assistant_response(transcribed_text, client, fine_tuning_data, fitness_discount_data, names_data)
#                 st.session_state.messages.append({"role": "assistant", "content": response})
#                 st.session_state.file_processed = True
#             else:
#                 st.error("Failed to transcribe audio. Please try again with a different file.")
#         except Exception as e:
#             st.error(f"Error processing audio file: {str(e)}")
#     else:
#         st.session_state.file_processed = False

#     if st.button("New audio"):
#         st.session_state.file_processed = False
    
#     # Use webrtc to record audio
#     webrtc_ctx = webrtc_streamer(
#         key="speech-to-text",
#         mode=WebRtcMode.SENDONLY,
#         client_settings=ClientSettings(
#             media_stream_constraints={
#                 "audio": True,
#                 "video": False
#             }
#         ),
#         sendback_audio=False,
#         audio_receiver_size=1024,
#     )

#     if webrtc_ctx.audio_receiver:
#         audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
#         if audio_frames:
#             audio_data = b"".join([af.to_ndarray().tobytes() for af in audio_frames])
#             transcribed_text = transcribe_audio(audio_data)
#             if transcribed_text:
#                 st.session_state.messages.append({"role": "user", "content": transcribed_text})
#                 response = generate_insurance_assistant_response(transcribed_text, client, fine_tuning_data, fitness_discount_data, names_data)
#                 st.session_state.messages.append({"role": "assistant", "content": response})
#                 st.experimental_rerun()
#             else:
#                 st.error("Failed to transcribe audio. Please try again.")

#     if send_button and user_input:
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         response = generate_insurance_assistant_response(user_input, client, fine_tuning_data, fitness_discount_data, names_data)
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.experimental_rerun()

# # Run the app
# if __name__ == "__main__":
#     ai_assistant_page()
import streamlit as st
import pandas as pd
import os
import io
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import tempfile
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
from pydub import AudioSegment

# Load environment variables from .env file
load_dotenv()

# Function to load fine-tuning data and bot_score.csv
def load_data():
    fine_tuning_file_path = 'tune_data.txt'
    csv_file_path = 'bot_score.csv'

    fine_tuning_data = ""
    fitness_discount_data = {}
    names_data = {}

    if os.path.exists(fine_tuning_file_path):
        with open(fine_tuning_file_path, 'r') as file:
            fine_tuning_data = file.read()

    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        for index, row in df.iterrows():
            name = row['Name'].strip().lower()
            fitness_score = row['Fitness Score']
            discount = row['Discount']
            names_data[name] = (fitness_score, discount)
            fitness_discount_data[fitness_score] = discount

    return fine_tuning_data, fitness_discount_data, names_data

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function to predict discount based on fitness score
def predict_discount(fitness_score):
    if fitness_score >= 90:
        return 30  # 30% discount
    elif fitness_score >= 80:
        return 25  # 25% discount
    elif fitness_score >= 70:
        return 20  # 20% discount
    elif fitness_score >= 60:
        return 15  # 15% discount
    elif fitness_score >= 50:
        return 10  # 10% discount
    elif fitness_score >= 40:
        return 5   # 5% discount
    else:
        return 0   # No discount

# Function to generate AI assistant response
def generate_insurance_assistant_response(prompt_input, client, fine_tuning_data, fitness_discount_data, names_data):
    system_message = "You are a consultant with expertise in personal finance and insurance. Provide crisp and short responses."

    if fine_tuning_data:
        system_message += f"\n\nFine-tuning data:\n{fine_tuning_data}"

    # Convert input to lowercase for consistency
    prompt_input_lower = prompt_input.lower()

    # Check if the input is related to requesting a discount based on fitness score
    if "discount" in prompt_input_lower and "fitness score" in prompt_input_lower:
        # Check for numbers in the input
        words = prompt_input_lower.split()
        for word in words:
            if word.isdigit():
                user_fitness_score = float(word)
                discount = predict_discount(user_fitness_score)
                return f"Based on a fitness score of {user_fitness_score}, you would get {discount}% discount."

        return "Please provide your name to check for your fitness score and discount."

    # Handle user-provided fitness score
    try:
        user_fitness_score = float(prompt_input_lower)
        discount = predict_discount(user_fitness_score)
        return f"Your fitness score is {user_fitness_score}. Based on this, you get {discount}% discount."
    except ValueError:
        pass

    # Check if input is a name
    name = prompt_input_lower.strip()
    if name in names_data:
        fitness_score, discount = names_data[name]
        return f"Hello {prompt_input}, your fitness score is {fitness_score}. Based on this, you get {discount}% discount."

    # Handle general questions using the AI model
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt_input}
    ]

    response = ""
    for message in client.chat_completion(
            messages=messages,
            max_tokens=120,
            stream=True
    ):
        response += message.choices[0].delta.content or ""

    if not response:
        response = "I'm not sure how to answer that. Could you please rephrase or ask another question?"

    return response



# Function to transcribe audio
def transcribe_audio(audio_data):
    try:
        r = sr.Recognizer()
        
        # Convert audio to WAV
        if isinstance(audio_data, bytes):
            audio = AudioSegment.from_file(io.BytesIO(audio_data))
        else:
            audio = AudioSegment.from_file(audio_data)
        
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")
        wav_data.seek(0)
        
        with sr.AudioFile(wav_data) as source:
            audio_data = r.record(source)
        
        text = r.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.getvalue()

# Define the AI Assistant page
def ai_assistant_page():
    st.title('AI Assistant')
    st.write("Your personal insurance and finance expert")

    if "file_processed" not in st.session_state:
        st.session_state.file_processed = False
    
    # Custom CSS for chat containers and buttons
    st.markdown("""
    <style>
    .user-container {
        background-color: #2b5c8a;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .assistant-container {
        background-color: #1e3d5a;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .chat-text {
        color: #ffffff;
    }
    .stButton > button {
        width: 100%;
        height: 40px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .button-container {
        display: flex;
        justify-content: space-between;
    }
    </style>
    """, unsafe_allow_html=True)

    # Load data and configurations
    fine_tuning_data, fitness_discount_data, names_data = load_data()

    # Define sidebar for AI Assistant configurations
    with st.sidebar:
        st.title('🏛️🔍 AI-Assistant Settings')
        hf_api_token = "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"
        if hf_api_token:
            st.success('API key loaded from environment variable!', icon='✅')
        else:
            st.error('API key not found. Please set the HUGGINGFACE_API_TOKEN environment variable.', icon='🚨')

        # Initialize the InferenceClient
        client = InferenceClient(
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            token=hf_api_token
        )

        st.button('Clear Chat History', on_click=clear_chat_history)

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            container_class = "user-container" if message['role'] == "user" else "assistant-container"
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f"""
                <div class="{container_class}">
                    <p class="chat-text"><strong>{'You' if message['role'] == 'user' else 'Assistant'}:</strong> {message['content']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                audio_button_label = f"Play Audio {i}"
                if st.button("Play", key=audio_button_label):
                    audio_bytes = text_to_speech(message['content'])
                    st.audio(audio_bytes, format="audio/mp3")

    # Handle user input and generate responses
    user_input = st.text_input("Type your message here:", key="user_input")
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        send_button = st.button("Send")
    with col2:
        speak_button = st.button("Speak")

    uploaded_file = st.file_uploader("Facing issues recording? Upload an audio file instead:", type=['wav', 'mp3', 'ogg', 'm4a', 'flac'])

    if uploaded_file is not None and not st.session_state.file_processed:
        try:
            audio_bytes = uploaded_file.read()
            transcribed_text = transcribe_audio(audio_bytes)
            if transcribed_text:
                st.write(f"Transcribed text: {transcribed_text}")
                st.session_state.messages.append({"role": "user", "content": transcribed_text})
                response = generate_insurance_assistant_response(transcribed_text, client, fine_tuning_data, fitness_discount_data, names_data)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.file_processed = True
            else:
                st.error("Failed to transcribe audio. Please try again with a different file.")
        except Exception as e:
            st.error(f"Error processing audio file: {str(e)}")
    else:
        st.session_state.file_processed = False

    if st.button("New audio"):
        st.session_state.file_processed = False
    
    # Use webrtc to record audio
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        client_settings=ClientSettings(
            media_stream_constraints={
                "audio": True,
                "video": False
            }
        ),
        sendback_audio=False,
        audio_receiver_size=1024,
    )

    if webrtc_ctx.audio_receiver:
        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        if audio_frames:
            audio_data = b"".join([af.to_ndarray().tobytes() for af in audio_frames])
            transcribed_text = transcribe_audio(audio_data)
            if transcribed_text:
                st.session_state.messages.append({"role": "user", "content": transcribed_text})
                response = generate_insurance_assistant_response(transcribed_text, client, fine_tuning_data, fitness_discount_data, names_data)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.experimental_rerun()
            else:
                st.error("Failed to transcribe audio. Please try again.")

    if send_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = generate_insurance_assistant_response(user_input, client, fine_tuning_data, fitness_discount_data, names_data)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    ai_assistant_page()