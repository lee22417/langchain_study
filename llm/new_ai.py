import streamlit as st
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import create_sql_query_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts.chat import HumanMessagePromptTemplate
import pymysql
import pandas as pd
import logging
import re


# from llm.llmcallback import ChatCallbackHandler


class new_ai:
    def __init__(self):
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        # HOST = st.secrets["host"]
        # PORT = st.secrets["port"]
        # USER = st.secrets["user"]
        # PASSWORD = st.secrets["password"]
        # DATABASE = st.secrets["database"]
        # self.connection = pymysql.connect(
        #     host=HOST,
        #     port=int(PORT),
        #     user=USER,
        #     password=PASSWORD,
        #     database=DATABASE
        # )
        self.llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo', verbose=True, streaming=True,
            callbacks=[
                # ChatCallbackHandler(),
        ],)
    
    def translate_msg(self, ask):
        try:
            result = []
            
            # ai가 실행할 행동 정의 (영어번역하기)
            translate = """
            Translate the incoming Question into English as accurate as possible.
            Question: {question}
            """
            
            # ai가 실행할 행동 정의 (3개의 다른 버전의 영어로 번역해서 가장 정확한거 선택)
            # translate = """
            # Translate the incoming question into English in three different versions as accurate as possible 
            # and pick the only one translated English sentence that is the most accurate.
            # Question: {question}
            # """
            
            # 정의한 행동 요청 (영어번역 행동 요청)
            translate_prompt = ChatPromptTemplate.from_template(translate)
            translate_response = (
                translate_prompt
                | self.llm
            )
            
            # 위에 정의한 행동 실행 (영어번역 실행)
            result = translate_response.invoke({"question": ask})
            print(f'convert to eng : ${result}')
            return result.content
        except Exception as e:
            logging.warning(e)
            return ['Error to translate to English']
