from django.test import TestCase
import os 
import sqlite3


def get_five_last_checks():
        statement = "SELECT * FROM log ORDER BY timestamp DESC LIMIT 5"
        os.chdir('Gurra')
        dir = os.getcwd()
        try:
                con = sqlite3.connect(dir + "\\tradingbot.db")
                cur = con.cursor()
                res = cur.execute(statement)
                con.commit()
                my_list = res.fetchall()
                return my_list
        except Exception as e:
                print(e)

print(get_five_last_checks())
