from urllib.request import Request, urlopen, URLError, HTTPError
import urllib.request
import json
import os
import datetime
from datetime import timedelta, timezone

def get_current_time():
    """
    Gets the current time in YYYY/MM/DD HH:MI:SS format.

    Returns:
    str: The current time in YYYY/MM/DD HH:MI:SS format.
    """

    # Seoul 시간대 객체 생성
    # seoul_timezone = pytz.timezone('Asia/Seoul')

    # 현재 시각을 Seoul 시간대로 가져옴
    # now = datetime.datetime.now(seoul_timezone)
    timezone(timedelta(hours=9))
    datetime.timezone(datetime.timedelta(seconds=32400))
    now = datetime.datetime.now( )    
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=32400)))
    now = datetime.datetime.now(timezone(timedelta(hours=9)))
    return now.strftime('%Y/%m/%d %H:%M:%S')


if __name__ == "__main__":  
    cur_time= get_current_time( )
    print(f"현재 날짜 : [{cur_time}]")
  