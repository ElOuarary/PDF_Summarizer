import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from llm.summarizer import Summarizer
from notion.notion_client import Client
import streamlit as st


st.set_page_config(
    page_title='las9',
    layout='wide',
    initial_sidebar_state='auto'
)

st.title('Trust Us')
st.markdown('Upload your file, summarize it push it to you notion workspace, and chat with our chatbot about it')

if 'app' not in st.session_state:
    st.session_state.app = None
    
app = st.session_state

if 'notion_token' not in app:
    st.session_state.notion_token = None
    
if 'notion_page_id' not in app:
    st.session_state.notion_page_id = None
    
if 'summary' not in app:
    st.session_state.summary = None

# Configuration for the notion Integration
with st.sidebar:
    st.header('Configuration')
    notion_token = st.text_input('Configure your notion token')
    notion_page_id = st.text_input('Configure your notion page url')
    
    if st.button('Connect to your Notion Workspace'):
        client = Client(notion_token, notion_page_id)
        if client is not None:
            st.session_state.notion_token = notion_token
            st.session_state.notion_page_id = notion_page_id
            st.write(st.session_state.notion_token)
            st.write(st.session_state.notion_page_id)
            st.write('Connection succed')
        else:
            st.write('Connection failed, try again')

# Main content area the upload file are and the configuration are for the model
columns = st.columns(2, gap='large')

with columns[0]:
    st.header('Upload File')
    uploaded_file = st.file_uploader(
        label='Upload file',
        type=['pdf', 'txt', 'docs', 'doc']
    )

with columns[1]:
    st.header('Processing Options')
    model = st.selectbox('Model Selection', ['bert', 'pegasus', 'gemini'])
    summarizer = Summarizer(model)
    auto_process = st.checkbox('Auto-process on upload', value=True)
    show_summary = st.checkbox('Show summary preview', value=True)
    process = st.button('Process file', disabled=not uploaded_file)

def process_file(uploaded_file, model):
    if model == 'gemini':
        summary = summarizer.summarize_with_gemini(uploaded_file)
    else:
        content = uploaded_file.getvalue().decode('utf-8')
        summary = summarizer.summarize_with_local_model(content)[0]['summary_text']
    return summary


if uploaded_file:
    if auto_process:
        summary = st.session_state.summary = process_file(uploaded_file, model)
    elif process:
        summary = st.session_state.summary = process_file(uploaded_file, model)
    if show_summary and st.session_state.summary is not None:
        st.title('Summary Preview')
        st.write(st.session_state.summary)
        
if uploaded_file and st.session_state.summary:
    title = st.text_input('Title of the summary:', value='Summary', max_chars=40)
    push_to_workspace = st.button('Push the summary to your notion workspace')
    if push_to_workspace:
        client = Client(st.session_state.notion_token, st.session_state.notion_page_id)
        try:
           client.create_page(title, st.session_state.summary)
           st.write('Summary pushed to your workplace in notion')
        except:
            st.error('something went wrong during creating the page')