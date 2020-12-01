import re
import json
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage

def notification(title, link):
    with open('data/notify_list.json', 'r') as file:
        notify_list = json.load(file)
        #print (notify_list)
    if len(notify_list) == 0:
        return False
    
    content = "{}\n{}".format(title, link)
    line_bot_api.multicast(notify_list, TextSendMessage(text=content))
    return True

line_bot_api = LineBotApi('iqBB2s4BXjlBy15Bq1TWLoYGx8iUzI5F1rcZsai29VCET40cATVuxiAWxx3DS6JyPPOcFMpK+SVaG3t9WIb2+fC8HYHAPOrz2qSbtLR3/JUOoyN0n3eMKBLvbe/CsmhRrql78xKkGO/dJ5CD35aVSgdB04t89/1O/w1cDnyilFU=')

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path='C:/Users/User/Downloads/railway_automation_booking-master/chromedriver.exe',options=chrome_options)
#driver = webdriver.PhantomJS()
driver.get('https://www.ptt.cc/bbs/Lifeismoney/index.html')
soup = BeautifulSoup(driver.page_source, "html.parser")

re_gs_title = re.compile(r'\[情報\s*\]\s*', re.I)
re_gs_id = re.compile(r'.*\/Lifeismoney\/M\.(\S+)\.html')

match = []
print('開始解析')
for article in soup.select('.r-list-container .r-ent .title a'):
    #print(article)
    title = article.string
    if re_gs_title.match(title) != None:
        #print(match)
        link = 'https://www.ptt.cc' + article.get('href')
        article_id = re_gs_id.match(link).group(1)
        match.append({'title':title, 'link':link, 'id':article_id})

if len(match) > 0:
    with open('data/history/history.json', 'r+') as file:
        history = json.load(file)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')       
        new_flag = False
        for article in match:
            if article['id'] in history:
                continue
            new_flag = True
            history.append(article['id'])
            notification(article['title'], article['link'])
            #print("{}: New Article: {} {}".format(now, article['title'], article['link']))

        if new_flag == True:
            file.seek(0)
            file.truncate()
            file.write(json.dumps(history))
        else:
            print("{}: Nothing".format(now))

driver.quit()