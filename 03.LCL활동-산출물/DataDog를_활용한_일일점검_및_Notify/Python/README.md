# Datadog
> [Python](https://docs.datadoghq.com/integrations/python/)  
> [datadog — Datadog Python library](https://datadogpy.readthedocs.io/en/latest/#)  
> [AWS Integration](https://docs.datadoghq.com/integrations/amazon_web_services/)  
> [AWS CloudWatch Metric Streams with Kinesis Data Firehose - 10분 지연 -> 3분 지연](https://docs.datadoghq.com/integrations/guide/aws-cloudwatch-metric-streams-with-kinesis-data-firehose/?tab=cloudformation)  
> [Datadog Lambda 함수를 사용하여 AWS 서비스 로그 보내기](https://docs.datadoghq.com/logs/guide/send-aws-services-logs-with-the-datadog-lambda-function/?tab=awsconsole)  
> [The AWS Integration with Terraform](https://docs.datadoghq.com/integrations/guide/aws-terraform-setup/)  
> [Slack Integration](https://docs.datadoghq.com/api/latest/slack-integration/)  

> [datadog-api-client-python](https://github.com/DataDog/datadog-api-client-python)  
> [Datadog API.](https://docs.datadoghq.com/api/latest/)  
> [Organizations - public_id 를 가져오기](https://docs.datadoghq.com/api/latest/organizations/?code-lang=python)  

## Metric 관련 링크
> [Amazon EFS 모니터링을 위한 주요 지표](https://www.datadoghq.com/blog/amazon-efs-metrics/)  

## 제공되는 것
| 모듈 | 설명 |
|:---|:---|  
| datadog.api | A client for Datadog’s HTTP API. |
| datadog.dogstatsd | A UDP/UDS DogStatsd client. |  
| datadog.threadstats | A client for Datadog’s HTTP API that submits metrics in a worker thread. |  


## 설치
```
pip install datadog
```
```
PS > pip install datadog
Collecting datadog
  Downloading datadog-0.45.0-py2.py3-none-any.whl (113 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 113.0/113.0 kB 6.4 MB/s eta 0:00:00
Requirement already satisfied: requests>=2.6.0 in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from datadog) (2.28.2)
Requirement already satisfied: charset-normalizer<4,>=2 in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from requests>=2.6.0->datadog) (3.1.0)
Requirement already satisfied: idna<4,>=2.5 in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from requests>=2.6.0->datadog) (3.4)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from requests>=2.6.0->datadog) (1.26.15)
Requirement already satisfied: certifi>=2017.4.17 in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from requests>=2.6.0->datadog) (2022.12.7)
Installing collected packages: datadog
Successfully installed datadog-0.45.0
PS > 
```

## API Key, Application Key
API 키와 Application 키는 Datadog API에 액세스하기 위한 두 가지 다른 유형의 사용자 인증 정보입니다.   

| Type | 설명 |  
|:---|:---|  
| API 키 | Datadog API에 액세스하는 데 사용되는 공개키 |
| Application 키 | Datadog API를 사용하는 애플리케이션을 식별하는 데 사용되는 비공개 키 </br> Datadog 자원(API)의 접근 권한 설정 |  


API 키는 Datadog API에 액세스하는 데 사용되는 공개 키이고 앱 키는 Datadog API를 사용하는 애플리케이션을 식별하는 데 사용되는 비공개 키입니다.

API 키는 Datadog API에 대한 액세스를 제어하는 데 사용할 수 있습니다. 예를 들어 API 키에 대한 요청 수 제한을 설정하거나 특정 API에 대한 액세스 권한을 부여할 수 있습니다. 앱 키는 Datadog API를 사용하는 애플리케이션을 식별하는 데 사용할 수 있습니다. 예를 들어 앱 키에 대한 요청 수 제한을 설정하거나 특정 API에 대한 액세스 권한을 부여할 수 있습니다.

API 키와 앱 키는 모두 Datadog 계정에서 생성할 수 있습니다. API 키를 생성하려면 "API" 페이지로 이동하여 "새 키 만들기" 버튼을 클릭합니다. 앱 키를 생성하려면 "앱" 페이지로 이동하여 "새 앱 만들기" 버튼을 클릭합니다.

API 키와 앱 키는 안전하게 보관해야 합니다. 다른 사람과 공유하거나 공개적으로 노출해서는 안 됩니다. API 키 또는 앱 키가 손상된 경우 즉시 취소해야 합니다.


## Datadog API Key, Application Key
DataDog API Key와 Application Key는 DataDog API를 사용하여 DataDog 모니터링 서비스를 프로그래밍 방식으로 제어할 수 있도록 인증을 제공하는 데 사용됩니다.

API Key는 API에 대한 인증을 제공하며, API를 사용하여 DataDog에서 데이터를 읽거나 쓸 수 있도록 권한을 부여합니다.

Application Key는 API Key와 함께 사용하여 DataDog API를 호출하는 데 필요한 API 엑세스 권한을 부여합니다. 애플리케이션 키는 DataDog에서 생성된 키이며, 보안을 위해 API Key와 별도로 관리되며 회전 가능합니다.

즉, API Key와 Application Key는 DataDog API를 사용하여 DataDog에서 모니터링하는 시스템을 제어하고, 데이터를 가져오거나 쓰는 권한을 부여하며, 이를 위한 보안 인증 수단입니다.

| 항목 | 값 |
|:---|:---|
| API Keys | ********** |  
| Application Keys | ********** |  
| public_id | ********** |  


## RDS MySQL CPU 사용율 90% 체크
- datadog-rds-mysql-cpu-check.py 


### 수행
- [python datadog-rds-mysql-cpu-check.py](./datadog-rds-mysql-cpu-check.py)  
```
PS LCL-14\03.운영자료\DataDog> python datadog-rds-mysql-cpu-check.py 
{'aggr': 'avg',
 'attributes': {},
 'display_name': 'aws.rds.cpuutilization',
 'end': 1685958241000,
 'expression': 'avg:aws.rds.cpuutilization{dbclusteridentifier:sksh-argos-p-aurora-mysql}',
 'interval': 2,
 'length': 3,
 'metric': 'aws.rds.cpuutilization',
 'pointlist': [[1685958120000.0, 13.140833059946695],
               [1685958180000.0, 11.860833009084066],
               [1685958240000.0, 11.988333423932394]],
 'query_index': 0,
 'scope': 'dbclusteridentifier:sksh-argos-p-aurora-mysql',
 'start': 1685958120000,
 'tag_set': [],
 'unit': [{'family': 'percentage',
           'id': 17,
           'name': 'percent',
           'plural': 'percent',
           'scale_factor': 1.0,
           'short_name': '%'},
          None]}
[1685958120000.0, 13.140833059946695]
[1685958180000.0, 11.860833009084066]
[1685958240000.0, 11.988333423932394]
dbclusteridentifier:sksh-argos-p-aurora-mysql OK -> 11.99%
PS LCL-14\03.운영자료\DataDog> 
```

## Query 
- avg:aws.rds.cpuutilization{dbclusteridentifier:sksh-argos-p-aurora-mysql}
- sum:aws.rds.login_failures{dbinstanceidentifier:sksh-argos-p-aurora-mysql-master-rci}.as_count()
- sum:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-aurora-mysql-master-rci}
- avg:aws.ec2.cpuutilization{*} by {host}


## AWS Integration
### Datadog
- Interations > Amazon Web Services > Add AWS Account

#### AWS Account
| 계정 | Account I.D | Datadog Interation | AWS Role Name |     
|:---|:---|:---|:---|   
| IAM | 123456789012 | ○ | DatadogIntegrationRole-argos |   
| Network | 123456789012 | ○ | DatadogIntegrationRole |  
| Dev | 123456789012 | X | - |  
| Stg | 123456789012 | X | - |  
| Prd | 123456789012 | X | - |   

### AWS
- AWS 계정 > IAM > Policys
- DatadogIntegrationPolicy 정책 생성
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "apigateway:GET",
                "autoscaling:Describe*",
                "backup:List*",
                "budgets:ViewBudget",
                "cloudfront:GetDistributionConfig",
                "cloudfront:ListDistributions",
                "cloudtrail:DescribeTrails",
                "cloudtrail:GetTrailStatus",
                "cloudtrail:LookupEvents",
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "codedeploy:List*",
                "codedeploy:BatchGet*",
                "directconnect:Describe*",
                "dynamodb:List*",
                "dynamodb:Describe*",
                "ec2:Describe*",
                "ecs:Describe*",
                "ecs:List*",
                "elasticache:Describe*",
                "elasticache:List*",
                "elasticfilesystem:DescribeFileSystems",
                "elasticfilesystem:DescribeTags",
                "elasticfilesystem:DescribeAccessPoints",
                "elasticloadbalancing:Describe*",
                "elasticmapreduce:List*",
                "elasticmapreduce:Describe*",
                "es:ListTags",
                "es:ListDomainNames",
                "es:DescribeElasticsearchDomains",
                "events:CreateEventBus",
                "fsx:DescribeFileSystems",
                "fsx:ListTagsForResource",
                "health:DescribeEvents",
                "health:DescribeEventDetails",
                "health:DescribeAffectedEntities",
                "kinesis:List*",
                "kinesis:Describe*",
                "lambda:GetPolicy",
                "lambda:List*",
                "logs:DeleteSubscriptionFilter",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:DescribeSubscriptionFilters",
                "logs:FilterLogEvents",
                "logs:PutSubscriptionFilter",
                "logs:TestMetricFilter",
                "organizations:Describe*",
                "organizations:List*",
                "rds:Describe*",
                "rds:List*",
                "redshift:DescribeClusters",
                "redshift:DescribeLoggingStatus",
                "route53:List*",
                "s3:GetBucketLogging",
                "s3:GetBucketLocation",
                "s3:GetBucketNotification",
                "s3:GetBucketTagging",
                "s3:ListAllMyBuckets",
                "s3:PutBucketNotification",
                "ses:Get*",
                "sns:List*",
                "sns:Publish",
                "sqs:ListQueues",
                "states:ListStateMachines",
                "states:DescribeStateMachine",
                "support:DescribeTrustedAdvisor*",
                "support:RefreshTrustedAdvisorCheck",
                "tag:GetResources",
                "tag:GetTagKeys",
                "tag:GetTagValues",
                "xray:BatchGetTraces",
                "xray:GetTraceSummaries"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

## Datadog Client
```
Start-Process -Wait msiexec -ArgumentList '/qn /i datadog-agent-7-latest.amd64.msi APIKEY="73db9c713f601a5855a2f1a6ae7a5afe1c2a6748"'
```

```bash
# Curl command
curl -X POST "https://api.datadoghq.com/api/v1/org" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
-d @- << EOF
{
  "name": "New child org"
}
EOF
```

## python
```
pip install datadog_api_client
$Env:DD_API_KEY="**********"
$Env:DD_APP_KEY="**********"
python get-org-list.py
```

```powershell
PS > pip install datadog_api_client
Collecting datadog_api_client
  Downloading datadog_api_client-2.13.2-py3-none-any.whl (1.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.9/1.9 MB 24.1 MB/s eta 0:00:00
Requirement already satisfied: urllib3<2.0,>=1.15 in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from datadog_api_client) (1.26.15)
Requirement already satisfied: certifi in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from datadog_api_client) (2022.12.7)
Requirement already satisfied: python-dateutil in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from datadog_api_client) (2.8.2)
Collecting typing-extensions (from datadog_api_client)
  Downloading typing_extensions-4.6.3-py3-none-any.whl (31 kB)
Requirement already satisfied: six>=1.5 in c:\users\XXXXX\appdata\local\programs\python\python311\lib\site-packages (from python-dateutil->datadog_api_client) (1.16.0)
Installing collected packages: typing-extensions, datadog_api_client
Successfully installed datadog_api_client-2.13.2 typing-extensions-4.6.3
PS > $Env:DD_API_KEY="**********"
PS > $Env:DD_APP_KEY="**********"
PS > python get-org-id.py
{'api_key': {'created': '2023-06-15 23:45:16',
             'created_by': 'taeeyoul@sk.com',
             'disabled': '',
             'disabled_by': '',
             'is_active': True,
             'key': '**********',
             'name': 'API Key created by taeeyoul@sk.com on 2023-06-15'},
 'application_key': {'hash': '**********',
                     'name': 'taeeyoul@sk.com (api)',
                     'org_id': 860972,
                     'owner': 'taeeyoul@sk.com',
                     'revoked': False},
 'org': {'billing': {},
         'created': '2023-06-15 23:45:15',
         'description': None,
         'name': 'New child org',
         'public_id': '**********',
         'settings': {'custom_landing_page': None,
                      'default_landing_page': 'Dashboard Lists',
                      'manage_reports': None,
                      'private_widget_share': False,
                      'saml': {'enabled': False},
                      'saml_autocreate_access_role': 'st',
                      'saml_autocreate_users_domains': {'domains': [],
                                                        'enabled': False},
                      'saml_can_be_enabled': False,
                      'saml_idp_endpoint': None,
                      'saml_idp_initiated_login': {'enabled': False},
                      'saml_idp_metadata_uploaded': False,
                      'saml_idp_metadata_valid_until': None,
                      'saml_login_url': None,
                      'saml_strict_mode': {'enabled': False}},
         'subscription': {'billing_plan_id': 2,
                          'expires': None,
                          'finished': None,
                          'id': 1233937,
                          'is_custom': False,
                          'is_expired': True,
                          'is_trial': False,
                          'started': 1686872716,
                          'type': 'pro'}},
 'user': {'access_role': 'adm',
          'disabled': False,
          'email': 'taeeyoul@sk.com',
          'handle': 'taeeyoul@sk.com',
          'icon': 'https://secure.gravatar.com/avatar/b928e41c99a8c740c4687c6c9e36f32e?s=48&d=retro',
          'is_admin': True,
          'name': None,
          'role': None,
          'title': None,
          'verified': True},
 'warning': ['Subscription field has been deprecated. Orgs inherit the parent '
             'plan unless the optional trial parameter is set to true']}
PS > 
```

### python get-org-list.py
```
PS > python get-org-list.py
{'orgs': [{'billing': {'type': 'parent_billing'},
           'created': '2022-07-21 15:01:39',
           'description': None,
           'name': 'SK Shieldus',
           'public_id': '**********',
           'settings': {'custom_landing_page': None,
                        'default_landing_page': 'APM Home',
                        'manage_reports': None,
                        'private_widget_share': False,
                        'saml': {'enabled': False},
                        'saml_autocreate_access_role': 'st',
                        'saml_autocreate_users_domains': {'domains': [],
                                                          'enabled': False},
                        'saml_can_be_enabled': False,
                        'saml_idp_endpoint': None,
                        'saml_idp_initiated_login': {'enabled': False},
                        'saml_idp_metadata_uploaded': False,
                        'saml_idp_metadata_valid_until': None,
                        'saml_login_url': None,
                        'saml_strict_mode': {'enabled': False}},
           'subscription': {'billing_plan_id': 2,
                            'expires': None,
                            'finished': None,
                            'id': 1049657,
                            'is_custom': False,
                            'is_expired': True,
                            'is_trial': False,
                            'started': 1659950378,
                            'type': 'pro'}}]}
PS > 
```

### python get-org-info.py
```
PS > python get-org-info.py
{'org': {'billing': {'type': 'parent_billing'},
         'created': '2022-07-21 15:01:39',
         'description': None,
         'name': 'SK Shieldus',
         'public_id': '**********',
         'settings': {'custom_landing_page': None,
                      'default_landing_page': 'APM Home',
                      'manage_reports': None,
                      'private_widget_share': False,
                      'saml': {'enabled': False},
                      'saml_autocreate_access_role': 'st',
                      'saml_autocreate_users_domains': {'domains': [],
                                                        'enabled': False},
                      'saml_can_be_enabled': False,
                      'saml_idp_endpoint': None,
                      'saml_idp_initiated_login': {'enabled': False},
                      'saml_idp_metadata_uploaded': False,
                      'saml_idp_metadata_valid_until': None,
                      'saml_login_url': None,
                      'saml_strict_mode': {'enabled': False}},
         'subscription': {'billing_plan_id': 2,
                          'expires': None,
                          'finished': None,
                          'id': 1049657,
                          'is_custom': False,
                          'is_expired': True,
                          'is_trial': False,
                          'started': 1659950378,
                          'type': 'pro'}}}
PS > 
```

## file write 시 한글 깨짐 방지
1. open 시 `encoding='utf-8'` 사용
2. json.dump 시 `ensure_ascii=False` 사용
```
with open("./test.json", 'w', encoding='utf-8') as file:
    # json.dump(data, file, indent="\t", ensure_ascii=False)
    json.dump(data, file, indent=4, ensure_ascii=False)                    
```
