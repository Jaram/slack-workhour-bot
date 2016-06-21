# import ConfigParser

# from slacker import Slacker

# config = ConfigParser.RawConfigParser()
# config.read('bot.properties')

# BOT_API_KEY = config.get('bot.api.key', None)

# if not BOT_API_KEY:
#     exit(1)

# slack = Slacker(BOT_API_KEY)


from service.worklog import CommuteLogger
import logging

logging.basicConfig(level=logging.DEBUG)

commute_logger = CommuteLogger()

