import streamlit as st
from langchain.memory import StreamlitChatMessageHistory
from llm.new_ai import new_ai

history = StreamlitChatMessageHistory(key="chat_messages")
ai = new_ai()

def send_msg(msg, role, save=True):
    with st.chat_message(role):
        st.write(msg)
    # 저장
    if save:
        st.session_state["msg"].append({"msg": msg, "role": role})


if "msg" not in st.session_state:
    st.session_state["msg"] = []

for msg in st.session_state["msg"]:
    send_msg(msg["msg"], msg['role'], False)

msg = st.chat_input('대화를 입력하세요')

if msg:
    send_msg(msg, "human")
    # 캐쉬작업 추가
    history.add_user_message(msg)
    with st.spinner("물어보는중"):
        # ai에 묻기
        data = ai.translate_msg(msg)
        history.add_ai_message(data)
        send_msg(data, "ai")
