from urllib.request import Request, urlopen, URLError, HTTPError
import urllib.request
import json
import os
# import datetime
import time
from datetime import datetime, timedelta, timezone
# import pytz

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
# from boto3.dynamodb.conditions import Key  # 조건이 항목의 키와 관련된 경우 사용
# from boto3.dynamodb.conditions import Attr # 조건이 항목의 속성과 관련된 경우 사용

# import dydb_helper
# import slack_helper

from pprint import pprint


# AWS_REGION        = os.environ.get('AWS_REGION')
SLACK_WEBHOOK_URL     = os.environ.get('SLACK_WEBHOOK_URL')
SLACK_CHANNEL         = os.environ.get('SLACK_CHANNEL')
LAMBDA_COLLECTION_URL = os.environ.get('LAMBDA_COLLECTION_URL')

dydb_system_check_name = os.environ.get('DYDB_SYSTEM_CHECK_NAME')
dydb_alert_list_name   = os.environ.get('DYDB_ALERT_LIST_NAME')

s3_url                 = os.environ.get('S3_URL')
s3_aws_logo_url        = os.environ.get('S3_AWS_LOGO_URL')
s3_title_icon_url      = os.environ.get('S3_TITLE_ICON_URL')

slack_mag              = "매우 중요한 알림이 있습니다!"
result                 = "<H1>매우 중요한 알림이 있습니다!</H1>"

print(f"SLACK_WEBHOOK_URL[{SLACK_WEBHOOK_URL}]")
print(f"SLACK_CHANNEL[{SLACK_CHANNEL}]")


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
    now = datetime.now(timezone(timedelta(hours=9)))
    return now.strftime('%Y/%m/%d %H:%M:%S')

def send_message_to_slack(text, lambda_url):
    print(f"text[{text}]")
    # url = "https://hooks.slack.com/services/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"
    url = SLACK_WEBHOOK_URL
    cur_time_str = get_current_time()

    # payload = {
    #     "username": "L2운영/T Biz Cloud",
    #     "channel": SLACK_CHANNEL,
    #     "icon_emoji": ":whale:", # ":satellite:"
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
        url, 
        data = send_text.encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    # Send the request.
    with urllib.request.urlopen(request) as response:
        slack_message = response.read()

def send_to_slack(message, webhookurl):
    slack_message = message
    req = Request(webhookurl, data=json.dumps(slack_message).encode("utf-8"),
                  headers={'content-type': 'application/json'})
    try:
        response = urlopen(req)
        response.read()
    except HTTPError as e:
        print("Request failed : ", e.code, e.reason)
    except URLError as e:
        print("Server connection failed: ", e.reason, e.reason)

def s3_get_html(s3_bucket_name, s3_object_key):
    print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]")
    # S3 객체를 읽어옴
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket_name, s3_object_key)
    html_content = obj.get()['Body'].read().decode('utf-8')
    # print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]\nhtml_content[{html_content}]")

    return html_content

