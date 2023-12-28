import streamlit as st
from langchain.llms import OpenAI

st.set_page_config(
    page_title='langchain_study ',
    page_icon='🏝️',
)
st.title('🦜🔗 Langchain App')
st.subheader('study')

st.chat_message("ai").write(
    """
    Hello, World!
    """
)