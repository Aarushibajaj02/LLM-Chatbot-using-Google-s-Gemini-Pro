import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
load_dotenv()

st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  #favicon emoji
    layout="centered",
)
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('models/gemini-2.5-pro')

def translate_role_for_streamlit(user_role):
    if user_role=="model":
        return "assistant"
    else:
        return user_role

#initialize chat sesh in streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session=model.start_chat(history=[])

#disp chatbot title
st.title("🚀AskGemini🚀")

#chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

#ip for users' msg
user_prompt = st.chat_input("What’s on your mind? Ask away!")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    # send user's que to gemini pro and get response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    # display response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