# 쿼리 결과를 테이블 형태로 변환하는 함수
def create_html_table(items):
    # item_cnt = {
    #     'Y' : 0,
    #     'N' : 0,
    #     'C' : 0,
    #     'D' : 0
    # }
    item_cnt = {
        'OK' : 0,
        'Not OK' : 0,
        '점검오류' : 0,
        'No Data' : 0
    }

    row = 0
    # print(f'create_html_table[{items}]')
    table_html = '<table class="type09">\n'
    table_html += '<thead>\n'
    table_html += '<tr>\n'
    table_html += '<th scope="cols">No.</th>'
    table_html += '<th scope="cols">Check DTM</th>'
    table_html += '<th scope="cols">Monitor ID</th>'
    table_html += '<th scope="cols">Check Result</th>'
    table_html += '<th scope="cols">Name</th>'
    table_html += '<th scope="cols">Priority</th>'
    table_html += '<th scope="cols">Query</th>'
    table_html += '<th scope="cols">Check Detail</th>'
    table_html += '</tr>\n'
    table_html += '</thead>\n'
    table_html += '<tbody>\n'
    for item in items:
        row += 1
        check_dtm   = item['check_dtm']
        monitor_id  = item['monitor_id']
        # 다른 열 데이터도 필요한 경우 해당 열의 키를 가져와서 item에서 값을 추출
        check_result = item['check_result']
        # check_result_str = 'OK' if check_result == 'Y' else 'Not OK' if check_result == 'N' else 'No Data' if check_result == 'D' else '점검오류'
        check_result_str = f'<span class=ok> {check_result} </span>' if check_result == 'OK' else f'<span class=notok> {check_result} </span>' if check_result == 'Not OK' else f'<span class=orange> {check_result} </span>' if check_result == '점검오류' else f'<span class=gray> {check_result} </span>'
        check_result_detail = item['check_result_detail']
        print(f"check_dtm[{check_dtm}], monitor_id[{monitor_id}], check_result[{check_result}]")
        
        item_cnt[check_result] += 1

        # monitor_details = check_result_detail.json()
        if isinstance(check_result_detail, str):
            monitor_details = json.loads(check_result_detail)
        else:
            monitor_details = check_result_detail

        # Extract the monitor status
        name                   = monitor_details.get("name")
        priority               = monitor_details.get("priority")
        overall_state_modified = monitor_details.get("overall_state_modified")
        query                  = monitor_details.get("query")
        tags                   = monitor_details.get("tags")

        monitor = '-'
        if tags is None:
            # print(f"table_html[{table_html}]")
            # return item_cnt, table_html
            continue

        for tag in tags:
            # if "team:" in tag:
            #     team = tag.split(":")[1].strip( )
            #     # print(f">> team:{team}")
            #     result_sheet.write(row, 2, team, string_format)
            #     is_found = True
            if "monitor:" in tag:
                monitor = tag.split(":")[-1].strip( )
                print(f">> monitor:{monitor}")

        result_detail_str = f"- name: {name}\n- overall_state_modified : {overall_state_modified}\n- query: {query}\n- monitor: {monitor}"
        
        # 테이블 행 생성
        row_html  = '<tr>\n'
        row_html += f'<th scope="row">{row}</th>\n'
        row_html += f'<td> {check_dtm} </td>\n'        
        # row_html += f'<td> <span class=olive>{monitor_id}</span> </td>\n'
        row_html += '<td>'
        row_html += f'<span class=ok>{monitor_id}</span>' if check_result == 'OK' else f'<span class=notok>{monitor_id}</span>' if check_result == 'Not OK' else f'<span class=error>{monitor_id}</span>' if check_result == '점검오류' else f'<span class=gray>{monitor_id}</span>'
        # s3_url = 'https://s3-lcl14-bucket-is07456.s3.ap-northeast-2.amazonaws.com/icon'

        icon = 'Amazon_Web_Services_Logo.png'
        
        if name is not None:
            if 'DB' in name:
                icon = 'RDS-Instance.png'
                if 'MySQL' in name:
                    # icon = 'MySQL-Instance.png'
                    icon = 'mysql_logo_black.png'
                elif 'MariaDB' in name:
                    # icon = 'MariaDB-Instance.png'
                    icon = 'mariadb_icon.png'
            elif 'Container' in name:
                icon = 'kubernetes_logo.png'
                if 'EKS' in name:
                    icon = 'EKS.png'
                    if 'POD' in name or 'Pod' in name:
                        icon = 'k8s-pod.png'                    
                    elif 'Node' in name or '노드' in name:
                        icon = 'k8s-node.png'
                    elif 'ALB' in name:
                        icon = 'k8s-ing.png'
                    elif 'Deployment' in name:
                        icon = 'k8s-deploy.png'
                    elif 'Statefulset' in name:
                        icon = 'k8s-sts.png'
                    elif 'Daemonset' in name:
                        icon = 'k8s-ds.png'
                    elif 'job' in name:
                        icon = 'k8s-cronjob.png'
                    elif 'OOM' in name:
                        icon = 'oom-out-memory.jpg'
                    elif 'Full GC' in name:
                        icon = 'Garbage_collector_Duke.png'
            elif 'System' in name or 'SYSTEM' in name:
                icon = 'EC2_Instance.png'
                if 'Host' in name or 'EC2' in name:
                    icon = 'EC2_Instance.png'
                elif 'S3' in name:
                    icon = 's3-bucket.png'
            elif 'Network' in name:
                icon = 'Networking.png'
                if 'TGW' in name:
                    icon = 'transit-gateway.jpg'
                elif 'DX' in name:
                    icon = 'direct-connetc.jpg'
            elif 'CSP' in name:
                icon = 'Amazon_Web_Services_Logo.png'
                if 'SQS' in name:
                    icon = 'SQS.png'
                elif 'MSK' in name:
                    # icon = 'msk.png'
                    icon = 'apache_kafka_vertical_logo.png'
            else:
                icon = 'Amazon_Web_Services_Logo.png'
        img_url = f'{s3_url}icon/{icon}'
        # row_html += f'<img src={img_url} alt={monitor_id} width="40">'        
        row_html += f'<img src={img_url} alt={monitor_id} height="40">'        
        row_html += '</td>\n'



        # row_html += f'<td> {check_result} </td>\n'
        row_html += f'<td> {check_result_str} </td>\n'
        row_html += f'<td> {name} </td>\n'
        priority_str = f'<span class=red>{priority}</span>' if priority in ['P1'] else f'<span class=orange>{priority}</span>'
        row_html += f'<td> {priority_str} </td>\n'
        # row_html += f'<th> {priority} </th>\n'
        row_html += f'<td> <span class=fixed-font>{query} </span> </td>\n'
        row_html += f'<td>\n<div class="item">\n<h4 class="tooltip"><pre>{result_detail_str}</pre>\n<span class="tooltiptext">\n{check_result_detail}\n</span>\n</h4>\n</div>\n</td>\n'
        row_html += '</tr>\n'

        table_html += row_html
    
    table_html += '</tbody>\n'
    table_html += '</table>\n'

    print(f"table_html[{table_html}]")
    return item_cnt, table_html

