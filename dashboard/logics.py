import sqlite3
import os

def get_account_balance(): 
        statement = "SELECT * FROM account_balance"
        os.chdir('dashboard')
        dir = os.getcwd()
        print(dir)
        try:
                con = sqlite3.connect(dir + "\\tradingbot.db")
                cur = con.cursor()
                res = cur.execute(statement)
                con.commit()
                my_list = res.fetchall()
                return my_list
        except Exception as e:
                print(e)


def account_balance_for_view():
        balance = get_account_balance()
        total_balance = 0
        asset_list = []
        for asset in balance:
                coin = {
                        'symbol':asset[1],
                        'qty':asset[2],
                        'value':asset[3]
                }
                total_balance += asset[3]
                asset_list.append(coin)
        return (asset_list,total_balance)

def get_five_last_checks():
        statement = "SELECT * FROM log ORDER BY timestamp DESC LIMIT 5"
        os.chdir('dashboard')
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

def checks_for_view():
        balance = get_five_last_checks()
        check_list = []
        for asset in balance:
                check = {
                        'timestamp':asset[0],
                        'symbol':asset[1],
                        'purchase_price':asset[2],
                        'current_price':asset[5],
                        'dynamic':asset[4]
                }
                check_list.append(check)
        return check_list

def get_ten_last_sold():
        statement = "SELECT * FROM purchases WHERE is_sold = 1 ORDER BY timestamp DESC LIMIT 10"
        os.chdir('dashboard')
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

def sold_for_view():
        balance = get_ten_last_sold()
        sold_list = []
        for asset in balance:
                percentage = ((float(asset[5]) / float(asset[2])) - 1) * 100
                percentage = round(percentage,3)
                sold = {
                        'timestamp':asset[0],
                        'symbol':asset[1],
                        'purchase_price':asset[2],
                        'sold_price':asset[5],
                        'percentage':percentage
                }
                sold_list.append(sold)
        return sold_list

