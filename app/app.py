import io
import pymupdf
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

def extract_file_text(file_bytes):
    pages = []
    with pymupdf.open(io.BytesIO(file_bytes)) as f:
        for page in f.pages:
            pages.append(page)
            print(page)

columns = st.columns(
    2,
    gap='large'
    )

with columns[0]:
    st.header('Upload File')
    uploaded_files = st.file_uploader(
        label='Upload files',
        type=['pdf', 'txt', 'docs', 'doc'],
        accept_multiple_files=True,
    )
    if uploaded_files:
        pass
        st.write(f'Uploaded {len(uploaded_files)} {'file' if len(uploaded_files) == 1 else 'files'}')
        for file in uploaded_files:
            st.write(f'{file.name} ({file.size} bytes)')

with columns[1]:
    st.header('Processing Options')
    auto_process = st.checkbox('Auto-process on upload', value=True)
    show_summary = st.checkbox('Show summary preview', value=True)
    if st.button("Process All Files", disabled=not uploaded_files):
        pass
    

st.title('Result')    
if uploaded_files:
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    for file in uploaded_files:
        st.title('Content')
        content = io.StringIO(file.getvalue().decode('utf-8'))
        st.write(content)
        st.title('Summary')
        
        summary = summarizer(content.getvalue())[0]['summary_text']
        st.write(summary)