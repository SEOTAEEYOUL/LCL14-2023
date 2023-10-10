# Slack 에 일일점검결과 URL  보내기
## DONE:
- 현재는 실시간으로 자료를 보는 형태로 되어 있음

## TODO:
- 정적 Page 를 PreSigned URL 로 보내는 형태가 추가 되어야 함
  - 수집하는 곳에서 PreSigned URL 를 만들어 주어야 함


  

## Lambda
| 항목 | 값 | 설명 |  
|:---|:---|:---|  
| Lambda Source | ./code/lambda_function.py | 간단한 Python 예제 소스 |  
| Python 버전 | 3.9 | |  
| IAM | iam_lcl14_function_0 | |  
| Amazon EventBride | cloudwatch-event-rule-lcl14_function_0 | 5분 주기로 lambda 를 호출 |  
| Lambda Function 명 | lcl14_function_0 | `Amazon EventBridge` 에서 호출 받을 경우 `Slack` 채널로 Alarm 을 보냄 </br> Slack link 를 타고 호출 될 경우 Browser상에 출력할 HTML 를 만들어 반환 |  

## 소스
| 소스명 | 설명 |  
|:---|:---|  
| backend.tf | 공동 작업을 위한 S3, DynamoDB 정보 |  
| provider.tf | AWS |  
| iam.tf | lambda 실행을 위한 iam role 생성 |  
| main.tf | lambda 생성을 위한 account 정보 |  
| lambda.tf | AWS Labmda 생성 - Python |  
| url.tf | Lambda 함수의 URL 로 browser 에서 접근 가능 |  
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
![slack-alarm-1.png](./img/slack-alarm-1.png)  
![lambda-slack-link-brower.png](./img/lambda-slack-link-brower.png)  

```
$Env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/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"
$Env:SLACK_CHANNEL="lcl14"
$Env:LAMBDA_URL="https://app.datadoghq.com/dashboard/xus-d8b-sej/skcc-argos-tf?from_ts=1687408110928&to_ts=1687422510928&live=true"
```

## Terraform

1. terraform init - 초기화 (provider 설치)
2. terraform plan - 생성 및 수정, 삭제할 자원을 보여줌
3. terraform apply - 자원 생성 및 backend(S3) 에 현재 자원 상태(tfstate) 저장
4. terraform state - 상태 보기
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
data.archive_file.python_lambda_package: Read complete after 0s [id=69b24900175afc8aea8ca81966a997b287870943]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]   
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]

