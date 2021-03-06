import os

from dotenv import load_dotenv

load_dotenv()

MONGO_URI=os.getenv('MONGO_URI')
WOL_URL=os.getenv('WOL_URL')
WOL_DAILY_TEXT_PATH=os.getenv('WOL_DAILY_TEXT_PATH')
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')
PORT=int(os.getenv('PORT', '5000'))
HEROKU_APP_URL=os.getenv('HEROKU_APP_URL')

REDIS_URL=os.getenv('REDIS_URL')
REDIS_TLS_URL=os.getenv('REDIS_TLS_URL', 'redis://localhost:6379')
REDIS_PORT=os.getenv('REDIS_PORT', '6379')
REDIS_DB=int(os.getenv('REDIS_DB', 0))

SCHEDULES_TIME=['07:00', '08:00', '09:00']
