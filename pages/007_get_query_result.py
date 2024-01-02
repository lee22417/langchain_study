import streamlit as st
from langchain.memory import StreamlitChatMessageHistory
import pandas as pd
from lib.db import db_info
from llm.new_ai import new_ai

history = StreamlitChatMessageHistory(key="chat_messages")
ai = new_ai()
db = db_info()

msg_session_name = "msg_007"

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
        query = ai.create_query(msg)
        # 쿼리문 실행
        data = db.run_query(query)
        data = pd.DataFrame(data)
        print(data)
        # 출력
        data_arr = []
        data_arr.append(data)
        history.add_ai_message(data_arr)
        for i in range(len(data_arr)):
            print(data_arr[i])
            send_msg(data_arr[i],"ai")
