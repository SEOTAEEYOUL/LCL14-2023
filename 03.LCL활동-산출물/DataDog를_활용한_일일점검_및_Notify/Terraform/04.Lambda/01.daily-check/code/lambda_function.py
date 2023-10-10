from urllib.request import Request, urlopen, URLError, HTTPError
import urllib.request
import urllib.parse
import json
import os
import datetime
import time
from datetime import timedelta, timezone
from pprint import pprint
# import pytz

import boto3
from botocore.exceptions import ClientError

import boto3
import datadog
# import datadog_api_client

# import boto3_helper
import datadog_helper
import datadog_alert
# import slack_helper

# import dd_dx_connection
import dydb_helper



AWS_REGION             = os.environ.get('REGION')
DYDB_TABLE_NAME        = os.environ.get('DYNAMODB_TABLE_NAME')
S3_BUCKET_NAME         = os.environ.get('S3_BUCKET_NAME')
s3_url                 = os.environ.get('S3_URL')
s3_aws_logo_url        = os.environ.get('S3_AWS_LOGO_URL')
s3_title_icon_url      = os.environ.get('S3_TITLE_ICON_URL')


print(f"AWS_REGION[{AWS_REGION}]")


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
    # timezone(timedelta(hours=9))
    # now = datetime.datetime.now( )
    now = datetime.datetime.now(timezone(timedelta(hours=9)))
    return now.strftime('%Y/%m/%d %H:%M:%S')



def s3_get_html(s3_bucket_name, s3_object_key):
    print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]")
    # S3 객체를 읽어옴
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket_name, s3_object_key)
    html_content = obj.get()['Body'].read().decode('utf-8')
    # print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]\nhtml_content[{html_content}]")

    return html_content



# 쿼리 결과를 테이블 형태로 변환하는 함수
def create_html_table(item):
    if item == None:
        table_html = '<table  class="custom-table">\n'

        # 테이블 행 생성
        table_html += '<tr><th>Check DTM</th><td>-</td></tr>\n'
        table_html += '<tr><th>Monitor ID</th><td>-</td></tr>\n'
        table_html += '<tr><th>Monitor Name</th><td>-</td></tr>\n'
        table_html += '<tr><th>Monitor Priority</th><td>-</td></tr>\n'
        table_html += '<tr><th>Check Result</th><td>-</td></tr>\n'
        table_html += '<tr><th>Check Result Detail</th><td><pre> { } </pre></td></tr>\n'
        
        
        table_html += '</table>\n'

        return table_html
    
    # print(f'create_html_table[{item}]')

    # { 'check_dtm':    'S' }
    # { 'monitor_id':   'S' }
    # { 'monitor_priority':  'S' }
    # { 'monitor_name': 'S' }
    # { 'check_result': 'S' }
    table_html = '<table class="custom-table">\n'
    
    check_dtm           = item['check_dtm']['S']
    monitor_id          = item['monitor_id']['S']
    monitor_name        = item['monitor_name']['S']
    monitor_priority    = item['monitor_priority']['S']
    check_result        = item['check_result']['S']
    check_result_detail = item['check_result_detail']['S']

    # check_result_str = 'OK' if check_result == 'Y' else 'Not OK' if check_result == 'N' else '점검 오류'
    # check_result_str = 'OK' if check_result == 'Y' else 'Not OK' if check_result == 'N' else 'No Data' if check_result == 'D' else '점검오류'

    # print(f"{check_result_detail}")

    # 테이블 행 생성
    table_html += f'<tr> <th>Check DTM</th> <td><pre>{check_dtm}</pre></td> </tr>\n'
    table_html += f'<tr> <th>Monitor ID</th> <td><pre>{monitor_id}</pre></td> </tr>\n'
    table_html += f'<tr> <th>Monitor Name</th> <td><pre>{monitor_name}</pre></td> </tr>\n'
    table_html += f'<tr> <th>Monitor Priority</th> <td><pre>{monitor_priority}</pre></td> </tr>\n'
    table_html += f'<tr> <th>Check Result</th> <td><pre>{check_result}</pre></td> </tr>\n'
    table_html += f'<tr> <th>Check Result Detail</th> <td><pre>{check_result_detail}</pre></td> </tr>\n'
    
    
    table_html += '</table>\n'

    # print(f"table_html[{table_html}]")
    return table_html

def dynamodb_get_html(table_name, check_dtm, monitor_id):
    print(f"dynamodb_get_html(table_name[{table_name}], check_dtm[{check_dtm}], monitor_id[{monitor_id}])")
    
    # DynamoDB 테이블과 S3 버킷 설정
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table(table_name)
    
    # 오늘 날짜를 가져옴 (YYYY-MM-DD 형식)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"dynamodb_get_html(table_name[{table_name}])")

    item = dydb_helper.get_item(table_name, check_dtm,  monitor_id)

    # 쿼리 결과를 테이블 형태로 변환하여 HTML 템플릿에 삽입
    table_html = create_html_table(item)

    return table_html


