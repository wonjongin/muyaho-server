import requests
from bs4 import BeautifulSoup
import json


def crawl_notices () :
    notitypes = "JANGHAKNOTICE GENERALNOTICE HAKSANOTICE IPSINOTICE GLOBALNOTICE HAKSULNOTICE SAFENOTICE BUDDHISTEVENT".split(" ")

    for notitype in notitypes:
        url = f"https://www.dongguk.edu/article/{notitype}/list?pageIndex=1"
        print(f"")
        print(f"Fetching Url: {url}")
        response = requests.get(url)
        notices_list = []

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            list = soup.select_one('div.board_list > ul')
            notices = list.select('li')
            for notice in notices:
                title = notice.select_one('p.tit').get_text().replace('\t', '').replace('\r\n', '').replace('\n', '')
                if title.startswith("\n공지\r\n"):
                    continue
                id = notice.select_one('a')["onclick"].replace('goDetail(', '').replace(');', '')
                notice_data = {
                    'id': id,
                    'title': title,
                }
                notices_list.append(notice_data)
            open(f"./data/{notitype}.json", 'w', encoding='UTF-8').write(json.dumps(notices_list,  ensure_ascii = False))

        else : 
            print(notitype)