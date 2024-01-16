from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings, OpenAIEmbeddings
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOpenAI

import streamlit as st

from llm.ai_rag import ai_file

ai = ai_file()


st.set_page_config(
    page_title="RAG Test Page",
)
st.title("DocumentGPT")

msg_session_name = "msg_008"


def send_msg(msg, role, save=True):
    with st.chat_message(role):
        st.write(msg)
    if save:
        st.session_state[msg_session_name].append({"msg": msg, "role": role})


@st.cache_resource(show_spinner="Embedding file...")
def paint_history():
    for msg in st.session_state[msg_session_name]:
        send_msg(msg["msg"], msg["role"], False)


st.markdown(
    """
Welcome!
            
Use this chatbot to ask questions to an AI about your files!

Upload your files on the sidebar.
"""
)

with st.sidebar:
    file = st.file_uploader(
        "Upload a .txt .pdf or .docx file",
        type=["pdf", "txt", "docx"],
    )

if file:
    send_msg("I'm ready! Ask away!", "ai", False)
    paint_history()
    ai.upload_file(file)
    message = st.chat_input("Ask anything about your file...")
    if message:
        send_msg(message, "human")
        with st.chat_message("ai"):
            answer = ai.answer(file, message)
            st.write(answer)
            # send_msg(answer, 'ai', False)
else:
    st.session_state[msg_session_name] = []
