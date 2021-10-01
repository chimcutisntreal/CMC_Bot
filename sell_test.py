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

# abi = json.loads(
#         '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"tokens","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeSub","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"tokens","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeDiv","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeMul","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"tokenOwner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"a","type":"uint256"},{"name":"b","type":"uint256"}],"name":"safeAdd","outputs":[{"name":"c","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"tokenOwner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"tokens","type":"uint256"}],"name":"Approval","type":"event"}]')
# bsc_node = 'https://bsc-dataseed.binance.org'
# web3 = Web3(Web3.HTTPProvider(bsc_node))

# token_contract = web3.eth.contract(address=token_to_buy, abi=abi)

def mornitoring_price():
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
                    print(result)
                    break
        except Exception as error:
            print(error)
        time.sleep(3)


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