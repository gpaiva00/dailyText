import redis
import bs4, requests
import logging
import re
import schedule
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup
from config.settings import WOL_URL, WOL_DAILY_TEXT_PATH, TELEGRAM_TOKEN, PORT, SCHEDULES_TIME, REDIS_URL
from utils.listToString import listToString
from datetime import date, datetime

db = redis.Redis(host=REDIS_URL, decode_responses=True)

# setting a logging to know when (and why) things don't work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

WOL_DAILY_URL = WOL_URL + WOL_DAILY_TEXT_PATH

def start(update, context):
  chat_id = str(update.effective_chat.id)
  message = 'Seja bem-vindo(a)! Use um dos seguintes comandos para começar:'
  message += '\n\n/ajustar - Ajuste o seu horário de ler o texto diário.'
  message += '\n\n/ler - Leia agora o texto para hoje.'
  
  # Commands menu
  main_menu_keyboard = [[KeyboardButton('/ajustar')], [KeyboardButton('/ler')]]
  reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                          resize_keyboard=True,
                                          one_time_keyboard=True)

  # Send the message with menu
  context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_kb_markup)
  # update.message.reply_text(message)
  # context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

def getCurrentDailyText():
  db_daily_text = db.get('daily_text')
  today = date.today().strftime('%d/%m/%Y')
  
  # check if today's text exists in redis
  if db_daily_text != None:
    (text, daily_date) = db_daily_text.split('||')

    if daily_date == today:
      return text

  # download wol page
  page = requests.get(WOL_DAILY_URL)
  # page.raise_for_status()

  parsed_page = bs4.BeautifulSoup(page.text, 'html.parser')
  parsed_page = parsed_page.select('.itemData')[0]

  # Daily text date
  daily_date = parsed_page.h2.string
  # Bible text of the day
  daily_bible_text = listToString(parsed_page.find('p', class_='themeScrp').contents)
  # Daily comment
  daily_comment = listToString(parsed_page.find('p', class_='sb').contents)

  message = ('<b>%s</b>' % daily_date)
  message += ('\n\n%s' % daily_bible_text)
  message += ('\n\n%s' % daily_comment)
  message += ('\n\nFonte: <a href="%s">%s</a>' % (WOL_DAILY_URL, WOL_DAILY_URL))

  db_message = ('%s||%s' % (message, today))
  db.set('daily_text', db_message)

  return message

def sendDailyText(update, context):
  message = getCurrentDailyText()
  update.message.reply_text(text=message, parse_mode='HTML')

def sendScheduleOptions(update, context):
  chat_id = str(update.effective_chat.id)
  message = 'Ok, vamos ajustar seu horário. '
  message += 'Escolha que horas você gostaria de receber o texto diário:'

  main_menu_keyboard = [[KeyboardButton('07:00')], [KeyboardButton('08:00')], [KeyboardButton('09:00')]]
  reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                          resize_keyboard=True,
                                          one_time_keyboard=True)

  context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_kb_markup)

def handleScheduleOption(update, context):
  selected_schedule = update.effective_message.text
  match = re.search('^(?:(?:([01]?\d|2[0-3]):([0-5]?\d)))', selected_schedule)

  if match == None:
    message = 'Desculpe, não entendi sua mensagem. Tente novamente.'
    update.message.reply_text(message)
    return

  elif selected_schedule not in SCHEDULES_TIME:
    message = 'Ops, por enquanto não contemplo esse horário. 🥲'
    update.message.reply_text(message)
    return

  chat_id = str(update.effective_chat.id)
  # today = date.today().strftime('%d/%m/%Y')
  db_schedule = ('%s||%s' % (selected_schedule, ''))

  db.set(chat_id, db_schedule)

  message = ('Ok, a partir de hoje você receberá o texto diário às %s horas. 😃🙏' % selected_schedule)

  main_menu_keyboard = [[KeyboardButton('/ajustar')], [KeyboardButton('/ler')]]
  reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                          resize_keyboard=True,
                                          one_time_keyboard=True)

  context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_kb_markup)

def prepareSchedule():
  db_schedules_keys = db.keys()[1:]
  today = date.today().strftime('%d/%m/%Y')
  now = datetime.now().strftime('%H:%M')
  message = getCurrentDailyText()

  for chat_id in db_schedules_keys:
    (db_time, db_date) = db.get(chat_id).split('||')

    if db_date == today:
      return

    if db_time == now:
      url_params = (TELEGRAM_TOKEN, chat_id, message, 'HTML')
      url = ('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&parse_mode=%s' % url_params)
      response = requests.get(url)
      print('schedule_response', response)
      
      # update db_date
      new_schedule = ('%s||%s' % (db_time, today))
      db.set(chat_id, new_schedule)

def startScheduler():
  for schedule_time in SCHEDULES_TIME:
    schedule.every().day.at(schedule_time).do(prepareSchedule)

  while True:
    schedule.run_pending()
    time.sleep(1)

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
  dp.add_handler(CommandHandler('ler', sendDailyText))
  dp.add_handler(CommandHandler('ajustar', sendScheduleOptions))
  dp.add_handler(MessageHandler(Filters.command, unknown))
  dp.add_handler(MessageHandler(Filters.text, handleScheduleOption))

  # start the bot
  updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TELEGRAM_TOKEN)
  updater.bot.setWebhook('https://daily-text-jw.herokuapp.com/'+TELEGRAM_TOKEN)

  # Run the bot until you press Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT. This should be used most of the time, since
  # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()
  # updater.start_polling()
  
  # start scheduler
  startScheduler()


if __name__ == '__main__':
  main()