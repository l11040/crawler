import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import pandas as ps

prd_list = {
    "아이폰 13": "https://m.bunjang.co.kr/search/products?category_id=600700001&order=score&q=%EC%95%84%EC%9D%B4%ED%8F%B0%2013",
    # "아이폰 13 pro": "https://m.bunjang.co.kr/search/products?category_id=600700001&order=score&q=%EC%95%84%EC%9D%B4%ED%8F%B0%2013%20pro",
    # "아이폰 14": "https://m.bunjang.co.kr/search/products?category_id=600700001&order=score&q=%EC%95%84%EC%9D%B4%ED%8F%B0%2014",
    # "아이폰 14 pro": "https://m.bunjang.co.kr/search/products?category_id=600700001&order=score&q=%EC%95%84%EC%9D%B4%ED%8F%B0%2014%20pro",
    # "에어팟 프로": "https://m.bunjang.co.kr/search/products?category_id=600500010&order=score&q=%EC%97%90%EC%96%B4%ED%8C%9F%20%ED%94%84%EB%A1%9C",
    # "에어팟 프로 2": "https://m.bunjang.co.kr/search/products?category_id=600500010&order=score&q=%EC%97%90%EC%96%B4%ED%8C%9F%20%ED%94%84%EB%A1%9C%202"
}


def product_detail_crawling(url, prd_id):
    browser.get(url)
    html = browser.page_source
    html_parser = BeautifulSoup(html, features="html.parser")

    # 판매완료인 경우
    done_text = ""
    try:
        done_text = html_parser.find(attrs={'class': 'hlRccl'}).get_text()
    except:
        done_text = ""
    if done_text == "이미 거래가 완료된 상품이네요":
        uri = html_parser.find(attrs={'class': 'cPixsD'}).attrs['href']
        url = "https://m.bunjang.co.kr{}".format(uri)
        browser.get(url)
        html = browser.page_source
        html_parser = BeautifulSoup(html, features="html.parser")

    title = html_parser.find(attrs={'class': 'gYcooF'}).get_text()
    price = html_parser.find(attrs={'class': 'dJuwUw'}).get_text()

    prd_summary_list = html_parser.find_all(
        attrs={'class': 'ProductSummarystyle__Row-sc-oxz0oy-18'})

    prd_Status = prd_summary_list[0].get_text(
        separator=';;;').split(sep=';;;')[1]

    prd_location = prd_summary_list[3].get_text(
        separator=';;;').split(sep=';;;')[1]

    detail = html_parser.find(attrs={'class': 'eJCiaL'}).get_text()

    prd_summary_list2 = html_parser.find_all(
        attrs={'class': 'cecDFG'})
    like_count = prd_summary_list2[0].get_text()
    view_count = prd_summary_list2[1].get_text()
    upload_date = prd_summary_list2[2].get_text()

    img_link = html_parser.find(
        attrs={'class': 'NhTxc'}).find('img').attrs['src']

    Subject.append(title)
    ProductId.append(prd_id)
    Price.append(price)
    Status.append(prd_Status)
    Location.append(prd_location)
    Like.append(like_count)
    View.append(view_count)

    now = datetime.datetime.now()

    if "초 전" in upload_date:
        upload_date = now.strftime('%Y-%m-%d')
    if "분 전" in upload_date:
        upload_date = now.strftime('%Y-%m-%d')
    if "시간 전" in upload_date:
        upload_date = now.strftime('%Y-%m-%d')
    if "일 전" in upload_date:
        day = int(upload_date.replace("일 전", ""))
        now = now + datetime.timedelta(days=-1 * day)
        upload_date = now.strftime('%Y-%m-%d')
        print(upload_date)
    if "주 전" in upload_date:
        week = int(upload_date.replace("주 전", ""))
        now = now + datetime.timedelta(weeks=-1 * week)
        upload_date = now.strftime('%Y-%m-%d')
        print(upload_date)
    if "달 전" in upload_date:
        month = int(upload_date.replace("달 전", ""))
        now = now + relativedelta(months=-1 * month)
        upload_date = now.strftime('%Y-%m-%d')
        print(upload_date)

    Date.append(upload_date)
    Detail.append(detail)
    Link.append(url)
    ImgLink.append(img_link)
    return


def product_crawling(url):
    page_num = 1
    while True:
        pagenation_url = url+"&page="+str(page_num)
        browser.get(pagenation_url)

        WebDriverWait(browser, 10).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, "app")))
        html = browser.page_source
        html_parser = BeautifulSoup(html, features="html.parser")

        none_text = html_parser.find(attrs={'class': 'lcPjKn'})
        if none_text != None:
            return

        list = html_parser.find_all(attrs={'alt': '상품 이미지'})

        for item in list:
            try:
                aTag = item.parent.parent
                for i, c in enumerate(aTag.children, 0):
                    if i == 1:
                        infor = c.get_text(separator=';;;')
                        infor = infor.split(sep=';;;')
                        if infor[2] == "AD":
                            break
                        detail_url = "https://m.bunjang.co.kr{}".format(
                            aTag.attrs['href'])
                        prd_id = aTag.attrs['data-pid']
                        product_detail_crawling(detail_url, prd_id)
            except:
                continue
        page_num = page_num+1
    return


def main():
    browser.implicitly_wait(time_to_wait=10)
    browser.get('https://m.bunjang.co.kr/')

    for product, url in prd_list.items():
        product_crawling(url)
    return


ProductId = []
Subject = []
Price = []
Status = []
Location = []
Like = []
View = []
Date = []
Detail = []
Link = []
ImgLink = []

browser = webdriver.Chrome()
main()

Datas = {
    "prd_id": ProductId,
    "subject": Subject,
    "price": Price,
    "status": Status,
    "location": Location,
    "like": Like,
    "view": View,
    "date": Date,
    "detail": Detail,
    "link": Link,
    "img_link": ImgLink
}
print(Datas)
DataTable = ps.DataFrame(Datas)
DataTable.to_csv('csv/data.csv', encoding='utf-8-sig')

print(DataTable)
