import boto3

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 이름
table_name = 'dynamodb_system_check_lcl16'

# 테이블 정의
table_definition = {
    'TableName': table_name,
    'KeySchema': [
        {'AttributeName': 'resource_id', 'KeyType': 'HASH'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'resource_id', 'AttributeType': 'S'}
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

# 테이블 생성 요청
dynamodb.create_table(**table_definition)

print(f"Table '{table_name}' created.")

# 데이터 추가
data = [
    {'resource_id': {'S': 'DB-MARIADDB-02'}, 'check_dtm': {'S': '2023/07/04 09:00:00'}},
    {'resource_id': {'S': 'DB-MARIADDB-02'}, 'check_dtm': {'S': '2023/07/04 20:00:00'}}
]

for item in data:
    dynamodb.put_item(
        TableName=table_name,
        Item=item
    )

print("Data added successfully.")