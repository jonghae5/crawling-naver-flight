from kakao import *
from util import *
from crawling import *
from logger import *
from crawling_2 import *

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


def main():
    logger(__name__).info("Crawling start")
    crawling_data = crawling_naver_flight()
    logger(__name__).info("Crawlingcomplele")
    logger(__name__).info("post processing")
    post_processing_data = post_processing(crawling_data)
    text_data = convert_list_to_kakao_text(post_processing_data)
    kakao = Kakao()
    kakao.send_to_kakao(text_data)
def main_2():
    logger(__name__).info("Crawling start")
    crawling_data = crawling_naver_flight_2()
    logger(__name__).info("Crawlingcomplele")
    logger(__name__).info("post processing")
    post_processing_data = post_processing(crawling_data)
    text_data = convert_list_to_kakao_text(post_processing_data)
    kakao = Kakao()
    kakao.send_to_kakao(text_data)    
if __name__ =="__main__":
    logger(__name__).info("System Start...")
    schedule = BlockingScheduler({'apscheduler.timezone':'Asia/seoul'})
    schedule.add_job(main, morning_trigger)
    schedule.add_job(main, evening_trigger)
    schedule.add_job(main_2, morning_trigger_2)
    schedule.add_job(main_2, evening_trigger_2)

    schedule.add_job(refresh_token, interval_trigger)
    #schedule.add_job(main_2, test_trigger)
    schedule.start()
