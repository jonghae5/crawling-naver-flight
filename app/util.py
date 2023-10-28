# 네이버 항공권
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict, Any
from datetime import datetime
from logger import *


def get_diff_month():
    from datetime import datetime
    current_date = datetime.now()
    start_date = datetime(current_date.year+1, 2, 17)
    months_difference = abs((current_date.year - start_date.year) * 12 + (current_date.month - start_date.month))
    return months_difference


def retry(times, exceptions):
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    logger(__name__).info(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt += 1
            return func(*args, **kwargs)
        return newfn
    return decorator




def post_processing(res_list:list) -> List[Dict[str,Any]]:
    result_list = []
    temp_list = []

    for item in res_list:
        if "전체" in item:  # "전체" 문자열이 포함된 경우
            if temp_list:  # 빈 리스트가 아니면 결과 리스트에 추가
                temp_list.append(item)
                result_list.append(temp_list)
            temp_list = []  # 임시 리스트 초기화
        else:
            temp_list.append(item)

    # 마지막으로 미처 추가되지 않은 나머지 임시 리스트를 결과 리스트에 추가
    if temp_list:
        result_list.append(temp_list)



    직항_list = [res for res in result_list if "직항" in res[3] or "직항" in res[4]]

    result = []
    for value in 직항_list:
        _dict = {
            "항공사": value[0],
            "출발시간": value[1],
            "도착시간": value[2],
            "추가시간": value[3] if len(value) != 6 else "+0일",
            "소요시간": value[4] if len(value) != 6 else value[3],
            "결제수단": value[5] if len(value) != 6 else value[4],
            "가격": value[6] if len(value) != 6 else value[5]
        }
        result.append(_dict)
    return result


def convert_list_to_kakao_text(result:List[Dict[str,Any]]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    text = f"{today} 오늘의 비행권 \n\n"

    for res in result[:3]:
        temp =""
        temp += f'항공사 : {res["항공사"]}\n출발시간 : {res["출발시간"]}\n도착시간 : {res["도착시간"]}\n'
        temp += f'소요시간 : {res["소요시간"]}\n결제수단 : {res["결제수단"]}\n가격 : {res["가격"]}\n\n'
        text += temp
    return text
    