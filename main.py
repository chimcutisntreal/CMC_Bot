
from telethon import TelegramClient, events, sync
import asyncio
from web3 import Web3
import datetime, threading
import json, os, time, requests

if __name__ == '__main__':

    web3, client = connection().create_connection()
    if not web3 or not client:
        exit()

    print('1. Buy immediately')
    print('2. Waiting for CMC Listing')
    option = int(input('Choose option: '))

    if option == 1:
        amount = float(input('Amount: '))
        token_to_buy = str(input('Address:'))
        execute().buy(web3, token_to_buy, amount)

    if option == 2:
        @client.on(events.NewMessage(chats='CMC_fastest_alerts'))
        async def get_message(event):
            msg = event.raw_text
            index_percentage = msg.find('%')
            index_address = msg.find('0x')
            is_first_pump = msg.find('first pump')
            index_liquidity = msg.find('BNB')
            if not index_liquidity:
                index_liquidity = msg.find('BUSD')

            if index_percentage >= 0 and index_address >= 0 and is_first_pump >= 0:
                percentage = int(msg[index_percentage-2:index_percentage].strip())
                liquidity = float(msg[index_liquidity-8:index_liquidity].strip())
                print(style.BLUE + currentTimeStamp + ' Received Token info ')
                if percentage <= 8 and (50 <= liquidity <= 300 or 18000 <= liquidity <= 120000):
                    token_to_buy = msg[index_address:index_address + 42]
                    print(currentTimeStamp + 'Token to buy: ' + token_to_buy)
                    execute().buy(web3, token_to_buy)
                else:
                    print('Buy/Sell Taxes are too high or Liquidity is lower than 50 BNB')

        client.start()
        client.run_until_disconnected()

