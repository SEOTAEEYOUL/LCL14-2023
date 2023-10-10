# labmda_function

## 환경변수
```
$Env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/**********t"
$Env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T0**********F0CYCDj"
$Env:SLACK_CHANNEL="# lcl14"
$Env:LAMBDA_URL="https://app.datadoghq.com/dashboard/x**********1687422510928&live=true"
$Env:LAMBDA_URL="https://**********.lambda-url.ap-northeast-2.on.aws/"
```

```
$Env:AWS_PROFILE="lcl14"
$Env:AWS_SECRET_NAME="secret_manager_aws_lcl14"
$Env:DD_SECRET_NAME="secret_manager_datadog_lcl14"
$Env:REGION="ap-northeast-2"                     
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
