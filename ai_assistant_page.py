import streamlit as st
import pandas as pd
import os
import io
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import tempfile

# Load environment variables from .env file
load_dotenv()

# Function to load fine-tuning data and bot_score.csv
def load_data():
    fine_tuning_file_path = 'D:/bot/tune_data.txt'
    csv_file_path = 'D:/bot/bot_score.csv'

    fine_tuning_data = ""
    fitness_discount_data = {}

    if os.path.exists(fine_tuning_file_path):
        with open(fine_tuning_file_path, 'r') as file:
            fine_tuning_data = file.read()

    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        for index, row in df.iterrows():
            fitness_score = row['Fitness Score']
            discount = row['Discount']
            fitness_discount_data[fitness_score] = discount

    return fine_tuning_data, fitness_discount_data

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
def generate_insurance_assistant_response(prompt_input, client, fine_tuning_data, fitness_discount_data):
    system_message = "You are a consultant with expertise in personal finance and insurance. Provide crisp and short responses."

    if fine_tuning_data:
        system_message += f"\n\nFine-tuning data:\n{fine_tuning_data}"

    if "fitness score" in prompt_input.lower() or "discount" in prompt_input.lower():
        return "Please provide your fitness score to get information about the discount you qualify for."

    try:
        user_fitness_score = float(prompt_input)
        discount = predict_discount(user_fitness_score)
        return f"Your fitness score is {user_fitness_score}. Based on this, you get {discount}% discount."
    except ValueError:
        pass

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

    return response

# Function to transcribe audio
def transcribe_audio(audio_file_path):
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Error transcribing audio: {e}")
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
    fine_tuning_data, fitness_discount_data = load_data()

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
        upload_button = st.file_uploader("Upload audio file:", type=["wav"])

    if upload_button:
        st.write("Processing uploaded audio...")
        audio_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with open(audio_file_path, "wb") as f:
            f.write(upload_button.getvalue())

        transcribed_text = transcribe_audio(audio_file_path)
        if transcribed_text:
            st.session_state.messages.append({"role": "user", "content": transcribed_text})
            response = generate_insurance_assistant_response(transcribed_text, client, fine_tuning_data, fitness_discount_data)
            st.session_state.messages.append({"role": "assistant", "content": response})
            os.unlink(audio_file_path)  # Delete the temporary audio file
            st.experimental_rerun()
        else:
            st.error("Failed to transcribe audio. Please try again.")

    if send_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = generate_insurance_assistant_response(user_input, client, fine_tuning_data, fitness_discount_data)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    ai_assistant_page()
