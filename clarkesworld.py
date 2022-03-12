import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import os.path

response = requests.get("https://clarkesworldmagazine.com/")
soup = bs(response.text, 'html.parser')
results = soup.select('div.index-col1,div.index-col2')

rows = []

for r in results:
    issue = []
    row = {}
    try:    
        row['Title'] = r.select_one('.story').text
    except:
        row['Title'] = 'unbekannt'

    try:    
        row['Byline'] = r.select_one('.byline').text  
    except:
        row['Byline'] = 'unbekannt'

    try:    
        row['URL to story'] = r.select_one('a').get('href')
    except:
        row['URL to story'] = 'unbekannt'

    try:    
        row['Category'] = r.parent.p.text.strip()
    except:
        row['Category'] = 'unbekannt'

    try:    
        issue = r.parent.parent.h1.text.split('–')
        row['Issue number'] = issue[0].replace('ISSUE','').strip()
        row['Publication date'] = issue[1]
    except:
        row['Issue number'] = 'unbekannt'
        row['Publication date'] = 'unbekannt'
    rows.append(row)
  
if os.path.isfile('clarkesworld.csv'):
    df1 = pd.read_csv('clarkesworld.csv',index_col=0)
    df2 = pd.DataFrame(rows)
    frames = [df1,df2]
    df3 = pd.concat(frames)
    
else:
    df3 = pd.DataFrame(rows)

df3.drop_duplicates(subset='URL to story', keep='first', inplace=True,ignore_index=True) 
df3.to_csv('clarkesworld.csv')
df3

