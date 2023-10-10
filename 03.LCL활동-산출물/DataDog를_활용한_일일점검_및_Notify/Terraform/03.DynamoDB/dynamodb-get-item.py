import boto3
import json

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 이름 설정
table_name = "dydb_system_check_lcl14"

# 조회할 아이템의 키 설정
resource_id = '1'
check_dtm = '20230623 192336'  # 적절한 check_dtm 값을 설정해야 합니다.

# 아이템 조회 요청
response = dynamodb.get_item(
    TableName=table_name,
    Key={
        'resource_id': {'S': resource_id},
        'check_dtm': {'S': check_dtm}
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
    print(f"resource_id: {resource_id}")
    print(f"check_dtm: {check_dtm}")
    print(f"check_result: {check_result}")
    print(f"check_result_detail: {check_result_detail}")
else:
    print("아이템을 찾을 수 없습니다.")
