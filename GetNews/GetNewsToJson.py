import json
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

start_date = datetime(2024, 5, 1)
start_date = str(start_date)[:10]

end_date = datetime(2024, 5, 10)
end_date = str(end_date)[:10]

cd_min = start_date[6:7] + '/' + start_date[8:10] + '/' + start_date[:4]
cd_max = end_date[6:7] + '/' + end_date[8:10] + '/' + end_date[:4]

tbs = 'qdr:w'

search = '삼성전자'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 '
                  'Safari/537.36'}
cookie = {'CONSENT': 'YES'}
url = 'https://www.google.com/search?'

news_data = []

# Loop over the first 10 pages
for page in range(10):
    start = page * 10
    params = {'q': search, 'hl': 'ko', 'tbm': 'nws', 'tbs': tbs, 'start': start}
    res = requests.get(url, params=params, headers=header, cookies=cookie)
    soup = bs(res.text, 'lxml')

    # Parsing the article titles
    list = soup.find_all('div', 'GI74Re nDgy9d')

    for i in list:
        news_item = {'title': i.get_text()}
        link = i.find('a')
        if link is not None:
            news_item['link'] = link['href']
        else:
            news_item['link'] = "No link found"
        news_data.append(news_item)

# Save to json file
# fime name is time based
file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.json'
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(news_data, file, ensure_ascii=False, indent='\t')
