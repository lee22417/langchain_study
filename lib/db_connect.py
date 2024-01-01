import pymysql
import pandas as pd
from langchain.chat_models import ChatOpenAI


class db_connect:
    def __init__(self, host, port, user, pw, db):
        try:
            self.connection = pymysql.connect(
                host=host,
                port=int(port),
                user=user,
                password=pw,
                database=db
            )
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        except:
            print('error connect')

    def get_connect(self):
        try:
            return self.connection.open
        except:
            return False
