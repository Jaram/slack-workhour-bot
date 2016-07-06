import logging

from bot import WorkHourBot

logging.basicConfig(level=logging.DEBUG)

BOT_API_KEY = 'xoxb-52734009232-jO4KNpOpq8AZnktWyJgmgAZW'

bot = WorkHourBot(BOT_API_KEY)
bot.run()
