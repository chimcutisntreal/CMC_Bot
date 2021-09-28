
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
            print(style.BLUE + msg)
            index_percentage = msg.find('%')
            index_address = msg.find('0x')
            is_first_pump = msg.find('first pump')
            if index_percentage >= 0 and index_address >= 0 and is_first_pump >= 0:
                percentage = int(msg[index_percentage-2:index_percentage].strip())
                if percentage <= 11:
                    token_to_buy = msg[index_address:index_address + 42]
                    print('Token to buy: ' + token_to_buy)
                    execute().buy(web3, token_to_buy)
                else:
                    print('Buy/Sell Taxes are too high')

        client.start()
        client.run_until_disconnected()

