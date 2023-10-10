import boto3
from boto3.dynamodb.conditions import Key

table_name = 'dydb_system_check_lcl14'

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.Table(table_name)

resp = table.query(
    # IndexName="check_dtm_resource_id_index",
    KeyConditionExpression=Key('check_dtm').eq('2023070600')
)

print("The query returned the following items:")
for item in resp['Items']:
    print(item)