import boto3

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 이름
table_name = 'dynamodb_system_check_lcl15'

# 테이블 삭제 요청
dynamodb.delete_table(TableName=table_name)

print(f"Table '{table_name}' deleted.")