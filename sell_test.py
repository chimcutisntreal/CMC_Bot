import requests, web3, time, threading
from pynput import keyboard
token_to_buy = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'
moralis_price_url = f'https://deep-index.moralis.io/api/v2/erc20/{token_to_buy}/price?chain=bsc'
moralis_headers = {
    'X-API-Key': 'iAIsu5OZv8iDWJnd8nH5cjoT23Cnyvp5acS6JFmRqLFTOLXSbJt8gt5lskruicfm'
}

def mornitoring_price():
    while True:
        try:
            response = requests.request("GET", moralis_price_url, headers=moralis_headers)
            result = response.json()
            price_bnb = web3.Web3.fromWei(int(result['nativePrice']['value']), 'ether')
            price_usdt = result['usdPrice']
            print(f"BNB: {price_bnb} | USDT: {price_usdt}")
        except Exception as error:
            print(error)
        time.sleep(4)


def on_press(key):
    global running  # inform function to assign (`=`) to external/global `running` instead of creating local `running`

    if key == keyboard.Key.f9:
        running = True
        # create thread with function `loading`
        t = threading.Thread(target=mornitoring_price)
        # start thread
        t.start()

    if key == keyboard.Key.f10:
        # to stop loop in thread
        print('Thread was stopped')
        running = False

    if key == keyboard.Key.f11:
        # stop listener
        return False


# --- main ---

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()