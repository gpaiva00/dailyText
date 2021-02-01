import bs4, requests

WOL_URL = 'https://wol.jw.org'
WOL_DAILY_TEXT_PATH = '/pt/wol/dt/r5/lp-t/'
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
# text_comment = parsed_page.select('#p4')[0]

# textBody2 = parsed_page.select('.billboardDescription')
