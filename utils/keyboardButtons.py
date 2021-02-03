from telegram import KeyboardButton, ReplyKeyboardMarkup

def getDefaultKeyboardButtons():
  main_menu_keyboard = [[KeyboardButton('/ajustar')], [KeyboardButton('/ler')]]
  reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                          resize_keyboard=True,
                                          one_time_keyboard=True)
  return reply_kb_markup

def getScheduleButtons():
  main_menu_keyboard = [[KeyboardButton('07:00')], [KeyboardButton('08:00')], [KeyboardButton('09:00')]]
  reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                          resize_keyboard=True,
                                          one_time_keyboard=True)
  return reply_kb_markup                                      
                                  