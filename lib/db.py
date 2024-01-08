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

    # DB 쿼리 실행 함수 dict
    def run_query_dict(self, query):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
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

    # 모든 테이블 정보 가져오는 함수
    def get_table_columns(self, _):
        # 토큰 용량과 타협
        sql = """
            SELECT 
                TABLE_NAME, COLUMN_NAME, LEFT(COLUMN_COMMENT, 10)
            FROM 
                INFORMATION_SCHEMA.COLUMNS
            WHERE 
                TABLE_SCHEMA = 'hairdb'
        """
        # 토큰 용량이 커서 사용 못하는 sql문
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

    # 해당 테이블들 정보 가져오는 함수
    def get_table_columns_by_table_name(self, _):
        sql = f"""
            SELECT 
                TABLE_NAME, COLUMN_NAME, COLUMN_TYPE, COLUMN_COMMENT
            FROM 
                INFORMATION_SCHEMA.COLUMNS
            WHERE 
                TABLE_SCHEMA = 'hairdb' AND TABLE_NAME IN ({self.table_names});
        """
        result = self.run_query(sql)
        return result

    # self에 table name set 함수
    def set_table_names(self, table_names):
        self.table_names = table_names