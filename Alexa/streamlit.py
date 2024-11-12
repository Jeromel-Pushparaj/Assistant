import streamlit as st
import config

import google.generativeai as genai
# Replace with your Gemini API key
api_key = config.GENAI_API_KEY
genai.configure(api_key=api_key)


model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
convo = model.start_chat(history=[])

def get_gemini_response(user_input):
    convo.send_message(user_input)
    return convo.last.text


    

def main():
    st.title("You can Ask Anything here")

    user_input = st.text_input("Ask your question:")

    if user_input:
        response = get_gemini_response(user_input)
        st.write(response)

if __name__ == "__main__":
    main()