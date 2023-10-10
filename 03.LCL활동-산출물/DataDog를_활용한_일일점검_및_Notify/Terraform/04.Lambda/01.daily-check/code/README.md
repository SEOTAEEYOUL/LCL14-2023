# labmda_function

> [Boto3 Secrets Manager – Complete Tutorial](https://hands-on.cloud/boto3-secrets-manager-tutorial/)  

## 환경변수
```
$Env:AWS_PROFILE="lcl14"
$Env:AWS_SECRET_NAME="secret_manager_aws_lcl14"
$Env:DD_SECRET_NAME="secret_manager_datadog_lcl14"
$Env:REGION="ap-northeast-2"                     
```
```
$Env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/**********"
$Env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/**********"
$Env:SLACK_CHANNEL="# lcl14"
$Env:LAMBDA_URL="https://app.datadoghq.com/dashboard/**********"
$Env:LAMBDA_URL="https://**********.lambda-url.ap-northeast-2.on.aws/"
```

## 수행
```
python lambda_function.py
```

## Troubleshooting
### Terraform Lock 발생시
```
PS > terraform apply
╷
│ Error: Error acquiring the state lock
│
│ Error message: ConditionalCheckFailedException: The conditional request failed
│ Lock Info:
│   ID:        4368775e-cc49-4f2c-267f-595a55c6e34b
│   Path:      s3-terraform-lcl14/terraform/lambda/terraform.tfstate
│   Operation: OperationTypeApply
│   Who:       TAEYEOL-PC\taeey@TAEYEOL-PC
│   Version:   1.3.4
│   Created:   2023-06-24 03:48:32.8075293 +0000 UTC
│   Info:
│
│
│ Terraform acquires a state lock to protect the state from being written
│ by multiple users at the same time. Please resolve the issue above and try
│ again. For most commands, you can disable locking with the "-lock=false"
│ flag, but this is not recommended.
╵
PS > 
```

#### Lock 해제
```
PS > terraform force-unlock 4368775e-cc49-4f2c-267f-595a55c6e34b
Do you really want to force-unlock?
  Terraform will remove the lock on the remote state.
  This will allow local Terraform commands to modify this state, even though it
  may be still be in use. Only 'yes' will be accepted to confirm.

  Enter a value: yes

Terraform state has been successfully unlocked!

The state has been unlocked, and Terraform commands should now be able to
obtain a new lock on the remote state.
PS > 
```

## Slack
> [Slack으로 process가 정상적으로 시작되었는지 나타내는 이쁜 메시지 만들기(Incoming webhook과 Attachment message 활용)](https://blog.voidmainvoid.net/221)  

### Attachment
- image, url button, 기타 여러상태를 보여주고 싶을때 사용. 시각적으로 효과적 전달 가능  


## Code 단위 테스트
#### python datadog_helper.py 
```
PS code> python datadog_helper.py 
[{'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:TEST/AURORA/AA-ZqaIl5',
  'CreatedDate': datetime.datetime(2020, 9, 22, 23, 22, 41, 371000, tzinfo=tzlocal()),
  'LastAccessedDate': datetime.datetime(2022, 9, 27, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2020, 9, 22, 23, 22, 41, 371000, tzinfo=tzlocal()),
  'Name': 'TEST/AURORA/AA',
  'SecretVersionsToStages': {'cf103071-322f-4409-8402-5dba6ee928c7': ['AWSCURRENT'],
                             'd06b646e-5ff7-4fb2-b04d-eb8412c8960d': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'Name', 'Value': 'DS09449_secret'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret05580-uMSfCl',
  'CreatedDate': datetime.datetime(2021, 4, 23, 11, 27, 0, 399000, tzinfo=tzlocal()),
  'LastAccessedDate': datetime.datetime(2021, 4, 27, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 19, 17, 13, 16, 178000, tzinfo=tzlocal()),
  'Name': 'secret05580',
  'SecretVersionsToStages': {'ed402c34-c9db-4f57-9906-de9b55f18990': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:test/ds08800/aurora-QecuUI',
  'CreatedDate': datetime.datetime(2021, 4, 25, 2, 50, 56, 134000, tzinfo=tzlocal()),
  'Description': 'test/ds08800/aurora',
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 25, 2, 50, 56, 134000, tzinfo=tzlocal()),
  'Name': 'test/ds08800/aurora',
  'SecretVersionsToStages': {'7c24d9bd-0701-45a6-91fe-53bcaa1871e7': ['AWSPREVIOUS'],
                             'e2dcabd1-550b-477e-b5c8-85d6ef032296': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:testuser/ds08800/aurora-iWjvLO',
  'CreatedDate': datetime.datetime(2021, 4, 27, 14, 47, 1, 735000, tzinfo=tzlocal()),
  'Description': 'user1 proxy',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 27, 14, 47, 1, 735000, tzinfo=tzlocal()),
  'Name': 'testuser/ds08800/aurora',
  'SecretVersionsToStages': {'0507b3a1-74d1-4b18-b928-fff0fedadb11': ['AWSCURRENT'],
                             '733ed1c0-3472-44f1-94b2-7fa892e97e3c': ['AWSPREVIOUS']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyung-iNMiuV',
  'CreatedDate': datetime.datetime(2021, 4, 27, 15, 45, 22, 469000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2021, 5, 31, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 19, 11, 22, 28, 100000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyung',
  'SecretVersionsToStages': {'5c009b1f-d95a-4006-bc35-cb4a959a3a9f': ['AWSCURRENT'],
                             'e582fcce-7cb0-4cb7-839e-564febc9103f': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'creator', 'Value': '05580'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:testuser2/ds08800/aurora-5uUWY2',
  'CreatedDate': datetime.datetime(2021, 4, 27, 16, 36, 43, 318000, tzinfo=tzlocal()),
  'Description': 'testuser2/ds08800/aurora',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 27, 16, 36, 43, 318000, tzinfo=tzlocal()),
  'Name': 'testuser2/ds08800/aurora',
  'SecretVersionsToStages': {'55f5f446-4579-4f11-9798-3d2c60b0b2f3': ['AWSPREVIOUS'],
                             '5f97ed4a-78f8-487c-b271-657c56025b5c': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyung2-6sZEpi',
  'CreatedDate': datetime.datetime(2021, 4, 27, 17, 44, 11, 920000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2021, 5, 31, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 20, 16, 25, 18, 948000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyung2',
  'SecretVersionsToStages': {'4e4e1cf5-bfbb-4739-bc1f-fdc42b97042e': ['AWSCURRENT'],
                             '5f843428-b185-403e-bad3-1433332c77e0': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'creator', 'Value': '05580'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:ukyung-test-secret-BujbR7',
  'CreatedDate': datetime.datetime(2021, 4, 27, 18, 32, 47, 153000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastChangedDate': datetime.datetime(2023, 4, 19, 11, 18, 55, 556000, tzinfo=tzlocal()),
  'Name': 'ukyung-test-secret',
  'SecretVersionsToStages': {'0f488045-1a44-4146-a4f1-dabded2b095d': ['AWSCURRENT']},
  'Tags': [{'Key': 'creator', 'Value': 'ukyung'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyungt-KDTImo',
  'CreatedDate': datetime.datetime(2021, 4, 27, 18, 37, 49, 734000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastChangedDate': datetime.datetime(2023, 4, 20, 11, 9, 0, 49000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyungt',
  'SecretVersionsToStages': {'716946d8-a4b3-4b8f-bd21-3b71b347b1ec': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:user03/ds08800/aurora-0WD713',
  'CreatedDate': datetime.datetime(2021, 4, 27, 19, 8, 3, 829000, tzinfo=tzlocal()),
  'Description': 'user03/ds08800/aurora',
  'LastChangedDate': datetime.datetime(2023, 4, 20, 12, 55, 3, 677000, tzinfo=tzlocal()),
  'Name': 'user03/ds08800/aurora',
  'SecretVersionsToStages': {'9de7bb35-0575-4558-9821-2ef7a7da8174': ['AWSCURRENT']},
  'Tags': []}]
{'api_key': 'a91ffcb920f040f74fd0f0612bda70df',
 'app_key': '73db9c713f601a5855a2f1a6ae7a5afe1c2a6748',
 'public_id': '06286340-0906-11ed-ac07-da7ad0900002'}
api_key[a91ffcb920f040f74fd0f0612bda70df], app_key[73db9c713f601a5855a2f1a6ae7a5afe1c2a6748], public_id[06286340-0906-11ed-ac07-da7ad0900002]
PS code> 
```

#### python lambda_function.py 
```
PS code> python lambda_function.py
SLACK_WEBHOOK_URL[https://hooks.slack.com/services/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]
SLACK_CHANNEL[# lcl14]
AWS_REGION[ap-northeast-2]
[{'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:TEST/AURORA/AA-ZqaIl5',
  'CreatedDate': datetime.datetime(2020, 9, 22, 23, 22, 41, 371000, tzinfo=tzlocal()),
  'LastAccessedDate': datetime.datetime(2022, 9, 27, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2020, 9, 22, 23, 22, 41, 371000, tzinfo=tzlocal()),
  'Name': 'TEST/AURORA/AA',
  'SecretVersionsToStages': {'cf103071-322f-4409-8402-5dba6ee928c7': ['AWSCURRENT'],
                             'd06b646e-5ff7-4fb2-b04d-eb8412c8960d': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'Name', 'Value': 'DS09449_secret'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret05580-uMSfCl',
  'CreatedDate': datetime.datetime(2021, 4, 23, 11, 27, 0, 399000, tzinfo=tzlocal()),
  'LastAccessedDate': datetime.datetime(2021, 4, 27, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 19, 17, 13, 16, 178000, tzinfo=tzlocal()),
  'Name': 'secret05580',
  'SecretVersionsToStages': {'ed402c34-c9db-4f57-9906-de9b55f18990': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:test/ds08800/aurora-QecuUI',
  'CreatedDate': datetime.datetime(2021, 4, 25, 2, 50, 56, 134000, tzinfo=tzlocal()),
  'Description': 'test/ds08800/aurora',
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 25, 2, 50, 56, 134000, tzinfo=tzlocal()),
  'Name': 'test/ds08800/aurora',
  'SecretVersionsToStages': {'7c24d9bd-0701-45a6-91fe-53bcaa1871e7': ['AWSPREVIOUS'],
                             'e2dcabd1-550b-477e-b5c8-85d6ef032296': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:testuser/ds08800/aurora-iWjvLO',
  'CreatedDate': datetime.datetime(2021, 4, 27, 14, 47, 1, 735000, tzinfo=tzlocal()),
  'Description': 'user1 proxy',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 27, 14, 47, 1, 735000, tzinfo=tzlocal()),
  'Name': 'testuser/ds08800/aurora',
  'SecretVersionsToStages': {'0507b3a1-74d1-4b18-b928-fff0fedadb11': ['AWSCURRENT'],
                             '733ed1c0-3472-44f1-94b2-7fa892e97e3c': ['AWSPREVIOUS']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyung-iNMiuV',
  'CreatedDate': datetime.datetime(2021, 4, 27, 15, 45, 22, 469000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2021, 5, 31, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 19, 11, 22, 28, 100000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyung',
  'SecretVersionsToStages': {'5c009b1f-d95a-4006-bc35-cb4a959a3a9f': ['AWSCURRENT'],
                             'e582fcce-7cb0-4cb7-839e-564febc9103f': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'creator', 'Value': '05580'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:testuser2/ds08800/aurora-5uUWY2',
  'CreatedDate': datetime.datetime(2021, 4, 27, 16, 36, 43, 318000, tzinfo=tzlocal()),
  'Description': 'testuser2/ds08800/aurora',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 27, 16, 36, 43, 318000, tzinfo=tzlocal()),
  'Name': 'testuser2/ds08800/aurora',
  'SecretVersionsToStages': {'55f5f446-4579-4f11-9798-3d2c60b0b2f3': ['AWSPREVIOUS'],
                             '5f97ed4a-78f8-487c-b271-657c56025b5c': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyung2-6sZEpi',
  'CreatedDate': datetime.datetime(2021, 4, 27, 17, 44, 11, 920000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2021, 5, 31, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 20, 16, 25, 18, 948000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyung2',
  'SecretVersionsToStages': {'4e4e1cf5-bfbb-4739-bc1f-fdc42b97042e': ['AWSCURRENT'],
                             '5f843428-b185-403e-bad3-1433332c77e0': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'creator', 'Value': '05580'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:ukyung-test-secret-BujbR7',
  'CreatedDate': datetime.datetime(2021, 4, 27, 18, 32, 47, 153000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastChangedDate': datetime.datetime(2023, 4, 19, 11, 18, 55, 556000, tzinfo=tzlocal()),
  'Name': 'ukyung-test-secret',
  'SecretVersionsToStages': {'0f488045-1a44-4146-a4f1-dabded2b095d': ['AWSCURRENT']},
  'Tags': [{'Key': 'creator', 'Value': 'ukyung'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyungt-KDTImo',
  'CreatedDate': datetime.datetime(2021, 4, 27, 18, 37, 49, 734000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastChangedDate': datetime.datetime(2023, 4, 20, 11, 9, 0, 49000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyungt',
  'SecretVersionsToStages': {'716946d8-a4b3-4b8f-bd21-3b71b347b1ec': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:user03/ds08800/aurora-0WD713',
  'CreatedDate': datetime.datetime(2021, 4, 27, 19, 8, 3, 829000, tzinfo=tzlocal()),
  'Description': 'user03/ds08800/aurora',
  'LastChangedDate': datetime.datetime(2023, 4, 20, 12, 55, 3, 677000, tzinfo=tzlocal()),
  'Name': 'user03/ds08800/aurora',
  'SecretVersionsToStages': {'9de7bb35-0575-4558-9821-2ef7a7da8174': ['AWSCURRENT']},
  'Tags': []}]
{'api_key': 'a91ffcb920f040f74fd0f0612bda70df',
 'app_key': '73db9c713f601a5855a2f1a6ae7a5afe1c2a6748',
 'public_id': '06286340-0906-11ed-ac07-da7ad0900002'}
api_key[a91ffcb920f040f74fd0f0612bda70df], app_key[73db9c713f601a5855a2f1a6ae7a5afe1c2a6748], public_id[06286340-0906-11ed-ac07-da7ad0900002]
[{'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:TEST/AURORA/AA-ZqaIl5',
  'CreatedDate': datetime.datetime(2020, 9, 22, 23, 22, 41, 371000, tzinfo=tzlocal()),
  'LastAccessedDate': datetime.datetime(2022, 9, 27, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2020, 9, 22, 23, 22, 41, 371000, tzinfo=tzlocal()),
  'Name': 'TEST/AURORA/AA',
  'SecretVersionsToStages': {'cf103071-322f-4409-8402-5dba6ee928c7': ['AWSCURRENT'],
                             'd06b646e-5ff7-4fb2-b04d-eb8412c8960d': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'Name', 'Value': 'DS09449_secret'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret05580-uMSfCl',
  'CreatedDate': datetime.datetime(2021, 4, 23, 11, 27, 0, 399000, tzinfo=tzlocal()),
  'LastAccessedDate': datetime.datetime(2021, 4, 27, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 19, 17, 13, 16, 178000, tzinfo=tzlocal()),
  'Name': 'secret05580',
  'SecretVersionsToStages': {'ed402c34-c9db-4f57-9906-de9b55f18990': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:test/ds08800/aurora-QecuUI',
  'CreatedDate': datetime.datetime(2021, 4, 25, 2, 50, 56, 134000, tzinfo=tzlocal()),
  'Description': 'test/ds08800/aurora',
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 25, 2, 50, 56, 134000, tzinfo=tzlocal()),
  'Name': 'test/ds08800/aurora',
  'SecretVersionsToStages': {'7c24d9bd-0701-45a6-91fe-53bcaa1871e7': ['AWSPREVIOUS'],
                             'e2dcabd1-550b-477e-b5c8-85d6ef032296': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:testuser/ds08800/aurora-iWjvLO',
  'CreatedDate': datetime.datetime(2021, 4, 27, 14, 47, 1, 735000, tzinfo=tzlocal()),
  'Description': 'user1 proxy',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 27, 14, 47, 1, 735000, tzinfo=tzlocal()),
  'Name': 'testuser/ds08800/aurora',
  'SecretVersionsToStages': {'0507b3a1-74d1-4b18-b928-fff0fedadb11': ['AWSCURRENT'],
                             '733ed1c0-3472-44f1-94b2-7fa892e97e3c': ['AWSPREVIOUS']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyung-iNMiuV',
  'CreatedDate': datetime.datetime(2021, 4, 27, 15, 45, 22, 469000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2021, 5, 31, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 19, 11, 22, 28, 100000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyung',
  'SecretVersionsToStages': {'5c009b1f-d95a-4006-bc35-cb4a959a3a9f': ['AWSCURRENT'],
                             'e582fcce-7cb0-4cb7-839e-564febc9103f': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'creator', 'Value': '05580'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:testuser2/ds08800/aurora-5uUWY2',
  'CreatedDate': datetime.datetime(2021, 4, 27, 16, 36, 43, 318000, tzinfo=tzlocal()),
  'Description': 'testuser2/ds08800/aurora',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 27, 16, 36, 43, 318000, tzinfo=tzlocal()),
  'Name': 'testuser2/ds08800/aurora',
  'SecretVersionsToStages': {'55f5f446-4579-4f11-9798-3d2c60b0b2f3': ['AWSPREVIOUS'],
                             '5f97ed4a-78f8-487c-b271-657c56025b5c': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyung2-6sZEpi',
  'CreatedDate': datetime.datetime(2021, 4, 27, 17, 44, 11, 920000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2021, 5, 31, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 20, 16, 25, 18, 948000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyung2',
  'SecretVersionsToStages': {'4e4e1cf5-bfbb-4739-bc1f-fdc42b97042e': ['AWSCURRENT'],
                             '5f843428-b185-403e-bad3-1433332c77e0': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'creator', 'Value': '05580'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:ukyung-test-secret-BujbR7',
  'CreatedDate': datetime.datetime(2021, 4, 27, 18, 32, 47, 153000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastChangedDate': datetime.datetime(2023, 4, 19, 11, 18, 55, 556000, tzinfo=tzlocal()),
  'Name': 'ukyung-test-secret',
  'SecretVersionsToStages': {'0f488045-1a44-4146-a4f1-dabded2b095d': ['AWSCURRENT']},
  'Tags': [{'Key': 'creator', 'Value': 'ukyung'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyungt-KDTImo',
  'CreatedDate': datetime.datetime(2021, 4, 27, 18, 37, 49, 734000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastChangedDate': datetime.datetime(2023, 4, 20, 11, 9, 0, 49000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyungt',
  'SecretVersionsToStages': {'716946d8-a4b3-4b8f-bd21-3b71b347b1ec': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:user03/ds08800/aurora-0WD713',
  'CreatedDate': datetime.datetime(2021, 4, 27, 19, 8, 3, 829000, tzinfo=tzlocal()),
  'Description': 'user03/ds08800/aurora',
  'LastChangedDate': datetime.datetime(2023, 4, 20, 12, 55, 3, 677000, tzinfo=tzlocal()),
  'Name': 'user03/ds08800/aurora',
  'SecretVersionsToStages': {'9de7bb35-0575-4558-9821-2ef7a7da8174': ['AWSCURRENT']},
  'Tags': []}]
{'api_key': 'a91ffcb920f040f74fd0f0612bda70df',
 'app_key': '73db9c713f601a5855a2f1a6ae7a5afe1c2a6748',
 'public_id': '06286340-0906-11ed-ac07-da7ad0900002'}
api_key[a91ffcb920f040f74fd0f0612bda70df], app_key[73db9c713f601a5855a2f1a6ae7a5afe1c2a6748], public_id[06286340-0906-11ed-ac07-da7ad0900002]
[{'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:TEST/AURORA/AA-ZqaIl5',
  'CreatedDate': datetime.datetime(2020, 9, 22, 23, 22, 41, 371000, tzinfo=tzlocal()),
  'LastAccessedDate': datetime.datetime(2022, 9, 27, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2020, 9, 22, 23, 22, 41, 371000, tzinfo=tzlocal()),
  'Name': 'TEST/AURORA/AA',
  'SecretVersionsToStages': {'cf103071-322f-4409-8402-5dba6ee928c7': ['AWSCURRENT'],
                             'd06b646e-5ff7-4fb2-b04d-eb8412c8960d': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'Name', 'Value': 'DS09449_secret'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret05580-uMSfCl',
  'CreatedDate': datetime.datetime(2021, 4, 23, 11, 27, 0, 399000, tzinfo=tzlocal()),
  'LastAccessedDate': datetime.datetime(2021, 4, 27, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 19, 17, 13, 16, 178000, tzinfo=tzlocal()),
  'Name': 'secret05580',
  'SecretVersionsToStages': {'ed402c34-c9db-4f57-9906-de9b55f18990': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:test/ds08800/aurora-QecuUI',
  'CreatedDate': datetime.datetime(2021, 4, 25, 2, 50, 56, 134000, tzinfo=tzlocal()),
  'Description': 'test/ds08800/aurora',
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 25, 2, 50, 56, 134000, tzinfo=tzlocal()),
  'Name': 'test/ds08800/aurora',
  'SecretVersionsToStages': {'7c24d9bd-0701-45a6-91fe-53bcaa1871e7': ['AWSPREVIOUS'],
                             'e2dcabd1-550b-477e-b5c8-85d6ef032296': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:testuser/ds08800/aurora-iWjvLO',
  'CreatedDate': datetime.datetime(2021, 4, 27, 14, 47, 1, 735000, tzinfo=tzlocal()),
  'Description': 'user1 proxy',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 27, 14, 47, 1, 735000, tzinfo=tzlocal()),
  'Name': 'testuser/ds08800/aurora',
  'SecretVersionsToStages': {'0507b3a1-74d1-4b18-b928-fff0fedadb11': ['AWSCURRENT'],
                             '733ed1c0-3472-44f1-94b2-7fa892e97e3c': ['AWSPREVIOUS']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyung-iNMiuV',
  'CreatedDate': datetime.datetime(2021, 4, 27, 15, 45, 22, 469000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2021, 5, 31, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 19, 11, 22, 28, 100000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyung',
  'SecretVersionsToStages': {'5c009b1f-d95a-4006-bc35-cb4a959a3a9f': ['AWSCURRENT'],
                             'e582fcce-7cb0-4cb7-839e-564febc9103f': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'creator', 'Value': '05580'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:testuser2/ds08800/aurora-5uUWY2',
  'CreatedDate': datetime.datetime(2021, 4, 27, 16, 36, 43, 318000, tzinfo=tzlocal()),
  'Description': 'testuser2/ds08800/aurora',
  'LastAccessedDate': datetime.datetime(2022, 11, 17, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2021, 4, 27, 16, 36, 43, 318000, tzinfo=tzlocal()),
  'Name': 'testuser2/ds08800/aurora',
  'SecretVersionsToStages': {'55f5f446-4579-4f11-9798-3d2c60b0b2f3': ['AWSPREVIOUS'],
                             '5f97ed4a-78f8-487c-b271-657c56025b5c': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyung2-6sZEpi',
  'CreatedDate': datetime.datetime(2021, 4, 27, 17, 44, 11, 920000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastAccessedDate': datetime.datetime(2021, 5, 31, 9, 0, tzinfo=tzlocal()),
  'LastChangedDate': datetime.datetime(2023, 4, 20, 16, 25, 18, 948000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyung2',
  'SecretVersionsToStages': {'4e4e1cf5-bfbb-4739-bc1f-fdc42b97042e': ['AWSCURRENT'],
                             '5f843428-b185-403e-bad3-1433332c77e0': ['AWSPREVIOUS']},
  'Tags': [{'Key': 'creator', 'Value': '05580'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:ukyung-test-secret-BujbR7',
  'CreatedDate': datetime.datetime(2021, 4, 27, 18, 32, 47, 153000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastChangedDate': datetime.datetime(2023, 4, 19, 11, 18, 55, 556000, tzinfo=tzlocal()),
  'Name': 'ukyung-test-secret',
  'SecretVersionsToStages': {'0f488045-1a44-4146-a4f1-dabded2b095d': ['AWSCURRENT']},
  'Tags': [{'Key': 'creator', 'Value': 'ukyung'}]},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:05580cluster-ukyungt-KDTImo',
  'CreatedDate': datetime.datetime(2021, 4, 27, 18, 37, 49, 734000, tzinfo=tzlocal()),
  'KmsKeyId': 'arn:aws:kms:ap-northeast-2:123456789012:key/e6dca13e-994a-4c11-b87b-82696f678c39',
  'LastChangedDate': datetime.datetime(2023, 4, 20, 11, 9, 0, 49000, tzinfo=tzlocal()),
  'Name': '05580cluster-ukyungt',
  'SecretVersionsToStages': {'716946d8-a4b3-4b8f-bd21-3b71b347b1ec': ['AWSCURRENT']},
  'Tags': []},
 {'ARN': 'arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:user03/ds08800/aurora-0WD713',
  'CreatedDate': datetime.datetime(2021, 4, 27, 19, 8, 3, 829000, tzinfo=tzlocal()),
  'Description': 'user03/ds08800/aurora',
  'LastChangedDate': datetime.datetime(2023, 4, 20, 12, 55, 3, 677000, tzinfo=tzlocal()),
  'Name': 'user03/ds08800/aurora',
  'SecretVersionsToStages': {'9de7bb35-0575-4558-9821-2ef7a7da8174': ['AWSCURRENT']},
  'Tags': []}]
{'api_key': 'a91ffcb920f040f74fd0f0612bda70df',
 'app_key': '73db9c713f601a5855a2f1a6ae7a5afe1c2a6748',
 'public_id': '06286340-0906-11ed-ac07-da7ad0900002'}
api_key[a91ffcb920f040f74fd0f0612bda70df], app_key[73db9c713f601a5855a2f1a6ae7a5afe1c2a6748], public_id[06286340-0906-11ed-ac07-da7ad0900002]
{'created': '2023-04-14T08:49:02.655103+00:00',
 'created_at': 1681462142000,
 'creator': {'email': 'yjbang@sk.com',
             'handle': 'yjbang@sk.com',
             'id': 4671517,
             'name': None},
 'deleted': None,
 'id': 116390058,
 'message': '[참고 - 연결 정보]\n'
            '# Data망\n'
            '- dxcon-fh5l0k7k : 1st VIF (KINX)\n'
            '- dxcon-fg6pdahf : 2nd VIF (LG U+)\n'
            '# 신호수신망\n'
            '- dxcon-fh891mus : \x081st VIF (KINX)\n'
            '- dxcon-fg44j36q : 2nd VIF (KINX)\n'
            '- dxcon-fg6a3n0g : 3rd VIF (LG U+)\n'
            '# 고객센터망\n'
            '- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\n'
            '- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \n'
            '\n'
            '@slack-skshieldusnextossdev-prd알람 \n'
            '@slack-SKCC_Digital_Service-ict_shieldus_argos\n'
            '@slack-SKCC_Digital_Service-ict_shieldus_argos_l1',
 'modified': '2023-05-02T15:46:38.055414+00:00',
 'multi': True,
 'name': '[P1][Network] DX Connection Down ({{connectionid.name}})',
 'options': {'evaluation_delay': 900,
             'include_tags': True,
             'new_group_delay': 60,
             'notify_audit': False,
             'notify_no_data': False,
             'renotify_interval': 0,
             'require_full_window': False,
             'silenced': {},
             'thresholds': {'critical': 1.0}},
 'org_id': 708429,
 'overall_state': 'OK',
 'overall_state_modified': '2023-04-14T08:49:05+00:00',
 'priority': 1,
 'query': 'max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} '
          'by {connectionid} < 1',
 'restricted_roles': None,
 'tags': ['team:skcc', 'DOWN', 'Network'],
 'type': 'query alert'}
# EventName: [P1][Network] DX Connection Down ({{connectionid.name}})
# Status: AWS Direct Connect connection is up!
# Priority: 1
check_result[Y]
check_result_detail[{'id': 116390058, 'org_id': 708429, 'type': 'query alert', 'name': '[P1][Network] DX Connection Down ({{connectionid.name}})', 'message': '[참고 - 연결 정보]\n# Data망\n- dxcon-fh5l0k7k : 1st VIF (KINX)\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\n# 신호수신망\n- dxcon-fh891mus : \x081st VIF (KINX)\n- dxcon-fg44j36q : 2nd VIF (KINX)\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\n# 고객센터망\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \n\n@slack-skshieldusnextossdev-prd알람 \n@slack-SKCC_Digital_Service-ict_shieldus_argos\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1', 'tags': ['team:skcc', 'DOWN', 'Network'], 'query': 'max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1', 'options': {'thresholds': {'critical': 1.0}, 'notify_audit': False, 'require_full_window': False, 'notify_no_data': False, 'renotify_interval': 0, 'include_tags': True, 'evaluation_delay': 900, 'new_group_delay': 60, 'silenced': {}}, 'multi': True, 'created_at': 1681462142000, 'created': '2023-04-14T08:49:02.655103+00:00', 'modified': '2023-05-02T15:46:38.055414+00:00', 'deleted': None, 'restricted_roles': None, 'priority': 1, 'overall_state_modified': '2023-04-14T08:49:05+00:00', 'overall_state': 'OK', 'creator': {'name': None, 'handle': 'yjbang@sk.com', 'email': 'yjbang@sk.com', 'id': 4671517}}]
데이터 삽입이 성공적으로 완료되었습니다.
send_message_to_slack(resource_id[NETWORK-DX-01] 에 대한 검사 및 DynamoDB 저장소 저장 성공)
text[resource_id[NETWORK-DX-01] 에 대한 검사 및 DynamoDB 저장소 저장 성공]
payload[{'username': 'L2운영/T Biz Cloud', 'channel': '# lcl14', 'icon_emoji': ':satellite:', 'text': 'resource_id[NETWORK-DX-01] 에 대한 검사 및 DynamoDB 저장소 저장 성공'}]   
send_text[{"username": "L2\uc6b4\uc601/T Biz Cloud", "channel": "# lcl14", "icon_emoji": ":satellite:", "text": "resource_id[NETWORK-DX-01] \uc5d0 \ub300\ud55c \uac80\uc0ac \ubc0f DynamoDB \uc800\uc7a5\uc18c \uc800\uc7a5 \uc131\uacf5"}]
{'resource_id': {'S': '1'}, 'check_result_detail': {'S': '{"key1": "value1", "key2": "value2"}'}, 'check_dtm': {'S': '20230623 192336'}, 'check_result': {'S': 'Y'}}
{'resource_id': {'S': 'example_resource_id'}, 'check_result_detail': {'S': '{"detail_key": "detail_value"}'}, 'check_dtm': {'S': '20230623 191434'}, 'check_result': {'S': 'success'}}
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:35:37'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:37:40'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:38:26'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:40:07'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:43:08'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:43:23'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:47:03'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 17:07:54'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 17:08:42'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:28:10'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:28:49'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:30:22'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:32:05'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:57:13'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:59:07'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "created_at": 1681462142000,\n  "creator": {\n    "email": "yjbang@sk.com",\n    "handle": "yjbang@sk.com",\n    "id": 4671517,\n    "name": null\n  },\n  "deleted": null,\n  "id": 116390058,\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "multi": true,\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "options": {\n    "evaluation_delay": 900,\n    "include_tags": true,\n    "new_group_delay": 60,\n    "notify_audit": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "require_full_window": false,\n    "silenced": {},\n    "thresholds": {\n      "critical": 1.0\n    }\n  },\n  "org_id": 708429,\n  "overall_state": "OK",\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "priority": 1,\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "restricted_roles": null,\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "type": "query alert"\n}'}, 'check_dtm': {'S': '20230626 141251'}, 'check_result': {'S': 'Y'}}       
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "created_at": 1681462142000,\n  "creator": {\n    "email": "yjbang@sk.com",\n    "handle": "yjbang@sk.com",\n    "id": 4671517,\n    "name": null\n  },\n  "deleted": null,\n  "id": 116390058,\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "multi": true,\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "options": {\n    "evaluation_delay": 900,\n    "include_tags": true,\n    "new_group_delay": 60,\n    "notify_audit": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "require_full_window": false,\n    "silenced": {},\n    "thresholds": {\n      "critical": 1.0\n    }\n  },\n  "org_id": 708429,\n  "overall_state": "OK",\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "priority": 1,\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "restricted_roles": null,\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "type": "query alert"\n}'}, 'check_dtm': {'S': '20230626 142257'}, 'check_result': {'S': 'Y'}}       
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "created_at": 1681462142000,\n  "creator": {\n    "email": "yjbang@sk.com",\n    "handle": "yjbang@sk.com",\n    "id": 4671517,\n    "name": null\n  },\n  "deleted": null,\n  "id": 116390058,\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "multi": true,\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "options": {\n    "evaluation_delay": 900,\n    "include_tags": true,\n    "new_group_delay": 60,\n    "notify_audit": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "require_full_window": false,\n    "silenced": {},\n    "thresholds": {\n      "critical": 1.0\n    }\n  },\n  "org_id": 708429,\n  "overall_state": "OK",\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "priority": 1,\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "restricted_roles": null,\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "type": "query alert"\n}'}, 'check_dtm': {'S': '20230626 142320'}, 'check_result': {'S': 'Y'}}       
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "created_at": 1681462142000,\n  "creator": {\n    "email": "yjbang@sk.com",\n    "handle": "yjbang@sk.com",\n    "id": 4671517,\n    "name": null\n  },\n  "deleted": null,\n  "id": 116390058,\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "multi": true,\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "options": {\n    "evaluation_delay": 900,\n    "include_tags": true,\n    "new_group_delay": 60,\n    "notify_audit": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "require_full_window": false,\n    "silenced": {},\n    "thresholds": {\n      "critical": 1.0\n    }\n  },\n  "org_id": 708429,\n  "overall_state": "OK",\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "priority": 1,\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "restricted_roles": null,\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "type": "query alert"\n}'}, 'check_dtm': {'S': '20230626 142345'}, 'check_result': {'S': 'Y'}}       
{'resource_id': {'S': '1'}, 'check_result_detail': {'S': '{"key1": "value1", "key2": "value2"}'}, 'check_dtm': {'S': '20230623 192336'}, 'check_result': {'S': 'Y'}}
{'resource_id': {'S': 'example_resource_id'}, 'check_result_detail': {'S': '{"detail_key": "detail_value"}'}, 'check_dtm': {'S': '20230623 191434'}, 'check_result': {'S': 'success'}}
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:35:37'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:37:40'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:38:26'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:40:07'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:43:08'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:43:23'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 16:47:03'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 17:07:54'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/26 17:08:42'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:28:10'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:28:49'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:30:22'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:32:05'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:57:13'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "id": 116390058,\n  "org_id": 708429,\n  "type": "query alert",\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "options": {\n    "thresholds": {\n      "critical": 1.0\n    },\n    "notify_audit": false,\n    "require_full_window": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "include_tags": true,\n    "evaluation_delay": 900,\n    "new_group_delay": 60,\n    "silenced": {}\n  },\n  "multi": true,\n  "created_at": 1681462142000,\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "deleted": null,\n  "restricted_roles": null,\n  "priority": 1,\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "overall_state": "OK",\n  "creator": {\n    "name": null,\n    "handle": "yjbang@sk.com",\n    "email": "yjbang@sk.com",\n    "id": 4671517\n  }\n}'}, 'check_dtm': {'S': '2023/06/27 00:59:07'}, 'check_result': {'S': 'Y'}}   
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "created_at": 1681462142000,\n  "creator": {\n    "email": "yjbang@sk.com",\n    "handle": "yjbang@sk.com",\n    "id": 4671517,\n    "name": null\n  },\n  "deleted": null,\n  "id": 116390058,\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "multi": true,\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "options": {\n    "evaluation_delay": 900,\n    "include_tags": true,\n    "new_group_delay": 60,\n    "notify_audit": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "require_full_window": false,\n    "silenced": {},\n    "thresholds": {\n      "critical": 1.0\n    }\n  },\n  "org_id": 708429,\n  "overall_state": "OK",\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "priority": 1,\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "restricted_roles": null,\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "type": "query alert"\n}'}, 'check_dtm': {'S': '20230626 141251'}, 'check_result': {'S': 'Y'}}       
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "created_at": 1681462142000,\n  "creator": {\n    "email": "yjbang@sk.com",\n    "handle": "yjbang@sk.com",\n    "id": 4671517,\n    "name": null\n  },\n  "deleted": null,\n  "id": 116390058,\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "multi": true,\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "options": {\n    "evaluation_delay": 900,\n    "include_tags": true,\n    "new_group_delay": 60,\n    "notify_audit": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "require_full_window": false,\n    "silenced": {},\n    "thresholds": {\n      "critical": 1.0\n    }\n  },\n  "org_id": 708429,\n  "overall_state": "OK",\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "priority": 1,\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "restricted_roles": null,\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "type": "query alert"\n}'}, 'check_dtm': {'S': '20230626 142257'}, 'check_result': {'S': 'Y'}}       
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "created_at": 1681462142000,\n  "creator": {\n    "email": "yjbang@sk.com",\n    "handle": "yjbang@sk.com",\n    "id": 4671517,\n    "name": null\n  },\n  "deleted": null,\n  "id": 116390058,\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "multi": true,\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "options": {\n    "evaluation_delay": 900,\n    "include_tags": true,\n    "new_group_delay": 60,\n    "notify_audit": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "require_full_window": false,\n    "silenced": {},\n    "thresholds": {\n      "critical": 1.0\n    }\n  },\n  "org_id": 708429,\n  "overall_state": "OK",\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "priority": 1,\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "restricted_roles": null,\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "type": "query alert"\n}'}, 'check_dtm': {'S': '20230626 142320'}, 'check_result': {'S': 'Y'}}       
{'resource_id': {'S': 'NETWORK-DX-01'}, 'check_result_detail': {'S': '{\n  "created": "2023-04-14T08:49:02.655103+00:00",\n  "created_at": 1681462142000,\n  "creator": {\n    "email": "yjbang@sk.com",\n    "handle": "yjbang@sk.com",\n    "id": 4671517,\n    "name": null\n  },\n  "deleted": null,\n  "id": 116390058,\n  "message": "[\\ucc38\\uace0 - \\uc5f0\\uacb0 \\uc815\\ubcf4]\\n# Data\\ub9dd\\n- dxcon-fh5l0k7k : 1st VIF (KINX)\\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\\n# \\uc2e0\\ud638\\uc218\\uc2e0\\ub9dd\\n- dxcon-fh891mus : \\b1st VIF (KINX)\\n- dxcon-fg44j36q : 2nd VIF (KINX)\\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\\n# \\uace0\\uac1d\\uc13c\\ud130\\ub9dd\\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \\n\\n@slack-skshieldusnextossdev-prd\\uc54c\\ub78c \\n@slack-SKCC_Digital_Service-ict_shieldus_argos\\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1",\n  "modified": "2023-05-02T15:46:38.055414+00:00",\n  "multi": true,\n  "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",\n  "options": {\n    "evaluation_delay": 900,\n    "include_tags": true,\n    "new_group_delay": 60,\n    "notify_audit": false,\n    "notify_no_data": false,\n    "renotify_interval": 0,\n    "require_full_window": false,\n    "silenced": {},\n    "thresholds": {\n      "critical": 1.0\n    }\n  },\n  "org_id": 708429,\n  "overall_state": "OK",\n  "overall_state_modified": "2023-04-14T08:49:05+00:00",\n  "priority": 1,\n  "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1",\n  "restricted_roles": null,\n  "tags": [\n    "team:skcc",\n    "DOWN",\n    "Network"\n  ],\n  "type": "query alert"\n}'}, 'check_dtm': {'S': '20230626 142345'}, 'check_result': {'S': 'Y'}}       
PS code> 
```

## Test
### Slack Helper - Secret Manager/Slack Channel 로 메시지 전송
```
$Env:REGION="ap-northeast-2"
$Env:AWS_PROFILE="lcl14"
$Env:SLACK_SECRET_NAME="secret_manager_slack_argos" 
$Env:DYNAMODB_TABLE_NAME="dydb_system_check_argos"
$Env:DD_SECRET_NAME='secret_manager_datadog_argos'
python slack_helper.py
python lambda_function.py
```

## Crontab의 시간 설정

| Expressions | Desc |  
|:---|:---|  
| 1 11 3 * * | 분 시 일 월 요일 |  
| * * * * * | 매일 1분마다 실행 |  
| 5 * * * * | 매일 매시간 05분에 실행 (1시간 간격으로 실행) | 
| */5 * * * * | 매일 5분마다 실행 | 
| */10 * * * * | 매일 10분마다 실행 | 
| 0,10,20,30,40,50 * * * * | 매일 10분마다 실행 | 
| 0 18 * * * | 매일 18시 00분에 실행 | 
| 45 22 * * * | 매일 22시 45분에 실행 | 
| 28 03 * * * | 매일 03시 28분에 실행 | 
| * 1 * * * | 매일 01시 00분 ~ 01시 59분 사이에 1분 간격으로 실행 | 
| 0 */1 * * * | 매일 1시간 간격으로 실행 (매시간 00분) | 
| 0 */12 * * * | 매일 12시간마다 실행 | 
| 0 6,12 * * * | 매일 06시, 12시에 실행 | 
| 10 2-5 * * * | 매일 02시 ~ 05시 사이 매시간 10분에 실행 </br> (02시 10분, 03시 10분, 04시 10분, 05시 10분) | 
| 5 8-20/3 * * * | 매일 08시 ~ 20시 사이 3시간 간격으로 05분에 실행 </br> (08시 05분, 11시 05분, 14시 05분, 17시 05분, 20시 05분) |  
| 42 4 10 * * | 매달 10일 04시 42분에 실행 | 
| 30 5 1,15 * * | 매달 1일과 15일 05시 30분에 실행 | 
| 0-10 17 1 * * | 매달 1일 17시 00분 ~ 17시 10분까지 1분 단위로 실행 | 
| 0 17 * * 1 | 매주 월요일 17시 00분에 실행 | 
| 0,10 17 * * 0,2,3 | 매주 일, 화, 수요일 17시 00분과 17시 10분에 실행 | 
| 0 0 1,15 * 1 | 매달 1일과 15일 그리고 월요일 24시 00분에 실행 | 
| 0 6,12 * * 0,3 | 수, 일요일마다 06시, 12시에 실행 | 
| 0 21 * * 1-6 | 월 ~ 토 21시 00분에 실행 |  
