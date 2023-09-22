import os
import sys
import asyncio
from itertools import cycle

from pyrogram import Client
from pyrogram.errors import UsernameInvalid, InviteHashExpired, FloodWait, AuthKeyUnregistered, SessionRevoked, \
    UserDeactivatedBan

sys.setrecursionlimit(100)

telegram_clients = list()
telegram_clients_iter = None
current_client = None


async def check_channel(link):
    await wait(1)

    global current_client

    name = 'notvalid'
    members = 0
    is_open = 'notvalid'
    valid = 'notvalid'

    try:
        try:
            chat = await current_client.get_chat(link)
        except UsernameInvalid:
            chat = await current_client.get_chat(link.replace('http://t.me/', '').replace('https://t.me/', ''))
        name = chat.title
        members = chat.members_count
        is_open = 'open' if hasattr(chat, 'username') and isinstance(chat.username, str) else 'close'
        valid = 'valid'
    except (InviteHashExpired, UsernameInvalid):
        pass
    except FloodWait as fw:
        print_destroyable_text(f'[INFO] Сплю {fw.value} секунд (Floodwait Error)')
        rotate_session()
        try:
            await check_channel(link)
        except RecursionError:
            print('100 tries to check one link at floodwait, seems like all accounts is floodwaited')
            sys.exit()
    except (AuthKeyUnregistered, SessionRevoked, UserDeactivatedBan):
        remove_session()
        try:
            await check_channel(link)
        except RecursionError:
            print('seems like no working accounts left because of auth key unregistered / .session revoked (100 tries)')
            sys.exit()
    return link, name, members, is_open, valid


def get_channels_from_file():
    with open('channels.txt', 'r') as f:
        return f.readlines()


def delete_channel_from_file(channel):
    with open('channels.txt', 'r') as f:
        lines = f.readlines()
    with open('channels.txt', 'w') as f:
        for line in lines:
            if channel not in line:
                f.write(line)


def normalize_channel(channel):
    return channel.replace('\n', '').replace(' ', '')


async def wait(seconds):
    await asyncio.sleep(seconds)


async def init_sessions():
    global current_client
    global telegram_clients
    global telegram_clients_iter
    for f in os.listdir('data'):
        telegram_client = Client("data/" + f.replace('.session', ''),
                                 api_id=2040,
                                 api_hash='b18441a1ff607e10a989891a5462e627',
                                 sleep_threshold=0)
        telegram_clients.append(telegram_client)
        await telegram_client.connect()

    telegram_clients_iter = cycle(telegram_clients)
    rotate_session()


def rotate_session():
    try:
        global current_client
        global telegram_clients_iter

        current_client = telegram_clients_iter.__next__()
    except StopIteration:
        print(f'you should add some pyrogram .session accounts in data folder')
        sys.exit()


def print_destroyable_text(text):
    print(text, end="")
    print("\r", end="")


def remove_session():
    global current_client
    global telegram_clients
    global telegram_clients_iter

    telegram_clients.remove(current_client)
    telegram_clients_iter = cycle(telegram_clients)

    rotate_session()

    print('1 session is removed because it is banned')


async def deinit_sessions():
    global telegram_clients
    for client in telegram_clients:
        await client.disconnect()


async def main():
    print('- If this project was useful, here is my USDT TRC20 address: ')
    print('TQqYH58Lhg1zNoaXNZERRtUyX31FRRHUoo')
    print('- My GitHub: https://github.com/plutonium777')
    print('- My Telegram: https://t.me/wasd_plutonium')
    print_destroyable_text('Started! Initializing.')
    await init_sessions()
    print(f'Initialized {len(telegram_clients)} accounts.')
    channels = get_channels_from_file()
    for channel in channels:
        delete_channel_from_file(channel)
        channel = normalize_channel(channel)
        link, name, members, is_open, valid = await check_channel(channel)
        print(f'{link}:{name}:{members}:{is_open}:{valid}')
    await deinit_sessions()


asyncio.run(main())
