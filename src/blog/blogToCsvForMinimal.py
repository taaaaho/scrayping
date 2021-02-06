# for スクレイピング
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# 出力フォーマットの定義
columns = ['title',  'category', 'date', 'url']
df = pd.DataFrame(columns=columns)

# スクレイピング先URL
# url = 'https://manablog.org/'
url = 'https://dividable.net/'

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
  entries = soup.find_all('div', class_='col-xs-12 wrap')
  global df

  for entry in entries:
      se = pd.Series([
          entry.find('h2').find('a').get('title'),  #title
          fetchCategories(entry.find('p', class_='cat').find_all('a')), #category
          entry.find('time').text,  #date
          entry.find('h2').find('a').get('href') #url
      ], columns)
      df = df.append(se, columns)
      
  nextPage = soup.find('div', class_='pull-right')   
  nextPageUrl = nextPage.find('a')
  if nextPageUrl:
    getTargetPageData(nextPageUrl.get('href'))
  else:
    print('Done')

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
  getTargetPageData(url)
  
  # 取得したデータを表示
  df
  
  # Googleドライブへ保存
  downloadToGoogleDrive(df)
  
  # 端末へダウンロード
  downloadToLocal(df)
  
