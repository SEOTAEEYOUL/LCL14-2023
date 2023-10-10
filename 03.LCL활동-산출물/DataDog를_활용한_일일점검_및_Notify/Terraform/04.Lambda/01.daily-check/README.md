# 일일점검

## DONE:
- Datadog Alert 를 이용한 일일점검 및 결과를 DynamoDB 에 저장
- 점검 결과를 Slack 으로 전송
- Slack 을 통해 개별 상세 점검 결과를 조회하는 Page 를 작성함
  - https://**********.lambda-url.ap-northeast-2.on.aws/?resource_id=CONTAINER-POD_UNSCHEDULABLE-01&check_dtm=2023070620

## TODO:
- 일일 점검 결과를 정적 Page (HTML)로 만들어 S3 에 저장하는 것을 해야 함
- HTML 형태에 고려 필요
 

> [Creating AWS Lambda functions with Terraform](https://pfertyk.me/2023/02/creating-aws-lambda-functions-with-terraform/)  
> [Datadog Docs API](https://docs.datadoghq.com/api/latest/)  
> [datadog-api-client 2.13.2](https://pypi.org/project/datadog-api-client/)  
> [Lambda 함수에서 계층(Layer) 사용](https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/invocation-layers.html)  
> [Boto3 Secrets Manager – Complete Tutorial](https://hands-on.cloud/boto3-secrets-manager-tutorial/)  
> [AWS Secrets Manager에 대한 권한 정책 예](https://docs.aws.amazon.com/ko_kr/secretsmanager/latest/userguide/auth-and-access_examples.html)  

## Lambda
| 항목 | 값 | 설명 |  
|:---|:---|:---|  
| Lambda Source | ./code/lambda_function.py | 간단한 Python 예제 소스 |  
| Lambda Function 명 | lcl14_function_01 | `Amazon EventBridge` 에서 호출 받을 경우 `Slack` 채널로 Alarm 을 보냄 </br> Slack link 를 타고 호출 될 경우 Browser상에 출력할 HTML 를 만들어 반환 |  
| AWS Secrets Manager | secret_manager_datadog_lcl14 | datadog api/app key 저장 |  
| AWS Secrets Manager | secret_manager_slack_lcl14 | slack incoming webhook/channel 저장 |  
| Python 버전 | 3.9 | |  
| IAM | iam_lcl14_function_01 | Role |  
| IAM | policy_lcl14_function_01 | Policy | 
| Amazon EventBride | cloudwatch-event-rule-lcl14_function_01 | 주기적(5/60분/하루) 주기로 lambda 를 호출 |  

### 환경변수
| 항목 | 값 | 설명 |  
|:---|:---|:---|  
| DD_SECRET_NAME | secret_manager_datadog_lcl14 | |  
| DYNAMODB_TABLE_NAME | dydb_system_check_lcl14 | |  
| REGION | ap-northeast-2 | |  
| S3_BUCKET_NAME | s3-bucket-lcl14 | |  
| SLACK_SECRET_NAME | secret_manager_slack_lcl14 | |  

## Lambda Layer
### Layer 을 만들기 위해 Package 설치 or terraform null statement 사용 
- pip install pymysql -t .
- python 런타임일 경우 항상 폴더명은 python 이어야 함
  - 가장 상위의 경로가 python 폴더이고, 그 안에 패키지가 있어야 함
```
PS code> pip install -t layer requests python-dotenv datadog
Collecting requests
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.6/62.6 kB 3.3 MB/s eta 0:00:00
Collecting python-dotenv
  Using cached python_dotenv-1.0.0-py3-none-any.whl (19 kB)
Collecting datadog
  Using cached datadog-0.45.0-py2.py3-none-any.whl (113 kB)
Collecting charset-normalizer<4,>=2 (from requests)
  Using cached charset_normalizer-3.1.0-cp311-cp311-win_amd64.whl (96 kB)
Collecting idna<4,>=2.5 (from requests)
  Using cached idna-3.4-py3-none-any.whl (61 kB)
Collecting urllib3<3,>=1.21.1 (from requests)
  Downloading urllib3-2.0.3-py3-none-any.whl (123 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 123.6/123.6 kB 7.1 MB/s eta 0:00:00
Collecting certifi>=2017.4.17 (from requests)
  Downloading certifi-2023.5.7-py3-none-any.whl (156 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 157.0/157.0 kB 9.2 MB/s eta 0:00:00
Installing collected packages: urllib3, python-dotenv, idna, charset-normalizer, certifi, requests, datadog
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
botocore 1.29.110 requires urllib3<1.27,>=1.25.4, but you have urllib3 2.0.3 which is incompatible.
datadog-api-client 2.13.2 requires urllib3<2.0,>=1.15, but you have urllib3 2.0.3 which is incompatible.
Successfully installed certifi-2023.5.7 charset-normalizer-3.1.0 datadog-0.45.0 idna-3.4 python-dotenv-1.0.0 requests-2.31.0 urllib3-2.0.3
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\certifi already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\certifi-2023.5.7.dist-info already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\charset_normalizer already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\charset_normalizer-3.1.0.dist-info already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\dotenv already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\idna already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\idna-3.4.dist-info already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\python_dotenv-1.0.0.dist-info already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\requests already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\requests-2.31.0.dist-info already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\urllib3 already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\urllib3-2.0.3.dist-info already exists. Specify --upgrade to force replacement.
WARNING: Target directory D:\workspace\LCL-14\03.운영자료\DataDog\Terraform\04.Lambda\01.collecting\layer\bin already exists. Specify --upgrade to force replacement.
PS code> 
```


#### ※ 현재는 Terraform null_resource 로 `pip install` 처리함

### Source Tree
```
├── code
│   └── lambda_funtion.py
├── layer
│   └── python
│       └── (Python dependencies)
├── lambda.tf
├── main.tf
└── requirements.txt
```
![src-tree.png](./img/src-tree.png)  

## 소스
| 소스명 | 설명 |  
|:---|:---|  
| backend.tf | 공동 작업을 위한 S3, DynamoDB 정보 |  
| provider.tf | AWS |  
| iam.tf | lambda 실행을 위한 iam role 생성 |  
| main.tf | lambda 생성을 위한 account 정보 |  
| lambda.tf | AWS Labmda 생성 - Python |  
| function_url.tf | Datadog Alarm 수행 결과를 확인하기 위한 Lambda Fuction URL 생성 |   
| cloudwatch_event.tf | CloudWatch EventBride 생성 |  
| variables.tf | terraform 에서 사용할 변수 기술 |  
| terraform.tfvars | terraform 변수의 기본 인자로 넘겨줄 값 기술 - AWS Profile, Region, 함수명 등 |  
| output.tf | `terraform output` 수행시 나오는 값에 대해 기술 |  

## 수행 결과 Capture 화면
![lambda-iam-0.png](./img/lambda-iam-0.png)  
![lambda-iam-1.png](./img/lambda-iam-1.png)  
![lambda.png](./img/lambda.png)  
![lambda-cloudwatch-event.png](./img/lambda-cloudwatch-event.png)  
![lambda-cloudwatch-event-1.png](./img/lambda-cloudwatch-event-1.png)  
![slack-alarm.png](./img/slack-alarm.png)  
![lambda-slack-link-brower.png](./img/lambda-slack-link-brower.png)  

```
$Env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/**********"
$Env:SLACK_CHANNEL="lcl14"
$Env:LAMBDA_URL="https://app.datadoghq.com/dashboard/**********"
```

## Error - Troubleshooting
### cannot import name 'DEFAULT_CIPHERS' from 'urllib3.util.ssl_
```
[ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': cannot import name 'DEFAULT_CIPHERS' from 'urllib3.util.ssl_' (/opt/python/urllib3/util/ssl_.py)
Traceback (most recent call last):
[ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': cannot import name 'DEFAULT_CIPHERS' from 'urllib3.util.ssl_' (/opt/python/urllib3/util/ssl_.py) Traceback (most recent call last):
```

### 해법
- 아래 library 에 버전을 명기하여 lambda 를 배포함
```
python-dotenv
requests==2.28.2
urllib3==1.26.15
datadog
datadog-api-client
boto3==1.26.110
```

## Terraform

1. terraform init - 초기화 (provider 설치)
2. terraform plan - 생성 및 수정, 삭제할 자원을 보여줌
3. terraform apply - 자원 생성 및 backend(S3) 에 현재 자원 상태(tfstate) 저장
4. terraform state list - 상태 보기
5. terraform output - output.tf 에 지정된 자원에 대해 보여줌
6. terraform destroy - 생성된 자원을 삭제 (주의)

### terraform init
```
PS > terraform init

Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/aws from the dependency lock file
- Finding latest version of hashicorp/archive...
- Using previously-installed hashicorp/aws v5.4.0
- Installing hashicorp/archive v2.4.0...
- Installed hashicorp/archive v2.4.0 (signed by HashiCorp)

Terraform has made some changes to the provider dependency selections recorded
in the .terraform.lock.hcl file. Review those changes and commit them to your
version control system if they represent changes you intended to make.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
PS >
```

### terraform plan
```
PS > terraform plan
data.archive_file.python_lambda_package: Reading...
data.archive_file.python_lambda_layer_package: Reading...
data.archive_file.python_lambda_layer_package: Read complete after 0s [id=dbcdeca3dda8cae9d031cc9f367492ff39e5316f]
data.archive_file.python_lambda_package: Read complete after 0s [id=dbcdeca3dda8cae9d031cc9f367492ff39e5316f]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]  
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]

Terraform used the selected providers to generate the following execution plan. Resource        
actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda will be created
  + resource "aws_cloudwatch_event_rule" "cloudwatch-event-rule-lambda" {
      + arn                 = (known after apply)
      + description         = "Schedule lambda function"
      + event_bus_name      = "default"
      + id                  = (known after apply)
      + is_enabled          = true
      + name                = "cloudwatch-event-rule-lcl14_function_01"
      + name_prefix         = (known after apply)
      + schedule_expression = "rate(5 minutes)"
      + tags_all            = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
    }

  # aws_cloudwatch_event_target.lambda-function-target will be created
  + resource "aws_cloudwatch_event_target" "lambda-function-target" {
      + arn            = (known after apply)
      + event_bus_name = "default"
      + id             = (known after apply)
      + rule           = "cloudwatch-event-rule-lcl14_function_01"
      + target_id      = "cloudwatch-event-target-lcl14_function_01"
    }

  # aws_iam_policy.lambda will be created
  + resource "aws_iam_policy" "lambda" {
      + arn         = (known after apply)
      + id          = (known after apply)
      + name        = "policy_lcl14_function_01"
      + name_prefix = (known after apply)
      + path        = "/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "logs:CreateLogGroup",
                        ]
                      + Effect   = "Allow"
                      + Resource = "arn:aws:logs:ap-northeast-2:123456789012:*"
                    },
                  + {
                      + Action   = [
                          + "logs:CreateLogStream",
                          + "logs:PutLogEvents",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/lambda/lcl14_function_01:*",
                        ]
                    },
                  + {
                      + Action   = [
                          + "s3:*",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:s3:::*",
                        ]
                    },
                  + {
                      + Action   = [
                          + "dynamodb:*",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:dynamodb:ap-northeast-2:123456789012:table/*",
                        ]
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + policy_id   = (known after apply)
      + tags_all    = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
    }

  # aws_iam_role.lambda will be created
  + resource "aws_iam_role" "lambda" {
      + arn                   = (known after apply)
      + assume_role_policy    = jsonencode(
            {
              + Statement = [
                  + {
                      + Action    = "sts:AssumeRole"
                      + Effect    = "Allow"
                      + Principal = {
                          + Service = "lambda.amazonaws.com"
                        }
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + create_date           = (known after apply)
      + force_detach_policies = false
      + id                    = (known after apply)
      + managed_policy_arns   = (known after apply)
      + max_session_duration  = 3600
      + name                  = "iam_lcl14_function_01"
      + name_prefix           = (known after apply)
      + path                  = "/"
      + tags_all              = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
      + unique_id             = (known after apply)
    }

  # aws_iam_role_policy_attachment.iam_for_lambda will be created
  + resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
      + id         = (known after apply)
      + policy_arn = (known after apply)
      + role       = "iam_lcl14_function_01"
    }

  # aws_lambda_function.lambda_function will be created
  + resource "aws_lambda_function" "lambda_function" {
      + architectures                  = (known after apply)
      + arn                            = (known after apply)
      + filename                       = "./artifacts/lambda.zip"
      + function_name                  = "lcl14_function_01"
      + handler                        = "lambda_function.lambda_handler"
      + id                             = (known after apply)
      + invoke_                     = (known after apply)
      + last_modified                  = (known after apply)
      + layers                         = (known after apply)
      + memory_size                    = 128
      + package_type                   = "Zip"
      + publish                        = false
      + qualified_arn                  = (known after apply)
      + qualified_invoke_arn           = (known after apply)
      + reserved_concurrent_executions = -1
      + role                           = (known after apply)
      + runtime                        = "python3.9"
      + signing_job_arn                = (known after apply)
      + signing_profile_version_arn    = (known after apply)
      + skip_destroy                   = false
      + source_code_hash               = "eQob83XRCUzRdrWuDv7Gei4/mb8MkUo8FSoNQ7XhDiM="
      + source_code_size               = (known after apply)
      + tags_all                       = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
      + timeout                        = 900
      + version                        = (known after apply)

      + environment {
          + variables = {
              + "SLACK_CHANNEL"     = "# lcl14"
              + "SLACK_WEBHOOK_URL" = "https://hooks.slack.com/services/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"
            }
        }
    }

  # aws_lambda_layer_version.requests_layer will be created
  + resource "aws_lambda_layer_version" "requests_layer" {
      + arn                         = (known after apply)
      + compatible_runtimes         = [
          + "python3.9",
        ]
      + created_date                = (known after apply)
      + filename                    = "./artifacts/requests_layer.zip"
      + id                          = (known after apply)
      + layer_arn                   = (known after apply)
      + layer_name                  = "requests_layer"
      + signing_job_arn             = (known after apply)
      + signing_profile_version_arn = (known after apply)
      + skip_destroy                = false
      + source_code_hash            = "eQob83XRCUzRdrWuDv7Gei4/mb8MkUo8FSoNQ7XhDiM="
      + source_code_size            = (known after apply)
      + version                     = (known after apply)
    }

  # aws_lambda_permission.allow_cloudwatch will be created
  + resource "aws_lambda_permission" "allow_cloudwatch" {
      + action              = "lambda:InvokeFunction"
      + function_name       = "lcl14_function_01"
      + id                  = (known after apply)
      + principal           = "events.amazonaws.com"
      + source_arn          = (known after apply)
      + statement_id        = "AllowExecutionFromCloudWatch"
      + statement_id_prefix = (known after apply)
    }

Plan: 8 to add, 0 to change, 0 to destroy.

─────────────────────────────────────────────────────────────────────────────────────────────── 

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take    
exactly these actions if you run "terraform apply" now.
PS > 
```

### terraform apply
```
PS > terraform apply
data.archive_file.python_lambda_package: Reading...
data.archive_file.python_lambda_layer_package: Reading...
data.archive_file.python_lambda_layer_package: Read complete after 1s [id=dbcdeca3dda8cae9d031cc9f367492ff39e5316f]
data.archive_file.python_lambda_package: Read complete after 1s [id=dbcdeca3dda8cae9d031cc9f367492ff39e5316f]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]  
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]

Terraform used the selected providers to generate the following execution plan. Resource        
actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda will be created
  + resource "aws_cloudwatch_event_rule" "cloudwatch-event-rule-lambda" {
      + arn                 = (known after apply)
      + description         = "Schedule lambda function"
      + event_bus_name      = "default"
      + id                  = (known after apply)
      + is_enabled          = true
      + name                = "cloudwatch-event-rule-lcl14_function_01"
      + name_prefix         = (known after apply)
      + schedule_expression = "rate(5 minutes)"
      + tags_all            = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
    }

  # aws_cloudwatch_event_target.lambda-function-target will be created
  + resource "aws_cloudwatch_event_target" "lambda-function-target" {
      + arn            = (known after apply)
      + event_bus_name = "default"
      + id             = (known after apply)
      + rule           = "cloudwatch-event-rule-lcl14_function_01"
      + target_id      = "cloudwatch-event-target-lcl14_function_01"
    }

  # aws_iam_policy.lambda will be created
  + resource "aws_iam_policy" "lambda" {
      + arn         = (known after apply)
      + id          = (known after apply)
      + name        = "policy_lcl14_function_01"
      + name_prefix = (known after apply)
      + path        = "/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "logs:CreateLogGroup",
                        ]
                      + Effect   = "Allow"
                      + Resource = "arn:aws:logs:ap-northeast-2:123456789012:*"
                    },
                  + {
                      + Action   = [
                          + "logs:CreateLogStream",
                          + "logs:PutLogEvents",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + ":aws:logs:ap-northeast-2:123456789012:log-group:/aws/lambda/lcl14_function_01:*",
                        ]
                    },
                  + {
                      + Action   = [
                          + "s3:*",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:s3:::*",
                        ]
                    },
                  + {
                      + Action   = [
                          + "dynamodb:*",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:dynamodb:ap-northeast-2:123456789012:table/*",
                        ]
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + policy_id   = (known after apply)
      + tags_all    = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
    }

  # aws_iam_role.lambda will be created
  + resource "aws_iam_role" "lambda" {
      + arn                   = (known after apply)
      + assume_role_policy    = jsonencode(
            {
              + Statement = [
                  + {
                      + Action    = "sts:AssumeRole"
                      + Effect    = "Allow"
                      + Principal = {
                          + Service = "lambda.amazonaws.com"
                        }
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + create_date           = (known after apply)
      + force_detach_policies = false
      + id                    = (known after apply)
      + managed_policy_arns   = (known after apply)
      + max_session_duration  = 3600
      + name                  = "iam_lcl14_function_01"
      + name_prefix           = (known after apply)
      + path                  = "/"
      + tags_all              = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
      + unique_id             = (known after apply)
    }

  # aws_iam_role_policy_attachment.iam_for_lambda will be created
  + resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
      + id         = (known after apply)
      + policy_arn = (known after apply)
      + role       = "iam_lcl14_function_01"
    }

  # aws_lambda_function.lambda_function will be created
  + resource "aws_lambda_function" "lambda_function" {
      + architectures                  = (known after apply)
      + arn                            = (known after apply)
      + filename                       = "./artifacts/lambda.zip"
      + function_name                  = "lcl14_function_01"
      + handler                        = "lambda_function.lambda_handler"
      + id                             = (known after apply)
      + invoke_arn                     = (known after apply)
      + last_modified                  = (known after apply)
      + layers                         = (known after apply)
      + memory_size                    = 128
      + package_type                   = "Zip"
      + publish                        = false
      + qualified_arn                  = (known after apply)
      + qualified_invoke_arn           = (known after apply)
      + reserved_concurrent_executions = -1
      + role                           = (known after apply)
      + runtime                        = "python3.9"
      + signing_job_arn                = (known after apply)
      + signing_profile_version_arn    = (known after apply)
      + skip_destroy                   = false
      + source_code_hash               = "eQob83XRCUzRdrWuDv7Gei4/mb8MkUo8FSoNQ7XhDiM="
      + source_code_size               = (known after apply)
      + tags_all                       = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
      + timeout                        = 900
      + version                        = (known after apply)

      + environment {
          + variables = {
              + "SLACK_CHANNEL"     = "# lcl14"
              + "SLACK_WEBHOOK_URL" = "https://hooks.slack.com/services/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"
            }
        }
    }

  # aws_lambda_layer_version.requests_layer will be created
  + resource "aws_lambda_layer_version" "requests_layer" {
      + arn                         = (known after apply)
      + compatible_runtimes         = [
          + "python3.9",
        ]
      + created_date                = (known after apply)
      + filename                    = "./artifacts/requests_layer.zip"
      + id                          = (known after apply)
      + layer_arn                   = (known after apply)
      + layer_name                  = "requests_layer"
      + signing_job_arn             = (known after apply)
      + signing_profile_version_arn = (known after apply)
      + skip_destroy                = false
      + source_code_hash            = "eQob83XRCUzRdrWuDv7Gei4/mb8MkUo8FSoNQ7XhDiM="
      + source_code_size            = (known after apply)
      + version                     = (known after apply)
    }

  # aws_lambda_permission.allow_cloudwatch will be created
  + resource "aws_lambda_permission" "allow_cloudwatch" {
      + action              = "lambda:InvokeFunction"
      + function_name       = "lcl14_function_01"
      + id                  = (known after apply)
      + principal           = "events.amazonaws.com"
      + source_arn          = (known after apply)
      + statement_id        = "AllowExecutionFromCloudWatch"
      + statement_id_prefix = (known after apply)
    }

Plan: 8 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_lambda_layer_version.requests_layer: Creating...
aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda: Creating...
aws_iam_policy.lambda: Creating...
aws_iam_role.lambda: Creating...
aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda: Creation complete after 0s [id=cloudwatch-event-rule-lcl14_function_01]
aws_iam_policy.lambda: Creation complete after 1s [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_01]
aws_iam_role.lambda: Creation complete after 2s [id=iam_lcl14_function_01]
aws_iam_role_policy_attachment.iam_for_lambda: Creating...
aws_iam_role_policy_attachment.iam_for_lambda: Creation complete after 0s [id=iam_lcl14_function_01-20230626075734884000000001]
aws_lambda_layer_version.requests_layer: Creation complete after 5s [id=arn:aws:lambda:ap-northeast-2:123456789012:layer:requests_layer:1]
aws_lambda_function.lambda_function: Creating...
aws_lambda_function.lambda_function: Still creating... [10s elapsed]
aws_lambda_function.lambda_function: Creation complete after 15s [id=lcl14_function_01]
aws_lambda_permission.allow_cloudwatch: Creating...
aws_cloudwatch_event_target.lambda-function-target: Creating...
aws_lambda_permission.allow_cloudwatch: Creation complete after 0s [id=AllowExecutionFromCloudWatch]
aws_cloudwatch_event_target.lambda-function-target: Creation complete after 0s [id=cloudwatch-event-rule-lcl14_function_01-cloudwatch-event-target-lcl14_function_01]

Apply complete! Resources: 8 added, 0 changed, 0 destroyed.
PS > 
```

### terraform destroy
```
PS > terraform destory
null_resource.pip_install: Refreshing state... [id=8739111475799404465]
data.archive_file.lambda-archive: Reading...
data.archive_file.lambda-archive: Read complete after 0s [id=c484d30e7d7805ee2566cebd0443e48b2a1cd0bf]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.secretsmanager_policy: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda: Refreshing state... [id=cloudwatch-event-rule-09-lcl14_function_01]
aws_lambda_layer_version.layer: Refreshing state... [id=arn:aws:lambda:ap-northeast-2:123456789012:layer:lcl14_function_01_layer:149]
aws_secretsmanager_secret.datadog_secret: Refreshing state... [id=arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ]
aws_secretsmanager_secret.slack_secret: Refreshing state... [id=arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt]
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]
data.aws_iam_policy_document.secretsmanager_policy: Read complete after 0s [id=1317256492]
aws_iam_role.lambda: Refreshing state... [id=iam_lcl14_function_01]
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]
aws_iam_policy.lambda: Refreshing state... [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_01]
aws_secretsmanager_secret_version.datadog_secret_version: Refreshing state... [id=arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ|3163427C-FB53-4E44-BC01-2B1647828A78]
aws_secretsmanager_secret_version.slack_secret_version: Refreshing state... [id=arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt|1C008E95-C619-43BC-9ADD-4D2751D01B82]
aws_iam_role_policy_attachment.iam_for_lambda: Refreshing state... [id=iam_lcl14_function_01-20230626075734884000000001]
aws_lambda_function.lambda_function: Refreshing state... [id=lcl14_function_01]
aws_lambda_function_url.lambda_function_url: Refreshing state... [id=lcl14_function_01]
aws_lambda_permission.allow_cloudwatch: Refreshing state... [id=AllowExecutionFromCloudWatch]
aws_cloudwatch_event_target.lambda-function-target: Refreshing state... [id=cloudwatch-event-rule-09-lcl14_function_01-cloudwatch-event-target-lcl14_function_01]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with    
the following symbols:
  - destroy

Terraform will perform the following actions:

  # aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda will be destroyed
  - resource "aws_cloudwatch_event_rule" "cloudwatch-event-rule-lambda" {
      - arn                 = "arn:aws:events:ap-northeast-2:123456789012:rule/cloudwatch-event-rule-09-lcl14_function_01" -> null
      - description         = "Schedule lambda function" -> null
      - event_bus_name      = "default" -> null
      - id                  = "cloudwatch-event-rule-09-lcl14_function_01" -> null
      - is_enabled          = true -> null
      - name                = "cloudwatch-event-rule-09-lcl14_function_01" -> null
      - schedule_expression = "cron(0 0,11 * * ? *)" -> null
      - tags                = {} -> null
      - tags_all            = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
    }

  # aws_cloudwatch_event_target.lambda-function-target will be destroyed
  - resource "aws_cloudwatch_event_target" "lambda-function-target" {
      - arn            = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_01" -> null
      - event_bus_name = "default" -> null
      - id             = "cloudwatch-event-rule-09-lcl14_function_01-cloudwatch-event-target-lcl14_function_01" -> null      - rule           = "cloudwatch-event-rule-09-lcl14_function_01" -> null
      - target_id      = "cloudwatch-event-target-lcl14_function_01" -> null

      - input_transformer {
          - input_paths    = {} -> null
          - input_template = jsonencode(
                {
                  - lambda_url = "https://uvr5meln3nmynytlbanfzg7j5u0mkbvn.lambda-url.ap-northeast-2.on.aws/"
                }
            ) -> null
        }
    }

  # aws_iam_policy.lambda will be destroyed
  - resource "aws_iam_policy" "lambda" {
      - arn       = "arn:aws:iam::123456789012:policy/policy_lcl14_function_01" -> null
      - id        = "arn:aws:iam::123456789012:policy/policy_lcl14_function_01" -> null
      - name      = "policy_lcl14_function_01" -> null
      - path      = "/" -> null
      - policy    = jsonencode(
            {
              - Statement = [
                  - {
                      - Action   = [
                          - "logs:CreateLogGroup",
                        ]
                      - Effect   = "Allow"
                      - Resource = "arn:aws:logs:ap-northeast-2:123456789012:*"
                    },
                  - {
                      - Action   = [
                          - "logs:CreateLogStream",
                          - "logs:PutLogEvents",
                        ]
                      - Effect   = "Allow"
                      - Resource = [
                          - "arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/lambda/lcl14_function_01:*",      
                          - "*",
                        ]
                    },
                  - {
                      - Action   = [
                          - "s3:*",
                        ]
                      - Effect   = "Allow"
                      - Resource = [
                          - "arn:aws:s3:::*",
                        ]
                    },
                  - {
                      - Action   = [
                          - "dynamodb:*",
                        ]
                      - Effect   = "Allow"
                      - Resource = [
                          - "arn:aws:dynamodb:ap-northeast-2:123456789012:table/*",
                        ]
                    },
                  - {
                      - Action   = [
                          - "secretsmanager:ListSecrets",
                          - "secretsmanager:GetSecretValue",
                          - "secretsmanager:DescribeSecret",
                        ]
                      - Effect   = "Allow"
                      - Resource = [
                          - "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:*",
                          - "*",
                        ]
                    },
                ]
              - Version   = "2012-10-17"
            }
        ) -> null
      - policy_id = "ANPAYUBQG6AHIKP3DMA2Z" -> null
      - tags      = {} -> null
      - tags_all  = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
    }

  # aws_iam_role.lambda will be destroyed
  - resource "aws_iam_role" "lambda" {
      - arn                   = "arn:aws:iam::123456789012:role/iam_lcl14_function_01" -> null
      - assume_role_policy    = jsonencode(
            {
              - Statement = [
                  - {
                      - Action    = "sts:AssumeRole"
                      - Effect    = "Allow"
                      - Principal = {
                          - Service = "lambda.amazonaws.com"
                        }
                    },
                ]
              - Version   = "2012-10-17"
            }
        ) -> null
      - create_date           = "2023-06-26T07:57:33Z" -> null
      - force_detach_policies = false -> null
      - id                    = "iam_lcl14_function_01" -> null
      - managed_policy_arns   = [
          - "arn:aws:iam::123456789012:policy/policy_lcl14_function_01",
        ] -> null
      - max_session_duration  = 3600 -> null
      - name                  = "iam_lcl14_function_01" -> null
      - path                  = "/" -> null
      - tags                  = {} -> null
      - tags_all              = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
      - unique_id             = "AROAYUBQG6AHP4T3OEHJZ" -> null
    }

  # aws_iam_role_policy_attachment.iam_for_lambda will be destroyed
  - resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
      - id         = "iam_lcl14_function_01-20230626075734884000000001" -> null
      - policy_arn = "arn:aws:iam::123456789012:policy/policy_lcl14_function_01" -> null
      - role       = "iam_lcl14_function_01" -> null
    }

  # aws_lambda_function.lambda_function will be destroyed
  - resource "aws_lambda_function" "lambda_function" {
      - architectures                  = [
          - "x86_64",
        ] -> null
      - arn                            = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_01" -> null
      - filename                       = "./artifacts/lambda.zip" -> null
      - function_name                  = "lcl14_function_01" -> null
      - handler                        = "lambda_function.lambda_handler" -> null
      - id                             = "lcl14_function_01" -> null
      - invoke_arn                     = "arn:aws:apigateway:ap-northeast-2:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_01/invocations" -> null
      - last_modified                  = "2023-07-13T04:09:04.000+0000" -> null
      - layers                         = [
          - "arn:aws:lambda:ap-northeast-2:123456789012:layer:lcl14_function_01_layer:149",
        ] -> null
      - memory_size                    = 128 -> null
      - package_type                   = "Zip" -> null
      - publish                        = false -> null
      - qualified_arn                  = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_01:$LATEST" -> null
      - qualified_invoke_arn           = "arn:aws:apigateway:ap-northeast-2:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_01:$LATEST/invocations" -> null
      - reserved_concurrent_executions = -1 -> null
      - role                           = "arn:aws:iam::123456789012:role/iam_lcl14_function_01" -> null
      - runtime                        = "python3.9" -> null
      - skip_destroy                   = false -> null
      - source_code_hash               = "9Z9VV3i3t6d2E9o+R5rRLBxnO/mpWSi4pWm2FgNzO5A=" -> null
      - source_code_size               = 27139 -> null
      - tags                           = {} -> null
      - tags_all                       = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
      - timeout                        = 300 -> null
      - version                        = "$LATEST" -> null

      - environment {
          - variables = {
              - "DD_SECRET_NAME"      = "secret_manager_datadog_lcl14"
              - "DYNAMODB_TABLE_NAME" = "dydb_system_check_lcl14"
              - "REGION"              = "ap-northeast-2"
              - "S3_BUCKET_NAME"      = "s3-bucket-lcl14"
              - "SLACK_SECRET_NAME"   = "secret_manager_slack_lcl14"
            } -> null
        }

      - ephemeral_storage {
          - size = 512 -> null
        }

      - tracing_config {
          - mode = "PassThrough" -> null
        }
    }

  # aws_lambda_function_url.lambda_function_url will be destroyed
  - resource "aws_lambda_function_url" "lambda_function_url" {
      - authorization_type = "NONE" -> null
      - function_arn       = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_01" -> null
      - function_name      = "lcl14_function_01" -> null
      - function_url       = "https://uvr5meln3nmynytlbanfzg7j5u0mkbvn.lambda-url.ap-northeast-2.on.aws/" -> null      
      - id                 = "lcl14_function_01" -> null
      - invoke_mode        = "BUFFERED" -> null
      - url_id             = "uvr5meln3nmynytlbanfzg7j5u0mkbvn" -> null
    }

  # aws_lambda_layer_version.layer will be destroyed
  - resource "aws_lambda_layer_version" "layer" {
      - arn                      = "arn:aws:lambda:ap-northeast-2:123456789012:layer:lcl14_function_01_layer:149" -> null
      - compatible_architectures = [] -> null
      - compatible_runtimes      = [
          - "python3.9",
        ] -> null
      - created_date             = "2023-07-13T04:09:04.477+0000" -> null
      - filename                 = "./artifacts/layer.zip" -> null
      - id                       = "arn:aws:lambda:ap-northeast-2:123456789012:layer:lcl14_function_01_layer:149" -> null
      - layer_arn                = "arn:aws:lambda:ap-northeast-2:123456789012:layer:lcl14_function_01_layer" -> null  
      - layer_name               = "lcl14_function_01_layer" -> null
      - skip_destroy             = false -> null
      - source_code_hash         = "5uQ/9rLoceHUxWxUIi8kzsowIw5ccl799TrGcR8XGt8=" -> null
      - source_code_size         = 7444252 -> null
      - version                  = "149" -> null
    }

  # aws_lambda_permission.allow_cloudwatch will be destroyed
  - resource "aws_lambda_permission" "allow_cloudwatch" {
      - action        = "lambda:InvokeFunction" -> null
      - function_name = "lcl14_function_01" -> null
      - id            = "AllowExecutionFromCloudWatch" -> null
      - principal     = "events.amazonaws.com" -> null
      - source_arn    = "arn:aws:events:ap-northeast-2:123456789012:rule/cloudwatch-event-rule-09-lcl14_function_01" -> null
      - statement_id  = "AllowExecutionFromCloudWatch" -> null
    }

  # aws_secretsmanager_secret.datadog_secret will be destroyed
  - resource "aws_secretsmanager_secret" "datadog_secret" {
      - arn                            = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ" -> null
      - force_overwrite_replica_secret = false -> null
      - id                             = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ" -> null
      - name                           = "secret_manager_datadog_lcl14" -> null
      - recovery_window_in_days        = 30 -> null
      - tags                           = {} -> null
      - tags_all                       = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
    }

  # aws_secretsmanager_secret.slack_secret will be destroyed
  - resource "aws_secretsmanager_secret" "slack_secret" {
      - arn                            = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt" -> null
      - force_overwrite_replica_secret = false -> null
      - id                             = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt" -> null
      - name                           = "secret_manager_slack_lcl14" -> null
      - recovery_window_in_days        = 30 -> null
      - tags                           = {} -> null
      - tags_all                       = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
    }

  # aws_secretsmanager_secret_version.datadog_secret_version will be destroyed
  - resource "aws_secretsmanager_secret_version" "datadog_secret_version" {
      - arn            = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ" -> null
      - id             = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ|3163427C-FB53-4E44-BC01-2B1647828A78" -> null
      - secret_id      = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ" -> null
      - secret_string  = (sensitive value) -> null
      - version_id     = "3163427C-FB53-4E44-BC01-2B1647828A78" -> null
      - version_stages = [
          - "AWSCURRENT",
        ] -> null
    }

  # aws_secretsmanager_secret_version.slack_secret_version will be destroyed
  - resource "aws_secretsmanager_secret_version" "slack_secret_version" {
      - arn            = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt" 
-> null
      - id             = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt|1C008E95-C619-43BC-9ADD-4D2751D01B82" -> null
      - secret_id      = "arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt" 
-> null
      - secret_string  = (sensitive value) -> null
      - version_id     = "1C008E95-C619-43BC-9ADD-4D2751D01B82" -> null
      - version_stages = [
          - "AWSCURRENT",
        ] -> null
    }

  # null_resource.pip_install will be destroyed
  - resource "null_resource" "pip_install" {
      - id       = "8739111475799404465" -> null
      - triggers = {
          - "always_run" = "2023-07-13T04:08:34Z"
        } -> null
    }

Plan: 0 to add, 0 to change, 14 to destroy.

Changes to Outputs:
  - lambda_url = "https://uvr5meln3nmynytlbanfzg7j5u0mkbvn.lambda-url.ap-northeast-2.on.aws/" -> null

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

aws_secretsmanager_secret_version.datadog_secret_version: Destroying... [id=arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ|3163427C-FB53-4E44-BC01-2B1647828A78]
aws_iam_role_policy_attachment.iam_for_lambda: Destroying... [id=iam_lcl14_function_01-20230626075734884000000001]
aws_secretsmanager_secret_version.slack_secret_version: Destroying... [id=arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt|1C008E95-C619-43BC-9ADD-4D2751D01B82]
aws_cloudwatch_event_target.lambda-function-target: Destroying... [id=cloudwatch-event-rule-09-lcl14_function_01-cloudwatch-event-target-lcl14_function_01]
aws_lambda_permission.allow_cloudwatch: Destroying... [id=AllowExecutionFromCloudWatch]
aws_secretsmanager_secret_version.datadog_secret_version: Destruction complete after 0s
aws_secretsmanager_secret_version.slack_secret_version: Destruction complete after 0s
aws_secretsmanager_secret.datadog_secret: Destroying... [id=arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_datadog_lcl14-wwDYEZ]
aws_secretsmanager_secret.slack_secret: Destroying... [id=arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:secret_manager_slack_lcl14-86mZBt]
aws_cloudwatch_event_target.lambda-function-target: Destruction complete after 0s
aws_lambda_function_url.lambda_function_url: Destroying... [id=lcl14_function_01]
aws_lambda_permission.allow_cloudwatch: Destruction complete after 0s
aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda: Destroying... [id=cloudwatch-event-rule-09-lcl14_function_01]
aws_secretsmanager_secret.datadog_secret: Destruction complete after 0s
aws_secretsmanager_secret.slack_secret: Destruction complete after 0s
aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda: Destruction complete after 0s
aws_lambda_function_url.lambda_function_url: Destruction complete after 0s
aws_lambda_function.lambda_function: Destroying... [id=lcl14_function_01]
aws_lambda_function.lambda_function: Destruction complete after 0s
aws_lambda_layer_version.layer: Destroying... [id=arn:aws:lambda:ap-northeast-2:123456789012:layer:lcl14_function_01_layer:149]
aws_lambda_layer_version.layer: Destruction complete after 1s
null_resource.pip_install: Destroying... [id=8739111475799404465]
null_resource.pip_install: Destruction complete after 0s
aws_iam_role_policy_attachment.iam_for_lambda: Destruction complete after 1s
aws_iam_policy.lambda: Destroying... [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_01]
aws_iam_role.lambda: Destroying... [id=iam_lcl14_function_01]
aws_iam_role.lambda: Destruction complete after 1s
aws_iam_policy.lambda: Destruction complete after 1s

Destroy complete! Resources: 14 destroyed.
PS > 
```