Terraform used the selected providers to generate the following execution plan. Resource actions 
are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda will be created
  + resource "aws_cloudwatch_event_rule" "cloudwatch-event-rule-lambda" {
      + arn                 = (known after apply)
      + description         = "Schedule lambda function"
      + event_bus_name      = "default"
      + id                  = (known after apply)
      + is_enabled          = true
      + name                = "cloudwatch-event-run-lambda-function"
      + name_prefix         = (known after apply)
      + schedule_expression = "rate(60 minutes)"
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
      + rule           = "cloudwatch-event-run-lambda-function"
      + target_id      = "cloudwatch-event-lambda-function-target"
    }

  # aws_iam_policy.lambda will be created
  + resource "aws_iam_policy" "lambda" {
      + arn         = (known after apply)
      + id          = (known after apply)
      + name        = "policy_lcl14_function_0"
      + name_prefix = (known after apply)
      + path        = "/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = "logs:CreateLogGroup"
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
                          + "arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/lambda/lcl14_function_0:*",
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
      + name                  = "iam_lcl14_function_0"
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
      + role       = "iam_lcl14_function_0"
    }

  # aws_lambda_function.lambda_function will be created
  + resource "aws_lambda_function" "lambda_function" {
      + architectures                  = (known after apply)
      + arn                            = (known after apply)
      + filename                       = "lambda.zip"
      + function_name                  = "lcl14_function_0"
      + handler                        = "lambda_function.lambda_handler"
      + id                             = (known after apply)
      + invoke_arn                     = (known after apply)
      + last_modified                  = (known after apply)
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
      + source_code_hash               = "aeU7K6YqH6pXMttdSYoktBt4GWSaxCK4z5mUn8AHro4="
      + source_code_size               = (known after apply)
      + tags_all                       = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
      + timeout                        = 10
      + version                        = (known after apply)

      + environment {
          + variables = {
              + "CHANNEL"     = "lcl14"
              + "WEBHOOK_URL" = "https://hooks.slack.com/services/**********"
            }
        }
    }

  # aws_lambda_function_url.lambda will be created
  + resource "aws_lambda_function_url" "lambda" {
      + authorization_type = "NONE"
      + function_arn       = (known after apply)
      + function_name      = "lcl14_function_0"
      + function_url       = (known after apply)
      + id                 = (known after apply)
      + invoke_mode        = "BUFFERED"
      + url_id             = (known after apply)
    }

  # aws_lambda_function_url.lambda_function_url will be created
  + resource "aws_lambda_function_url" "lambda_function_url" {
      + authorization_type = "NONE"
      + function_arn       = (known after apply)
      + function_name      = "lcl14_function_0"
      + function_url       = (known after apply)
      + id                 = (known after apply)
      + invoke_mode        = "BUFFERED"
      + url_id             = (known after apply)
    }

  # aws_lambda_permission.allow_cloudwatch will be created
  + resource "aws_lambda_permission" "allow_cloudwatch" {
      + action              = "lambda:InvokeFunction"
      + function_name       = "lcl14_function_0"
      + id                  = (known after apply)
      + principal           = "events.amazonaws.com"
      + source_arn          = (known after apply)
      + statement_id        = "AllowExecutionFromCloudWatch"
      + statement_id_prefix = (known after apply)
    }

Plan: 9 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + lambda_url = (known after apply)

──────────────────────────────────────────────────────────────────────────────────────────────── 

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take     
exactly these actions if you run "terraform apply" now.
PS > 
```

### terraform apply
```
PS > terraform apply
data.archive_file.python_lambda_package: Reading...
data.archive_file.python_lambda_package: Read complete after 0s [id=c19712f15d5d47d62461e54a6de95f67ba4adefd]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
aws_cloudwatch_event_rule.test-lambda: Refreshing state... [id=run-lambda-function]
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]   
aws_iam_role.lambda: Refreshing state... [id=iam_lcl14_function_0]
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]
aws_iam_policy.lambda: Refreshing state... [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_0]
aws_iam_role_policy_attachment.iam_for_lambda: Refreshing state... [id=iam_lcl14_function_0-20230622063853128600000001]

