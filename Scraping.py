# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import pandas as pd

def main():
  """_summary_
  Amazonの売れ筋ランキングページからカテゴリ別に商品名とURLをcsvに出力する。
  """


  try:

    time.sleep(3) 

    df = pd.DataFrame(columns = ['カテゴリ', 'ランキング', '商品名', 'URL'])    

    url = 'https://www.amazon.co.jp/gp/bestsellers'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    for header_tag in soup.select('div.a-carousel-header-row'):

      for category_tag in header_tag.select('div > h2'):

        category_name = category_tag.string.replace(' の 売れ筋ランキング', '')
        items_tag = header_tag.next_sibling
        # [print_element(x) for x in items_tag]

        for item in items_tag.select('li'):
          item_name = (item.select("div > div > a > span > div"))[0].string
          item_rank = (item.select("div > div > span"))[0].string.replace('#', '') + '位'
          item_url = "https://www.amazon.co.jp/" + (item.select("div > div > a"))[0].attrs.get('href')

          df = df.append({'カテゴリ':category_name, 'ランキング':item_rank, '商品名':item_name, 'URL':item_url}, ignore_index=True)

    
    df.to_csv('./result.csv', index=False, encoding='utf_8_sig')

  except Exception as e:
    print(e.args)
    print('異常終了')

  finally:
    print('正常終了')


def print_element(elem):

  if isinstance(elem, NavigableString):
      print(type(elem), elem.string)   
  else:
      print(type(elem), elem.name, elem.attrs.get('class'))
      


if __name__ == '__main__':
  main()