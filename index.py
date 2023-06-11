import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
baseUrl = "https://oversystem.co.kr"

def replaceTrash(n):
    n = n.replace("\t", "")
    n = n.replace("\n", "")
    return n.strip()

def home():
    print("-----------------------------------\n명령어 목록:\nSearch : 부품을 검색 하여 부품 정보를 얻을 수 있습니다.\nExit : 프로그램 종료\n-----------------------------------")
    eval(f"{input('입력 : ').lower()}()")

def search():
    search_term = input("\n\n\n\n\n검색하실 키워드를 입력 해 주세요. (사이트에 피해가 가지 않도록 1페이지만 탐색합니다.)\n입력 : ")
    print(f"로딩 중...")
    browser.get(f'{baseUrl}/stuff/stuff_search_list/0?keyword={search_term}')
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.link-primary.fs-5')))

    soup = BeautifulSoup(browser.page_source, "html.parser")
    items = soup.find_all('div', class_="SearchStuffInfor row")
    print(f"로딩 완료 ! ({len(items)}개의 상품)\n")
    time.sleep(2)
    print("\n\n\n\n\n-----------------------------------")
    for item in items:
        info = {
            'name': replaceTrash(item.find('a', class_="link-primary fs-5").get_text(strip=True)),
            'spec': replaceTrash(item.find('h6', class_="StuffPerfor").get_text(strip=True)),
            'code': replaceTrash(item.find('h6', class_="StuffCode").find('small').get_text(strip=True).replace("상품코드 : ", "")),
            'price': replaceTrash(item.find('text', class_="stuff_card_pay").get_text(strip=True).replace("판매가 : ", "")),
            'link' : f'{baseUrl}{replaceTrash(item.find("a", class_="link-primary fs-5")["href"])}'
        }
        print(f"\n이름 :\n{info['name']}\n\n스펙 :\n{info['spec']}\n\n상품코드 :\n{info['code']}\n\n가격 :\n{info['price']}\n\n바로가기 :\n{info['link']}\n\n-----------------------------------")
    print("\n\n")
    if input("이어서 검색 하시겠습니까? (y/n)\n입력 : ").lower()=="y":
        search()
    else:
        print("\n\n\n\n\n")
        home()
home()