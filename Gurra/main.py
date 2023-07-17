import functions
from global_variables import client
from time import sleep 

while(True):
    client = ""
    # 1. connect to binance & update account balance
    functions.connect_to_binance()
    functions.update_account_balance()

    # 2. check if there is something to sell and if it is worth it
    if functions.get_current_coins():
        print("sold coins sleeping for 30 seconds")
        sleep(30)

    # 3. check purchase power 
    if functions.check_purchase_power():

        # 4. purchase logics
        functions.purchase_logics()
    else:
        print('not buying at this time...')
    
    del client
    sleep(10)