import streamlit_app as st
from langflow.load import run_flow_from_json
from PIL import Image
import json

import logging
import http.client as http_client

http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, as by default it will not do anything
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

TWEAKS = {
  "ChatInput-HeWl6": {},
  "AstraVectorStoreComponent-FIN66": {},
  "ParseData-gNi04": {},
  "Prompt-Hy4kp": {},
  "ChatOutput-z24kV": {},
  "SplitText-dAwQi": {},
  "File-scEPA": {},
  "AstraVectorStoreComponent-RsC1t": {},
  "URL-qhZZi": {},
  "CohereEmbeddings-BUsbP": {},
  "CohereEmbeddings-QMoaR": {},
  "CohereModel-MlqY4": {}
}
st.set_page_config(
    page_title="GynaeGenius",
    page_icon="assets/gynae_genius.png",
    layout="centered"
)

st.markdown("""
    <style>
        body {
            color: #333;
            background-color: #F0F0F0;
        }
        .stButton>button {
            padding: 0.5rem 1rem;
            font-size: 1rem;
            background-color: #FF66C4;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #e55ab0;
        }
        .stInfo {
            background-color: #e8f0fe;
            border-left: 4px solid #0CB8B6;
            padding: 0.5rem;
            margin: 1rem 0;
        }
        .stMarkdown {
            font-size: 1rem;
            line-height: 1.5;
        }
        .logo {
        display: block; 
            margin: 0 auto;  
            }
        .logo-text {
            font-size: 2.5rem;
            color: #FF66C4;
            margin-bottom: 0;
        }
        .subheader {
            color: #0CB8B6;
            font-size: 1.2rem;
            margin-top: 0;
        }
    </style>
""", unsafe_allow_html=True)
# Title and display
logo = Image.open("assets/gynae_genius.png") 
st.image(logo, width=160)

st.markdown("<h1 class='logo-text'>Meet your GynaeGenius</h1>", unsafe_allow_html=True)

st.write(
    "This is a GynaeGenius bot to generate responses based on your symptoms. Please feel free to ask questions. "
    "To use this app, you need to provide a key provided to you."
)

# Start with empty messages, stores in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm GynaeGenius, your AI assistant for maternal and infant health queries. How can I help you today?"})

# Display the existing chat messages
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

# Chat input
if question := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "human", "content": question})
    
    # Draw user question
    with st.chat_message("human"):
        st.markdown(question)

    # Extract the message text from the output
    with st.spinner("Generating response..."):
        output = run_flow_from_json(flow="RAG.json",
                            input_value=question,
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)
        result_data = output[0].outputs[0].results['message']

        if result_data and hasattr(result_data, 'data'):
            response_data = result_data.data
            answer = response_data.get('text', "Please contact a professional doctor for further assistance.")
        else:
            answer = "Please contact a professional doctor for further assistance."
        
        # Store the bot's answer in a session object for redrawing next time
        st.session_state.messages.append({"role": "assistant", "content": answer})

    # Draw the bot's answer
    with st.chat_message('assistant'):
        st.markdown(answer)
