import boto3

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 목록 조회 요청
response = dynamodb.list_tables()

# 테이블 목록 및 생성일자 출력
if 'TableNames' in response:
    table_names = response['TableNames']
    for table_name in table_names:
        # 테이블 정보 조회
        table_info = dynamodb.describe_table(TableName=table_name)
        creation_date = table_info['Table']['CreationDateTime']
        
        # 생성일자를 문자열로 변환
        creation_date_str = creation_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # 테이블 이름과 생성일자 출력
        print(f"테이블 이름: {table_name}, 생성일자: {creation_date_str}")
else:
    print("테이블을 찾을 수 없습니다.")