import os
import json
from pprint import pprint

import boto3 
import time
from datetime import date, datetime

import urllib.request


# SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
# SLACK_CHANNEL     = os.environ.get('SLACK_CHANNEL')
# global SLACK_INCOMING_WEBHOOK
# global SLACK_CHANNEL




def init_slack_webhook( ):

    global SLACK_INCOMING_WEBHOOK
    global SLACK_CHANNEL
    
    
    client = boto3.client('secretsmanager')
    # response = client.list_secrets()
    # pprint(response['SecretList'])


    secret_name = os.getenv('SLACK_SECRET_NAME')  # 시크릿의 이름을 지정하세요.
    region_name = os.getenv('REGION')          # 시크릿 매니저가 있는 지역을 지정하세요.

    response = client.get_secret_value(
        SecretId=secret_name
    )
    slack_secrets = json.loads(response['SecretString'])
    pprint(slack_secrets)
    SLACK_INCOMING_WEBHOOK = slack_secrets['incoming_webhook']
    SLACK_CHANNEL          = slack_secrets['channel']

    print(f"SLACK_INCOMING_WEBHOOK[{SLACK_INCOMING_WEBHOOK}]")
    print(f"SLACK_CHANNEL[{SLACK_CHANNEL}]")

    return SLACK_INCOMING_WEBHOOK, SLACK_CHANNEL

def send_message(text, fields):
    print(f"send_message(text[{text}],\ntitle_url\n")
    pprint(fields)
    print(f"SLACK_INCOMING_WEBHOOK[{SLACK_INCOMING_WEBHOOK}]")
    print(f"SLACK_CHANNEL[{SLACK_CHANNEL}]")
    # url = SLACK_INCOMING_WEBHOOK
    # cur_time_str = get_current_time()

    # payload = {
    #     "username": "L2운영/T Biz Cloud",
    #     "channel": SLACK_CHANNEL,
    #     "icon_emoji": ":satellite:", # ":whale:" 
    #     "text" : text
    # }

    current_timestamp = int(time.time())

    payload = {
        "username": "L2운영/T Biz Cloud", # 보내는 사람 이름
        "channel": SLACK_CHANNEL,
        "icon_emoji": ":whale:",
        "attachments": [
            {
                "fallback": "Argos 자원 체크 결과",
                "pretext": "Argos 자원 체크 결과",
                "author_name": "L2운영/T Biz Cloud",
                "author_link": "https://app.datadoghq.com/dashboard/xus-d8b-sej/skcc-argos-tf?from_ts=1687671409331&to_ts=1687685809331&live=true",
                "author_icon": "https://docs.datadoghq.com/",
                "title": "Argos 자원 체크 결과.",
                "title_link": lambda_url,
                "text": "Argos 자원 체크 결과",
                "color": "#9733EE",
                "fields": [
                    {
                        "title": "시간",
                        "value": cur_time_str,
                        "short": "false",
                    },
                    {
                        "title": "상태",
                        "value": "OK!!!",
                        "short": "false",
                    },
                    {
                        "title": "운영 상황 체크!",
                        "value": text,
                        "short": "false",
                    }
                ],
                "image_url": "http://my-website.com/path/to/image.jpg",
                "thumb_url": "http://example.com/path/to/thumb.png",
                "footer": "L2운영/T Biz Cloud",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": current_timestamp
            }
        ]
    }
    print(f"payload[{payload}]")
    send_text = json.dumps(payload)
    print(f"send_text[{send_text}]")

    # Create the request object.
    request   = urllib.request.Request(
        SLACK_INCOMING_WEBHOOK, 
        data = send_text.encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    # Send the request.
    with urllib.request.urlopen(request) as response:
        slack_message = response.read()


if __name__ == "__main__":
    # boto3_helper.init_aws_session( )
    incoming_webhook, channel = init_slack_webhook()
    print(f">>>>> incoming_webhook[{incoming_webhook}], channel[{channel}]") 

    # send_message('Test', 'www.naver.com')