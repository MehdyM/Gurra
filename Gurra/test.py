import functions
from global_variables import client
import sqlite3
import os 



def get_account_balance(): 
        statement = "DELETE FROM purchases"
        os.chdir('../Gurra')
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

print(get_account_balance())

'''
functions.connect_to_binance()
functions.update_account_balance()
statement = "SELECT stop_loss, new_stop_loss, purchase_price, last_price_check from purchases where is_sold = 0"
try:
        con = sqlite3.connect("tradingbot.db")
        cur = con.cursor()
        res = cur.execute(statement)
        con.commit()
        my_list = res.fetchall()
        print(my_list)
except Exception as e:
        print(e)

price = 100
current_price = 100
percentage = 0.97
stop_loss = price * percentage 
updated_stop_loss = current_price * percentage

for i in range(0,10):
  current_price += 1
  diff = current_price / price
  updated_percentage = percentage * (diff + 0.005)
  print(updated_percentage, diff)

balance object = asset & price

cur.execute("CREATE TABLE purchases(timestamp, symbol, purchase_price, qty, stop_loss, last_price_check, new_stop_loss, is_sold)")
purchases

purchases table
# timestamp
# symbol
# purchase_price 
# qty
# stop_loss
# last_price_check
# new_stop_loss
# is_sold
# id
# sell_price

log table
# timestamp
# symbol
# purchase_price 
# stop_loss
# new_stop_loss
# last_price_check

account balance
#timestamp
#asset
#qty
#price


api_secret = 'Y3hJF7Jh0uimNmVwZAQ2yEyrAEpyLFm9zREKYNkZn3AxMPRQad6E4aMpE6kFFpBK'
api_key = 'NYKfJjNQDHPIk8QG49kVEsflG2NEOH6jDpOry3ETjDsYWK9bz1Tjo969EgnnGe7G'
client = Client(api_key, api_secret)

info = client.get_symbol_info('XMRUSDT')
avg_price = client.get_avg_price(symbol='XMRUSDT')
print(info)
print(avg_price)
'''