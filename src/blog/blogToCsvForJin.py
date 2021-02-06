# for Wordpress JIN
# for スクレイピング
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# 出力フォーマットの定義
columns = ['title',  'category', 'date', 'url']
df = pd.DataFrame(columns=columns)

# スクレイピング先URL
url = 'https://hitodeblog.com/'
targetYear = ['2018', '2019']

# url = 'https://www.hitode-festival.com/'
# targetYear = ['2014', '2015', '2016', '2017', '2018', '2019']

# 複数カテゴリ付いている場合に分割する
def fetchCategories(categories):
  categoriList = []
  for category in categories:
    categoriList.append(category.text)
  return ' '.join(categoriList)
  
# ブログ記事取得
def getTargetPageData(targetUrl):
  print(targetUrl)
  html = urlopen(targetUrl)
  soup = BeautifulSoup(html, 'html.parser')
  entries = soup.find_all('article', class_='post-list-item')
  global df

  for entry in entries:
      se = pd.Series([
          entry.find('h2').text,  #title  
          entry.find('span', class_='post-list-cat').text if entry.find('span', class_='post-list-cat') else '', #category
          entry.find('span', class_='post-list-date').text,  #date 
          entry.find('a', class_='post-list-link').get('href') #url 
      ], columns)
      df = df.append(se, columns)
      
      
def downloadToGoogleDrive(df):
  # for download to Google Drive
  from google.colab import drive
  drive.mount('/gdrive')
  
  # Google Driveに保存
  with open('/gdrive/My Drive/dai.csv', 'w', encoding = 'utf-8-sig') as f:
    df.to_csv(f)

def downloadToLocal(df):
  # for download to local
  from google.colab import files

  # ローカルにダウンロード
  df.to_csv('df.csv')
  files.download('df.csv')
  
  
if __name__ == '__main__':
  for year in targetYear:
    maxPageNumber = 0
    html = urlopen(url + year)
    soup = BeautifulSoup(html, 'html.parser')
    pager = soup.find('ul', class_='pagination ef')
    if pager:
      pageNations = pager.find_all('li')  
      for pageNation in pageNations:
        if pageNation.find('a'):
          pageNumber = int(pageNation.find('a').find('span').text)
          if maxPageNumber < pageNumber:
            maxPageNumber = pageNumber

      for page in range(maxPageNumber):
        nextPageUrl = url + year + '/page/' + str(page + 1)
        getTargetPageData(nextPageUrl)
    else:
      getTargetPageData(url + year)
   
  # データをGoogleドライブへ保存
  downloadToGoogleDrive(df)
  
  # データを描画
  df

  
