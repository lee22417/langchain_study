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


# from llm.llmcallback import ChatCallbackHandler


class new_ai:
    def __init__(self):
        #  Openai information
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        self.llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo', verbose=True, streaming=True,
                            callbacks=[
                                # ChatCallbackHandler(),
                            ],)
        # DB information
        HOST = st.secrets["host"]
        PORT = st.secrets["port"]
        USER = st.secrets["user"]
        PASSWORD = st.secrets["password"]
        DATABASE = st.secrets["database"]
        self.connection = pymysql.connect(
            host=HOST,
            port=int(PORT),
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

    # DB 스키마 가져오는 함수
    def get_schema(self, _):
        sql = """
            SELECT 
                table_name, table_comment
            FROM
                information_schema.tables
            WHERE
                table_schema = 'hairdb'
            """
        schema = self.run_query(sql)
        return schema

    # DB 쿼리 실행 함수
    def run_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

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
                RunnablePassthrough.assign(schema=self.get_schema)
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
