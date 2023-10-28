import requests
import json
from datetime import datetime
import os
from logger import *

from dotenv import load_dotenv

load_dotenv(verbose=True)

API_KEY = os.getenv('API_KEY')

class Kakao():
    def __init__(self):
        self.app_key = API_KEY ## REST API 키 입력 
        # 저장 된 json 파일 읽어오기
        with open(f"{os.getcwd()}/app/kakao_token.json", "r") as fp:
            self.tokens = json.load(fp)
            self.refresh_token()
            now = datetime.now().strftime("%Y%m%d%H%M")
            logger(__name__).info("Refresh Token ..." + now)


    # 카카오 토큰 갱신하기
    def refresh_token(self):
        url = "https://kauth.kakao.com/oauth/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
        "grant_type": "refresh_token",
        "client_id": self.app_key,
        "refresh_token": self.tokens['refresh_token']
        }

        response = requests.post(url, data=data, headers=headers)

        # 갱신 된 토큰 내용 확인
        result = response.json()
        logger(__name__).info(result)
        # 갱신 된 내용으로 파일 업데이트
        if 'access_token' in result:
            self.tokens['access_token'] = result['access_token']

        if 'refresh_token' in result:
            self.tokens['refresh_token'] = result['refresh_token']
        else:
            pass

        with open(f"{os.getcwd()}/app/kakao_token.json", "w") as fp:
            json.dump(self.tokens, fp)

    def send_to_kakao(self, text):
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {"Authorization": "Bearer " + self.tokens['access_token']}
        content = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://flight.naver.com/",
            "mobile_web_url": "https://flight.naver.com/"
        },
        "button_title": "확인"
        }
        

        data = {"template_object": json.dumps(content)}
        now = datetime.now().strftime("%Y%m%d%H%M")
        try:
            res = requests.post(url, headers=headers, data=data)
            logger(__name__).info("메세지가 성공적으로 전달되었습니다." + now)
        except:
            logger(__name__).info("에러가 발생했습니다." + now)
        ## 에러메시지 확인
        res.json()