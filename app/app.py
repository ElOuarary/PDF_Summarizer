import io
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
columns = st.columns(
    2,
    gap='large'
    )

with columns[0]:
    st.header('Upload File')
    uploaded_file = st.file_uploader(
        label='Upload file',
        type=['pdf', 'txt', 'docs', 'doc']
    )
    if uploaded_file:
        st.write(f'{uploaded_file.name} ({uploaded_file.size} bytes)')

with columns[1]:
    st.header('Processing Options')
    model = st.selectbox('Model Selection', ['bert', 'google'])
    auto_process = st.checkbox('Auto-process on upload', value=True)
    show_summary = st.checkbox('Show summary preview', value=True)
    if st.button("Process File", disabled=not uploaded_file):
        pass
    

st.title('Result')    
if uploaded_file:
    #summarizer = Summarizer()
    st.title('Content')
    content = io.StringIO(uploaded_file.getvalue().decode('utf-8'))
    st.write(content)
    st.title('Summary')
        
    #summary = summarizer(content.getvalue())[0]['summary_text']
    #st.write(summary)