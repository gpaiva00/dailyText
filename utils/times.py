from datetime import date, datetime

def getToday():
  return date.today().strftime('%d/%m/%Y')

def getNow():
  return datetime.now().strftime('%H:%M')