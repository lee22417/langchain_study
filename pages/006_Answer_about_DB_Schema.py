import streamlit as st
from langchain.memory import StreamlitChatMessageHistory
from llm.new_ai import new_ai

history = StreamlitChatMessageHistory(key="chat_messages")
ai = new_ai()

msg_session_name = "msg_006"

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
        # 영어 질문에 맞는 쿼리문 생성
        data = ai.answer_about_schema(msg)
        print(data)
        history.add_ai_message(data)
        send_msg(data, "ai")
