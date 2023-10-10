import boto3

# DynamoDB 클라이언트 생성
dynamodb = boto3.client('dynamodb')

# 테이블 이름
table_name = 'dynamodb_system_check_lcl14'

# 금일 날짜 ('2023/07/04')
date = '2023/07/04'

# Query 파라미터 설정
query_params = {
    'TableName': table_name,
    'IndexName': 'resource_id-check_dtm-index',  # 인덱스 이름
    'KeyConditionExpression': 'resource_id = :resource_id and begins_with(check_dtm, :date)',
    'ExpressionAttributeValues': {
        ':resource_id': {'S': '전체'},  # resource_id 값
        ':date': {'S': date}  # 날짜 값
    },
    'ScanIndexForward': False,  # 내림차순 정렬 (가장 최근 값부터 가져옴)
    'Limit': 1  # 가져올 아이템 개수
}

# 쿼리 실행
response = dynamodb.query(**query_params)

# 결과 처리
for item in response['Items']:
    resource_id = item['resource_id']['S']
    check_dtm = item['check_dtm']['S']
    print(f"resource_id: {resource_id}, check_dtm: {check_dtm}")