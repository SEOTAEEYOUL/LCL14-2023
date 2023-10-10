# Python Test

### DynamoDB 구조

| field 명 | 설명 | 속성 |  
|:---|:---|:---|  
| resource_id | 점검 자원 ID | 파티션 키 (hash key) |  
| check_dtm | 점검일시분초 | 정렬키 (range key)  |  
| check_result | 점검 결과 | `Y` 양호 </br> `C` 확인 필요 </br> `N` 불량 |  
| check_result_detail | 상세 결과 값 | |  


### 고려사항
- resource_id (Alert) 별로 매일 한건 혹은 2건이 쌓일 경우
1. 각 resource_id 별로 마지막 수행 결과를 가져와서 출력하는 것이 필요
2. Datadog Alert 이 왔을 때 수집, 기록하여 별도의 테이블에 기록하여 일별 상태 점검시 보여주는 것이 필요

### 현재 되어 있는 것 
1. Alert 를 점검하여 결과 저장하고 각각 Alert 별 개별 결과를 조회하는 것 (S3 에 Static 문서를 읽어서 DynamoDB 테이블을 조회하여 보여주는 것 포함)
2. PreSigned URL 를 Slack 으로 전송하는 것
3. 전체 Alert Data 를 가져와서 출력하는 것  -> Resource ID 별 금일 수행된 마지막 건을 가져온 것이 필요

### 안되어 있는 것 혹은 해야 할 것
#### 1. DynamoDB 를 구조 변경 혹은 현상태에서 resource_id 별로 금일 마지막 건 가져오기
#### 2. 현재 시스템 건전성을 확인하기 위해서는 추가 데이터 필요
- Datadog 에서 보낸 Alert 를 식별하여 저장
- 일별 리포팅때 같이 보여 줘야 함
- Alert 외에 추가할 자료는 없는지 ?








- python test-all.py   
```
DB-MARIADDB-02                 : 2023/07/05 09:00:21
CSP-MSK-01                     : 2023/06/29 14:55:26
CONTAINER-EKS_JOB-01           : 2023/07/05 09:01:06
DB-MYSQL_MEM-01                : 2023/07/05 09:00:38
DB-MARIADDB-01                 : 2023/07/05 09:00:19
CONTAINER-EKSNODE-01           : 2023/07/05 09:00:25
SYSTEM-EC2_INODE-01            : 2023/07/05 09:00:57
CSP-MSK_DISK-01                : 2023/07/05 09:01:05
DB-CPU-02                      : 2023/06/29 14:55:17
CONTAINER-EKS_DISK-01          : 2023/07/05 09:00:54
CONTAINER-TX_ERROR-01          : 2023/07/05 09:00:46
NETWORK-TGW_DROP-02            : 2023/07/05 09:01:03
DB-MYSQL_DML-01                : 2023/06/29 15:24:23
```


- test-all-2.py
```python
import boto3
from pprint import pprint

# DynamoDB 연결
dynamodb = boto3.resource('dynamodb')
table_name = 'dynamodb_system_check_lcl14'
table = dynamodb.Table(table_name)

# 쿼리 조건 설정
expression_attribute_values = {':check_dtm': '2023/07/04 09:'}
key_condition_expression = 'contains(check_dtm, :check_dtm)'

# 결과 조회
response = table.scan(
    FilterExpression=key_condition_expression,
    ExpressionAttributeValues=expression_attribute_values
)

pprint(response)

# 모든 resource_id 가져오기
resource_ids = []
for item in response['Items']:
    resource_id = item['resource_id']
    if resource_id not in resource_ids:
        resource_ids.append(resource_id)

pprint(resource_ids)

# 각 resource_id 별로 최신 날짜의 값 가져오기
latest_data = {}
for resource_id in resource_ids:
    latest_check_dtm = None
    for item in response['Items']:
        if item['resource_id'] == resource_id:
            check_dtm = item['check_dtm']
            if latest_check_dtm is None or check_dtm > latest_check_dtm:
                latest_check_dtm = check_dtm
    if latest_check_dtm is not None:
        latest_data[resource_id] = latest_check_dtm

# 결과 출력
for resource_id, check_dtm in latest_data.items():
    print(f"{resource_id:30} : {check_dtm}")
```
- 수행결과
```
01-[DB-MARIADDB-02]
02-[CONTAINER-EKS_JOB-01]
03-[DB-MYSQL_MEM-01]
04-[DB-MARIADDB-01]
05-[CONTAINER-EKSNODE-01]
06-[SYSTEM-EC2_INODE-01]
07-[SYSTEM-EC2_INODE-01]
08-[CSP-MSK_DISK-01]
09-[CONTAINER-EKS_DISK-01]
10-[CONTAINER-TX_ERROR-01]
11-[NETWORK-TGW_DROP-02]
['DB-MARIADDB-02',
 'CONTAINER-EKS_JOB-01',
 'DB-MYSQL_MEM-01',
 'DB-MARIADDB-01',
 'CONTAINER-EKSNODE-01',
 'SYSTEM-EC2_INODE-01',
 'CSP-MSK_DISK-01',
 'CONTAINER-EKS_DISK-01',
 'CONTAINER-TX_ERROR-01',
 'NETWORK-TGW_DROP-02']
DB-MARIADDB-02                 : 2023/07/05 09:00:21
CONTAINER-EKS_JOB-01           : 2023/07/05 09:01:06
DB-MYSQL_MEM-01                : 2023/07/05 09:00:38
DB-MARIADDB-01                 : 2023/07/05 09:00:19
CONTAINER-EKSNODE-01           : 2023/07/05 09:00:25
SYSTEM-EC2_INODE-01            : 2023/07/05 09:00:57
CSP-MSK_DISK-01                : 2023/07/05 09:01:05
CONTAINER-EKS_DISK-01          : 2023/07/05 09:00:54
CONTAINER-TX_ERROR-01          : 2023/07/05 09:00:46
NETWORK-TGW_DROP-02            : 2023/07/05 09:01:03
```