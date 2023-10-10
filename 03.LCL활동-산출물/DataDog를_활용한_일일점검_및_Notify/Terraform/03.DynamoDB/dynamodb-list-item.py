import boto3

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 이름 설정
table_name = "dydb_system_check_lcl14"

# # 조회할 아이템의 키 설정
# resource_id = '1'
# check_dtm = '20230623 100000'  # 적절한 check_dtm 값을 설정해야 합니다.

# # 아이템 조회 요청
# response = dynamodb.get_item(
#     TableName=table_name,
#     Key={
#         'resource_id': {'S': resource_id},
#         'check_dtm': {'S': check_dtm}
#     }
# )

# # 응답 확인
# if 'Item' in response:
#     item = response['Item']
#     print("아이템 상세:")
#     for key, value in item.items():
#         field_name = key
#         field_value = value['S'] if 'S' in value else value['N'] if 'N' in value else value['BOOL']
#         print(f"{field_name}: {field_value}")
# else:
#     print("아이템을 찾을 수 없습니다.")



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