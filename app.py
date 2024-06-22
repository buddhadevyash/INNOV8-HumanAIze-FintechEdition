import streamlit as st
import replicate
import os
import pandas as pd


st.set_page_config(page_title="Your AI-Assistant")

# Define paths and configurations
with st.sidebar:
    st.title('🏛️🔍 Your AI-Assistant')
    replicate_api = 'r8_LP6L8iECuDLGHDT1HwLvNyaeDBDKW7I3Ja0Pz'
    st.success('API key already provided!', icon='✅')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)

# File paths for fine-tuning data and bot_score.csv
fine_tuning_file_path = 'D:/bot/tune_data.txt'
csv_file_path = 'D:/bot/bot_score.csv'

# Load fine-tuning data
fine_tuning_data = ""
if os.path.exists(fine_tuning_file_path):
    with open(fine_tuning_file_path, 'r') as file:
        fine_tuning_data = file.read()

# Load bot_score.csv and preprocess data for lookup
fitness_discount_data = {}
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        fitness_score = row['Fitness Score']
        discount = row['Discount']
        fitness_discount_data[fitness_score] = discount

# Initialize session state for messages
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function to generate response based on user input
def generate_insurance_assistant_response(prompt_input):
    string_dialogue = "Talking to a consultant with expertise in personal finance, insurance, and the responses must be crisp and short.\n\n"
    
    if fine_tuning_data:
        string_dialogue += "Fine-tuning data:\n" + fine_tuning_data + "\n\n"
    
    # Check if the prompt input is asking about fitness score and discount
    if "fitness score" in prompt_input.lower() or "discount" in prompt_input.lower():
        return "Please provide your fitness score to get information about the discount you qualify for."
    
    # Check if there's a valid fitness score input
    try:
        user_fitness_score = float(prompt_input)
        if user_fitness_score in fitness_discount_data:
            discount = fitness_discount_data[user_fitness_score]
            return f"Your fitness score is {user_fitness_score}. Based on this, you get {discount}% discount."
        else:
            return "I'm sorry, I couldn't find any discount information for your fitness score."
    except ValueError:
        pass  # Ignore if the prompt input is not a valid number for fitness score
    
    # If none of the above conditions match, use the original AI assistant functionality
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return ''.join(output)

# Main Streamlit app logic
if prompt := st.chat_input("You: ", disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = generate_insurance_assistant_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display all messages in the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
