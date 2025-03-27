#!/usr/bin/python3

import cx_Oracle
import key

class DatabaseManager:
    def __init__(self):
        self.user = key.return_config("user")
        self.senha = key.return_secret("adbinvest")
        self.db = key.return_config("db")
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = cx_Oracle.connect(f"{self.user}/{self.senha}@{self.db}")
        self.cursor = self.conn.cursor()
        self.cursor.execute("alter session set nls_date_format='mm/dd/yyyy hh24:mi:ss'")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def get_current_time(self):
        self.cursor.execute("select sysdate from dual")
        return self.cursor.fetchall()[0][0] 