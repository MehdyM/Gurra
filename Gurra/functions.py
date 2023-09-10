import os 
from binance.client import Client 
from classes import Coin
from global_variables import purchase_coin, client, balance, sell_coin
from binance.helpers import round_step_size
from datetime import datetime, date
import sqlite3

#connect to binance
def connect_to_binance():
    global client
    api_secret = ''
    api_key = ''
    client = Client(api_key, api_secret)


#get current not sold in db
def get_current_coins():
    global sell_coin
    statement = "SELECT symbol, stop_loss, new_stop_loss, qty, purchase_price, static_win_price FROM purchases WHERE is_sold = 0"
    os.chdir('../Gurra')
    dir = os.getcwd()
    try:
            con = sqlite3.connect(dir + "\\tradingbot.db")
            cur = con.cursor()
            res = cur.execute(statement)
            con.commit()
            my_list = res.fetchall()
            purchase_price = get_current_purchase_price(my_list[0][0])
            sell_coin = Coin(my_list[0][0], purchase_price)
            get_stepsize_and_minqty_sell()
            sell_coin.stop_loss = float(my_list[0][1])
            sell_coin.sell_price = float(my_list[0][2])
            get_sell_quantity()
            sell_coin.purchase_price = float(my_list[0][4])
            sell_coin.static_win_price = float(my_list[0][5])
            check_if_sell()
    except Exception as e:
            print(e)
            return

#get sell quantity
def get_sell_quantity():
    global client 
    global sell_coin
    coin = sell_coin.symbol.replace('USDT','')
    balance = client.get_asset_balance(asset=coin)
    sell_coin.qty = float(balance['free'])


# get current purchase price
def get_current_purchase_price(symbol):
    list_of_coins = get_current_tickers()
    for coin in list_of_coins:
        if symbol == coin.symbol:
            return coin.current_price

# check if the coin should be sold
def check_if_sell():
    global sell_coin 
    if sell_coin.current_price < sell_coin.stop_loss \
        or sell_coin.current_price < sell_coin.sell_price: \
        #or sell_coin.current_price > sell_coin.static_win_price:
        dump_coin()
    else:
        if sell_coin.current_price > sell_coin.purchase_price:
            diff= sell_coin.current_price / sell_coin.purchase_price 
            updated_percentage = 0.97 * (diff + 0.005)
            print("procenten just nu: " + str(updated_percentage))
            if updated_percentage > 1:
                updated_percentage = 1
            sell_coin.sell_price = updated_percentage * sell_coin.current_price
        else:
            sell_coin.sell_price = sell_coin.current_price * 0.97
        print("not worth selling...")
        update_new_stop_loss()
        update_log()
            
#update coin with new stop loss price
def update_new_stop_loss():
    global sell_coin
    if sell_coin.current_price > sell_coin.purchase_price:
        statement = "UPDATE purchases SET new_stop_loss = " + str(sell_coin.sell_price) + ", last_price_check = "+ str(sell_coin.current_price) +", static_win_price = " + str(sell_coin.static_win_price) + "  WHERE is_sold = 0"
        os.chdir('../Gurra')
        dir = os.getcwd()
        try:
                con = sqlite3.connect(dir + "\\tradingbot.db")
                cur = con.cursor()
                cur.execute(statement)
                con.commit()
                print("purchases table updated!")
        except Exception as e:
                print(e)

#update the log
def update_log():
    global sell_coin
    statement = "INSERT INTO log(timestamp, symbol, purchase_price, stop_loss, new_stop_loss, last_price_check)\
        VALUES(datetime('now'), '"+ sell_coin.symbol +"', "+ str(sell_coin.purchase_price) +", \
        "+ str(sell_coin.stop_loss) +", "+ str(sell_coin.sell_price) +", "+ str(sell_coin.current_price) +")"
    os.chdir('../Gurra')
    dir = os.getcwd()
    try:
        con = sqlite3.connect(dir + "\\tradingbot.db")
        cur = con.cursor()
        cur.execute(statement)
        con.commit()
        print("log updated!")
        print_latest_log()
    except Exception as e:
        print(e)

