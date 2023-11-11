from kakao import *
from util import *
from app.crawling_frm_SFO_to_LAX import *
from logger import *
from app.crawling_frm_LAX_to_SFO import *

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

morning_trigger = CronTrigger(hour=9)
evening_trigger = CronTrigger(hour=18)
morning_trigger_2 = CronTrigger(hour=10)
evening_trigger_2 = CronTrigger(hour=19)
interval_trigger = IntervalTrigger(minutes=30)
test_trigger = IntervalTrigger(seconds=30)


def refresh_token():
    kakao = Kakao()
    return


def main_LAX_SFO():
    logger(__name__).info("Crawling start")
    crawling_data = crawling_naver_flight_from_LAX_to_SFO()
    logger(__name__).info("Crawlingcomplele")
    logger(__name__).info("post processing")
    post_processing_data = post_processing(crawling_data)
    text_data = convert_list_to_kakao_text(post_processing_data)
    kakao = Kakao()
    kakao.send_to_kakao(text_data)
def main_SFO_LAX():
    logger(__name__).info("Crawling start")
    crawling_data = crawling_naver_flight_from_SFO_to_LAX()
    logger(__name__).info("Crawlingcomplele")
    logger(__name__).info("post processing")
    post_processing_data = post_processing(crawling_data)
    text_data = convert_list_to_kakao_text(post_processing_data)
    kakao = Kakao()
    kakao.send_to_kakao(text_data)    
if __name__ =="__main__":
    logger(__name__).info("System Start...")
    schedule = BlockingScheduler({'apscheduler.timezone':'Asia/seoul'})
    schedule.add_job(main_LAX_SFO, morning_trigger)
    schedule.add_job(main_LAX_SFO, evening_trigger)
    schedule.add_job(main_SFO_LAX, morning_trigger_2)
    schedule.add_job(main_SFO_LAX, evening_trigger_2)

    schedule.add_job(refresh_token, interval_trigger)
    #schedule.add_job(main_2, test_trigger)
    schedule.start()
