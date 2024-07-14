import streamlit as st
import openai
from openai import OpenAI
from PIL import Image

st.set_page_config(
    page_title="GynaeGenius",
    page_icon="👩‍⚕️",
    layout="centered"
)

st.markdown("""
    <style>
        body {
            color: #333;
            background-color: #f0f0f0;
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


logo = Image.open("assets/gynae_genius_logo.png") 
st.image(logo, width=160)


st.markdown("<h1 class='logo-text'>Gynae Genius Bot</h1>", unsafe_allow_html=True)
# st.markdown("<p class='subheader'>Mama and Baby Care</p>", unsafe_allow_html=True)

st.write(
    "This is a simple chatbot to generate responses based on your symptoms. Please feel free to ask questions. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)


openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    try:
        # Set the OpenAI API key
        openai.api_key = openai_api_key

        # Create a session state variable to store the chat messages
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm GynaeGenius, your AI assistant for maternal and infant health. How can I help you today?"})

        # Display the existing chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Type your question here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate a response using the OpenAI API
            with st.spinner("Generating response..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                )
                reply = response.choices[0].message["content"]

            # Display the response
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        # Reset chat button
        if st.button("Reset Chat"):
            st.session_state.messages = []
            st.experimental_rerun()

    except openai.NotFoundError:
        st.error("The provided OpenAI API key is invalid. Please check and try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: Whoops! It seems like your OpenAI API Key is not valid, Please check and try again.")

# Footer
st.markdown("---")
st.markdown("*Disclaimer: This AI assistant is for informational purposes only and should not replace professional medical advice.*")
