from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import bs4, requests
from config.settings import WOL_URL, WOL_DAILY_TEXT_PATH, TELEGRAM_TOKEN, PORT
from datetime import date
import logging

# setting a logging to know when (and why) things dont work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

WOL_DAILY_URL = WOL_URL + WOL_DAILY_TEXT_PATH

page = requests.get(WOL_DAILY_URL)
# page.raise_for_status()

parsed_page = bs4.BeautifulSoup(page.text, 'html.parser')
parsed_page = parsed_page.select('.itemData')[0]

# Daily text date
date = parsed_page.h2.string
# Bible text of the day
daily_bible_text = parsed_page.find('p', class_='themeScrp').contents
# Daily comment
daily_comment = parsed_page.find('p', class_='sb').contents

print(daily_comment)


def start(update, context):
  update.message.reply_text(
    'Seja bem-vindo(a)! Para começar, me informe o horário que você gostaria de receber o texto diário.'
    )

def unknown(update, context):
  update.message.reply_text('Desculpe, não entendi o que você quis dizer. Tente outro comando.')

def main():
  """Start the bot."""

  # Updater continuously fetches new updates from telegram and passes them to the Dispather
  updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

  # get the dispatcher to register handlers
  dp = updater.dispatcher

  # register handlers
  dp.add_handler(CommandHandler('start', start))
  dp.add_handler(MessageHandler(Filters.command, unknown))
  # dp.add_handler(MessageHandler(Filters.text, get_number_of_phones))

  # start the bot
  updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TELEGRAM_TOKEN)
  updater.bot.setWebhook('https://daily-text-jw.herokuapp.com/'+TELEGRAM_TOKEN)

  # Run the bot until you press Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT. This should be used most of the time, since
  # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()


if __name__ == '__main__':
  main()