Terraform used the selected providers to generate the following execution plan. Resource actions 
are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_cloudwatch_event_target.lambda-function-target will be created
  + resource "aws_cloudwatch_event_target" "lambda-function-target" {
      + arn            = (known after apply)
      + event_bus_name = "default"
      + id             = (known after apply)
      + rule           = "run-lambda-function"
      + target_id      = "lambda-function-target"
    }

  # aws_lambda_function.lambda_function will be created
  + resource "aws_lambda_function" "lambda_function" {
      + architectures                  = (known after apply)
      + arn                            = (known after apply)
      + filename                       = "lambda.zip"
      + function_name                  = "lcl14_function_0"
      + handler                        = "lambda_function.lambda_handler"
      + id                             = (known after apply)
      + invoke_arn                     = (known after apply)
      + last_modified                  = (known after apply)
      + memory_size                    = 128
      + package_type                   = "Zip"
      + publish                        = false
      + qualified_arn                  = (known after apply)
      + qualified_invoke_arn           = (known after apply)
      + reserved_concurrent_executions = -1
      + role                           = "arn:aws:iam::123456789012:role/iam_lcl14_function_0"   
      + runtime                        = "python3.9"
      + signing_job_arn                = (known after apply)
      + signing_profile_version_arn    = (known after apply)
      + skip_destroy                   = false
      + source_code_hash               = "p261EFAECbWmpKi6wXTntstOnefOL7Ry8a2uLNWFJKY="
      + source_code_size               = (known after apply)
      + tags_all                       = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
      + timeout                        = 10
      + version                        = (known after apply)
    }

  # aws_lambda_function_url.lambda will be created
  + resource "aws_lambda_function_url" "lambda" {
      + authorization_type = "NONE"
      + function_arn       = (known after apply)
      + function_name      = "lcl14_function_0"
      + function_url       = (known after apply)
      + id                 = (known after apply)
      + invoke_mode        = "BUFFERED"
      + url_id             = (known after apply)
    }

  # aws_lambda_function_url.lambda_function_url will be created
  + resource "aws_lambda_function_url" "lambda_function_url" {
      + authorization_type = "NONE"
      + function_arn       = (known after apply)
      + function_name      = "lcl14_function_0"
      + function_url       = (known after apply)
      + id                 = (known after apply)
      + invoke_mode        = "BUFFERED"
      + url_id             = (known after apply)
    }

  # aws_lambda_permission.allow_cloudwatch will be created
  + resource "aws_lambda_permission" "allow_cloudwatch" {
      + action              = "lambda:InvokeFunction"
      + function_name       = "lcl14_function_0"
      + id                  = (known after apply)
      + principal           = "events.amazonaws.com"
      + source_arn          = "arn:aws:events:ap-northeast-2:123456789012:rule/run-lambda-function"
      + statement_id        = "AllowExecutionFromCloudWatch"
      + statement_id_prefix = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + lambda_url = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_lambda_function.lambda_function: Creating...
aws_lambda_function.lambda_function: Creation complete after 6s [id=lcl14_function_0]
aws_lambda_function_url.lambda: Creating...
aws_lambda_permission.allow_cloudwatch: Creating...
aws_lambda_function_url.lambda_function_url: Creating...
aws_cloudwatch_event_target.lambda-function-target: Creating...
aws_cloudwatch_event_target.lambda-function-target: Creation complete after 0s [id=run-lambda-function-lambda-function-target]
aws_lambda_permission.allow_cloudwatch: Creation complete after 0s [id=AllowExecutionFromCloudWatch]
aws_lambda_function_url.lambda: Creation complete after 0s [id=lcl14_function_0]
aws_lambda_function_url.lambda_function_url: Creation complete after 0s [id=lcl14_function_0]

Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

Outputs:

lambda_url = "https://**********.lambda-url.ap-northeast-2.on.aws/"        
PS > 
```

#### terraform state list
```
PS > terraform state list
data.archive_file.python_lambda_package
data.aws_caller_identity.current
data.aws_iam_policy_document.lambda_assume_role_policy
aws_cloudwatch_event_rule.test-lambda
aws_cloudwatch_event_target.lambda-function-target
aws_iam_policy.lambda
aws_iam_role.lambda
aws_iam_role_policy_attachment.iam_for_lambda
aws_lambda_function.lambda_function
aws_lambda_function_url.lambda
aws_lambda_function_url.lambda_function_url
aws_lambda_permission.allow_cloudwatch
PS > 
```

#### terraform output
```
PS > terraform output    
lambda_url = "https://**********.lambda-url.ap-northeast-2.on.aws/"
PS > 
```

#### terraform destroy
```
PS > terraform destroy
data.terraform_remote_state.collection_labmda: Reading...
data.archive_file.python_lambda_package: Reading...
data.archive_file.python_lambda_package: Read complete after 0s [id=c5511f1fc9ab1ad127eb63e644ceb48b5a62a94c]
data.terraform_remote_state.collection_labmda: Read complete after 0s
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda: Refreshing state... [id=cloudwatch-event-rule-lcl14_function_02]
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]
aws_iam_role.lambda: Refreshing state... [id=iam_lcl14_function_02]
data.aws_caller_identity.current: Read complete after 1s [id=123456789012]
aws_iam_policy.lambda: Refreshing state... [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_02]
aws_iam_role_policy_attachment.iam_for_lambda: Refreshing state... [id=iam_lcl14_function_02-20230626053104263800000001]
aws_lambda_function.lambda_function: Refreshing state... [id=lcl14_function_02]
aws_lambda_permission.allow_cloudwatch: Refreshing state... [id=AllowExecutionFromCloudWatch]
aws_lambda_function_url.lambda_function_url: Refreshing state... [id=lcl14_function_02]
aws_cloudwatch_event_target.lambda-function-target: Refreshing state... [id=cloudwatch-event-rule-lcl14_function_02-cloudwatch-event-target-lcl14_function_02]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with    
the following symbols:
  - destroy

