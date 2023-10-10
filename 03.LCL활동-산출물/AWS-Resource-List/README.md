# AWS 자원 Excel 로 내리기

> [Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)  
> [Code examples for SDK for Python (Boto3)](https://docs.aws.amazon.com/code-library/latest/ug/python_3_secrets-manager_code_examples.html)  
> [JMESPath](https://jmespath.org/)  
> [JMESPath Tutorial](https://jmespath.org/tutorial.html)  
> [JMESPath - Usage Tutorial](https://scrapfly.io/blog/parse-json-jmespath-python/)  
> [JMESPath Examples](https://jmespath.org/examples.html)  
> [pprintpp 0.4.0](https://pypi.org/project/pprintpp/)  

![aws_light_theme_logo](./img/aws_light_theme_logo.svg)

## 파일
| 파일명 | 설명 |
|:---|:---|
| requirements.txt | Python library </br> ex) boto3 ... | 
| .env | AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION 정보가 있는 파일 |
| aws-resource-list.py | 위의 `.env` 파일의 정보를 기반으로 account 내의 자원을 읽어 Excel 로 저장함 |  

### .env 에 들어가는 항목
| 항목 | 값 | 설명 |  
|:---|:---|:---|  
| AWS_ACCESS_KEY | | AWS 접근용 KEY - 사용자의 장기 자격 증명 |    
| AWS_SECRET_KEY | | AWS 접근용 보안 키 - AWS의 CLI 도구나 API를 사용할 때 인증을 위하여 사용되는 수단 |   
| AWS_REGION | ap-northeast-2 | AWS 리전 명 |    
| NAME | is_testbed | 엑셀 파일 만들때 사용하는 시스템 구분명 |  
| ARCH_IMG | Arch.jpg | 아키텍처를 그린 이미지 파일, 없을 경우 사용치 않음 |  
| S3_OBJECT | [True|False] | S3 Object 검색하여 갯수와 크기 계산 여부 설정, True -> 계산 |

## boto3
### Client
- low-level interface
- service description에 의해 만들어짐
- AWS CLI와 boto3의 기초가 되는 라이브러리인 botocore 수준의 client를 공개
- 가끔 botocore의 API를 찾아봐야하는 경우가 있기도 함
- 모든 AWS 서비스 API와 1:1 매핑됨
- 메소드가 스네이크 케이스로 정의되어 있음
- 예시
  ```
  import boto3

  BUCKET_NAME = 'mybucket'
  client = boto3.client('s3')
  response = client.list_objects(Bucket=BUCKET_NAME)

  for content in response['Contents']:
    obj_dict = client.get_object(Bucket=BUCKET_NAME, Key=content['Key'])
    print(content['Key'], obj_dict['LastModified'])
  ```

### Resource
- boto3.client를 wrapping한 high-level, 객체지향적 interface
- 높은 수준의 추상화
- resource description에 의해 만들어짐
- Identifiers
  - 특정 리소스를 고유하게 식별하는 데 사용되는 고유한 값
  - bucket_name과 key가 있음
- Attributes
  - 리소스 속성에 액세스. load() 메소드를 통해 로드되므로 처음 액세스 시 느리게 로드 됨
  - accept_ranges, metadata, last_modified 등 👉 공식 문서 참고
- Actions
  - 리소스에 대한 작업 호출. 식별자와 일부 특성으로부터 인수 전달을 자동으로 처리 가능
  - copy(), delete(), get(), download_file(), upload_file() 등 👉 공식 문서 참고
- 자원에 대한 조작 위주 → 직관적, 사용 편리
- AWS 서비스와 상호작용할 때 기본 디테일에 대한 고민이 많이 필요하지 않아 boto3 사용에서 권장됨
- boto3.client의 모든 기능을 wrapping한 것이 아니라서 필요하다면 boto3.client 혹은 boto3.resource.meta.client를 - 사용해야 함
- 예시
  ```
  import boto3

  BUCKET_NAME = 'mybucket'
  s3 = boto3.resource('s3')

  # S3 bucket identifier
  bucket = s3.Bucket(BUCKET_NAME)

  # S3 object identifier
  obj = s3.Object(bucket_name="my_bucket", key="test.py")

  # action on S3 Object
  response = obj.get()

  for obj in bucket.objects.all():
    # S3 object identifier, attribute
    print(obj.key, obj.last_modified)
  ```

#### Resource 자원 수집 현황  
- ○ : 완료
- △ : 일부 완료
- ★ : 향후 진행 해야 할 것  

| 구분 | 자원명 | 자원목록 생성 여부 |    
|:---|:---|:---|  
| IAM | User,Group | ○ |  
| Direct Connect | DirectConnect | ○ | 
| VPC | VPC, Subnet, Routes, Inernet Gateway, NAT Gateway, VPC Connection, VPC  Peering, Attachment | ○ |
| Compute | EC2, Lambda  | ○ |  
| Storage | EBS, S3, EFS | ○ |
| Container | ECR, ECS, EKS | ○ |  
| DB | Aurora, RDS, Dynamodb, ElastiCache  | ○ |
| Streams  | MSK(Kafka), SQS, Kinesis Firehose, SNS | ○ |  
| Security | Secrets Manager, Cretificate Manager, Key Management | ○ |
| Network Security | Firewall, Shield, WAF | ○ |    
| CodeSeries | CodeCommit, CodeBuild, CodePipeline, CodeArtifact | ○ |  
| Loging/Monitoring | CloudWatch Metrics, CloudWatch Logs, CloudWatch Events, CloudWatch Alarm, CloudTrail | ○ |  
| Edge Networking | Route53, CloudFront | ○ |  
| - | AWS Config | ★ |   
| | AWS DataSync | ★ |  
| ETL | AWS Glue | ★ |  
| |  Amazon DevOps Guru | ★ |
| | AWS CloudShell | ★ |  
|  | AWS Step Functions | ★ |  
| 기타 | Tax |  ○ |  

#### AWS Config
- AWS 리소스의 구성 상태를 지속적으로 모니터링하고 관리하는 데 사용되는 서비스

#### AWS DataSync
-  AWS (Amazon Web Services)에서 제공하는 데이터 전송 및 동기화 서비스

#### AWS Glue 
- 관리형 ETL (Extract, Transform, Load) 서비스

#### Amazon DevOps Guru
- 기계 학습을 활용하여 애플리케이션 및 인프라스트럭처의 문제를 자동으로 감지하고 대응하는 도구

#### AWS Step Functions
- 워크플로우 오케스트레이션

#### Cloud Shell
- 무료로 사용 가능한 인터랙티브한 쉘 환경 


## dependency 설치
```
pip install -r requirement.txt
```

## 환경변수 설정
### `.env` 파일에 설정
#### 설정항목
`IAM` > `사용자` > `userid` > `보안자격증명` > `액세스 키` > `액세스 키 만들기`
- AWS_ACCESS_KEY : 위의 메뉴에서 만든 ACCESS KEY 
- AWS_SECRET_KEY : 위의 메뉴에서 만든 SECRET KEY
- AWS_REGION : 리전 정보 ex) ap-northeast-2

## 특정 계정의 자원 목록 Excel 로 내리기
- python aws-resource-list.py


## CloudTrail vs CloudWatch
CloudTrail은 AWS API 호출 로그를 수집하여 감사 및 보안 검토를 위한 용도로 사용되며, CloudWatch는 리소스 성능 및 상태 모니터링, 경보 설정, 대시보드 생성, 이벤트 기반 자동화 등 다양한 모니터링 및 운영 관련 작업에 사용할 수 있음

| 항목 | CloudTrail | CloudWatch |  
|:---|:---|:---|  
| 목적 |AWS 리소스의 API 호출 및 관리 작업 로그를 캡처하고 저장하여 보안 및 규정 준수 검토를 위한 감사 및 추적을 제공  | AWS 리소스 및 응용 프로그램의 성능 및 상태를 모니터링하고, 모니터링 데이터를 수집하여 분석하며 경고 및 액션을 트리거하는 용도로 사용 |  
| 기능 | 모든 AWS 계정 활동에 대한 로그를 생성하여 이를 S3 버킷에 저장하거나 CloudWatch Logs 그룹으로 전송할 수 있음 </br> 이를 통해 리소스 변경 및 API 호출의 이력을 추적하여 보안 이슈 및 잠재적인 문제를 식별하고 해결할 수 있음 | CloudWatch는 각종 메트릭과 로그 데이터를 수집하고, 이를 대시보드에 표시하거나 경보를 설정하여 리소스의 성능을 실시간으로 모니터링하고 관리할 수 있음 </br> CloudWatch Events를 통해 다양한 AWS 리소스에서 발생하는 이벤트에 대한 경보 및 자동화된 액션을 설정할 수 있음 |  

