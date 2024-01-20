
import cohere
from helpers import *
import streamlit as st


# Initialize Cohere client with API key from st.secrets
conn = cohere.Client(st.secrets["cohere"]["api_key"])

st.title('Cohere LLM Streamlit App')
username = st.text_input("Who's the boss ?")
if username.lower().replace(" ", "") != st.secrets["user_credential"]["username"]:
    st.warning('You guessed wrong!')
    st.stop()

prompt = st.text_input('Enter your text here:')
model_options = ['command-nightly']
model = st.selectbox('Select Model', options = model_options, index = 0)
max_tokens = st.slider('Max Tokens to be generated', min_value = 10, max_value = 100, value = 55)
if st.button('Generate Text'):
    response = generate(conn, prompt, model, max_tokens)
    st.text_area('Generated Text:', value=response.generations[0].text, height=200)

# conversation = [
#         {"role": "USER", "message": "Who is current CEO of Openai"},
#         {"role": "CHATBOT", "message": "There has been a lot of turmoil surrounding the leadership of OpenAI in recent months. Former CEO, Sam Altman, was briefly ousted in November 2023, with the board appointing Chief Technology Officer, Mira Murati, as interim CEO. However, just days later, a deal was struck and Altman returned as CEO of the company. There has been speculation about Altman's dealings with the board, with claims that he had been dishonest in his communication with them, and a desire from Altman to install an entirely new slate of directors."}
#     ]

# query = "What happened in openai in lastweek, explain clearly"
# response = conversation_query(conn, conversation, query)

# print(response.text)