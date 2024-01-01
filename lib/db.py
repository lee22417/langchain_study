import streamlit as st
import pymysql
import logging


class db_info:
    def __init__(self):
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

    # DB 쿼리 실행 함수
    def run_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    # DB 스키마 가져오는 함수
    def get_schema(self, _):
        sql = """
            SELECT 
                TABLE_NAME, TABLE_COMMENT
            FROM
                INFORMATION_SCHEMA.TABLES
            WHERE
                TABLE_SCHEMA = 'hairdb'
        """
        result = self.run_query(sql)
        return result
    
    # 테이블 정보 가져오는 함수
    def get_table_columns(self, _):
        sql = """
            SELECT 
                TABLE_NAME, COLUMN_NAME, COLUMN_COMMENT
            FROM 
                INFORMATION_SCHEMA.COLUMNS
            WHERE 
                TABLE_SCHEMA = 'hairdb'
        """
        # 크기가 커서 사용 못하는 sql문
        # This model's maximum context length is 4097 tokens. However, your messages resulted in 6032 tokens
        # sql = """
        #     SELECT 
        #         TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, COLUMN_COMMENT
        #     FROM 
        #         INFORMATION_SCHEMA.COLUMNS
        #     WHERE 
        #         TABLE_SCHEMA = 'hairdb'
        # """
        result = self.run_query(sql)
        return result