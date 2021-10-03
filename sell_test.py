import requests, time, threading, json
from pynput import keyboard
from web3 import Web3

main_address = '0x4C8247025222B218b02E1ac4779EFEa19c48860C'
token_to_buy = '0x0cca95fd87441dcd90fddb4e34526c1b3cc6f660'
moralis_price_url = f'https://deep-index.moralis.io/api/v2/erc20/{token_to_buy}/price?chain=bsc'
moralis_balance_url = f'https://deep-index.moralis.io/api/v2/{main_address}/erc20?chain=bsc'
moralis_headers = {
    'X-API-Key': 'iAIsu5OZv8iDWJnd8nH5cjoT23Cnyvp5acS6JFmRqLFTOLXSbJt8gt5lskruicfm'
}

test_data = [1.06,1.2,1.3,1.1,1.5,1.6,1,1.8,1.9,2.2,2.1,2.5,2.4,2.0,1.6,1.7,1.9,1.1,0.5,1.6]


# def mornitoring_price_test():
#     target = 2
#     trailing_stop_loss = 30
#     stop_loss = 10
#     buy_price = 1.1
#     max = 0
#     sell_target = buy_price * target
#     for result in test_data:
#         print('price %f'%result)
#         if result >= sell_target or max >= sell_target:
#             if result >= max:
#                 max = result
#                 print('max = %f' %max)
#                 print('-----------')
#             elif result <= max - max * (trailing_stop_loss / 100):
#                 print('Sold at %f'% result)
#                 break
#             else:
#                 pass
#         elif result <= buy_price - buy_price * (stop_loss / 100):
#             print('Stop lost at %f'% result)
#             break
#         time.sleep(0.5)
#
# mornitoring_price_test()

def mornitoring_price():
    target = 2
    trailing_stop_loss = 20
    stop_loss = 5
    buy_price = 0
    max = 0
    sell_target = buy_price * target
    while True:
        try:
            price_response = requests.request("GET", moralis_price_url, headers=moralis_headers)
            balance_response = requests.request("GET", moralis_balance_url, headers=moralis_headers)
            price = price_response.json()
            price = int(price['nativePrice']['value'])
            balances = balance_response.json()
            for i in balances:
                if i['token_address'] == token_to_buy:
                    balance = int(i.get('balance', 0))
                    result = Web3.fromWei(balance, 'ether') * Web3.fromWei(price, 'ether')
                    if result >= sell_target or max >= sell_target:
                        if result >= max:
                            max = result
                        elif result <= max - max*(trailing_stop_loss/100):
                            pass #sell
                        else:
                            pass
                    elif result <= buy_price - buy_price*(stop_loss/100):
                        pass #sell
                    break
        except Exception as error:
            print(error)
        time.sleep(5)

def on_press(key):
    global running  # inform function to assign (`=`) to external/global `running` instead of creating local `running`

    if key == keyboard.Key.f8:
        running = True
        # create thread with function `loading`
        t = threading.Thread(target=mornitoring_price)
        # start thread
        t.start()

    if key == keyboard.Key.f9:
        # to stop loop in thread
        print('Thread was stopped')
        running = False

    if key == keyboard.Key.f10:
        # stop listener
        return False

# --- main ---

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()