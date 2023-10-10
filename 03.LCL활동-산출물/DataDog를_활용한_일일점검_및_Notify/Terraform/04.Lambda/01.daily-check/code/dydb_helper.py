import boto3
from datetime import datetime
import json
from pprint import pprint
import os


def put_item(table_name, data, check_result_detail):
    # DynamoDB 클라이언트 생성
    dynamodb = boto3.client('dynamodb')

    check_dtm              = data.get('check_dtm')
    monitor_id             = data.get('monitor_id')
    monitor_priority       = data.get('monitor_priority')
    monitor_name           = data.get('monitor_name')
    check_result           = data.get('check_result')


    print(f"check_dtm[{check_dtm}], monitor_id[{monitor_id}], monitor_priority[{monitor_priority}], monitor_name[{monitor_name}], check_result[{check_result}]")

    # 아이템 삽입 요청
    item = {
        'check_dtm': {'S': check_dtm},
        'monitor_id': {'S': monitor_id},
        'monitor_priority': {'S': monitor_priority},
        'monitor_name': {'S': monitor_name},
        'check_result': {'S': check_result},
        'check_result_detail': {'S': json.dumps(check_result_detail, indent=2)}
    }

    response = dynamodb.put_item(TableName=table_name, Item=item)

    # 응답 확인
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("데이터 삽입이 성공적으로 완료되었습니다.")
        return True
    else:
        print("데이터 삽입 중에 오류가 발생하였습니다.")
        return False


def get_item(table_name, check_dtm, monitor_id):

    print(f"table_name[{table_name}], check_dtm[{check_dtm}], monitor_id[{monitor_id}]")
    # DynamoDB 클라이언트 생성
    dynamodb = boto3.client('dynamodb')
    
    # 아이템 조회 요청
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'check_dtm': {'S': check_dtm},
            'monitor_id': {'S': monitor_id}
        }
    )

    # 응답 확인
    if 'Item' in response:
        item = response['Item']
        check_result = item['check_result']['S']
        check_result_detail = item['check_result_detail']['S']
        
        # check_result_detail은 JSON 형태로 저장되었으므로 다시 파싱하여 사용할 수 있습니다.
        check_result_detail = json.loads(check_result_detail)

        print("아이템 조회 결과:")
        print(f"check_dtm: {check_dtm}, monitor_id: {monitor_id}, check_result: {check_result}, check_result_detail: {check_result_detail}")

        return item
    else:
        print("아이템을 찾을 수 없습니다.")
        return None

def get_items(table_name):
    # DynamoDB 클라이언트 생성
    dynamodb = boto3.client('dynamodb')
    
    # 시스템 체크 목록 조회
    response = dynamodb.scan(TableName=table_name)

    # 목록 출력
    for item in response['Items']:
        print(item)

    # 전체 아이템 조회 요청
    response = dynamodb.scan(
        TableName=table_name,
        # 필요에 따라 다른 옵션을 추가할 수 있습니다.
        # 예: Limit, FilterExpression 등
    )

    # 응답 확인
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = dynamodb.scan(
            TableName=table_name,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response['Items'])

    # 조회된 아이템 출력
    for item in items:
        print(item)



if __name__ == "__main__":
    table_name = os.environ.get('DYNAMODB_TABLE_NAME')
    # 데이터 생성
    # resource_id = 'NETWORK-DX-01'
    # check_dtm = datetime.now().strftime("%Y%m%d %H%M%S")
    # check_result = 'Y'
    # check_result_detail = {
    #     'created': '2023-04-14T08:49:02.655103+00:00',
    #     'created_at': 1681462142000,
    #     'creator': {'email': 'yjbang@sk.com',
    #                 'handle': 'yjbang@sk.com',
    #                 'id': 4671517,
    #                 'name': None},
    #     'deleted': None,
    #     'id': 116390058,
    #     'message': '[참고 - 연결 정보]\n'
    #                 '# Data망\n'
    #                 '- dxcon-fh5l0k7k : 1st VIF (KINX)\n'
    #                 '- dxcon-fg6pdahf : 2nd VIF (LG U+)\n'
    #                 '# 신호수신망\n'
    #                 '- dxcon-fh891mus : \x081st VIF (KINX)\n'
    #                 '- dxcon-fg44j36q : 2nd VIF (KINX)\n'
    #                 '- dxcon-fg6a3n0g : 3rd VIF (LG U+)\n'
    #                 '# 고객센터망\n'
    #                 '- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\n'
    #                 '- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \n'
    #                 '\n'
    #                 '@slack-skshieldusnextossdev-prd알람 \n'
    #                 '@slack-SKCC_Digital_Service-ict_shieldus_argos\n'
    #                 '@slack-SKCC_Digital_Service-ict_shieldus_argos_l1',
    #     'modified': '2023-05-02T15:46:38.055414+00:00',
    #     'multi': True,
    #     'name': '[P1][Network] DX Connection Down ({{connectionid.name}})',
    #     'options': {'evaluation_delay': 900,
    #                 'include_tags': True,
    #                 'new_group_delay': 60,
    #                 'notify_audit': False,
    #                 'notify_no_data': False,
    #                 'renotify_interval': 0,
    #                 'require_full_window': False,
    #                 'silenced': {},
    #                 'thresholds': {'critical': 1.0}},
    #     'org_id': 708429,
    #     'overall_state': 'OK',
    #     'overall_state_modified': '2023-04-14T08:49:05+00:00',
    #     'priority': 1,
    #     'query': 'max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} '
    #             'by {connectionid} < 1',
    #     'restricted_roles': None,
    #     'tags': ['team:skcc', 'DOWN', 'Network'],
    #     'type': 'query alert'}
    # # Call the function to check the DX connection status
    # put_item(resource_id, check_dtm, check_result, check_result_detail)

    # get_items(table_name)

    resource_id = 'DB-MARIADDB-01'
    check_dtm   = '2023070600'
    item = get_item(table_name, check_dtm, resource_id)
    pprint(item)