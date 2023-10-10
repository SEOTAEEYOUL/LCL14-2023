import boto3
from pprint import pprint
import datetime


table_name = 'dydb_system_check_lcl14'

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.Table(table_name)

# check_dtm = '2023070600'
check_dtm = datetime.datetime.now().strftime('%Y%m%d%H')

response = table.scan(
    # FilterExpression='begins_with(check_dtm, :check_dtm_val)',
    FilterExpression='begins_with(check_dtm, :check_dtm_val)',
    ExpressionAttributeValues={
        ':check_dtm_val': check_dtm
    }
)

print(f"The scan returned the following items:[{len(response)}]")
cnt = 0
for item in response['Items']:
    cnt += 1
    # pprint(item)
    check_dtm = item['check_dtm']
    resource_id = item['resource_id']
    check_result = item['check_result']
    print(f"{cnt:02}-{resource_id:30} : {check_dtm} : {check_result}")

print(f"총갯수[{cnt}]")

   