Terraform will perform the following actions:

  # aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda will be destroyed
  - resource "aws_cloudwatch_event_rule" "cloudwatch-event-rule-lambda" {
      - arn                 = "arn:aws:events:ap-northeast-2:123456789012:rule/cloudwatch-event-rule-lcl14_function_02" -> null
      - description         = "Schedule lambda function" -> null
      - event_bus_name      = "default" -> null
      - id                  = "cloudwatch-event-rule-lcl14_function_02" -> null
      - is_enabled          = true -> null
      - name                = "cloudwatch-event-rule-lcl14_function_02" -> null
      - schedule_expression = "cron(5 0,11 * * ? *)" -> null
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
      - arn            = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_02" -> null
      - event_bus_name = "default" -> null
      - id             = "cloudwatch-event-rule-lcl14_function_02-cloudwatch-event-target-lcl14_function_02" -> null   
      - rule           = "cloudwatch-event-rule-lcl14_function_02" -> null
      - target_id      = "cloudwatch-event-target-lcl14_function_02" -> null

      - input_transformer {
          - input_paths    = {} -> null
          - input_template = jsonencode(
                {
                  - lambda_url = "https://hnuclv3idsldlfjzii3vc5kltq0xmkrj.lambda-url.ap-northeast-2.on.aws/"
                }
            ) -> null
        }
    }

  # aws_iam_policy.lambda will be destroyed
  - resource "aws_iam_policy" "lambda" {
      - arn       = "arn:aws:iam::123456789012:policy/policy_lcl14_function_02" -> null
      - id        = "arn:aws:iam::123456789012:policy/policy_lcl14_function_02" -> null
      - name      = "policy_lcl14_function_02" -> null
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
                          - "arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/lambda/lcl14_function_02:*",      
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
                ]
              - Version   = "2012-10-17"
            }
        ) -> null
      - policy_id = "ANPAYUBQG6AHCL36V75MV" -> null
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
      - arn                   = "arn:aws:iam::123456789012:role/iam_lcl14_function_02" -> null
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
      - create_date           = "2023-06-26T05:31:03Z" -> null
      - force_detach_policies = false -> null
      - id                    = "iam_lcl14_function_02" -> null
      - managed_policy_arns   = [
          - "arn:aws:iam::123456789012:policy/policy_lcl14_function_02",
        ] -> null
      - max_session_duration  = 3600 -> null
      - name                  = "iam_lcl14_function_02" -> null
      - path                  = "/" -> null
      - tags                  = {} -> null
      - tags_all              = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
      - unique_id             = "AROAYUBQG6AHFEHESVNBS" -> null
    }

  # aws_iam_role_policy_attachment.iam_for_lambda will be destroyed
  - resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
      - id         = "iam_lcl14_function_02-20230626053104263800000001" -> null
      - policy_arn = "arn:aws:iam::123456789012:policy/policy_lcl14_function_02" -> null
      - role       = "iam_lcl14_function_02" -> null
    }

  # aws_lambda_function.lambda_function will be destroyed
  - resource "aws_lambda_function" "lambda_function" {
      - architectures                  = [
          - "x86_64",
        ] -> null
      - arn                            = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_02" -> null
      - filename                       = "./artifacts/lambda.zip" -> null
      - function_name                  = "lcl14_function_02" -> null
      - handler                        = "lambda_function.lambda_handler" -> null
      - id                             = "lcl14_function_02" -> null
      - invoke_arn                     = "arn:aws:apigateway:ap-northeast-2:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_02/invocations" -> null
      - last_modified                  = "2023-07-13T04:02:15.000+0000" -> null
      - layers                         = [] -> null
      - memory_size                    = 128 -> null
      - package_type                   = "Zip" -> null
      - publish                        = false -> null
      - qualified_arn                  = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_02:$LATEST" -> null
      - qualified_invoke_arn           = "arn:aws:apigateway:ap-northeast-2:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_02:$LATEST/invocations" -> null
      - reserved_concurrent_executions = -1 -> null
      - role                           = "arn:aws:iam::123456789012:role/iam_lcl14_function_02" -> null
      - runtime                        = "python3.9" -> null
      - skip_destroy                   = false -> null
      - source_code_hash               = "3AKp61H1G3tk7fMtfzoty4X1RTqeLBd6qBu2WpD1ta4=" -> null
      - source_code_size               = 5176 -> null
      - tags                           = {} -> null
      - tags_all                       = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
      - timeout                        = 900 -> null
      - version                        = "$LATEST" -> null

      - environment {
          - variables = {
              - "DYDB_ALERT_LIST_NAME"   = "dydb_alert_history_lcl14"
              - "DYDB_SYSTEM_CHECK_NAME" = "dydb_system_check_lcl14"
              - "LAMBDA_COLLECTION_URL"  = "https://**********.lambda-url.ap-northeast-2.on.aws/"              - "S3_BUCKET_NAME"         = "s3-bucket-lcl14"
              - "SLACK_CHANNEL"          = "# lcl14"
              - "SLACK_WEBHOOK_URL"      = "https://hooks.slack.com/services/**********"
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
      - function_arn       = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_02" -> null
      - function_name      = "lcl14_function_02" -> null
      - function_url       = "https://hnuclv3idsldlfjzii3vc5kltq0xmkrj.lambda-url.ap-northeast-2.on.aws/" -> null      
      - id                 = "lcl14_function_02" -> null
      - invoke_mode        = "BUFFERED" -> null
      - url_id             = "hnuclv3idsldlfjzii3vc5kltq0xmkrj" -> null
    }

  # aws_lambda_permission.allow_cloudwatch will be destroyed
  - resource "aws_lambda_permission" "allow_cloudwatch" {
      - action        = "lambda:InvokeFunction" -> null
      - function_name = "lcl14_function_02" -> null
      - id            = "AllowExecutionFromCloudWatch" -> null
      - principal     = "events.amazonaws.com" -> null
      - source_arn    = "arn:aws:events:ap-northeast-2:123456789012:rule/cloudwatch-event-rule-lcl14_function_02" -> null
      - statement_id  = "AllowExecutionFromCloudWatch" -> null
    }

Plan: 0 to add, 0 to change, 8 to destroy.

Changes to Outputs:
  - lambda_url = "https://**********.lambda-url.ap-northeast-2.on.aws/" -> null

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

aws_iam_role_policy_attachment.iam_for_lambda: Destroying... [id=iam_lcl14_function_02-20230626053104263800000001]
aws_lambda_permission.allow_cloudwatch: Destroying... [id=AllowExecutionFromCloudWatch]
aws_cloudwatch_event_target.lambda-function-target: Destroying... [id=cloudwatch-event-rule-lcl14_function_02-cloudwatch-event-target-lcl14_function_02]
aws_cloudwatch_event_target.lambda-function-target: Destruction complete after 0s
aws_lambda_function_url.lambda_function_url: Destroying... [id=lcl14_function_02]
aws_lambda_permission.allow_cloudwatch: Destruction complete after 0s
aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda: Destroying... [id=cloudwatch-event-rule-lcl14_function_02]
aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda: Destruction complete after 0s
aws_lambda_function_url.lambda_function_url: Destruction complete after 0s
aws_lambda_function.lambda_function: Destroying... [id=lcl14_function_02]
aws_lambda_function.lambda_function: Destruction complete after 0s
aws_iam_role_policy_attachment.iam_for_lambda: Destruction complete after 0s
aws_iam_policy.lambda: Destroying... [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_02]
aws_iam_role.lambda: Destroying... [id=iam_lcl14_function_02]
aws_iam_role.lambda: Destruction complete after 1s
aws_iam_policy.lambda: Destruction complete after 1s

Destroy complete! Resources: 8 destroyed.
PS > 
```
