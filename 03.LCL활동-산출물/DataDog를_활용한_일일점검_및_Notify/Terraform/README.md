# Terraform 
- LCL 14 에서 설계한 자원 생성  
- 일일 점검

| 자원 | 이름 | 용도 |  
|:---|:---|:---|  
| S3 Bucket | s3-terraform-lcl14 | Terraform 공동작업용</br>(Terraform Backend) |  
| Dynamo DB Table | dydb-terraform-lcl14 | Terraform 공동작업용</br>(Terraform Backend) |  
| S3 Bucket | s3-bucket-lcl14 | 정적 문서 저장용 |  
| Dynamo DB Table | dynamodb_system_check_lcl14 | Alert 수행 결과 저장용 |  
| CloudWatch EventBridge | cloudwatch-event-rule-lcl14_function_0 | CronJob 형태로 Lambda 호출용을 사용 |  
| Lambda | lcl14_function_0 | Datadog Alert 수행용 | 
| Datadog Alert | lcl14_datadog_alert | AWS 자원 모니터링을 위한 Alert |   


## 기본 명령
#### `terraform version`
```
PS > 
Terraform v1.3.4
on windows_amd64

Your version of Terraform is out of date! The latest version
is 1.5.1. You can update by downloading from https://www.terraform.io/downloads.html
PS > 
```
#### `terraform init`

#### `terraform plan`
#### `terraform apply`
#### `terraform destroy`
#### `terraform state list`
#### `terraform output`

## [00.backend](./00.backend/README.md)
- Terraform 공동 작업을 위한 `terraform.tfstate` 저장소 (S3) 생성
- S3 저장소 접근을 위한 Lock Table 생성 (DynamoDB)

## [01.Datadog](./01.Datadog/README.md)  
- Backend 사용(S3, DynamoDB)
- Provider : Datadog

## [02.S3](./02.S3/README.md)  
- 점검 결과를 보여주는 정적 웹페이지를 담는 저장소

## [03.DynamoDB](./03.DynamoDB/README.md)  
- 점검 결과를 담는 Table

## [04.Lambda](./04.Lambda/README.md)
- Backend 사용(S3, DynamoDB)
- Provider : AWS
- S3 : static 문서(Template) 저장소 - system_check.html
- DynamoDB : 
- Lambda
  - 소스 : ./code 디렉토리
  - 아키이브 : ./artifacts/lambda.zip