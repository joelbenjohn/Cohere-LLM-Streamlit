
import cohere
from helpers import *
import streamlit as st
import time
import threading


@st.cache_data
def youtube_api_object():
    return youtube_service(st.secrets["google"]["api_key"])

@st.cache_data
def search_youtube_cache(_youtube, query):
    return search_youtube(youtube, query)

@st.cache_data
def summarize_cache(_conn, video_id):
    return summarize(conn, video_id)

@st.cache_data
def fetch_youtube_transcript_cache(video_id):
    return fetch_youtube_transcript(video_id)

@st.cache_data
def load_cache_variables(video_id):
    st.session_state.summary_cache = {'-1':''}
    st.session_state.transcript_cache = {'-1':''}
    st.session_state.time_select = ['-1']

# @st.cache_data
def create_word(video_details):
    return create_word_document(video_details, st.session_state.summary_cache)

def new_run():
    st.session_state.summarized = False

def youtube_summarize(_conn, transcript_df):
    

    # Process and display summaries in real-time
    # summaries_display = ""
    
    # time_selector = st.select_slider('Time, options = ')
    
    for summary in process_transcript_for_summaries(conn, transcript_df, batch_size=50):
        time_start = summary['start']
        st.session_state.time_select.append(time_start)
        st.session_state.summary_cache[time_start] = f"- {summary['summary']}"
        st.session_state.transcript_cache[time_start] = f"- {summary['original']}"
        st.session_state.last_time = time_start
        run_time = summary['run_time']
        if run_time<7.0:
            time.sleep(7.0-run_time)
        yield time_start


# Initialize Cohere client with API key from st.secrets
conn = cohere.Client(st.secrets["cohere"]["api_key"])

st.title('Cohere LLM Streamlit App')
st.write('This app is an attempt/experiment to understand cohere LLM functionalities')
st.markdown('''
          #### Generic Apps
         - Q&A : using Cohere 'generate' endpoint
         - ChatBot : using Cohere 'chat' endpoint (RAG enabled)''')
st.markdown('''
          #### Unique Apps
          ##### Youtube Video Summarizer : 
         - Cohere 'summarize' endpoint to summarize transcripts texts
         - Youtube Data API to search for youtube videos in app by user
         - Youtube Transcipt API to get transcripts of video selected by user''')
st.markdown(
         '''
         **Note**: This app utilizes personal api-keys which are **not production api-keys**
         The username to be entered below at Who's the boss? is provided only to those that the boss shared the app link to..
         ''')
# st.markdown(body)

# username = st.text_input("Who's the boss ?")
# if username.lower().replace(" ", "") not in st.secrets["user_credential"]["username"] and username!="":
#     st.warning('You guessed wrong!')
#     st.stop()

select_app = st.selectbox('Select Application', options = ['Youtube Summarizer', 'Q&A', 'Minutes', 'Chat'])
if select_app == 'Youtube Summarizer':
    if 'summarized' not in st.session_state:
        st.session_state.summarized = False
    query = st.text_input('Search for Youtube Video')
    youtube = youtube_api_object()
    results = search_youtube_cache(youtube, query)
    if results:
        video_options = {video['snippet']['title']: video['id']['videoId'] for video in results}
        video_title= st.selectbox('Select a video:', options=list(video_options.keys()), on_change = new_run)
        video_id = video_options[video_title]
        load_cache_variables(video_id)
        time_placeholder = st.empty()
        columns = st.columns([1, 1])
        # Placeholder for displaying summaries
        
        transcript_placeholder = columns[0].empty()
        summary_placeholder = columns[1].empty()
        # Display selected video and fetch transcript
        if st.button('Summarize'):
            
            transcript_df = fetch_youtube_transcript_cache(video_id)
            # output = summarize_cache(conn, video_id)
            if not isinstance(transcript_df, str):

                for time_start in youtube_summarize(conn, transcript_df):
                    time_generated = time_placeholder.select_slider('Summarized Time (in secs)', options = st.session_state.time_select, value = st.session_state.time_select[-1], disabled=True)
                    summary_placeholder.write(st.session_state.summary_cache[time_generated])
                    transcript_placeholder.write(st.session_state.transcript_cache[time_generated])
                st.session_state.summarized = True
            else:
                st.warning(transcript_df)

        if st.session_state.summarized:
            time_selected = time_placeholder.select_slider('Choose Time (in secs)', options = st.session_state.time_select, value = st.session_state.time_select[-1])
            summary_placeholder.write(st.session_state.summary_cache[time_selected])
            transcript_placeholder.write(st.session_state.transcript_cache[time_selected])    
             # Create the Word document
            doc_file = create_word({'video_title' : video_title,
                                    'video_id': video_id})

            # Create a download button and offer the file for download .read()
            st.download_button(
                label="Download Summary",
                data=doc_file,
                file_name=f"{video_title}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.error("No results found.")
        
    
    # video_link = st.text_input('Enter Youtube Video Link')

elif select_app == 'Q&A':
    prompt = st.text_input('Enter your text here:')
    model_options = ['command-nightly']
    model = st.selectbox('Select Model',
                        options = model_options,
                        index = 0)
    max_tokens = st.slider('Max Tokens to be generated',
                        min_value = 10,
                        max_value = 100,
                        value = 55)

    if st.button('Generate Text'):

        response = generate(conn, prompt, model, max_tokens)
        
        st.text_area('Generated Text:', value = response.generations[0].text, height = 200)


# conversation = [
#         {"role": "USER", "message": "Who is current CEO of Openai"},
#         {"role": "CHATBOT", "message": "There has been a lot of turmoil surrounding the leadership of OpenAI in recent months. Former CEO, Sam Altman, was briefly ousted in November 2023, with the board appointing Chief Technology Officer, Mira Murati, as interim CEO. However, just days later, a deal was struck and Altman returned as CEO of the company. There has been speculation about Altman's dealings with the board, with claims that he had been dishonest in his communication with them, and a desire from Altman to install an entirely new slate of directors."}
#     ]

# query = "What happened in openai in lastweek, explain clearly"
# response = conversation_query(conn, conversation, query)

# print(response.text)