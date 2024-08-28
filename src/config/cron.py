import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

def hello_world():
    print("Hello world!")


def crawl_notices():
    # notitypes = "JANGHAKNOTICE GENERALNOTICE HAKSANOTICE IPSINOTICE GLOBALNOTICE HAKSULNOTICE SAFENOTICE BUDDHISTEVENT".split(" ")
    notitypes = ["HAKSANOTICE"]

    for notitype in notitypes: #종류별로 for문 돌리기
        url = f"https://www.dongguk.edu/article/{notitype}/list?pageIndex=1"
        print(f"")
        print(f"Fetching Url: {url}")
        response = requests.get(url)
        notices_list = []

        if response.status_code == 200:
            html = response.text #받아온 것의 텍스트
            soup = BeautifulSoup(html, 'html.parser') #텍스트 해석??
            list = soup.select_one('div.board_list > ul')
            notices = list.select('li')
            for notice in notices: #각 공지별로 for문 돌리기
                title = notice.select_one('p.tit').get_text().replace('\t', '').replace('\r\n', '').replace('\n', '')
                if title.startswith("\n공지\r\n"):
                    continue
                id = notice.select_one('a')["onclick"].replace('goDetail(', '').replace(');', '')
                notice_url = f"https://www.dongguk.edu/article/{notitype}/detail/{id}"
                #새 url 접속
                response_detail = requests.get(notice_url)
                soup_detail = BeautifulSoup(response_detail.text, 'html.parser')
                
                description = soup_detail.select_one('#content_focus > div > div.board_view > div.view_cont').get_text()
                date = soup_detail.select_one('#content_focus > div > div.board_view > div.tit > div > span:nth-child(1)').get_text()
                # author =   작성자 #content_focus > div > div.board_view > div.tit > div > span:nth-child(2)
                # views =    조회수 #content_focus > div > div.board_view > div.tit > div > span:nth-child(3)
                # to. 서연 위에 주석 두 줄 신경쓰지 마세욥~

                ps = soup_detail.select('#content_focus > div > div.board_view > div.view_cont > p')
                imgs = []
                for p in ps:
                    imgsS = p.select('img')
                    for img in imgsS:
                        imgs.append(img['src'])


                #링크(디코 음성채팅방 참고)
                
                #첨부파일(지원서 양식 등)


                notice_data = {
                    'id': id,
                    'title': title,
                    'url' : notice_url,
                    'notitype' : notitype,
                    'description' : description,
                    'date' : date,
                    'imgs' : imgs,
                }
                notices_list.append(notice_data)
            open(f"./data/{notitype}.json", 'w', encoding='UTF-8').write(json.dumps(notices_list,  ensure_ascii = False))

        else : 
            pprint(response)


