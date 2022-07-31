import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import pandas as pd

try:
    
    URL = "http://uta.pw/sakusibbs/users.php?action=login&"
    USER = "shun001"
    PASS = "vP9fj5Bc9agVgjE"
    
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Chrome('chromedriver.exe', options=options)
    browser.get(URL)

    sleep(1)
    elem_username = browser.find_element_by_id('user')
    elem_username.send_keys(USER)

    elem_password = browser.find_element_by_id('pass')
    elem_password.send_keys(PASS)

    sleep(1)
    
    elem_login_btn = browser.find_element_by_xpath("//input[@value='ログイン']")
    elem_login_btn.click()
    
    elem_mypage_btn = browser.find_element_by_class_name('islogin')
    elem_mypage_btn.click()
    
    sleep(1)
    cur_url = browser.current_url    
    mypage_res = requests.get(cur_url)

    soup = BeautifulSoup(mypage_res.text, 'lxml')
    
    
    df = pd.DataFrame(columns = ['item', 'content'])
    
    
    tr_tags = soup.select('#tbl > tr')
    for tr_tag in tr_tags:
        item = tr_tag.select_one('th').string
        content = tr_tag.select_one('td').string
        
        df = df.append({'item':item, 'content':content}, ignore_index=True)
    
    df.to_csv('./result.csv', index=False, encoding='utf_8_sig')
    
    print('正常終了')
    
except Exception as e:
    print(e)
    print('異常終了')
    
