import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI model with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini Pro model and initialize the chat instance
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get the response from the Gemini model
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error in getting response: {e}")
        return None

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Session")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input:", key="input_text")
submit = st.button("Ask the question")

if submit and input_text:
    response = get_gemini_response(input_text)
    
    if response:
        st.session_state['chat_history'].append(("You", input_text))
        
        st.subheader("The response is:")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("The chat history is:")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
