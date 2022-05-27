from khl import Bot, Message
from mc import MC
from config import mc_server, bot_token

bot = Bot(token=bot_token)
mc = MC(mc_server)


def chat_event(chat_packet):
    print('Message (%s): %s' % (chat_packet.field_string('position'), chat_packet.json_data))


def disconnect_event(disconnect_packet):
    mc.connect()
    print('Reconnecting...')


@bot.command('hello')
async def hello(msg: Message):
    await msg.reply('Hello World')


if __name__ == '__main__':
    mc.register_chat_listener(chat_event)
    mc.register_disconnect_listener(disconnect_event)
    mc.connect()
    mc.login('bot online')
    bot.run()
