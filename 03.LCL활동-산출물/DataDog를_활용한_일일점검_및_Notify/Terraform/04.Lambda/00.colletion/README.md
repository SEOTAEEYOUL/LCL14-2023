# Datadog Alert 수집
## DONE:
- 일별로 Alert 를 저장
- 일별 Summary 를 보여주는 페이지

## TODO:
- 일별 Summary 에는 해소된 건에 대해서 구분하여 개수하는 것이 필요
- 월별 Summary 는 집계하는 Program 에서 보여주는 형태
  - 월별 Summary 는 해당 월의 시작일 부터 현재까지 일자, Priority, 건수 를 집계하여 보여줌(02.notification 에서 URL 지정)
    - 02. notification 에서 수행하거나
    - 04. Daily 점검 Report 에서 출력

> [Built In Variable](https://docs.datadoghq.com/integrations/webhooks/#usage)

![webhook-integration.png](./img/webhook-integration.png)  
![webhook-integration-1.png](./img/webhook-integration-1.png)  

## Alert List 조회 결과
- Lambda URL 에 today 인자로 조회  
  - https://github.com/SEOTAEEYOUL/LCL-14/blob/main/03.%EC%9A%B4%EC%98%81%EC%9E%90%EB%A3%8C/DataDog/Terraform/04.Lambda/00.colletion/README.md  
![chrome.png](./img/chrome.png)  

| 변수 | 설명 | 예 |     
|:---|:---|:---|  
| $AGGREG_KEY | 함께 속한 이벤트를 집계하기 위한 ID입니다 |  `9bd4ac313a4d1e8fae2482df7b77628` |  
| $ALERT_CYCLE_KEY | 경고가 트리거된 시간부터 해결될 때까지 이벤트를 연결하는 ID입니다. | |  
| $ALERT_ID | 경고 ID입니다. | `1234` |  
| $ALERT_METRIC | 경고인 경우 메트릭의 이름입니다. | `system.load.1` |  
| $ALERT_PRIORITY | 경고 모니터의 우선 순위입니다. | `P1`, `P2` |  
| $ALERT_QUERY | 웹후크를 트리거한 모니터의 쿼리입니다. | |  
| $ALERT_SCOPE | 알림을 트리거하는 쉼표로 구분된 태그 목록입니다. | `availability-zone:us-east-1a`, `role:computing-node` |   
| $ALERT_STATUS | 경보 상태 요약. </br> 로그 모니터 알림의 웹후크 페이로드에 이 변수를 채우려면 $ALERT_STATUS웹후크 통합 타일에 수동으로 추가해야 합니다.| `system.load.1 over host:my-host was > 0 at least once during the last 1m` |    
| $ALERT_TITLE | 경고의 제목입니다. | `[Triggered on {host:ip-012345}] Host is Down` |  
| $ALERT_TRANSITION | 경고 알림 유형입니다. | `Recovered`, `Triggered`/ `Re-Triggered`, `No Data`/ `Re-No Data`, `Warn`/ `Re-Warn`,`Renotify` |  
| $ALERT_TYPE | 경고 유형입니다. | `error`, `warning`, `success`, `info` |  
| $DATE | 이벤트가 발생한 날짜 (epoch)입니다. | `1406662672000` |   
| $EMAIL | 웹후크를 트리거한 이벤트를 게시하는 사용자의 이메일. | |  
| $EVENT_MSG | 이벤트 텍스트입니다. | `@webhook-url Sending to the webhook` |  
| $EVENT_TITLE | 이벤트의 제목입니다. | `[Triggered] [Memory Alert]` |  
| $HOSTNAME | 이벤트와 연결된 서버의 호스트 이름(있는 경우). | |   
| $ID | 이벤트의 ID입니다. |  `1234567` |  
| $INCIDENT_ATTACHMENTS | 사후 분석 및 문서와 같은 인시던트 첨부 파일이 있는 JSON 개체 목록입니다. | `[{"attachment_type": "postmortem", "attachment": {"url": "https://app.datadoghq.com/notebook/123","title": "Postmortem IR-1"}}]` |   
| $INCIDENT_COMMANDER | 인시던트 커맨더의 핸들, uuid, 이름, 이메일 및 아이콘이 포함된 JSON 개체입니다. | |  
| $INCIDENT_CUSTOMER_IMPACT | 인시던트의 고객 영향 상태, 기간 및 범위가 포함된 JSON 개체입니다. | `{"customer_impacted": true, "customer_impact_duration": 300 ,"customer_impact_scope": "scope here"}` |  
| $INCIDENT_FIELDS | 인시던트의 각 필드를 해당 값에 매핑하는 JSON 개체입니다. | `{"state": "active", "datacenter": ["eu1", "us1"]}` |  
| $INCIDENT_INTEGRATIONS | Slack 및 Jira와 같은 인시던트 통합이 포함된 JSON 개체 목록입니다. | `[{"uuid": "11a15def-eb08-52c8-84cd-714e6651829b", "integration_type": 1, "status": 2, "metadata": {"channels": [{"channel_name": "#incident-1", "channel_id": "<channel_id>", "team_id": "<team_id>", "redirect_url": "<redirect_url>"}]}}]` |  
| $INCIDENT_MSG | `인시던트 알림의 메시지입니다.` | |  
| $INCIDENT_PUBLIC_ID | 관련 사건의 공개 ID입니다. | `123` |  
| $INCIDENT_SEVERITY | 사건의 심각도. |  |  
| $INCIDENT_STATUS | 사건의 상태. | |  
| $INCIDENT_TITLE | 사건의 제목. | |  
| $INCIDENT_TODOS | 인시던트의 수정 작업이 포함된 JSON 개체 목록입니다. | `[{"uuid": "01c03111-172a-50c7-8df3-d61e64b0e74b", "content": "task description", "due_date": "2022-12-02T05:00:00+00:00", "completed": "2022-12-01T20:15:00.112207+00:00", "assignees": []}]` |  
| $INCIDENT_URL | 사건의 URL | `https://app.datadoghq.com/incidents/1` |  
| $INCIDENT_UUID | 관련 사건의 UUID. | `01c03111-172a-50c7-8df3-d61e64b0e74b` |  
| $LAST_UPDATED | 이벤트가 마지막으로 업데이트된 날짜입니다. | |  
| $LINK | 이벤트의 URL입니다. | `https://app.datadoghq.com/event/jump_to?event_id=123456` |  
| $LOGS_SAMPLE | 로그 모니터 알림에서 샘플을 기록합니다. | |  
| $METRIC_NAMESPACE | 경고인 경우 메트릭의 네임스페이스입니다. | |  
| $ORG_ID | 조직의 ID입니다. | `11023` |  
| $ORG_NAME | 조직의 이름입니다. | `Datadog` |  
| $PRIORITY |이벤트의 우선 순위.  | `normal` 또는 `low` |  
| $SECURITY_RULE_NAME | 보안 규칙의 이름입니다. | |  
| $SECURITY_SIGNAL_ID | 신호의 고유 식별자입니다. | `AAAAA-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` |  
| $SECURITY_SIGNAL_SEVERITY | 보안 신호의 심각도입니다. | `medium` |  
| $SECURITY_SIGNAL_TITLE | 보안 신호의 제목입니다. | |  
| $SECURITY_SIGNAL_MSG | 보안 신호의 메시지입니다. | |  
| $SECURITY_SIGNAL_ATTRIBUTES | 보안 신호 속성입니다. | `{"network":{"client":{"ip":"1.2.3.4"}}, "service": ["agent"]}` |  
| $SECURITY_RULE_ID | 보안 규칙 ID입니다. | `aaa-aaa-aaa` |  
| $SECURITY_RULE_MATCHED_QUERIES | 보안 규칙과 관련된 쿼리입니다. | `["@evt.name:authentication"]` |  
| $SECURITY_RULE_GROUP_BY_FIELDS | 키 값 쌍에 의한 보안 그룹. | `{"@usr.name":"john.doe@your_domain.com"}` |  
| $SECURITY_RULE_TYPE | 보안 규칙 유형입니다. | `log_detection` |  
| $SNAPSHOT | 이벤트에 스냅샷이 포함된 경우 이미지의 URL입니다. | `https://p.datadoghq.com/path-to-snapshot` |  
| $SYNTHETICS_TEST_NAME | Synthetics 테스트의 이름입니다. | |  
| $SYNTHETICS_FIRST_FAILING_STEP_NAME | Synthetics 테스트의 첫 번째 실패 단계 이름입니다. | |  
| $SYNTHETICS_SUMMARY | 합성 테스트 세부 정보 요약. | |  
| $TAGS | 쉼표로 구분된 이벤트 태그 목록입니다. | `monitor, name:myService, role:computing-node` |  
| $TAGS[key] | 태그 의 값입니다 key. key태그 가 없거나 key태그에 값이 없으면 이 표현식은 빈 문자열로 평가됩니다. | |  
| $TEXT_ONLY_MSG | Markdown 형식이 없는 이벤트의 텍스트입니다. | |  
| $USER | 웹후크를 트리거한 이벤트를 게시하는 사용자. | `rudy` |  
| $USERNAME | 웹후크를 트리거한 이벤트를 게시하는 사용자의 사용자 이름입니다. | |  

### `$ALERT_TYPE` 
- 알림이 설정된 Datadog 모니터링 설정에 따라 error 또는 success 알림이 트리거될 수 있습니다.
- 예를 들어, 특정 메트릭 값이 임계값을 초과하면 error 알림을 받을 수 있고, 해당 메트릭 값이 다시 정상 범위로 돌아가면 success 알림을 받을 수 있습니다.
- 상황에 따라 이러한 알림 유형을 사용하여 시스템 상태를 모니터링하고 이벤트를 추적할 수 있습니다.

#### `error`
- Metric, Event, Log, 또는 Service Check에 오류가 감지되었을 때 발생합니다.
- 예를 들어, 임계값을 초과하는 메트릭 값을 감지하거나, 예상치 못한 이벤트가 발생한 경우 등이 이에 해당합니다.
- 이러한 경우에는 시스템에 문제가 있거나 예외 상황이 발생했음을 나타냅니다.

#### `success`
- Metric, Event, Log, 또는 Service Check에서 정상적인 상태가 감지되었을 때 발생합니다.
- 예를 들어, 시스템이 기대한 대로 작동하고 모든 지표가 정상 범위에 있는 경우, 또는 특정 이벤트 또는 로그 메시지가 예상된 상태인 경우 등이 이에 해당합니다.
- 이러한 경우에는 정상 작동 상태임을 나타냅니다.





## Alter
### webhook
- https://c5tm2sxn2gacvkbdaspchk5ofu0alzty.lambda-url.ap-northeast-2.on.aws/

### Payload
- LCL14
    - default message
    ```
    {
        "id": "$ID",
        "user": "$USER",
        "username": "$USERNAME",
        "email": "$EMAIL",
        "date": "$DATE",
        "hostname" : "$HOSTNAME",
        "textOnlyMsg": "$TEXT_ONLY_MSG",
        "tags": "$TAGS",
        "lastUpdated": "$LAST_UPDATED",
        "event": {
            "type": "$EVENT_TYPE",
            "title": "$EVENT_TITLE",
            "msg": "$EVENT_MSG"
        },
        "alert": {
            "id": "$ALERT_ID",
            "type": "$ALERT_TYPE",
            "priority": "$ALERT_PRIORITY",
            "title": "$ALERT_TITLE",
            "metric": "$ALERT_METRIC",
            "query": "$ALERT_QUERY",
            "status": "$ALERT_STATUS",
            "scope": "$ALERT_SCOPE"
        },
        "org": {
            "id": "$ORG_ID",
            "name": "$ORG_NAME"
        }
    }
    ```

- saveEventHist
    ```
    {
        "id" : "$ID",
        "orgId" : "$ORG_ID",
        "lastUpdated" : "$LAST_UPDATED",
        "hostname" : "$HOSTNAME",
        "date" : "$DATE",
        "alertId" : "$ALERT_ID",
        "alertPriority" : "$ALERT_PRIORITY",
        "alertTransition" : "$ALERT_TRANSITION",
        "alertType" : "$ALERT_TYPE",
        "eventTitle" : "$EVENT_TITLE",
        "eventType" : "$EVENT_TYPE",
        "eventMsg" : "$EVENT_MSG",
        "link" : "$LINK",
        "alertScope": "$ALERT_SCOPE",
        "alertMetric": "$ALERT_METRIC",
        "tags": "$TAGS",
        "textOnlyMsg": "$TEXT_ONLY_MSG",
        "user": "$USER",
        "username": "$USERNAME",
        "aggergKey": "$AGGREG_KEY",
        "alertCycleKey": "$ALERT_CYCLE_KEY"
    }
    ```

- AlertNow
    ```
    {
        "id":"$ID",
        "email":"$EMAIL",
        "eventTitle":"$EVENT_TITLE",
        "eventMsg":"$EVENT_MSG",
        "textOnlyMsg":"$TEXT_ONLY_MSG",
        "eventType":"$EVENT_TYPE",
        "date":"$DATE",
        "datePosix":"$DATE_POSIX",
        "alertId":"$ALERT_ID",
        "alertType":"$ALERT_TYPE",
        "aggregKey":"$AGGREG_KEY",
        "orgId":"$ORG_ID",
        "alertStatus":"$ALERT_STATUS",
        "alertScope":"$ALERT_SCOPE",
        "hostname":"$HOSTNAME",
        "user":"$USER",
        "username":"$USERNAME",
        "snapshot":"$SNAPSHOT",
        "link":"$LINK",
        "priority":"$PRIORITY",
        "tags":"$TAGS",
        "lastUpdated":"$LAST_UPDATED",
        "lastUpdatedPosix":"$LAST_UPDATED_POSIX",
        "alertMetric":"$ALERT_METRIC",
        "metricNamespace":"$METRIC_NAMESPACE",
        "alertTransition":"$ALERT_TRANSITION",
        "orgName":"$ORG_NAME",
        "alertQuery":"$ALERT_QUERY",
        "alertTitle":"$ALERT_TITLE",
        "alertCycleKey":"$ALERT_CYCLE_KEY"
    }
    ```

- sendSKCCTeam
    ```
    {
        "@context": "https://schema.org/extensions",
        "@type": "MessageCard",
        "themeColor": "64a837",
        "title": "$EVENT_TITLE",
        "text": "$EVENT_MSG"
    }
    ```

## terraform
```
terraform init
terraform plan
terraform apply
terraform state list
terraform output
```

### terraform init
```
PS > terraform init

Initializing the backend...

Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Finding latest version of hashicorp/archive...
- Finding hashicorp/aws versions matching ">= 3.50.0"...
- Installing hashicorp/archive v2.4.0...
- Installed hashicorp/archive v2.4.0 (signed by HashiCorp)
- Installing hashicorp/aws v5.7.0...
- Installed hashicorp/aws v5.7.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

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
data.archive_file.python_lambda_package: Read complete after 0s [id=f8c252b903c8d7a6391553efad568068f5a421d1]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_iam_policy.lambda will be created
  + resource "aws_iam_policy" "lambda" {
      + arn         = (known after apply)
      + id          = (known after apply)
      + name        = "policy_lcl14_function_03"
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
                          + "arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/lambda/lcl14_function_03:*",
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
      + name                  = "iam_lcl14_function_03"
      + name_prefix           = (known after apply)
      + path                  = "/"
      + tags_all              = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
      + unique_id             = (known after apply)

      + inline_policy {
          + name   = (known after apply)
          + policy = (known after apply)
        }
    }

  # aws_iam_role_policy_attachment.iam_for_lambda will be created
  + resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
      + id         = (known after apply)
      + policy_arn = (known after apply)
      + role       = "iam_lcl14_function_03"
    }

  # aws_lambda_function.lambda_function will be created
  + resource "aws_lambda_function" "lambda_function" {
      + architectures                  = (known after apply)
      + arn                            = (known after apply)
      + filename                       = "./artifacts/lambda.zip"
      + function_name                  = "lcl14_function_03"
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
      + source_code_hash               = "zhErOYh9vYDiu6X5g2xh+u7/OtZPVdwohcEKr72cHXA="
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
              + "DYNAMODB_TABLE_NAME" = "dydb_system_check_lcl14"
              + "S3_BUCKET_NAME"      = "s3-bucket-lcl14"
              + "SLACK_CHANNEL"       = "# lcl14"
              + "SLACK_WEBHOOK_URL"   = "https://hooks.slack.com/services/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"
            }
        }

      + ephemeral_storage {
          + size = (known after apply)
        }

      + tracing_config {
          + mode = (known after apply)
        }
    }

  # aws_lambda_function_url.lambda_function_url will be created
  + resource "aws_lambda_function_url" "lambda_function_url" {
      + authorization_type = "NONE"
      + function_arn       = (known after apply)
      + function_name      = "lcl14_function_03"
      + function_url       = (known after apply)
      + id                 = (known after apply)
      + invoke_mode        = "BUFFERED"
      + url_id             = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + lambda_url = (known after apply)

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
PS > 
```

### terraform apply
```
PS > terraform apply
data.archive_file.python_lambda_package: Reading...
data.archive_file.python_lambda_package: Read complete after 0s [id=f8c252b903c8d7a6391553efad568068f5a421d1]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_iam_policy.lambda will be created
  + resource "aws_iam_policy" "lambda" {
      + arn         = (known after apply)
      + id          = (known after apply)
      + name        = "policy_lcl14_function_03"
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
                          + "arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/lambda/lcl14_function_03:*",
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
      + name                  = "iam_lcl14_function_03"
      + name_prefix           = (known after apply)
      + path                  = "/"
      + tags_all              = {
          + "Environment"         = "prd"
          + "Personalinformation" = "no"
          + "ServiceName"         = "lcl14"
          + "owner"               = "lcl14"
        }
      + unique_id             = (known after apply)

      + inline_policy {
          + name   = (known after apply)
          + policy = (known after apply)
        }
    }

  # aws_iam_role_policy_attachment.iam_for_lambda will be created
  + resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
      + id         = (known after apply)
      + policy_arn = (known after apply)
      + role       = "iam_lcl14_function_03"
    }

  # aws_lambda_function.lambda_function will be created
  + resource "aws_lambda_function" "lambda_function" {
      + architectures                  = (known after apply)
      + arn                            = (known after apply)
      + filename                       = "./artifacts/lambda.zip"
      + function_name                  = "lcl14_function_03"
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
      + source_code_hash               = "zhErOYh9vYDiu6X5g2xh+u7/OtZPVdwohcEKr72cHXA="
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
              + "DYNAMODB_TABLE_NAME" = "dydb_system_check_lcl14"
              + "S3_BUCKET_NAME"      = "s3-bucket-lcl14"
              + "SLACK_CHANNEL"       = "# lcl14"
              + "SLACK_WEBHOOK_URL"   = "https://hooks.slack.com/services/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"
            }
        }

      + ephemeral_storage {
          + size = (known after apply)
        }

      + tracing_config {
          + mode = (known after apply)
        }
    }

  # aws_lambda_function_url.lambda_function_url will be created
  + resource "aws_lambda_function_url" "lambda_function_url" {
      + authorization_type = "NONE"
      + function_arn       = (known after apply)
      + function_name      = "lcl14_function_03"
      + function_url       = (known after apply)
      + id                 = (known after apply)
      + invoke_mode        = "BUFFERED"
      + url_id             = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + lambda_url = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_iam_policy.lambda: Creating...
aws_iam_role.lambda: Creating...
aws_iam_policy.lambda: Creation complete after 1s [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_03]
aws_iam_role.lambda: Creation complete after 1s [id=iam_lcl14_function_03]
aws_iam_role_policy_attachment.iam_for_lambda: Creating...
aws_lambda_function.lambda_function: Creating...
aws_iam_role_policy_attachment.iam_for_lambda: Creation complete after 1s [id=iam_lcl14_function_03-20230707044436401000000001]
aws_lambda_function.lambda_function: Still creating... [10s elapsed]
aws_lambda_function.lambda_function: Still creating... [20s elapsed]
aws_lambda_function.lambda_function: Creation complete after 22s [id=lcl14_function_03]
aws_lambda_function_url.lambda_function_url: Creating...
aws_lambda_function_url.lambda_function_url: Creation complete after 0s [id=lcl14_function_03]

Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

Outputs:

lambda_url = "https://c5tm2sxn2gacvkbdaspchk5ofu0alzty.lambda-url.ap-northeast-2.on.aws/"
PS > 
```

### terraform state list
```
PS > terraform state list
data.archive_file.python_lambda_package
data.aws_caller_identity.current
data.aws_iam_policy_document.lambda_assume_role_policy
aws_iam_policy.lambda
aws_iam_role.lambda
aws_iam_role_policy_attachment.iam_for_lambda
aws_lambda_function.lambda_function
aws_lambda_function_url.lambda_function_url
PS > 
```

### terraform output
```
PS > terraform output    
lambda_url = "https://c5tm2sxn2gacvkbdaspchk5ofu0alzty.lambda-url.ap-northeast-2.on.aws/"
PS >
```


### terraform destroy
```
PS > terraform plan
data.archive_file.python_lambda_package: Reading...
data.archive_file.python_lambda_package: Read complete after 0s [id=75f522603286ded30e2d6151d0601de763da5247]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]
aws_iam_role.lambda: Refreshing state... [id=iam_lcl14_function_03]
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]
aws_iam_policy.lambda: Refreshing state... [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_03]
aws_iam_role_policy_attachment.iam_for_lambda: Refreshing state... [id=iam_lcl14_function_03-20230707044436401000000001]
aws_lambda_function.lambda_function: Refreshing state... [id=lcl14_function_03]
aws_lambda_function_url.lambda_function_url: Refreshing state... [id=lcl14_function_03]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following
symbols:
  ~ update in-place

Terraform will perform the following actions:

  # aws_lambda_function.lambda_function will be updated in-place
  ~ resource "aws_lambda_function" "lambda_function" {
        id                             = "lcl14_function_03"
      ~ last_modified                  = "2023-07-13T10:04:31.000+0000" -> (known after apply)
      ~ source_code_hash               = "Ro4mVzL/TrbLVQ15sqDAK4iADwIJURtEZ5e3iegyNQI=" -> "MrDuYzxSE0w/mqrD53F38gtpW39Xhyru/YSbSibPRfM="
        tags                           = {}
        # (20 unchanged attributes hidden)

        # (3 unchanged blocks hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run     
"terraform apply" now.
PS D:\workspace\LCL-14.20230712\03.운영자료\DataDog\Terraform\04.Lambda\00.colletion> terraform destroy
data.archive_file.python_lambda_package: Reading...
data.archive_file.python_lambda_package: Read complete after 0s [id=75f522603286ded30e2d6151d0601de763da5247]
data.aws_caller_identity.current: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Reading...
data.aws_iam_policy_document.lambda_assume_role_policy: Read complete after 0s [id=2690255455]
aws_iam_role.lambda: Refreshing state... [id=iam_lcl14_function_03]
data.aws_caller_identity.current: Read complete after 0s [id=123456789012]
aws_iam_policy.lambda: Refreshing state... [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_03]
aws_iam_role_policy_attachment.iam_for_lambda: Refreshing state... [id=iam_lcl14_function_03-20230707044436401000000001]
aws_lambda_function.lambda_function: Refreshing state... [id=lcl14_function_03]
aws_lambda_function_url.lambda_function_url: Refreshing state... [id=lcl14_function_03]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following 
symbols:
  - destroy

Terraform will perform the following actions:

  # aws_iam_policy.lambda will be destroyed
  - resource "aws_iam_policy" "lambda" {
      - arn       = "arn:aws:iam::123456789012:policy/policy_lcl14_function_03" -> null
      - id        = "arn:aws:iam::123456789012:policy/policy_lcl14_function_03" -> null
      - name      = "policy_lcl14_function_03" -> null
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
                          - "arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws/lambda/lcl14_function_03:*",
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
      - policy_id = "ANPAYUBQG6AHCGNKURZGL" -> null
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
      -                    = "arn:aws:iam::123456789012:role/iam_lcl14_function_03" -> null
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
      - create_date           = "2023-07-07T04:44:36Z" -> null
      - force_detach_policies = false -> null
      - id                    = "iam_lcl14_function_03" -> null
      - managed_policy_arns   = [
          - "arn:aws:iam::123456789012:policy/policy_lcl14_function_03",
        ] -> null
      - max_session_duration  = 3600 -> null
      - name                  = "iam_lcl14_function_03" -> null
      - path                  = "/" -> null
      - tags                  = {} -> null
      - tags_all              = {
          - "Environment"         = "prd"
          - "Personalinformation" = "no"
          - "ServiceName"         = "lcl14"
          - "owner"               = "lcl14"
        } -> null
      - unique_id             = "AROAYUBQG6AHPYNW7AQAX" -> null
    }

  # aws_iam_role_policy_attachment.iam_for_lambda will be destroyed
  - resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
      - id         = "iam_lcl14_function_03-20230707044436401000000001" -> null
      - policy_arn = "arn:aws:iam::123456789012:policy/policy_lcl14_function_03" -> null
      - role       = "iam_lcl14_function_03" -> null
    }

  # aws_lambda_function.lambda_function will be destroyed
  - resource "aws_lambda_function" "lambda_function" {
      - architectures                  = [
          - "x86_64",
        ] -> null
      - arn                            = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_03" -> null
      - filename                       = "./artifacts/lambda.zip" -> null
      - function_name                  = "lcl14_function_03" -> null
      - handler                        = "lambda_function.lambda_handler" -> null
      - id                             = "lcl14_function_03" -> null
      - invoke_arn                     = "arn:aws:apigateway:ap-northeast-2:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_03/invocations" -> null
      - last_modified                  = "2023-07-13T10:04:31.000+0000" -> null
      - layers                         = [] -> null
      - memory_size                    = 128 -> null
      - package_type                   = "Zip" -> null
      - publish                        = false -> null
      - qualified_arn                  = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_03:$LATEST" -> null  
      - qualified_invoke_arn           = "arn:aws:apigateway:ap-northeast-2:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_03:$LATEST/invocations" -> null
      - reserved_concurrent_executions = -1 -> null
      - role                           = "arn:aws:iam::123456789012:role/iam_lcl14_function_03" -> null
      - runtime                        = "python3.9" -> null
      - skip_destroy                   = false -> null
      - source_code_hash               = "Ro4mVzL/TrbLVQ15sqDAK4iADwIJURtEZ5e3iegyNQI=" -> null
      - source_code_size               = 3899 -> null
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
              - "S3_BUCKET_NAME"         = "s3-bucket-lcl14"
              - "S3_COLLECTION_TEMPLATE" = "template/alert_list.html"
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
      - function_arn       = "arn:aws:lambda:ap-northeast-2:123456789012:function:lcl14_function_03" -> null
      - function_name      = "lcl14_function_03" -> null
      - function_url       = "https://c5tm2sxn2gacvkbdaspchk5ofu0alzty.lambda-url.ap-northeast-2.on.aws/" -> null
      - id                 = "lcl14_function_03" -> null
      - invoke_mode        = "BUFFERED" -> null
      - url_id             = "c5tm2sxn2gacvkbdaspchk5ofu0alzty" -> null
    }

Plan: 0 to add, 0 to change, 5 to destroy.

Changes to Outputs:
  - lambda_url = "https://c5tm2sxn2gacvkbdaspchk5ofu0alzty.lambda-url.ap-northeast-2.on.aws/" -> null

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

aws_iam_role_policy_attachment.iam_for_lambda: Destroying... [id=iam_lcl14_function_03-20230707044436401000000001]     
aws_lambda_function_url.lambda_function_url: Destroying... [id=lcl14_function_03]
aws_lambda_function_url.lambda_function_url: Destruction complete after 0s
aws_lambda_function.lambda_function: Destroying... [id=lcl14_function_03]
aws_lambda_function.lambda_function: Destruction complete after 1s
aws_iam_role_policy_attachment.iam_for_lambda: Destruction complete after 1s
aws_iam_policy.lambda: Destroying... [id=arn:aws:iam::123456789012:policy/policy_lcl14_function_03]
aws_iam_role.lambda: Destroying... [id=iam_lcl14_function_03]
aws_iam_policy.lambda: Destruction complete after 1s
aws_iam_role.lambda: Destruction complete after 1s

Destroy complete! Resources: 5 destroyed.
PS >
```