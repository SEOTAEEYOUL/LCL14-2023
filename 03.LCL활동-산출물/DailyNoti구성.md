# Daily Noti 전송 (S3 Presigned URL 생성 후 Slack 전파)

## 1. Slack 구성
### 워크스페이스 및 채널 생성
- 워크스페이스 이름: https://skcc-lcl14.slack.com
- 채널 이름: skcc-lcl14-2023
### Webhook 설정
- 웹후크 URL: https://hooks.slack.com/services/**********

## 2. S3 구성
### 버킷 및 객체 생성
- 퍼블릭 액세스 차단
- 객체 URL: https://yjbang-lcl14-test.s3.ap-northeast-2.amazonaws.com/surfing.jpg

## 3. Lambda 구성
### Code 작성
```
import boto3
import requests
import os


def lambda_handler(event, context):
    # Get the S3 bucket and object key from the event
    bucket_name = event["bucket"]
    object_key = event["object_key"]

    # Generate a pre-signed URL for the S3 object
    s3_client = boto3.client("s3")
    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        #ExpiresIn=3600,  # URL expiration time in seconds (1 hour in this example)
        ExpiresIn=30
    )

    # Compose the Slack message with the pre-signed URL
    message = {"text": f"Pre-signed URL for S3 object: {presigned_url}"}

    # Send the Slack message
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    response = requests.post(slack_webhook_url, json=message)

    # Check if the Slack message was sent successfully
    if response.status_code != 200:
        raise Exception(
            f"Slack API request failed with status code {response.status_code}"
        )

    return {"statusCode": 200, "body": "Success"}

```
- 런타임 설정: Python 3.8
- 계층(Layer): AWS에서 제공하는 계층 목록에서 AWSSDKPandas-Python38 추가 
- 환경 변수 추가
	- key: SLACK_WEBHOOK_URL	
	- Value: https://hooks.slack.com/services/**********

### EventBridge 규칙 생성
- 규칙 유형: 일정(Schedule)
https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/services-cloudwatchevents-expressions.html
- Schedule type : Cron-based schedule 또는 Rate-based schedule 중 선택
- 추가 설정 > 대상 입력 구성 > 상수(JSON 텍스트)
```
{
  "bucket": "yjbang-lcl14-test",
  "object_key": "surfing.jpg"
}
```
## 4. 수행 결과
![스크린샷 2023-06-28 오전 12 13 31](https://github.com/SEOTAEEYOUL/LCL-14/assets/36718991/fdead87f-978c-4022-9d8e-8725203e9a3c)
