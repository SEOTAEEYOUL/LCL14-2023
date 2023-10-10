import boto3
from datetime import datetime
import json

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 이름 설정
table_name = "dydb_system_check_lcl14"

# 데이터 생성
resource_id = '1'
check_dtm = datetime.now().strftime("%Y%m%d %H%M%S")
check_result = 'Y'
check_result_detail = {
    'key1': 'value1',
    'key2': 'value2'
}

# 아이템 삽입 요청
item = {
    'resource_id': {'S': resource_id},
    'check_dtm': {'S': check_dtm},
    'check_result': {'S': check_result},
    'check_result_detail': {'S': json.dumps(check_result_detail)}
}

response = dynamodb.put_item(TableName=table_name, Item=item)

# 응답 확인
if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    print("데이터 삽입이 성공적으로 완료되었습니다.")
else:
    print("데이터 삽입 중에 오류가 발생하였습니다.")