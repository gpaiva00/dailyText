import os

from dotenv import load_dotenv

load_dotenv()

MONGO_URI=os.getenv('MONGO_URI')
WOL_URL=os.getenv('WOL_URL')
WOL_DAILY_TEXT_PATH=os.getenv('WOL_DAILY_TEXT_PATH')
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN')
PORT=int(os.getenv('PORT', '5000'))
