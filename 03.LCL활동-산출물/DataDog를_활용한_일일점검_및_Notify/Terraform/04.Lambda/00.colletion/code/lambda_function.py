import json
import boto3
import time
from datetime import datetime, timedelta, timezone

from pprint import pprint
import os

s3_url                 = os.environ.get('S3_URL')
s3_aws_logo_url        = os.environ.get('S3_AWS_LOGO_URL')
s3_title_icon_url      = os.environ.get('S3_TITLE_ICON_URL')

def get_current_time():
    now = datetime.now(timezone(timedelta(hours=9)))
    return now.strftime('%Y/%m/%d %H:%M:%S')

def dydb_put_alert(payload, table_name):
    # 필요한 정보를 파싱하여 출력
    id             = payload['id']
    user           = payload['user']
    username       = payload['username']
    email          = payload['email']
    date           = payload['date']
    hostname       = payload['hostname']
    text_only_msg  = payload['textOnlyMsg']
    tags           = payload['tags']
    last_updated   = payload['lastUpdated']

    event_type     = payload['event']['type']
    event_title    = payload['event']['title']
    event_msg      = payload['event']['msg']

    alert_id       = payload['alert']['id']
    alert_type     = payload['alert']['type']
    alert_priority = payload['alert']['priority']
    alert_title    = payload['alert']['title']
    alert_metric   = payload['alert']['metric']
    alert_query    = payload['alert']['query']
    alert_status   = payload['alert']['status']
    alert_scope    = payload['alert']['scope']

    org_id         = payload['org']['id']
    org_name       = payload['org']['name']

    

    # 파싱한 정보를 다른 처리에 활용하거나 응답으로 반환할 수도 있음
    # Saving data to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table     = dynamodb.Table(table_name)

    # Convert `date` to datetime object
    date_obj = date_obj = datetime.fromtimestamp(int(date) / 1000)
    # Add 9 hours to the datetime object
    date_obj += timedelta(hours=9)
    
    # Format the datetime object as per your requirement
    date_str = date_obj.strftime("%Y%m%d")
    time_str = date_obj.strftime("%H%M%S")
    
    last_updated_obj = datetime.fromtimestamp(int(date) / 1000) 
    last_updated_obj += timedelta(hours=9)
    last_updated_str = last_updated_obj.strftime('%Y/%m/%d %H:%M:%S')

    # date[1688741962000] : [2023070723], last_updated[1688741962000]:[2023/07/07 23:59:22]
    print(f"date[{date}] : [{date_str}], last_updated[{last_updated}] : [{last_updated_str}]")
    print(f"alert_id : {alert_id}, Date: {date_str}/{last_updated_str}, Priority : {alert_priority}, Title: {alert_title}/{text_only_msg}, Event Message: {event_msg},  Query : {alert_query}")
    


    item = {
        'alert_id': alert_id,
        'day_': date_str,
        'time': time_str,
        'user': user,
        'username': username,        
        'email': email,
        'hostname': hostname,
        'text_only_msg': text_only_msg,
        'tags': tags,
        'event_type': event_type,
        'event_title': event_title,
        'event_msg': event_msg,
        'id': id,
        'alert_type': alert_type,
        'alert_priority': alert_priority,
        'alert_title': alert_title,
        'alert_metric': alert_metric,
        'alert_query': alert_query,
        'alert_status': alert_status,
        'alert_scope': alert_scope,
        'org_id': org_id,
        'org_name': org_name,
        'last_updated': last_updated_str,
        'payload': payload
    }

    # table.put_item(Item=item)
    status_code = 200
    body        = 'Lambda function executed successfully'
    response = table.put_item(Item=item)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Item saved successfully")        
    else:
        print("Error saving item:")
        print(response['ResponseMetadata']['HTTPStatusCode'])
        print(response['ResponseMetadata']['HTTPHeaders'])
        print(response['ResponseMetadata']['Error'])
        status_code = 500
        body = f"DynamoDB put 오류[{response['ResponseMetadata']['HTTPStatusCode']}, {response['ResponseMetadata']['HTTPHeaders']}, {response['ResponseMetadata']['Error']}]"

    return status_code, body

