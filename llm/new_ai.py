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
import pandas as pd
import logging

from lib.db import db_info
# from llm.llmcallback import ChatCallbackHandler

db = db_info()

class new_ai:
    def __init__(self):
        #  Openai information
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        self.llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo', verbose=True, streaming=True,
                            callbacks=[
                                # ChatCallbackHandler(),
                            ],)

    # Ai가 질문을 다른 언어로 변역하는 함수
    def translate_msg(self, ask, language):
        try:
            result = []

            # ai가 실행할 행동 정의 (질문을 입력한 언어로 번역하기)
            translate = """
            Translate the incoming Question into the language below as accurate as possible.
            {language}
            
            Question: {question}
            """

            # 정의한 행동 요청 (질문을 입력한 언어로 번역 요청)
            translate_prompt = ChatPromptTemplate.from_template(translate)
            translate_response = (
                translate_prompt
                | self.llm
            )

            # 위에 정의한 행동 실행 (질문을 입력한 언어로 번역 실행)
            result = translate_response.invoke(
                {"question": ask, "language": language})
            print(f'convert to eng : ${result}')
            return result.content
        except Exception as e:
            logging.warning(e)
            return 'Error: fail to translate to '+language

    # Ai가 질문에 적절한 쿼리문 만드는 함수
    def create_query(self, ask):
        try:
            result = []

            # ai가 실행할 행동 정의 (쿼리문 작성)
            translate = """
            Based on the table schema below, write a SQL query that would answer the question:
            {schema}

            Question: {question}
            SQL Query:
            """

            # 정의한 행동 요청 (쿼리문 작성 요청)
            prompt = ChatPromptTemplate.from_template(translate)
            response = (
                RunnablePassthrough.assign(schema=db.get_table_columns)
                | prompt
                | self.llm
            )
            
            # 위에 정의한 행동 실행 (쿼리문 작성 실행)
            result = response.invoke({"question": ask})
            print(f'sql query : ${result}')
            return result.content
        except Exception as e:
            logging.warning(e)
            return 'Error: fail to create a query'

    # Ai가 DB 관련 질문에 적절한 답변 만드는 함수
    def answer_about_schema(self, ask):
        try:
            result = []

            # ai가 실행할 행동 정의 (DB 관련 답변 작성)
            translate = """
            Based on the table schema below, answer the question:
            {schema}

            Question: {question}
            """

            # 정의한 행동 요청 (DB 관련 답변 작성 요청)
            prompt = ChatPromptTemplate.from_template(translate)
            response = (
                RunnablePassthrough.assign(schema=db.get_table_columns)
                | prompt
                | self.llm
            )
            
            # 위에 정의한 행동 실행 (DB 관련 답변 작성 실행)
            result = response.invoke({"question": ask})
            print(f'answer : ${result}')
            return result.content
        except Exception as e:
            logging.warning(e)
            return 'Error: fail to answer'
