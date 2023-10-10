import os
import json
from pprint import pprint

import boto3 
from datetime import date, datetime, timedelta
import time

import datadog
# import datadog_api
# from datadog import api
# from datadog_api_client import ApiClient, Configuration
# from datadog_api_client.v1.api.organizations_api import OrganizationsApi



def get_datadog_keys( ):
    client = boto3.client('secretsmanager')
    # response = client.list_secrets()
    # pprint(response['SecretList'])


    secret_name = os.getenv('DD_SECRET_NAME')  # 시크릿의 이름을 지정하세요.
    region_name = os.getenv('REGION')          # 시크릿 매니저가 있는 지역을 지정하세요.
    table_name  = os.getenv('DYNAMODB_TABLE_NAME')

    print(f"secret_name[{secret_name}], region_name[{region_name}], table_name[{table_name}]")
    response = client.get_secret_value(
        SecretId=secret_name
    )
    dd_secrets = json.loads(response['SecretString'])
    pprint(dd_secrets)
    api_key = dd_secrets['api_key']
    app_key = dd_secrets['app_key']
    public_id = dd_secrets['public_id']

    print(f"api_key[{api_key}], app_key[{app_key}], public_id[{public_id}]")

    return api_key, app_key, public_id




# Boto3 세션 을 초기화하고 객체를 사용자에게 반환
def init_datadog_session():
    api_key, app_key, public_id = get_datadog_keys()

    # API 키와 애플리케이션 키를 설정합니다.
    options = {
        "api_key": api_key,
        "app_key": app_key,
    }

    datadog.initialize(**options)

    
    os.environ['DD_SITE']    = 'datadoghq.com'
    os.environ['DD_API_KEY'] = api_key
    os.environ['DD_APP_KEY'] = app_key

    # return api_key, app_key


# def get_alert_count( ):
#     # 조회할 기간 설정
#     start_time = datetime(2023, 7, 1, 12, 0, 0)
#     end_time = datetime(2023, 7, 3, 12, 0, 0)

#     # 타임스탬프로 변환
#     start_timestamp = int(time.mktime(start_time.timetuple()))
#     end_timestamp = int(time.mktime(end_time.timetuple()))

#     # Alert 조회 쿼리
#     query = 'status:open'  # 필요에 따라 쿼리를 조정할 수 있습니다.


#     # Alert 조회
#     response = datadog.api.Event.query(start=start_timestamp, end=end_timestamp, priority='normal', tags=['alert'], sources=['*'], unaggregated=True)

#     # 조회된 Alert 수 출력
#     print(f"조회된 Alert 수: {len(response['events'])}")

#     # 조회된 Alert 정보 출력
#     for event in response['events']:
#         print(f"Alert: {event['title']}, 상태: {event['alert_type']}")

# import requests
# def get_alert_count2(api_key):
#     # Set the Datadog API key and the start and end times.
#     start_time = "2023-07-02T12:00:00Z"
#     end_time = "2023-07-03T09:00:00Z"

#     # Make a request to the Datadog API to get the list of alerts.
#     url = "https://api.datadoghq.com/api/v1/alerts?start_time=" + start_time + "&end_time=" + end_time
#     headers = {
#         "Authorization": "Bearer " + api_key,
#         "Content-Type": "application/json",
#     }

#     response = requests.get(url, headers=headers)

#     # Check the response status code.
#     if response.status_code == 200:
#         # The request was successful.
#         alerts = json.loads(response.content)

#         # Count the number of alerts.
#         alert_count = len(alerts)

#         print("The number of alerts is:", alert_count)
#     else:
#         # The request failed.
#         print("The request failed with status code:", response.status_code)


# def get_alert_count3(api_key):
#     start_time = "2023-07-02T12:00:00Z"
#     end_time = "2023-07-03T09:00:00Z"

#     # Create a Datadog client.
#     client = datadog_api.Client(api_key)

#     # Get the list of alerts.
#     alerts = client.get_alerts(start_time=start_time, end_time=end_time)

#     # Count the number of alerts.
#     alert_count = len(alerts)

#     # Print the number of alerts.
#     print("The number of alerts is:", alert_count)

if __name__ == "__main__":
    # boto3_helper.init_aws_session( )
    api_key, app_key, public_id = init_datadog_session( )
    # api_key, app_key, public_id = get_datadog_keys( )
    get_alert_count( )
    get_alert_count2(api_key)
    get_alert_count3(api_key)