import boto3
import json
from datetime import datetime

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 이름 설정
table_name = "dydb_system_check_lcl14"

# 시스템 체크 데이터 생성
resource_id = "1"
check_dtm = datetime.now().strftime("%Y%m%d %H%M%S")
check_result = "success"
check_result_detail = {
    "detail_key": "detail_value"
}

# 시스템 체크 아이템 삽입
item = {
    "resource_id": {"S": resource_id},
    "check_dtm": {"S": check_dtm},
    "check_result": {"S": check_result},
    "check_result_detail": {"S": json.dumps(check_result_detail)}
}

# 아이템 삽입 요청
dynamodb.put_item(TableName=table_name, Item=item)

# 시스템 체크 목록 조회
response = dynamodb.scan(TableName=table_name)

# 목록 출력
for item in response['Items']:
    print(item)

# 특정 행 조회 및 출력
partition_key_value = resource_id
sort_key_value = check_dtm

response = dynamodb.get_item(
    TableName=table_name,
    Key={
        "resource_id": {"S": partition_key_value},
        "check_dtm": {"S": sort_key_value}
    }
)

if 'Item' in response:
    item = response['Item']
    print(item)
else:
    print("행을 찾을 수 없습니다.")