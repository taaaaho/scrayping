# -*- coding: utf-8 -*-
# https://crowdworks.jp/public/jobs/6118337
# for スクレイピング
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re

# Define export format 
columns = ['company', 'address', 'phone', 'url']
  
domain = 'https://atsumaru.jp'
if __name__ == '__main__':
  pager, count = 1, 0
  datas = []
  while True:
    html = urlopen('https://atsumaru.jp/area/7/list?sagid=27&page={}'.format(pager))
    soup = BeautifulSoup(html, 'html.parser')
    companies = soup.select('li.name > span.exe')

    if len(companies) == 0:
      print('会社数:{} ページ数:{}'.format(count, pager-1))
      df = pd.DataFrame(datas, columns=columns)
      df.to_csv("employee.csv")
      break
    for company in companies:
      # print(company.find('a').text)
      # print(company.find('a').get('href'))
      # 企業情報取得
      detail = urlopen('{}{}'.format(domain,company.find('a').get('href')))
      detail_bs = BeautifulSoup(detail, 'html.parser')
      address = detail_bs.select('article table > tr:nth-of-type(3) > td > p')
      # print(address[1].text)
      phone = detail_bs.select('article table > tr:nth-of-type(3) > td > p:nth-of-type(2) > a')
      phone = re.search(r'tel=\d+-\d+-\d+',phone[0].get('href'))
      # print(phone.group().replace('tel=',''))

      datas.append([
          company.find('a').text,  # company
          address[1].text, # address
          phone.group().replace('tel=',''), # phone
          '{}{}'.format(domain,company.find('a').get('href'))  #url
      ])

    count+=len(companies)
    pager+=1