def s3_get_html(s3_bucket_name, s3_object_key):
    print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]")
    # S3 객체를 읽어옴
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket_name, s3_object_key)
    html_content = obj.get()['Body'].read().decode('utf-8')
    # print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]\nhtml_content[{html_content}]")
    # print(f"s3_get_html - s3_bucket_name[{s3_bucket_name}] s3_object_key[{s3_object_key}]")

    return html_content

def dydb_get_alert_list(today, table_name):
    # DynamoDB 테이블과 S3 버킷 설정
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table(table_name)

    print(f"dydb_get_alert_list(table_name[{table_name}], today[{today}])")
    
    # DynamoDB에서 조건에 맞는 항목 쿼리
    # response = table.scan(
    #         # "begins_with", "contains", "between", "gt" (greater than), "lt" (less than), etc.
    #         # FilterExpression='begins_with(day_, :today_val)',
    #         FilterExpression='day_ = :today_val',
    #         ExpressionAttributeValues={
    #             ':today_val': today
    #         }
    #     )
    
    response = table.query(
        TableName=table_name,
        KeyConditionExpression='#DDB_day_ = :pkey',
        ExpressionAttributeValues={
            ':pkey': today
        },
        ExpressionAttributeNames={
            '#DDB_day_': 'day_'
        },
        ScanIndexForward=True
        # Limit=100
    )
    
    return response['Items']


# 쿼리 결과를 테이블 형태로 변환하는 함수
def create_html_table(items):
    priority_cnt = {
        'P1' : {
            'recovered': 0,
            'triggered': 0
        },
        'P2' : {
            'recovered': 0,
            'triggered': 0
        },
        'P3' : {
            'recovered': 0,
            'triggered': 0
        },
        'P4' : {
            'recovered': 0,
            'triggered': 0
        },
        'P5' : {
            'recovered': 0,
            'triggered': 0
        }
    }
    row = 0
    print(f'create_html_table[{items}]')
    
    table_html = '<table class="type09">\n'
    table_html += '<thead>\n'
    table_html += '<tr>\n'
    table_html += '<th scope="cols">No.</th>'
    table_html += '<th scope="cols">date</th>'
    table_html += '<th scope="cols">Alert I.D</th>'
    table_html += '<th scope="cols">Title</th>'
    table_html += '<th scope="cols">Priority</th>'
    table_html += '<th scope="cols">Type</th>'
    table_html += '<th scope="cols">Metric</th>'
    table_html += '<th scope="cols">Query</th>'
    table_html += '</tr>\n'
    table_html += '</thead>\n'
    table_html += '<tbody>\n'
    for item in items:
        row += 1
        date_    = item['day_']
        time_    = item['time']
        date     = f"{date_[:4]}/{date_[4:6]}/{date_[6:]} {time_[:2]}:{time_[2:4]}:{time_[4:]}"
        alert_id = item['alert_id']
        title    = item['alert_title']
        priority = item['alert_priority']
        metric   = item['alert_metric']
        query    = item['alert_query']
        type     = item['alert_type']

        if type == 'success':
            priority_cnt[priority]['recovered'] += 1
        else:
            priority_cnt[priority]['triggered'] += 1


        # 테이블 행 생성
        row_html  = '<tr>\n'
        row_html += f'<th scope="row">{row}</th>\n'
        row_html += f'<th> {date} </th>\n'
        row_html += f'<td> {alert_id} </td>\n'
        row_html += f'<td> {title} </td>\n'
        priority_str = f'<span class=red>{priority}</span>' if priority in ['P1', 'P2'] else f'<span class=orange>{priority}</span>'
        row_html += f'<td> {priority_str} </td>\n'
        type_str = f'<span class=success>Recovered({type})</span>' if type == 'success' else f'<span class=error>Triggered({type})</span>'
        row_html += f'<td> {type_str} </td>\n'
        row_html += f'<td> {metric} </td>\n'
        row_html += f'<td> {query} </td>\n'

        row_html += '</tr>\n'

        table_html += row_html
    
    table_html += '</tbody>\n'
    table_html += '</table>\n'

    print(f"table_html[{table_html}]")
    return priority_cnt, table_html


