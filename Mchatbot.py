import asyncio
import json
from typing import List

from khl import Bot, Message
from khl.command import Lexer

from mc import MC
from config import mc_server, bot_token, bot_channel
from minecraftTellrawGenerator import MinecraftTellRawGenerator as mctellraw


bot = Bot(token=bot_token)
mc = MC(mc_server)
msg_queue = []


class KeyWord(Lexer):
    keyword: str
    start_with: bool
    no_space: bool

    def __init__(self, keyword: str, start_with: bool = True, no_space: bool = False):
        self.keyword = keyword
        self.start_with = start_with
        self.no_space = no_space

    def lex(self, msg: Message) -> List[str]:
        if self.no_space:
            command = msg.content.split('\n')[0].strip()
            if command != self.keyword:
                raise Lexer.NotMatched(msg)
        elif self.start_with:
            command = msg.content.split(' ')[0].strip()
            if command != self.keyword:
                raise Lexer.NotMatched(msg)
        else:
            if msg.content.find(self.keyword) < 0:
                raise Lexer.NotMatched(msg)
        return []


def get_player_and_text(json_data):
    json_data = json.loads(json_data)
    player = json_data['with'][0]['text']
    msg_text = json_data['with'][1]['text']
    return player, msg_text


def chat_event(chat_packet):
    global msg_queue
    if chat_packet.field_string('position') == 'CHAT':
        player, msg_text = get_player_and_text(chat_packet.json_data)
        print(f'<{player}> {msg_text}')
        msg_queue.append({'player': player, 'text': msg_text})


async def send_mc_text_to_khl():
    global msg_queue
    while True:
        if len(msg_queue) != 0:
            msg = msg_queue.pop(0)
            player, msg_text = msg['player'], msg['text']
            await (await bot.fetch_public_channel(bot_channel)).send(f'<{player}> {msg_text}')
            continue
        else:
            await asyncio.sleep(1)


def disconnect_event(disconnect_packet):
    mc.connect()
    print('Reconnecting...')


@bot.command(lexer=KeyWord(keyword='/hello'))
async def hello(msg: Message):
    await msg.reply('Hello World')


@bot.command(lexer=KeyWord(keyword='/say'))
async def say(msg: Message):
    send_msg = msg.content.replace('/say', '').strip()
    tellraw_msg = mctellraw(text=f'<{msg.author.nickname}> {send_msg}')
    print(f'<{msg.author.nickname}> {send_msg}')
    mc.message(f'/tellraw @a {str(tellraw_msg)}')


async def main():
    await asyncio.gather(
        send_mc_text_to_khl(),
        bot.start()
    )


if __name__ == '__main__':
    mc.register_chat_listener(chat_event)
    mc.register_disconnect_listener(disconnect_event)
    mc.connect()
    mc.login('bot online')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
