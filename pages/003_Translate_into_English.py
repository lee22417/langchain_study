import streamlit as st
from langchain.memory import StreamlitChatMessageHistory
from llm.ai_v1 import ai_v1

history = StreamlitChatMessageHistory(key="chat_messages")
ai = ai_v1()

msg_session_name = "msg_003"

def send_msg(msg, role, save=True):
    with st.chat_message(role):
        st.write(msg)
    # 저장
    if save:
        st.session_state[msg_session_name].append({"msg": msg, "role": role})


if msg_session_name not in st.session_state:
    st.session_state[msg_session_name] = []

for msg in st.session_state[msg_session_name]:
    send_msg(msg["msg"], msg['role'], False)

msg = st.chat_input('Enter the message.')

if msg:
    send_msg(msg, "human")
    # 캐쉬작업 추가
    history.add_user_message(msg)
    with st.spinner("Waiting for the response..."):
        # ai에 묻기
        data = ai.translate_msg(msg, "English")
        history.add_ai_message(data)
        send_msg(data, "ai")
