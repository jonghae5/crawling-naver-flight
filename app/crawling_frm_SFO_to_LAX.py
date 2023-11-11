from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from util import *
from logger import *

@retry(times=5, exceptions=(ValueError))
def crawling_naver_flight_from_SFO_to_LAX() -> list:

    try:
        url = "http://flight.naver.com/flights"

        START_DAY="17"
        END_DAY="1"
        START_POINT = "LAX"
        END_POINT= "SFO"

        DIFF_MONTH = get_diff_month()

        # 옵션 생성
        options = webdriver.ChromeOptions()
        # 창 숨기는 옵션 추가

        user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
        options.add_argument('user-agent=' + user_agent)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--single-process")
        #from webdriver_manager.chrome import ChromeDriverManager

        #service = Service(webdriver.Chrome(ChromeDriverManager().install()))
        #browser = webdriver.Chrome(service=service, options=options)
        browser = webdriver.Chrome(options=options)

    #     browser.maximize_window() # 창 최대화

        browser.get(url) 

        def wait_until_by_xpath(xpath_str):
            WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, xpath_str)))

        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "anchor")))
        # remove AD popup
        find = browser.find_elements(By.CLASS_NAME, "anchor")
        for f in find:
            if f.get_attribute("title") == "지금 바로 혜택 확인하기":
                browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[9]/div/div[2]/button[1]').click()
                logger(__name__).info("remove pop up")
                break

        wait_until_by_xpath('//button[text() = "가는 날"]')                  
        # push 가는 날 
        browser.find_element(By.XPATH, '//button[text() = "가는 날"]').click()
        time.sleep(3)

        # 날짜 정하기
        months = browser.find_elements(By.CSS_SELECTOR, ".sc-kDDrLX.ctbFvd.month")
        time.sleep(3)
        #wait_until_by_xpath(f'//b[text() = "{START_DAY}"]')
        months[0].find_elements(By.XPATH, f'//b[text() = "{START_DAY}"]')[DIFF_MONTH].click()
        time.sleep(3)
        #wait_until_by_xpath(f'//b[text() = "{END_DAY}"]')
        months[0].find_elements(By.XPATH, f'//b[text() = "{END_DAY}"]')[DIFF_MONTH +1].click()
        wait_until_by_xpath('//i[contains(text(), "다구간")]')
        browser.find_element(By.XPATH, '//i[contains(text(), "다구간")]').click()
        wait_until_by_xpath('//b[text() = "도착"]')
        browser.find_element(By.XPATH, '//b[text() = "도착"]').click()
        wait_until_by_xpath('//button[text() = "미주"]')
        browser.find_element(By.XPATH, '//button[text() = "미주"]').click()
        time.sleep(3)
        browser.find_element(By.XPATH, '//i[contains(text(), "LAX")]').click()
        time.sleep(3)
        browser.find_elements(By.XPATH, '//b[text() = "LAX"]')[1].click()
        time.sleep(3)
        browser.find_element(By.XPATH, '//button[text() = "미주"]').click()
        wait_until_by_xpath('//i[contains(text(), "SFO")]')
        browser.find_element(By.XPATH, '//i[contains(text(), "SFO")]').click()
        time.sleep(2)
        browser.find_element(By.XPATH, '//span[contains(text(), "항공권 검색")]').click()
        
        time.sleep(10)
        res = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".indivisual_results__3bdgf")))
        res_list = res.text.split("\n")
        #browser.quit()
    except:
        #browser.quit()
        raise ValueError("Crawling 에러입니다.")
    
    return res_list
