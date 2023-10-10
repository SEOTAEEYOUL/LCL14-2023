import boto3

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 이름 설정
table_name = "dydb_system_check_lcl14"

# 테이블 정보 조회 요청
response = dynamodb.describe_table(TableName=table_name)

# 테이블 필드 정보 출력
if 'Table' in response:
    table_info = response['Table']
    attribute_definitions = table_info['AttributeDefinitions']
    
    print("테이블 필드 정보:")
    for attribute in attribute_definitions:
        attribute_name = attribute['AttributeName']
        attribute_type = attribute['AttributeType']
        print(f"필드명: {attribute_name}, 타입: {attribute_type}")
else:
    print("테이블을 찾을 수 없습니다.")