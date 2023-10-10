import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.create_table(
    TableName='dynamodb_system_check_lcl14',
    KeySchema=[
        {
            'AttributeName': 'check_dtm',
            'KeyType': 'HASH'  # Use 'RANGE' if you want a composite key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'check_dtm',
            'AttributeType': 'S'  # Assuming check_dtm is of type string
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)