def dydb_check_system_data(table_name, check_dtm):
    print(f"dynamodb_get_html(table_name[{table_name}], check_dtm[{check_dtm}])")
    # DynamoDB 테이블과 S3 버킷 설정
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table    = dynamodb.Table(table_name)
    
    # 오늘 날짜를 가져옴 (YYYY-MM-DD 형식)
    # today = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(f"dynamodb_get_data(table_name[{table_name}])")

    # DynamoDB에서 조건에 맞는 항목 쿼리
    # response = table.scan(
    #         FilterExpression='begins_with(check_dtm, :check_dtm_val)',
    #         ExpressionAttributeValues={
    #             ':check_dtm_val': check_dtm
    #         }
    #     )
    response = table.query(
        # KeyConditionExpression='check_dtm begins_with :check_dtm_val',
        KeyConditionExpression=Key('check_dtm').eq(check_dtm),
        # ExpressionAttributeValues={
        #     # ':check_dtm': {'S': check_dtm }
        #     ':check_dtm': check_dtm
        # },
        ScanIndexForward=True
    )


    return response['Items']


def dydb_alert_count_items_by_priority(dydb_alert_list_name, date_value):
    print(f'dydb_alert_count_items_by_priority({dydb_alert_list_name}, {date_value})')
    dynamodb   = boto3.resource('dynamodb')
    table_name = 'dydb_alert_history_lcl14'  # 테이블 이름을 여기에 입력하세요

    date_attribute     = 'day_'
    priority_attribute = 'alert_priority'

    table = dynamodb.Table(dydb_alert_list_name)
    # response = table.scan(
    #     FilterExpression=f"#{date_attribute} = :date_value",
    #     ExpressionAttributeNames={
    #         f"#{date_attribute}": date_attribute,
    #     },
    #     ExpressionAttributeValues={
    #         ":date_value": date_value,
    #     },
    #     ProjectionExpression=priority_attribute
    # )
    response = table.query(
        TableName=dydb_alert_list_name,
        KeyConditionExpression='#DDB_day_ = :pkey',
        ExpressionAttributeValues={
            ':pkey': date_value
        },
        ExpressionAttributeNames={
            '#DDB_day_': 'day_'
        },
        ScanIndexForward=True
        # Limit=100
    )
    count_by_priority = {}

    for item in response['Items']:
        priority = item.get(priority_attribute)
        count_by_priority[priority] = count_by_priority.get(priority, 0) + 1

    return count_by_priority

