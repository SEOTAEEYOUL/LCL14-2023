import requests
import datadog_helper
from pprint import pprint

from datetime import timedelta, timezone
import datetime

import dydb_helper
import slack_helper

from alert_list import alert_list


def get_check_dtm():
    """
    Gets the current time in YYYY/MM/DD HH:MI:SS format.

    Returns:
    str: The current time in YYYY/MM/DD HH:MI:SS format.
    """

    # Seoul 시간대 객체 생성
    # seoul_timezone = pytz.timezone('Asia/Seoul')

    # 현재 시각을 Seoul 시간대로 가져옴
    # now = datetime.datetime.now(seoul_timezone)
    # timezone(timedelta(hours=9))
    # now = datetime.datetime.now( )
    now = datetime.datetime.now(timezone(timedelta(hours=9)))
    # return now.strftime('%Y/%m/%d %H:%M:%S')
    return now.strftime('%Y%m%d%H')




def check_status(monitor_id, headers):
    print(f"check_status({monitor_id})")


    # Set up the Datadog API endpoint
    url = f"https://api.datadoghq.com/api/v1/monitor/{monitor_id}"

    # Send the GET request to retrieve the monitor details
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        monitor_details = response.json( )
        # print(str(monitor_details) + "\n\n")
        # pprint(monitor_details)
        check_result_detail = monitor_details

        # Extract the monitor status
        name                   = monitor_details.get("name")
        priority               = monitor_details.get("priority")
        overall_state_modified = monitor_details.get("overall_state_modified")
        overall_state          = monitor_details.get("overall_state")

        # Check if the connection is up or down
        if overall_state == "OK":
            print(
                "# EventName: "
                + str(name)
                + "\n"
                + "# Priority: "
                + str(priority)
                + "\n"
                + "# Status: "
                + overall_state
                + "\n"
                + "# Status Modified: "
                + overall_state_modified
                + "\n"
            )
            check_result = 'Y'
        elif overall_state == 'No Data':
            check_result = 'D'
        else:
            print(f"Please Check the alert[{monitor_id}]")
            check_result = 'N'
    else:
        print("Failed to retrieve monitor details. Check your API keys and monitor ID.")
        check_result        = 'C'
        check_result_detail = { }

    return check_result, check_result_detail


def chk_monitor(lambda_url, table_name, no, monitor_id, dynamodb_key, check_dtm, headers):
    """
    Slack Message 생성 및 반환
    """
    print(f"chk_monitor(lambda_url[{lambda_url}], table_name[{table_name}], no[{no}], monitor_id[{monitor_id}], dynamodb_key[{dynamodb_key}], check_dtm[{check_dtm}]")




    # Call the function to check the DX connection status
    check_result, check_result_detail = check_status(monitor_id, headers)
    print(f"check_result[{check_result}]")
    # print(f"check_result_detail[{check_result_detail}]")

    # id               = check_result_detail.get('id')
    priority         = check_result_detail.get('priority')
    monitor_name     = check_result_detail.get('name')    

    # monitor_id       = '0' if id is None else str(id)
    monitor_priority = f"-" if priority is None else f"{priority}"

    # check_result_str = 'OK' if check_result == 'Y' else 'Not OK' if check_result == 'N' else '점검 오류'
    check_result_str = 'OK' if check_result == 'Y' else 'Not OK' if check_result == 'N' else 'No Data' if check_result == 'D' else '점검오류'


    return_code   = True
    # title         = f"{no}. {dynamodb_key}>{check_result_str}"
    title         = ""
    # check_dtm     = get_check_dtm( )
    check_url_str = f'{lambda_url}?check_dtm={check_dtm}&monitor_id={monitor_id}'
    # value         = f"`<{check_url_str}|상세점검결과보기>`"
    # value         = f"{no}. {monitor_id} `<{check_url_str}|{check_result_str}>`"
    # value         = f"{no}. {monitor_name} `<{check_url_str}|{check_result_str}>`"
    value         = f"{no}. {dynamodb_key} `<{check_url_str}|{check_result_str}>`"



    # { 'check_dtm':    'S' }
    # { 'monitor_id':   'S' }
    # { 'monitor_priority':  'S' }
    # { 'monitor_name': 'S' }
    # { 'check_result': 'S' }
    data = {
        'check_dtm': check_dtm,
        'monitor_id': '-' if monitor_id is None else str(monitor_id),
        'monitor_priority': monitor_priority,
        'monitor_name': '-' if monitor_name is None else monitor_name,
        'check_result': check_result_str
    }


    # resource_id = 'NETWORK-DX-01'
    result = dydb_helper.put_item(table_name, data, check_result_detail)
    if result:
        return_code   = True
    else:
        value         = f"~결과 저장 실패~"
        return_code   = False
        check_result  = 'F'

    # Send the message to Slack.
    # slack_helper.send_message(slack_msg, check_url_str)        

    # html_str = "SUCCESS"
    slack_dict = {
        # "title": title,
        "value": value,
        "short": "false"
    }

    # 'Y' : OK
    # 'N' : Not OK
    # 'D' : No Data
    # 'F' : DynamoDB Insert 오류

    return check_result, slack_dict

def check_alerts(lambda_url, table_name):
    slack_fields = []
    result_cnt   = {}
    check_dtm    = get_check_dtm( )

    datadog_helper.init_datadog_session( )
    api_key, app_key, public_id = datadog_helper.get_datadog_keys()

    # Set the headers with the API and application keys
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }
    print(f"headers[{headers}]")


    for alert in alert_list:
        no           = alert['no']
        monitor_id   = alert['monitor_id']       
        dynamodb_key = alert['dynamodb_key']
        print(f"{no}. Monitor ID: {monitor_id}, check_dtm:[{check_dtm}], dynamodb_key[{dynamodb_key}]")

        # "fields":[
        #     {
        #         "title":"자원 점검 수행",
        #         "value": text,
        #         "short": "false"
        #     }
        # ],
        check_result, result_dict = chk_monitor(lambda_url, table_name, no, monitor_id, dynamodb_key, check_dtm, headers)

        slack_fields.append(result_dict)
        check_result_str = 'OK' if check_result == 'Y' else 'Not OK' if check_result == 'N' else 'No Data' if check_result == 'D' else '점검오류'
        result_cnt[check_result_str] = result_cnt.get(check_result_str, 0) + 1


    text = "Argos 자원 점검수행[_"

    size = len(result_cnt)
    cnt  = 0
    for key, value in result_cnt.items( ):
        text += f"{key}:{value}"
        cnt += 1
        if cnt < size:
            text += ", "
            
    text += "_]"


    # Send the message to Slack.
    slack_helper.init_slack_webhook( )
    slack_helper.send_message(text, slack_fields)      

if __name__ == "__main__":
    # Enter the monitor ID associated with the DX connection status monitor
    monitor_id = "116390058"
    lambda_url = "https://uvr5meln3nmynytlbanfzg7j5u0mkbvn.lambda-url.ap-northeast-2.on.aws/"
    # Call the function to check the DX connection status
    # slack_helper.init_slack_webhook( )
    check_alerts(lambda_url, table_name)