def lambda_handler(event, context):
    # pprint(event)
    # pprint(context)    


    s3_bucket_name          = os.environ.get('S3_BUCKET_NAME')
    # s3_object_key  = "index.html"
    s3_object_key           = os.environ.get('S3_COLLECTION_TEMPLATE') # "template/system_check.html"

    dydb_system_check_name  = os.environ.get('DYDB_SYSTEM_CHECK_NAME')
    dydb_alert_list_name    = os.environ.get('DYDB_ALERT_LIST_NAME')

    cur_time_str            = get_current_time()


    status_code = 200
    body        = ''

    if 'queryStringParameters' in event:
        # URL 파라미터를 가져오기 위해 "queryStringParameters" 키로부터 값을 추출
        params                   = event.get('queryStringParameters', {})
        today                    = params['today']
        items                    = dydb_get_alert_list(today, dydb_alert_list_name)
        print(f"items[{len(items)}]")
        if len(items) == 0:
            title         = "Alert 목록 조회 오류"
            inner_status  = "Opps! 조회된 Alert 데이터가 없습니다"
            inner_detail  = f"\"{today}\" 로 Alert 목록을 조회時 결과가 없습니다"
            html_template = s3_get_html(s3_bucket_name, "template/404.html")
            body          = html_template.replace('{{timestamp}}', cur_time_str).replace('{{title}}', title).replace('{{inner-status}}', inner_status).replace('{{inner-detail}}', inner_detail)
            status_code   = 404
        else:
            priority_cnt, table_html = create_html_table(items)

            # <h1> {{today}} : {{title}} - {{timestamp}} </h1>
            # <h2> {{subtitle}} </h2>
            # {{table_content}}


            alert_cnt       = 0
            total_recovered = 0
            total_triggered = 0
            _alert_title    = 'Priority(<span class=error>Triggered</span>, <span class=success>Recovered</span>):'
            for priority, values in priority_cnt.items( ):
                print(f"{priority}({values['recovered']}, {values['triggered']})")
                total_recovered  += values['recovered']
                total_triggered  += values['triggered']                
                _alert_title     += f"<span class=error>{priority}({values['triggered']}</span>, <span class=success>{values['recovered']}</span>) "
            alert_cnt        = total_recovered + total_triggered
                

            alert_title      = f'<font size="2" color="blue"> {_alert_title} </font>'

            title            = f'발생한 Alert 목록'
            subtitle         = f'{today} Argos System Alert 발생건수 {alert_cnt}건(Triggered:{total_triggered}, Recovered:{total_recovered})</br>[{alert_title}]'

            html_template    = s3_get_html(s3_bucket_name, s3_object_key)
            body             = html_template.replace('{{s3_title_icon_url}}', s3_title_icon_url).replace('{{s3_aws_logo_url}}', s3_aws_logo_url).replace('{{today}}', today).replace('{{title}}', title).replace('{{timestamp}}', cur_time_str).replace('{{subtitle}}', subtitle).replace('{{table_content}}', table_html) 
    else:
        if 'body' not in event:
            #  'body' 키가 없을 때 오류 코드를 기록합니다.
            title         = "Alert 기록 요청 오류"
            inner_status  = "Opps! body 가 들어 오지 않았습니다!"
            inner_detail  = "API Gateway나 Lambda Proxy Integration과 같은 AWS 서비스를 사용한 표준 형식의 요청 이벤트가 아닙니다."
            html_template = s3_get_html(s3_bucket_name, "template/error.html")
            body          = html_template.replace('{{timestamp}}', cur_time_str).replace('{{title}}', title).replace('{{inner-status}}', inner_status).replace('{{inner-detail}}', inner_detail)
            status_code   = 500
        else:
            # Datadog 알림 데이터를 이벤트로부터 가져옴
            payload           = json.loads(event['body'])
            status_code, body = dydb_put_alert(payload, dydb_alert_list_name)


    return {
        'statusCode': status_code,
        'body': body,
        'headers': {'Content-Type': 'text/html'}
    }