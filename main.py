import logging

from bot import WorkHourBot

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.DEBUG, format=FORMAT)

BOT_API_KEY = 'xoxb-52734009232-jO4KNpOpq8AZnktWyJgmgAZW'

bot = WorkHourBot(BOT_API_KEY)
bot.run()
