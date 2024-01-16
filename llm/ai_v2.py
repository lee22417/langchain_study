import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import logging

from lib.db import db_info
# from llm.llmcallback import ChatCallbackHandler

db = db_info()

# 토큰 용량 제한으로, 모든 테이블의 컬럼 정보를 못 보냄
# 먼저 관련 테이블들을 선택하고 해당 테이블의 컬럼 정보만 보내서 sql 생성
# This model's maximum context length is 4097 tokens. However, your messages resulted in 6032 tokens


class ai_v2:
    def __init__(self):
        #  Openai information
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        self.llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo', verbose=True, streaming=True,
                              callbacks=[
                                  # ChatCallbackHandler(),
                              ],)

    # Ai가 질문에 적절한 테이블을 선택하는 함수
    def select_table(self, ask):
        try:
            # ai가 실행할 행동 정의 (테이블을 선택)
            translate = """
            Based on the table schema below, choose the tables that would be used to answer the question:
            {schema}

            Question: {question}
            Tables:
            """

            # 정의한 행동 요청 (테이블을 선택)
            prompt = ChatPromptTemplate.from_template(translate)
            response = (
                RunnablePassthrough.assign(schema=db.get_schema)
                | prompt
                | self.llm
            )

            # 위에 정의한 행동 실행 (테이블을 선택 실행)
            result = response.invoke({"question": ask})
            print(f'table names : ${result}')
            return result.content
        except Exception as e:
            logging.warning(e)
            return 'Error: fail to select tables'

    # Ai가 질문에 입력된 테이블들로 적절한 쿼리문 만드는 함수
    def create_query_w_selected_table_name(self, ask):
        try:
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
                RunnablePassthrough.assign(
                    schema=db.get_table_columns_by_table_name)
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

    # Ai가 질문에 적절한 쿼리문 만드는 함수
    def create_query(self, ask):
        try:
            # 질문과 관련된 DB 테이블 이름 가져오기
            table_names = self.select_table(ask)
            table_names_str = self.format_tuple_to_string(table_names)
            # DB 테이블 이름을 db.self에 저장
            db.set_table_names(table_names_str)
            # 위의 DB 테이블 정보로 쿼리 생성
            result = self.create_query_w_selected_table_name(ask)
            return result
        except Exception as e:
            logging.warning(e)
            return 'Error: fail to create a query'

    # format from tuple to string 
    def format_tuple_to_string(self, tuple_input):
        input_arr = str(tuple_input).split(',')
        result = """"""
        for i in range(len(input_arr)):
            element_fixed = input_arr[i].replace("(", "").replace("'", "").replace(")", "").replace(' ','')
            if element_fixed != '':
                if i != 0:
                    result += ","
                result += f"'{element_fixed}'"
        return result;