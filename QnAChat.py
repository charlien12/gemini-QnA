from pydantic_settings import BaseSettings
import streamlit as st
import google.generativeai as genai

class Settings(BaseSettings):
    gemini_api_key: str
    class Config:
        env_file = ".env"

settings = Settings()

genai.configure(api_key=settings.gemini_api_key)
model=genai.GenerativeModel("models/gemini-2.5-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=model.generate_content(question)
    return response

#Initialize streamlit app

st.set_page_config(page_title="Gemini Copilot")
st.header("Gemini LLM App")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]
    
input=st.text_input("Input: ",key="Input")
submit=st.button("Ask Any Prompt")

if submit and input:
    response=get_gemini_response(input)
    st.session_state['chat_history'].append(("You",input))
    for chunk in response:
        st.session_state['chat_history'].append(("Bot",chunk.text))
    st.subheader("The Chat History is")
    for role,text in st.session_state['chat_history']:
        st.write(f"{role}:{text}")