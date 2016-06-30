import logging

from bot import WorkHourBot

logging.basicConfig(level=logging.DEBUG)

BOT_API_KEY = 'xoxp-48868443122-48812271987-55711001217-1ec739d99f'

bot = WorkHourBot(BOT_API_KEY)
bot.run()