#print last updated log
def print_latest_log():
    statement = "SELECT * FROM log WHERE rowid = (SELECT MAX(rowid) FROM log);"
    os.chdir('../Gurra')
    dir = os.getcwd()    
    try:
            con = sqlite3.connect(dir + "\\tradingbot.db")
            cur = con.cursor()
            res = cur.execute(statement)
            con.commit()
            my_list = res.fetchall()
            for row in my_list:
                    print(row)
    except Exception as e:
            print(e)


# make sale
def dump_coin():
    global sell_coin
    global client  
    order_qty = round_step_size(sell_coin.qty, sell_coin.step_size)
    order_qty = "{:0.0{}f}".format(order_qty, sell_coin.precision)
    try:
        client.order_market_sell(
        symbol=sell_coin.symbol,
        quantity=order_qty)
        print("coin sold! updating db")
        statement = "UPDATE purchases SET is_sold = 1, sell_price = "+ str(sell_coin.current_price) +" WHERE is_sold = 0"
        os.chdir('../Gurra')
        dir = os.getcwd()    
        try:
            con = sqlite3.connect(dir + "\\tradingbot.db")
            cur = con.cursor()
            cur.execute(statement)
            con.commit()
            print("db updated successfully")
        except Exception as e:
            print(e)    
        
    except Exception as e:
        print(e)


#get balance in USDT and check if you can purchase
def check_purchase_power():
    global balance
    balance = float(client.get_asset_balance(asset='USDT')['free'])
    if balance > 20:
        return True
    
#get current alts 
def get_current_tickers():
    prices = client.get_all_tickers()
    list_of_currencies = []
    for price in prices:
        if 'USDT' in price['symbol']   \
            and 'XMR' not in price['symbol'] \
            and ('USDC' or 'UST' or 'TUSD') not in price['symbol'] :
            my_coin = Coin(price['symbol'],float(price['price']))
            list_of_currencies.append(my_coin)
    return list_of_currencies

#get stepsize and min quantity
def get_stepsize_and_minqty():
    global purchase_coin
    info = client.get_symbol_info(purchase_coin.symbol)
    purchase_coin.precision = int(info['quoteAssetPrecision'])
    for coin_params in info['filters']:
        if coin_params['filterType'] == 'LOT_SIZE':
            purchase_coin.min_qty = coin_params['minQty']
            purchase_coin.step_size = coin_params['stepSize']


#get stepsize and min quantity sell_coin
def get_stepsize_and_minqty_sell():
    global sell_coin
    info = client.get_symbol_info(sell_coin.symbol)
    sell_coin.precision = int(info['quoteAssetPrecision'])
    for coin_params in info['filters']:
        if coin_params['filterType'] == 'LOT_SIZE':
            sell_coin.min_qty = coin_params['minQty']
            sell_coin.step_size = coin_params['stepSize']


#make purchase 
def make_purchase():
    get_stepsize_and_minqty()
    global purchase_coin
    global client
    global balance
    qty = (balance * 0.99) / purchase_coin.current_price
    order_qty = round_step_size(qty, purchase_coin.step_size)
    order_qty = "{:0.0{}f}".format(order_qty, purchase_coin.precision)
    try:
        client.order_market_buy(
        symbol=purchase_coin.symbol,
        quantity=order_qty)
        purchase_coin.qty = order_qty
        purchase_coin.stop_loss = purchase_coin.current_price * 0.97
        purchase_coin.sell_price = purchase_coin.current_price * 0.97
        purchase_coin.purchase_price = purchase_coin.current_price
        purchase_coin.static_win_price = purchase_coin.current_price * 1.03
        print("Bought coin " + purchase_coin.symbol + "with qty: " + str(order_qty))
        update_purchase_to_database()
    except Exception as e:
        print(e)

#sql after purchase
def update_purchase_to_database():
    global purchase_coin 
    global client
    coin = purchase_coin.symbol.replace('USDT','')
    balance = client.get_asset_balance(asset=coin)
    statement = "INSERT INTO \
    purchases(timestamp, symbol, purchase_price, qty, stop_loss, \
    last_price_check, new_stop_loss, is_sold, static_win_price) \
    VALUES(datetime('now'),'"+ str(purchase_coin.symbol) +"', '" + str(purchase_coin.purchase_price) + "' , \
    '" + str(balance['free']) + "', '"+ str(purchase_coin.stop_loss) +"', \
    '" + str(purchase_coin.current_price) + "', '" + str(purchase_coin.sell_price) + "', FALSE, " + str(purchase_coin.static_win_price) + ")"
    os.chdir('../Gurra')
    dir = os.getcwd()    
    try:
        con = sqlite3.connect(dir + "\\tradingbot.db")
        cur = con.cursor()
        cur.execute(statement)
        con.commit()
    except Exception as e:
        print(e)

