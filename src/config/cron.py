import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from datetime import date, datetime
from notice.models import Notice


def hello_world():
    print("Hello world!")

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def crawl_main_notices():
    # notitypes = "JANGHAKNOTICE GENERALNOTICES HAKSANOTICE IPSINOTICE GLOBALNOLTICE HAKSULNOTICE SAFENOTICE BUDDHISTEVENT".split(
    #     " "
    # )
    notitypes = ["GENERALNOTICES"]

    # pages = {
    #     "GENERALNOTICES": 88,
    #     "IPSINOTICE": 10,
    #     "HAKSANOTICE": 56,
    #     "GLOBALNOLTICE": 42,
    #     "HAKSULNOTICE": 5,
    #     "BUDDHISTEVENT": 12,
    #     "JANGHAKNOTICE": 54,
    #     "SAFENOTICE": 3,
    # }

    pages = {
        "GENERALNOTICES": 3,
        "IPSINOTICE": 2,
        "HAKSANOTICE": 2,
        "GLOBALNOLTICE": 2,
        "HAKSULNOTICE": 2,
        "BUDDHISTEVENT": 2,
        "JANGHAKNOTICE": 2,
        "SAFENOTICE": 2,
    }

    for notitype in notitypes:  # 종류별로 for문 돌리기
        for i in range(1, pages[notitype]):
            url = f"https://www.dongguk.edu/article/{notitype}/list?pageIndex=1"
            base_url = "https://www.dongguk.edu"
            print(f"{notitype}")
            print(f"Fetching Url: {url}")
            response = requests.get(url)
            notices_list = []

            if response.status_code == 200:
                html = response.text  # 받아온 것의 텍스트
                soup = BeautifulSoup(html, "html.parser")  # 텍스트 해석??
                noti_list = soup.select_one("div.board_list > ul")
                notices = noti_list.select("li") 
                for notice in notices:  # 각 공지별로 for문 돌리기
                    title = (
                        notice.select_one("p.tit")
                        .get_text()
                        .replace("\t", "")
                        .replace("\r\n", "")
                        .replace("\n", "")
                    )
                    if title.startswith("\n공지\r\n"):
                        continue
                        
                    print(f"Title: {title}")
                    id = (
                        notice.select_one("a")["onclick"]
                        .replace("goDetail(", "")
                        .replace(");", "")
                    )
                    notice_url = f"https://www.dongguk.edu/article/{notitype}/detail/{id}"
                    # 새 url 접속
                    print(f"Fetching Url: {notice_url}")
                    response_detail = requests.get(notice_url)
                    soup_detail = BeautifulSoup(response_detail.text, "html.parser")

                    description_html = soup_detail.select_one(
                        "#content_focus > div > div.board_view > div.view_cont"
                    )
                    if description_html is None:
                        print(f"ERROR: Can't find #content_focus > div > div.board_view > div.view_cont in {notice_url}")
                        break
                    for s in description_html.select("script"):
                        s.extract()
                    date_html = soup_detail.select_one(
                        "#content_focus > div > div.board_view > div.tit > div > span:nth-child(1)"
                    )
                    notice_date_str = (
                        date_html
                        .get_text()
                        .replace("등록일 ", "")
                    )
                    ymds = notice_date_str.split('.')[:-1]
                    ymd = [int(x) for x in ymds]
                    notice_date = date(ymd[0], ymd[1], ymd[2])
                    # author =   작성자 #content_focus > div > div.board_view > div.tit > div > span:nth-child(2)
                    # views =    조회수 #content_focus > div > div.board_view > div.tit > div > span:nth-child(3)

                    ps = soup_detail.select(
                        "#content_focus > div > div.board_view > div.view_cont > p"
                    )
                    imgs = []
                    for p in ps:
                        imgsS = p.select("img")
                        for img in imgsS:
                            v = img.get("src", img.get("dfr-src"))
                            if v is None:
                                continue
                            imgs.append(base_url + img["src"])

                    # 링크(디코 음성채팅방 참고)
                    links = []
                    for p in ps:
                        linksS = p.select("a")
                        for link in linksS:
                            links.append({"name": link.get_text(), "url": link["href"]})

                    # 첨부파일(지원서 양식 등)
                    attachments = []
                    view_files = soup_detail.select_one(
                        "#content_focus > div > div.board_view > div.view_files > ul"
                    )
                    # location.href="/cmmn/fileDown.do?filename="+encodeURIComponent(file_nm)+"&filepath="+file_path+"&filerealname="+file_sys_nm;

                    if view_files:
                        attachment_elements = view_files.select("li > a")
                        for attachment in attachment_elements:
                            href: str = attachment["href"]
                            file_url = None
                            down_file = ""
                            if href.startswith("javascript:downGO("):
                                parts = href[len("javascript:downGO(") : -1].split("','")
                                if len(parts) >= 3:
                                    down_file = f"/cmmn/fileDown.do?filename={parts[0]}&filepath={parts[1]}&filerealname={parts[2].replace("')", "")}"
                            if down_file != "":
                                attachments.append(
                                    {
                                        "name": attachment.get_text(),
                                        "url": base_url + down_file,
                                    }
                                )

                    notice_data = {
                        "notice_id": id,
                        "title": title,
                        "url": notice_url,
                        "base_url": "https://www.dongguk.edu",
                        "notitype": notitype,
                        "description": description_html.prettify(),
                        "tdindex": title + description_html.get_text().replace("\n", ""),
                        "date": notice_date,
                        "imgs": imgs,
                        "links": links,
                        "attachments": attachments,
                        "univ_code": "DONGGUK",
                        "org_code": "MAIN",
                        "sub_code": "MAIN",
                    }
                    
                    try: 
                        Notice.objects.get(
                            notice_id=id,
                            univ_code="DONGGUK",
                            org_code="MAIN",
                            sub_code="MAIN",)
                    except Notice.DoesNotExist:
                        notice_object = Notice(**notice_data)
                        notice_object.save()
                        notices_list.append(notice_data)
                        print(f"Save to DB: {notice_url}\n")
                    print(f"Complete: {notice_url}")
                open(f"./data/{notitype}.json", "w", encoding="UTF-8").write(
                    json.dumps(notices_list, ensure_ascii=False, default=json_serial)
                )
                print(f"Complete: {url}")
            else:
                pprint(response)


if __name__ == "__main__":
    crawl_main_notices()