def lambda_handler(event, context):
    """
    Lambda function handler.

    Args:
        event (dict): The event object.
        context (dict): The context object.
    """

    print('## ENVIRONMENT VARIABLES')
    print(os.environ['AWS_LAMBDA_LOG_GROUP_NAME'])
    print(os.environ['AWS_LAMBDA_LOG_STREAM_NAME'])
    print('## EVENT')
    
    # print(event)
    # print(json.dumps(event, indent=2))


    # S3 버킷 및 파일 정보
    # s3_bucket_name = "s3-bucket-lcl14"
    s3_bucket_name  = os.getenv('S3_BUCKET_NAME')
    # s3_object_key  = "index.html"
    s3_object_key   = "template/system_check.html"
    
    # DynamoDB 테이블 정보
    # dynamodb_table_name = "dydb_system_check_lcl14"
    # dydb_system_check_name = os.environ.get('DYDB_SYSTEM_CHECK_NAME')
    # dydb_alert_list_name   = os.environ.get('DYDB_ALERT_LIST_NAME')

    # dynamodb_key        = "index.html"
    dynamodb_key        = "1"
    status_code         = 200

    # Access specific fields within the payload
    # Get the lambda_url text.
    if 'lambda_url' in event:
        # print(event['lambda_url'])
        LAMBDA_URL = event['lambda_url']


        now = datetime.now(timezone(timedelta(hours=9)))
        check_dtm = now.strftime('%Y%m%d%H')

        # print(f"LAMBDA_URL[{LAMBDA_URL}] ++++++++++++++")
        slack_msg = f"*Argos* _상태체크_ 를 하였습니다.! 자세히 알아보려면 `<{LAMBDA_URL}?check_dtm={check_dtm}|여기를 클릭>`하세요."
        # result    = f'<H1>Lambda에서 Slack으로 보내는 메시지 입니다.! </H1> </br> <H2> 자세히 알아보려면 <a href="{LAMBDA_URL}"> 여기를 클릭</a> 하세요.</H2>'
        result = "Success"


        # Send the message to Slack.
        # send_to_slack(slack_msg, SLACK_WEBHOOK_URL)
        send_message_to_slack(slack_msg, LAMBDA_URL)
    else:
        print('lambda_url 이 없음 - check_dtm -> dynamo_db 에서 system check 상황 조회')
        # s3_bucket_name = "s3-bucket-lcl14"
        # s3_object_key  = "system_check.html"
        # dynamodb_table_name = "dynamodb_system_check_lcl14"
        # check_dtm = datetime.datetime.now().strftime('%Y%m%d%H')
        cur_time_str  = get_current_time()
        # pprint(event)

        if 'queryStringParameters' in event:
            print('queryStringParameters 가 존재함')
            # URL 파라미터를 가져오기 위해 "queryStringParameters" 키로부터 값을 추출합니다.
            params        = event.get('queryStringParameters', {})
            print("==================================")
            print(params)

            check_dtm   = params['check_dtm']
            print(f"check_dtm[{check_dtm}]")
            # now = datetime.datetime.now(timezone(timedelta(hours=9)))
            # check_dtm = now.strftime('%Y%m%d%H')
            # check_dtm = f"{today}09"
            html_template = s3_get_html(s3_bucket_name, s3_object_key)
            print(f"Call dynamodb_get_html(dydb_system_check_name[{dydb_system_check_name}], check_dtm[{check_dtm}])")        
            items         = dydb_check_system_data(dydb_system_check_name, check_dtm)

            # 20230708
            # today = datetime.now().strftime('%Y%m%d')
            # date_value = '20230708'
            today = check_dtm[:8]
            alert_count_results = dydb_alert_count_items_by_priority(dydb_alert_list_name, today)

            
            cnt = 0
            _alert_title = ' '
            for priority, count in alert_count_results.items( ):
                print(f"Priority: {priority}, Count: {count}")                
                _alert_title += f"{priority}:{count} "
                cnt += count
            
            
            alert_title = f'<font size="2" color="blue"> <a href="{LAMBDA_COLLECTION_URL}?today={today}">Alert  발생 건수 총 {cnt} 건</a>[{_alert_title}]</font></a>'

            # 쿼리 결과를 테이블 형태로 변환하여 HTML 템플릿에 삽입
            item_cnt, table_html = create_html_table(items)

            # total_cnt = item_cnt['Y'] + item_cnt['N'] + item_cnt['C'] + item_cnt['D']
            # ok_cnt     = item_cnt['Y']
            # notok_cnt  = item_cnt['N']
            # error_cnt  = item_cnt['C']
            # nodata_cnt = item_cnt['D']
            ok_cnt     = item_cnt['OK']
            notok_cnt  = item_cnt['Not OK']
            error_cnt  = item_cnt['점검오류']
            nodata_cnt = item_cnt['No Data']            
            total_cnt  = ok_cnt + notok_cnt + error_cnt + nodata_cnt

            if total_cnt == 0:
                print(f'[{dydb_system_check_name}] 조회 건수가 없음')
                status_code   = 404
                title         = "자원 점검 결과 오류"
                inner_status  = f"Opps! 데이타가 없습니다.!"
                inner_detail  = f"\"{check_dtm}\" 으로 조회된 데이터가 없습니다."
                html_template = s3_get_html(s3_bucket_name, "template/404.html")
                result        = html_template.replace('{{s3_check_list_icon_url}}', s3_title_icon_url).replace('{{timestamp}}', cur_time_str).replace('{{title}}', title).replace('{{inner-status}}', inner_status).replace('{{inner-detail}}', inner_detail)
            else:
                status_code   = 200
                title         = '자원 점검 결과'
                subtitle      = f'{today} Argos System Check 총 {total_cnt}건 점검[<span class=green>OK:{ok_cnt}</span>, <span class=red>Not OK:{notok_cnt}</span>, <span class=orange>점검데이타부재:{nodata_cnt}</span>, <span class=gray>점검오류:{error_cnt}</span>] </br> {alert_title}'
                
                result = html_template.replace('{{s3_title_icon_url}}', s3_title_icon_url).replace('{{s3_aws_logo_url}}', s3_aws_logo_url).replace('{{timestamp}}', cur_time_str).replace('{{title}}', title).replace('{{subtitle}}', subtitle).replace('{{table_content}}', table_html)

                # 결과 HTML을 S3에 저장 (선택 사항)
                # output_key = 'output.html'
                # s3.Object(bucket_name, output_key).put(Body=final_html, ContentType='text/html')
        else:
            print('queryStringParameters 가 없음')
            pprint(event)
            status_code   = 500
            title         = "자원 점검 결과 오류"
            inner_status  = "Opps! 인자 전달 오류!"
            inner_detail  = "Query String 이 들어 오지 않았습니다"
            html_template = s3_get_html(s3_bucket_name, "template/error.html")
            result        = html_template.replace('{{timestamp}}', cur_time_str).replace('{{title}}', title).replace('{{inner-status}}', inner_status).replace('{{inner-detail}}', inner_detail)

    # Return a response if needed
    print(f"status_code[{status_code}]\nbody[{result}]")
    return {
        'statusCode' : status_code,
        # 'statusCode' : 200,
        'body': result,
        'headers': {'Content-Type': 'text/html'}
    }

if __name__ == "__main__":
    LAMBDA_URL        = os.environ.get('LAMBDA_URL')
    # send_message_to_slack(f"매우 중요한 알림이 있습니다! 자세히 알아보려면 <{LAMBDA_URL}|여기를 클릭>하세요.")