#purchase logics
def purchase_logics():
    global purchase_coin
    list_of_currencies = get_current_tickers()
    today = date.today()
    
    for symbol in list_of_currencies:
        klines = client.get_klines(symbol=symbol.symbol,interval=Client.KLINE_INTERVAL_15MINUTE)
        klines.reverse()
        var = str(klines[0][0])
        var = var[0:10]
        timestamp = datetime.fromtimestamp(int(var))
        if today.strftime('%Y-%m-%d') == timestamp.strftime('%Y-%m-%d'):
            total_average_trades_loop = 30
            loop_count = 0
            average_trades_last_10 = 0
            average_trades_last_30 = 0
            volume_usd = 0
            while total_average_trades_loop >= 0:
                if loop_count <= 10:
                    average_trades_last_10 = average_trades_last_10 + klines[loop_count][8]
                    volume_usd = volume_usd + float(klines[0][5])
                average_trades_last_30 = average_trades_last_30 + klines[loop_count][8] 
                loop_count += 1
                total_average_trades_loop -= 1
            

            average_trades_last_10 = average_trades_last_10 / 10
            average_trades_last_30 = average_trades_last_30 / 30  
            results = average_trades_last_10 / average_trades_last_30
            volume_usd = volume_usd * symbol.current_price
            
            if results > 1.1 and volume_usd > 500000 and volume_usd < 5000000:
                print(symbol.symbol, average_trades_last_10, average_trades_last_30, volume_usd)
                purchase_coin = symbol
                make_purchase()
                break

#get account balance
def update_account_balance():
    delete_balance()
    global client
    info = client.get_account()
    balance_coins = []
    for coin in info['balances']:
            if float(coin['free']) > 0:
                    balance_coins.append(coin)

    final_balance = []
    prices = client.get_all_tickers()
    for price in prices:
     for coin in balance_coins:
        if coin['asset'] + 'USDT' == price['symbol']:
            money = float(coin['free']) * float(price['price'])
            qty = float(coin['free'])
            coin_object = {'asset':coin['asset'], 'qty':qty ,'price':money}
            if money > 1:
             final_balance.append(coin_object)

    for coin in balance_coins:
            if coin['asset'] == 'USDT':
             money = float(coin['free'])
             coin_object = {'asset':coin['asset'],'qty':money ,'price':money}
             final_balance.append(coin_object)
    
    for balance in final_balance:
        update_balance(balance)

def update_balance(balance):
    update_statement = "INSERT INTO account_balance(timestamp, asset, qty, price) \
    VALUES(datetime('now'),'" + str(balance['asset']) + "', " + str(balance['qty']) + " , " + str(balance['price']) + ")"
    os.chdir('../Gurra')
    dir = os.getcwd()    
    try:
        con = sqlite3.connect(dir + "\\tradingbot.db")
        cur = con.cursor()
        cur.execute(update_statement)
        con.commit()
    except Exception as e:
        print(e)
        

def delete_balance():
    delete_statement = "DELETE from account_balance"
    os.chdir('../Gurra')
    dir = os.getcwd()    
    try:
        con = sqlite3.connect(dir + "\\tradingbot.db")
        cur = con.cursor()
        cur.execute(delete_statement)
        con.commit()
    except Exception as e:
        print(e)

'''    
kline data

1499040000000,       Open time
    "0.01634790",        Open
    "0.80000000",        High
    "0.01575800",        Low
    "0.01577100",        Close
    "148976.11427815",   Volume
    1499644799999,       Close time
    "2434.19055334",     Quote asset volume
    308,                 Number of trades
    "1756.87402397",     Taker buy base asset volume
    "28.46694368",       Taker buy quote asset volume
    "17928899.62484339"  Ignore


purchase logics 
'''
