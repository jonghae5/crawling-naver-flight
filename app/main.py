from kakao import *
from util import *
from crawling import *
from logger import *


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

morning_trigger = CronTrigger(hour=9)
evening_trigger = CronTrigger(hour=18)
interval_trigger = IntervalTrigger(minutes=10)

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
    
if __name__ =="__main__":
    logger(__name__).info("System Start...")
    schedule = BlockingScheduler({'apscheduler.timezone':'Asia/seoul'})
    schedule.add_job(main, morning_trigger)
    schedule.add_job(main, evening_trigger)
    schedule.add_job(refresh_token, interval_trigger)
    #schedule.add_job(main, interval_trigger)
    schedule.start()
