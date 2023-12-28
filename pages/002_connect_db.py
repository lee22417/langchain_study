import streamlit as st

from llm.db_connect import db_connect

if "step" not in st.session_state:
    st.session_state["step"] = 0
step = st.session_state["step"]

if step == 0:
    """
    Insert your database url only mysql, mariadb 
    ex) {mysql+pymysql://user:password@ip:port/dbname}
    """
    ip = st.text_input('IP ex: 127.0.0.1')
    port = st.text_input('PORT ex: 3306')
    user = st.text_input('USER ex: user')
    pw = st.text_input('PASSWORD ex: 1234567')
    db = st.text_input('PORT ex: yout database name')

    bt = st.button('Connect Database', type="primary")
    if bt:
        if ip == '':
            'input your ip'
        elif port == '':
            'input your port'
        elif user == '':
            'input your user'
        elif pw == '':
            'input your pw'
        elif db == '':
            'input your db'
        else:
            cai = db_connect(ip, port, user, pw, db)
            status = cai.get_connect()
            if status:
                status
                st.session_state["ip"] = ip
                st.session_state["port"] = port
                st.session_state["user"] = user
                st.session_state["pw"] = pw
                st.session_state["db"] = db
                st.session_state["step"] = 1
            else:
                st.header('check your databse info')

if step == 1:
    ip = st.session_state["ip"]
    port = st.session_state["port"]
    user = st.session_state["user"]
    pw = st.session_state["pw"]
    db = st.session_state["db"]
    ai = db_connect(ip, port, user, pw, db)
    status = ai.get_connect()
    st.title(status)