def s3_get_html(s3_bucket_name, s3_object_key):
    print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]")
    # S3 객체를 읽어옴
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket_name, s3_object_key)
    html_content = obj.get()['Body'].read().decode('utf-8')
    print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]\nhtml_content[{html_content}]")

    return html_content


def lambda_handler(event, context):
    """
    Lambda function handler.

    Args:
        event (dict): The event object.
        context (dict): The context object.
    """
    # boto3_helper.init_aws_session( )
    datadog_helper.init_datadog_session( )
    # slack_helper.init_slack_webhook( )

    print('## ENVIRONMENT VARIABLES')
    print(os.environ['AWS_LAMBDA_LOG_GROUP_NAME'])
    print(os.environ['AWS_LAMBDA_LOG_STREAM_NAME'])
    print('## EVENT')
    
    print(event)
    print(json.dumps(event, indent=2))

    # DynamoDB 테이블 정보
    dynamodb_table_name = "dynamodb_system_check_lcl14"
    # # dynamodb_key        = "index.html"
    # dynamodb_key        = "NETWORK-DX-01"
    # # Enter the monitor ID associated with the DX connection status monitor
    # monitor_id          = "116390058"


    html_str     = ''
    cur_time_str = get_current_time( )

    if 'lambda_url' in event:
        # print(event['lambda_url'])
        lambda_url    = event['lambda_url']

        datadog_alert.check_alerts(lambda_url, DYDB_TABLE_NAME)

        html_str = 'SUCCESS'

    else:
        if 'queryStringParameters' in event:
            # URL 파라미터를 가져오기 위해 "queryStringParameters" 키로부터 값을 추출합니다.
            params        = event.get('queryStringParameters', {})
            print("==================================")
            print(params)

            check_dtm  = params['check_dtm']
            monitor_id = params['monitor_id']
            print(f"check_dtm[{check_dtm}] monitor_id[{monitor_id}] ")

            # S3 버킷 및 파일 정보
            # s3_bucket_name = "s3-bucket-lcl14"
            s3_object_key  = "template/resource_check.html"
            html_template  = s3_get_html(S3_BUCKET_NAME, s3_object_key)
            
            table_html     = dynamodb_get_html(DYDB_TABLE_NAME, check_dtm, monitor_id)
            # cur_time_str = get_current_time()

            html_str = html_template.replace('{{s3_title_icon_url}}', s3_title_icon_url).replace('{{s3_aws_logo_url}}', s3_aws_logo_url).replace('{{table_content}}', table_html).replace('{{date}}', check_dtm).replace('{{monitor_id}}', monitor_id)

            print("++++++++++++++++++++++++++++++++++")
            html_str_size = len(html_str)
            print(f"html_str 의 크기[{html_str_size}]")
            print(html_str)
            print("++++++++++++++++++++++++++++++++++")
        else:
            title         = "일일 자원 점검 수행 오류"
            inner_status  = "Opps! 인자 전달 오류!"
            inner_detail  = "Query String 이 들어 오지 않았습니다"
            html_template = s3_get_html(S3_BUCKET_NAME, "template/error.html")
            html_str      = html_template.replace('{{timestamp}}', cur_time_str).replace('{{title}}', title).replace('{{inner-status}}', inner_status).replace('{{inner-detail}}', inner_detail)

    # Return a response if needed
    return {
        'statusCode' : 200,
        'body': html_str,
        'headers': {'Content-Type': 'text/html'}
    }




if __name__ == "__main__":    
    datadog_helper.init_datadog_session( )
    slack_helper.init_slack_webhook( )


    # S3 버킷 및 파일 정보
    s3_bucket_name = "s3-bucket-lcl14"
    
    # DynamoDB 테이블 정보
    dynamodb_table_name = "dynamodb_system_check_lcl14"
    # dynamodb_key        = "index.html"
    # dynamodb_key        = "NETWORK-DX-01"
    # Enter the monitor ID associated with the DX connection status monitor
    # monitor_id          = "116390058"
    # Call the function to check the DX connection status
    check_result, check_result_detail = datadog_alert.check_alerts( )

    print(f"check_result[{check_result}]")
    print(f"check_result_detail[{check_result_detail}]")

    resource_id = dynamodb_key
    check_dtm  = get_current_time( )
    table_name = os.environ.get('DYNAMODB_TABLE_NAME')

    result = dydb_helper.put_item(table_name, resource_id, check_dtm, check_result, check_result_detail)
    if result:
        message = f"resource_id[{resource_id}] 에 대한 검사 및 DynamoDB 저장소 저장 성공 - check_dtm[{check_dtm}]"
        return_code = "SUCCESS"
    else:
        message = f"resource_id[{resource_id}] 에 대한 검사 및 DynamoDB 저장소 저장 실패"
        return_code = "Fail"
    
    print(f"send_message_to_slack({message})")
    slack_helper.send_message(message, 'https://uvr5meln3nmynytlbanfzg7j5u0mkbvn.lambda-url.ap-northeast-2.on.aws/')
    

    table_name="dynamodb_system_check_lcl14"
    dydb_helper.get_items(table_name)

