import os
import json
import boto3
from pprint import pprint

client = boto3.client('secretsmanager')
response = client.list_secrets()
pprint(response['SecretList'])


secret_name = os.getenv('DD_SECRET_NAME')  # 시크릿의 이름을 지정하세요.
region_name = os.getenv('REGION')          # 시크릿 매니저가 있는 지역을 지정하세요.

response = client.get_secret_value(
    SecretId=secret_name
)
dd_secrets = json.loads(response['SecretString'])
pprint(dd_secrets)
api_key = dd_secrets['api_key']
app_key = dd_secrets['app_key']
public_id = dd_secrets['public_id']

print(f"api_key[{api_key}], app_key[{app_key}], public_id[{public_id}]")