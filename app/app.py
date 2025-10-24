import io
from src.llm.summarizer import Summarizer
import streamlit as st
from transformers import pipeline


st.set_page_config(
    page_title='las9',
    layout='wide',
    initial_sidebar_state='auto'
)

if 'app' not in st.session_state:
    st.session_state.app = None
    
app = st.session_state

# Configuration for the notion Integration and model selection
with st.sidebar:
    st.header('Configuration')
    st.text_input('Configure your notion token')
    st.text_input('Configure your Notion Database ID')
    st.selectbox('Model', ['bert', 'google'])

columns = st.columns(
    2,
    gap='large'
    )

with columns[0]:
    st.header('Upload File')
    uploaded_file = st.file_uploader(
        label='Upload files',
        type=['pdf', 'txt', 'docs', 'doc']
    )
    if uploaded_file:
        st.write(f'{uploaded_file.name} ({uploaded_file.size} bytes)')

with columns[1]:
    st.header('Processing Options')
    auto_process = st.checkbox('Auto-process on upload', value=True)
    show_summary = st.checkbox('Show summary preview', value=True)
    if st.button("Process All Files", disabled=not uploaded_file):
        pass
    

st.title('Result')    
if uploaded_file:
    summarizer = Summarizer()
    st.title('Content')
    content = io.StringIO(uploaded_file.getvalue().decode('utf-8'))
    st.write(content)
    st.title('Summary')
        
    summary = summarizer(content.getvalue())[0]['summary_text']
    st.write(summary)