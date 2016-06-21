# import ConfigParser

# from slacker import Slacker

# config = ConfigParser.RawConfigParser()
# config.read('bot.properties')

# BOT_API_KEY = config.get('bot.api.key', None)

# if not BOT_API_KEY:
#     exit(1)

# slack = Slacker(BOT_API_KEY)


from service.message import MessageParser
import logging

logging.basicConfig(level=logging.DEBUG)


message_parser = MessageParser()

message = message_parser.parse('''{
    "type": "hello"
}''')

message.process()
