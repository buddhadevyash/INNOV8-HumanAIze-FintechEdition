import streamlit as st
import pandas as pd
import os
import replicate
import logging
import json

# Load environment variables from .env file


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to load fine-tuning data and bot_score.csv
def load_data():
    fine_tuning_data = ""
    fitness_discount_data = {}
    
    # Add dummy data for testing
    fitness_discount_data = {50: 5, 60: 10, 70: 15, 80: 20, 90: 25, 100: 30}
    
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
def generate_insurance_assistant_response(prompt_input, model, temperature, max_length, fine_tuning_data, fitness_discount_data):
    string_dialogue = "You are an AI assistant specializing in insurance and finance. Provide concise and helpful responses.\n\n"

    if "fitness score" in prompt_input.lower() or "discount" in prompt_input.lower():
        return "Please provide your fitness score to get information about the discount you qualify for."

    try:
        user_fitness_score = float(prompt_input)
        discount = predict_discount(user_fitness_score)
        return f"Your fitness score is {user_fitness_score}. Based on this, you get {discount}% discount."
    except ValueError:
        pass

    try:
        logger.info(f"Attempting to run Replicate model with parameters: model={model}, temperature={temperature}, max_tokens={max_length}")
        
        api_token = os.environ.get('REPLICATE_API_TOKEN', '')
        logger.info(f"API Token (first 5 chars): {api_token[:5]}...")
        
        output = replicate.run(
            model,
            input={
                "prompt": f"{string_dialogue}Human: {prompt_input}\nAI:",
                "temperature": temperature,
                "max_new_tokens": max_length,
                "repetition_penalty": 1
            }
        )
        
        response = ''.join(output)
        logger.info(f"Replicate API call successful. Output: {response}")
        return response
    except replicate.exceptions.ReplicateError as e:
        logger.error(f"Replicate API error: {str(e)}")
        return f"I'm sorry, but I encountered an error while processing your request. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"An unexpected error occurred. Please try again later."

# Define the AI Assistant page
def ai_assistant_page():
    st.title('AI Assistant')
    st.write("Your personal insurance and finance expert")

    # Custom CSS for chat containers
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
    </style>
    """, unsafe_allow_html=True)

    # Load data and configurations
    fine_tuning_data, fitness_discount_data = load_data()

    # Define sidebar for AI Assistant configurations
    with st.sidebar:
        st.title('🏛️🔍 AI-Assistant Settings')
        replicate_api = os.environ.get('REPLICATE_API_TOKEN')
        if replicate_api:
            st.success(f'API key loaded from environment variable! (First 5 chars: {replicate_api[:5]}...)', icon='✅')
            logger.info(f"API Token loaded (first 5 chars): {replicate_api[:5]}...")
        else:
            st.error('API key not found. Please set the REPLICATE_API_TOKEN environment variable.', icon='🚨')
            logger.error("API Token not found in environment variables")
            st.stop()

        st.subheader('Model and parameters')
        model = "replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781"
        temperature = st.slider('Temperature', min_value=0.01, max_value=2.0, value=0.75, step=0.01)
        max_length = st.slider('Max Length', min_value=32, max_value=512, value=256, step=8)

        st.button('Clear Chat History', on_click=clear_chat_history)

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            container_class = "user-container" if message['role'] == "user" else "assistant-container"
            st.markdown(f"""
            <div class="{container_class}">
                <p class="chat-text"><strong>{'You' if message['role'] == 'user' else 'Assistant'}:</strong> {message['content']}</p>
            </div>
            """, unsafe_allow_html=True)

    # Handle user input and generate responses
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Type your message here:", key="user_input")
        submit_button = st.form_submit_button("Send")

    if submit_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            response = generate_insurance_assistant_response(user_input, model, temperature, max_length, fine_tuning_data, fitness_discount_data)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            logger.error(f"Error in generate_insurance_assistant_response: {str(e)}")
            st.error(f"An error occurred: {str(e)}")
        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    ai_assistant_page()