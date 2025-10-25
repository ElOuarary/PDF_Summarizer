import io
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from llm.summarizer import Summarizer
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

if 'notion token' not in st.session_state:
    st.session_state.notion_token = None

if 'notion_database_id' not in st.session_state:
    st.session_state.notion_database_id = None

app = st.session_state

# Configuration for the notion Integration
with st.sidebar:
    st.header('Configuration')
    st.session_state.notion_token = st.text_input('Configure your notion token')
    st.session_state.notion_database_id = st.text_input('Configure your Notion Database ID')
    
    if st.button('Connect to your Notion Workspace'):
        pass

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

summary = None
if uploaded_file:
    if auto_process:
        summary = process_file(uploaded_file, model)
    elif process:
        summary = process_file(uploaded_file, model)
    if show_summary and summary is not None:
        st.title('Summary Preview')
        st.write(summary)
        
if uploaded_file and summary:
    push_to_workspace = st.button('Push the summary to your notion workspace')
    if push_to_workspace:
        pass