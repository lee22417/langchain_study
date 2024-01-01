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
        st.session_state["msg_004"].append({"msg": msg, "role": role})


if "msg_004" not in st.session_state:
    st.session_state["msg_004"] = []

for msg in st.session_state["msg_004"]:
    send_msg(msg["msg"], msg['role'], False)

msg = st.chat_input('Enter the message.')

if msg:
    send_msg(msg, "human")
    # 캐쉬작업 추가
    history.add_user_message(msg)
    with st.spinner("Waiting for the response..."):
        # 질문 영어로 번역
        msg_eng = ai.translate_msg(msg, 'English')
        if (msg_eng == 'Error to translate to English'):  # 번역에서 에러가 생겼을 경우 끝
            send_msg(msg_eng, "ai")
        else:  # 영어로 변역된 질문에 맞는 쿼리문 생성
            data = ai.create_query(msg_eng)
            print(data)
            history.add_ai_message(data)
            send_msg(data, "ai")
