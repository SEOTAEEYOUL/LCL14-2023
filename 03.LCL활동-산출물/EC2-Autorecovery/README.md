# EC2 Auto Recover

> [How can I set up a CloudWatch alarm to automatically recover my EC2 instance?](https://repost.aws/knowledge-center/automatic-recovery-ec2-cloudwatch)  
> [How to create multple cloudwatch alarms using Boto3 in a one shot](https://stackoverflow.com/questions/52109398/how-to-create-multple-cloudwatch-alarms-using-boto3-in-a-one-shot)  
> [boto3 - CloudWatch](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html)  
> [boto3 - CloudWatch > put_metric_alarm](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_alarm.html)

- CloudWatch 설정을 통해서 EC2 가 systems checked failed 발생시 건강한 Host 로 recover 하는 방법
안내 드립니다.
- 첨부파일 처럼 Console 에서 설정이 가능하지만, EC2 인스턴스 개수가 많을 경우 CLI 를 통해서
작업하는게 편리합니다.


## 프로그램 목록  
| Program | 설명 | 비고 |      
|:---|:---|:---|    
| ec2-autorecovery.py | ec2 autorecovery 설정하는 program | `ec2_autorecovery_list.py` 에 있는 목록으 대상으로 작업 |    
| ec2-not-autorecovery-list.py | ec2 에 autorecovery 가 설정되어 있지 않는 목록을 출력하는 program | `ec2_autorecovery_list.py` 을 만들 대상을 출력 |    
| ec2_autorecovery_list.py | ec2-autorecovery.py 에서 사용하는 ec2 autorecovery 적용 대상 ec2 의 instance id 와 name 을 적어 놓은 파일 | ec2 autorecovery 설정이 안되어 있는 ec2 instance 목록을 출력 |   

### 프로그램을 사용한 작업 절차
1. ec2 autorecovery 를 적용할 대상을 찾는다. - `python ec2-not-autorecovery-list.py`
2. ec2 autorecovery 적용 대상 중 적용할 목록을 작성한다. - `edit ec2_autorecovery_list.py`
3. ec2 autorecovery 적용한다. - `python ec2-autorecovery.py`


## 작업 절차
### (1) system checked failed - H/W 이슈일때 Recover   
```
aws cloudwatch put-metric-alarm 
  --alarm-name StatusCheckFailedSystem-Alarmfor-i-0a7cc129687581xxx 
  --metric-name StatusCheckFailed_System 
  --namespace AWS/EC2 
  --statistic Minimum 
  --dimensions Name=InstanceId,Value=i0a7cc129687581xxx 
  --unit Count 
  --period 60 
  --evaluation-periods 1 
  --threshold 1 
  --comparison-operator GreaterThanOrEqualToThreshold 
  --alarm-actions arn:aws:sns:ap-northeast-2:91902386xxxx:myMail arn:aws:automate:ap-northeast2:ec2:recover 
  --region ap-northeast-2
```

```
aws cloudwatch get-metric-statistics 
  --metric-name Buffers 
  --namespace AWS/EC2 
  --dimensions Name=InstanceId,Value=1-23456789 Name=InstanceType,Value=m1.small 
  --start-time 2016-10-15T04:00:00Z 
  --end-time 2016-10-19T07:00:00Z --statistics Average --period 60

```
```
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name StatusCheckFailed_System  --period 1 --start-time 2023-04-08T00:04:30Z  --end-time 2023-04-08T05:00:00Z 
```

### (2) instance checked failed - OS Level 이슈일때 Recover CLI 명령어에서 아래 부분만 변경해주시면 됩니다   
--metric-name StatusCheckFailed_Instance

### (3) 위 2 가지 경우 중 하나만 해당해도 Recover CLI 명령어에서 아래 부분만 변경해주시면 됩니다  
--metric-name StatusCheckFailed   
위 메트릭 이름은 CloudWatch 의 Metric Name 과 같습니다.   


## EC2 Systems Checked Failed 발생시 Auto Recovery 방법

- EC2 가 System Status Check 에 실패하여 Auto Recovery 되는 이유는 Hardware Failure 에 의해서
정상적으로 동작하는 Host 로 EC2 를 재기동 시킵니다. H/W Failure 를 대비하여 아래와같이
설정하시는것을 권고합니다.
- Cloudwatch 에 경보를 설정하여 상태검사 실패 시 자동으로 인스턴스 복구를 하는 옵션을
켜두시는것이 좀 더 빠르게 Auto-Recovery 하는 방법입니다.
- EC2 Console 에서 아래와같이 설정이 가능합니다.

### EC2 Console > 인스턴스 선택 > 작업 > 모니터링 및 문제 해결 > CloudWatch 경보관리
![EC2-CloudWatch-Alter-Management.JPG](./img/EC2-CloudWatch-Alter-Management.JPG)  

## Python 사용
### CloudWatch / Client / put_metric_alarm
```
response = client.put_metric_alarm(
    AlarmName='string',
    AlarmDescription='string',
    ActionsEnabled=True|False,
    OKActions=[
        'string',
    ],
    AlarmActions=[
        'string',
    ],
    InsufficientDataActions=[
        'string',
    ],
    MetricName='string',
    Namespace='string',
    Statistic='SampleCount'|'Average'|'Sum'|'Minimum'|'Maximum',
    ExtendedStatistic='string',
    Dimensions=[
        {
            'Name': 'string',
            'Value': 'string'
        },
    ],
    Period=123,
    Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None',
    EvaluationPeriods=123,
    DatapointsToAlarm=123,
    Threshold=123.0,
    ComparisonOperator='GreaterThanOrEqualToThreshold'|'GreaterThanThreshold'|'LessThanThreshold'|'LessThanOrEqualToThreshold'|'LessThanLowerOrGreaterThanUpperThreshold'|'LessThanLowerThreshold'|'GreaterThanUpperThreshold',
    TreatMissingData='string',
    EvaluateLowSampleCountPercentile='string',
    Metrics=[
        {
            'Id': 'string',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'string',
                    'MetricName': 'string',
                    'Dimensions': [
                        {
                            'Name': 'string',
                            'Value': 'string'
                        },
                    ]
                },
                'Period': 123,
                'Stat': 'string',
                'Unit': 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
            },
            'Expression': 'string',
            'Label': 'string',
            'ReturnData': True|False,
            'Period': 123,
            'AccountId': 'string'
        },
    ],
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ],
    ThresholdMetricId='string'
)
```

### ec2 action
- arn:aws:automate:region:ec2:stop
- arn:aws:automate:region:ec2:terminate
- arn:aws:automate:region:ec2:reboot
- `arn:aws:automate:region:ec2:recover`
- arn:aws:swf:region:account-id:action/actions/AWS_EC2.InstanceId.Stop/1.0
- arn:aws:swf:region:account-id:action/actions/AWS_EC2.InstanceId.Terminate/1.0
- arn:aws:swf:region:account-id:action/actions/AWS_EC2.InstanceId.Reboot/1.0
- arn:aws:swf:region:account-id:action/actions/AWS_EC2.InstanceId.Recover/1.0

### ec2-auto-recover-v1.py


```
$Env:AWS_PROFILE="argos_prd"
aws sts get-caller-identity
python ec2-failover-v1.py
```

#### 정상 수행 결과
```
PS D:\workspace\Project-S\3.Prod\98.Monitoring\EC2-Autorecovery> python ec2-auto-recover-v1.py
[1] sksh-argos-p-infra-ops-ec2-2c-01 (i-078a4ecdf8ddca377)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-infra-ops-ec2-2c-01
{'ResponseMetadata': {'RequestId': '9756116e-b840-450b-943f-8f175049f769', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '9756116e-b840-450b-943f-8f175049f769', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:04:37 GMT'}, 'RetryAttempts': 0}}
총 1 개 EC2 Instance 에 대해서 Auto Recover 설정 함
PS D:\workspace\Project-S\3.Prod\98.Monitoring\EC2-Autorecovery> python ec2-auto-recover-v1.py
[1] sksh-argos-p-infra-ops-ec2-2c-01 (i-078a4ecdf8ddca377)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-infra-ops-ec2-2c-01
{'ResponseMetadata': {'RequestId': 'f24067ce-2608-435e-bad7-1271955bb28d', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'f24067ce-2608-435e-bad7-1271955bb28d', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:13 GMT'}, 'RetryAttempts': 0}}
[2] sksh-argos-p-gw-sksig-ec2-2a-01 (i-0cbcc929b34b6da3f)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-sksig-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'd5debbb2-bbb0-4c4e-93b4-47b48aaa450a', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'd5debbb2-bbb0-4c4e-93b4-47b48aaa450a', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:13 GMT'}, 'RetryAttempts': 0}}
[3] sksh-argos-p-gw-skali-ec2-2a-01 (i-0c48fac11776b951d)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-skali-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'b1fa9d29-27f6-473f-abaa-93bab6ffc34e', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'b1fa9d29-27f6-473f-abaa-93bab6ffc34e', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:13 GMT'}, 'RetryAttempts': 0}}
[4] sksh-argos-p-gw-cmliv-ec2-2a-01 (i-0657b4198cb0482ab)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-cmliv-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'e8f38eee-c0eb-44d0-aae1-b75bdeb6419f', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'e8f38eee-c0eb-44d0-aae1-b75bdeb6419f', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:14 GMT'}, 'RetryAttempts': 0}}
[5] sksh-argos-p-sol-msg-ec2-2a-01 (i-0bdf84db4cff57fcf)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-sol-msg-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'b4a0f053-1aa1-4f01-8272-8c9e70f1c603', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'b4a0f053-1aa1-4f01-8272-8c9e70f1c603', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:14 GMT', 'connection': 'close'}, 'RetryAttempts': 0}}
[6] sksh-argos-p-mob-arg-ec2-2a-01 (i-02338f30e868863c1)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-mob-arg-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'fc2b900c-0bdd-4791-9acf-86c7a2a8402a', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'fc2b900c-0bdd-4791-9acf-86c7a2a8402a', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:16 GMT'}, 'RetryAttempts': 0}}
[7] sksh-argos-p-gw-blbi-ec2-2a-01 (i-0c748f61767de82ec)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-blbi-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'cb735d1d-8203-48c2-95c8-b97147f80959', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'cb735d1d-8203-48c2-95c8-b97147f80959', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:16 GMT'}, 'RetryAttempts': 0}}
[8] sksh-argos-p-mob-cap-ec2-2a-01 (i-0b9c780927933e23e)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-mob-cap-ec2-2a-01
{'ResponseMetadata': {'RequestId': '38f27ad0-24cf-42f2-a9de-2027cd767d59', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '38f27ad0-24cf-42f2-a9de-2027cd767d59', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:16 GMT'}, 'RetryAttempts': 0}}
[9] sksh-argos-p-gw-rrs-ec2-2a-01 (i-0aa556126cdde83aa)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-rrs-ec2-2a-01
{'ResponseMetadata': {'RequestId': '2f1e0de2-2b26-43f1-935b-f7ac65e140ee', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '2f1e0de2-2b26-43f1-935b-f7ac65e140ee', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:17 GMT'}, 'RetryAttempts': 0}}
[10] sksh-argos-p-gw-upali-ec2-2a-01 (i-0126cebdd3e6876c8)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-upali-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'e06bbc45-0407-4489-ab12-45ddc64d03ec', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'e06bbc45-0407-4489-ab12-45ddc64d03ec', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:17 GMT', 'connection': 'close'}, 'RetryAttempts': 0}}
[11] sksh-argos-p-gw-upwlt-ec2-2a-01 (i-0e7a0c877666b9f7f)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-upwlt-ec2-2a-01
{'ResponseMetadata': {'RequestId': '72ac25a6-dd6b-47f6-8e09-de3ec589e056', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '72ac25a6-dd6b-47f6-8e09-de3ec589e056', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:17 GMT'}, 'RetryAttempts': 0}}
[12] sksh-argos-p-gw-ktcdc-ec2-2a-01 (i-018e7e025e3d7e60a)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-ktcdc-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'afefe81b-fd82-4b28-9f55-2d407ca41256', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'afefe81b-fd82-4b28-9f55-2d407ca41256', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:18 GMT'}, 'RetryAttempts': 0}}
[13] sksh-argos-p-gw-ktcdc-ec2-2a-02 (i-02b845a7f1bfc23fa)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-ktcdc-ec2-2a-02
{'ResponseMetadata': {'RequestId': '87ac1d75-54c9-410e-ae60-3b375b7fb17c', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '87ac1d75-54c9-410e-ae60-3b375b7fb17c', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:18 GMT'}, 'RetryAttempts': 0}}
[14] sksh-argos-p-gw-skali-ec2-2b-02 (i-022ab6568304de22a)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-skali-ec2-2b-02
{'ResponseMetadata': {'RequestId': '3c30470e-6f3b-4686-ad5e-0d0d3fb64480', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '3c30470e-6f3b-4686-ad5e-0d0d3fb64480', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:18 GMT'}, 'RetryAttempts': 0}}
[15] sksh-argos-p-gw-upali-ec2 (i-0e8bb8af914e553b1)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-upali-ec2
{'ResponseMetadata': {'RequestId': 'a66e417c-77a1-4043-b886-d21e971c9f1e', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'a66e417c-77a1-4043-b886-d21e971c9f1e', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:19 GMT', 'connection': 'close'}, 'RetryAttempts': 0}}
[16] sksh-argos-p-mob-arg-ec2-2b-02 (i-00f6a779330fda51b)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-mob-arg-ec2-2b-02
{'ResponseMetadata': {'RequestId': '4b786906-4b3f-45e9-88e6-eb5ad41622af', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '4b786906-4b3f-45e9-88e6-eb5ad41622af', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:19 GMT'}, 'RetryAttempts': 0}}
[17] sksh-argos-p-sol-msg-ec2-2b-02 (i-093fbdb94bc0aa4e4)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-sol-msg-ec2-2b-02
{'ResponseMetadata': {'RequestId': '833f18f4-e226-44ff-98fc-92195d811f00', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '833f18f4-e226-44ff-98fc-92195d811f00', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:20 GMT'}, 'RetryAttempts': 0}}
[18] sksh-argos-p-gw-sksig-ec2-2b-02 (i-0ddf43bf20a4a0d71)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-sksig-ec2-2b-02
{'ResponseMetadata': {'RequestId': '8d01c94c-7788-48af-8b7e-9b2b8e269d7e', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '8d01c94c-7788-48af-8b7e-9b2b8e269d7e', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:20 GMT'}, 'RetryAttempts': 0}}
[19] sksh-argos-p-gw-upwlt-ec2-2b-02 (i-0eb56cb65646c008b)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-upwlt-ec2-2b-02
{'ResponseMetadata': {'RequestId': 'cd052bf1-c961-488b-a33a-17e32952bbdc', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'cd052bf1-c961-488b-a33a-17e32952bbdc', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:21 GMT'}, 'RetryAttempts': 0}}
[20] sksh-argos-p-gw-rrs-ec2-2b-02 (i-0ebfb725bb97a4e2f)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-rrs-ec2-2b-02
{'ResponseMetadata': {'RequestId': '1ee777be-3955-4965-98fb-82590d93e32b', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '1ee777be-3955-4965-98fb-82590d93e32b', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:21 GMT', 'connection': 'close'}, 'RetryAttempts': 0}}
[21] sksh-argos-p-gw-blbi-ec2-2b-02 (i-0abaf2b0139e4ce6f)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-blbi-ec2-2b-02
{'ResponseMetadata': {'RequestId': 'e6b473fd-0903-4e1d-8c69-e7b099730747', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'e6b473fd-0903-4e1d-8c69-e7b099730747', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:22 GMT'}, 'RetryAttempts': 0}}
[22] sksh-argos-p-mob-cap-ec2-2b-02 (i-06025d9d8ac5e52f6)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-mob-cap-ec2-2b-02
{'ResponseMetadata': {'RequestId': '84b20c2b-1f21-4741-9b7a-7f22a9c8f835', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '84b20c2b-1f21-4741-9b7a-7f22a9c8f835', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:22 GMT'}, 'RetryAttempts': 0}}
[23] sksh-argos-p-gw-moni-ec2-2b-01 (i-0d24dc9975772e079)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-moni-ec2-2b-01
{'ResponseMetadata': {'RequestId': '9908ab80-ee0f-4882-aea2-c3b1c96316ee', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '9908ab80-ee0f-4882-aea2-c3b1c96316ee', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:22 GMT'}, 'RetryAttempts': 0}}
[24] sksh-argos-p-gw-cmliv-ec2-2b-02 (i-0b59b456fcbc09c4b)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-cmliv-ec2-2b-02
{'ResponseMetadata': {'RequestId': '9d7ef05d-2c16-4f55-95ee-c0feee2cb352', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '9d7ef05d-2c16-4f55-95ee-c0feee2cb352', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:23 GMT'}, 'RetryAttempts': 0}}
[25] sksh-argos-p-gw-blbk-ec2-2b-02 (i-0126ed5c2b27cbc0f)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-blbk-ec2-2b-02
{'ResponseMetadata': {'RequestId': '416a19b1-8fbd-4d60-873d-40df309a8dc7', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '416a19b1-8fbd-4d60-873d-40df309a8dc7', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:23 GMT', 'connection': 'close'}, 'RetryAttempts': 0}}
[26] sksh-argos-p-icms-rrs-ec2-2b-02 (i-02904aaf51d275639)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-icms-rrs-ec2-2b-02
{'ResponseMetadata': {'RequestId': '7d6a7a22-9dde-42a6-add2-73f51f746d49', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '7d6a7a22-9dde-42a6-add2-73f51f746d49', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:24 GMT'}, 'RetryAttempts': 0}}
[27] sksh-argos-p-icms-icms-ec2-2b-02 (i-0f702f3bb6859479f)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-icms-icms-ec2-2b-02
{'ResponseMetadata': {'RequestId': 'de047da0-1001-40c3-ba61-6cb2f7bdeb82', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'de047da0-1001-40c3-ba61-6cb2f7bdeb82', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:24 GMT'}, 'RetryAttempts': 0}}
[28] sksh-argos-p-gw-moni-ec2-2c-02 (i-0975e0d79731b849f)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-moni-ec2-2c-02
{'ResponseMetadata': {'RequestId': '4d53c21b-93c9-4243-a6c8-7a1e83312f31', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '4d53c21b-93c9-4243-a6c8-7a1e83312f31', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:24 GMT'}, 'RetryAttempts': 0}}
[29] sksh-argos-p-sol-sear-ec2-2c-01 (i-04f5cbb3cc4a6da4a)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-sol-sear-ec2-2c-01
{'ResponseMetadata': {'RequestId': '925df91b-7ee6-4dc7-83df-efe6584be554', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '925df91b-7ee6-4dc7-83df-efe6584be554', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:25 GMT'}, 'RetryAttempts': 0}}
[30] sksh-argos-p-mob-cad-ec2-2a-01 (i-0a4de731b1d513707)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-mob-cad-ec2-2a-01
{'ResponseMetadata': {'RequestId': '440b3718-aec2-482e-bfeb-114c7b280d3f', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '440b3718-aec2-482e-bfeb-114c7b280d3f', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:25 GMT', 'connection': 'close'}, 'RetryAttempts': 0}}
[31] sksh-argos-p-gw-blbk-ec2-2a-01 (i-0b21b6d2fb7b7fac7)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-blbk-ec2-2a-01
{'ResponseMetadata': {'RequestId': '468c4299-46bb-44d3-905f-46d897faaac7', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '468c4299-46bb-44d3-905f-46d897faaac7', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:26 GMT'}, 'RetryAttempts': 0}}
[32] sksh-argos-p-icms-icms-ec2-2a-01 (i-0abda1f5f8c77eb26)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-icms-icms-ec2-2a-01
{'ResponseMetadata': {'RequestId': '12484904-6de1-4bc6-a784-54e6407a0ecd', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '12484904-6de1-4bc6-a784-54e6407a0ecd', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:27 GMT'}, 'RetryAttempts': 0}}
[33] sksh-argos-p-icms-rrs-panel-ec2-2a-01 (i-0ace600ebe75ebd91)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-icms-rrs-panel-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'f113b33b-a54c-4f52-93eb-3762b10a2fdc', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'f113b33b-a54c-4f52-93eb-3762b10a2fdc', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:27 GMT'}, 'RetryAttempts': 0}}
[34] sksh-argos-p-icms-rrs-ec2-2a-03 (i-04244a2afc61ed164)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-icms-rrs-ec2-2a-03
{'ResponseMetadata': {'RequestId': '38162ace-d725-406d-bfda-341dd6178f92', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '38162ace-d725-406d-bfda-341dd6178f92', 'content-type': 'text/xml', 
'content-length': '214', 'date': 'Fri, 07 Apr 2023 09:08:28 GMT'}, 'RetryAttempts': 0}}
총 34 개 EC2 Instance 에 대해서 Auto Recover 설정 함
PS D:\workspace\Project-S\3.Prod\98.Monitoring\EC2-Autorecovery> 
```

#### 오류 메시지
- recover 는 `StatusCheckFailed_System` 메트릭만 설정 가능하며 그외는 아래와 같은 오류 발생
```
botocore.exceptions.ClientError: An error occurred (ValidationError) when calling the PutMetricAlarm 
operation: The EC2 'Recover' action can only be defined on the 'StatusCheckFailed_System' metric and 
'AWS/EC2' namespace.
```

![EC2-CloudWatch-Alarm-list](./img/EC2-CloudWatch-Alter.JPG)  
![EC2-CloudWatch-Alarm-Recover](./img/EC2-CloudWatch-Alarm-Recover.JPG)   


```
PS > python ec2-not-autorecovery-list.py
CloudWatch Alarms
{'ActionsEnabled': True,
 'AlarmActions': ['arn:aws:automate:ap-northeast-2:ec2:recover'],
 'AlarmArn': 'arn:aws:cloudwatch:ap-northeast-2:123456789012:alarm:StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-blbi-ec2-2a-01',
 'AlarmConfigurationUpdatedTimestamp': datetime.datetime(2023, 4, 7, 9, 8, 16, 462000, tzinfo=tzutc()),   
 'AlarmDescription': 'Alarm when status check fails on '
                     'i-0c748f61767de82ec(sksh-argos-p-gw-blbi-ec2-2a-01) ',
 'AlarmName': 'StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-blbi-ec2-2a-01',
 'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
 'Dimensions': [{'Name': 'InstanceId', 'Value': 'i-0c748f61767de82ec'}],
 'EvaluationPeriods': 1,
 'InsufficientDataActions': [],
 'MetricName': 'StatusCheckFailed_System',
 'Namespace': 'AWS/EC2',
 'OKActions': [],
 'Period': 60,
 'StateReason': 'Threshold Crossed: 1 datapoint [0.0 (07/04/23 09:08:00)] was '
                'not greater than or equal to the threshold (1.0).',
 'StateReasonData': '{"version":"1.0","queryDate":"2023-04-07T09:09:15.917+0000","startDate":"2023-04-07T09:08:00.000+0000","unit":"Count","statistic":"Minimum","period":60,"recentDatapoints":[0.0],"threshold":1.0,"evaluatedDatapoints":[{"timestamp":"2023-04-07T09:08:00.000+0000","sampleCount":1.0,"value":0.0}]}',   
 'StateTransitionedTimestamp': datetime.datetime(2023, 4, 7, 9, 9, 15, 920000, tzinfo=tzutc()),
 'StateUpdatedTimestamp': datetime.datetime(2023, 4, 7, 9, 9, 15, 920000, tzinfo=tzutc()),
 'StateValue': 'OK',
 'Statistic': 'Minimum',
 'Threshold': 1.0,
 'Unit': 'Count'}
['i-0c748f61767de82ec', 'i-0abaf2b0139e4ce6f', 'i-0b21b6d2fb7b7fac7', 'i-0126ed5c2b27cbc0f', 'i-0657b4198cb0482ab', 'i-0b59b456fcbc09c4b', 'i-018e7e025e3d7e60a', 'i-02b845a7f1bfc23fa', 'i-0d24dc9975772e079', 'i-0975e0d79731b849f', 'i-0aa556126cdde83aa', 'i-0ebfb725bb97a4e2f', 'i-0c48fac11776b951d', 'i-022ab6568304de22a', 'i-0cbcc929b34b6da3f', 'i-0ddf43bf20a4a0d71', 'i-0e8bb8af914e553b1', 'i-0126cebdd3e6876c8', 'i-0e7a0c877666b9f7f', 'i-0eb56cb65646c008b', 'i-0abda1f5f8c77eb26', 'i-0f702f3bb6859479f', 'i-04244a2afc61ed164', 
'i-02904aaf51d275639', 'i-0ace600ebe75ebd91', 'i-078a4ecdf8ddca377', 'i-02338f30e868863c1', 'i-00f6a779330fda51b', 'i-0a4de731b1d513707', 'i-0b9c780927933e23e', 'i-06025d9d8ac5e52f6', 'i-0bdf84db4cff57fcf', 'i-093fbdb94bc0aa4e4', 'i-04f5cbb3cc4a6da4a']
총갯수[34]

>>>>>instance_info[sksh-argos-p-gw-sksig-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-skali-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-sol-msg-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-mob-arg-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-blbi-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-mob-cap-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-rrs-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-gwicms-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-upali-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-upwlt-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-ktcdc-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-ktcdc-ec2-2a-02], False
>>>>>instance_info[sksh-argos-p-gw-skali-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-gw-upali-ec2], False
>>>>>instance_info[sksh-argos-p-mob-arg-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-sol-msg-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-gw-sksig-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-gw-upwlt-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-gw-rrs-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-gw-blbi-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-mob-cap-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-gw-moni-ec2-2b-01], False
>>>>>instance_info[sksh-argos-p-gw-blbk-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-icms-rrs-ec2-2b-02], False
>>>>>instance_info[sksh-argos-p-gw-moni-ec2-2c-02], False
>>>>>instance_info[sksh-argos-p-gw-gwicms-ec2-2c-02], False
>>>>>instance_info[sksh-argos-p-infra-ops-ec2-2c-01], False
>>>>>instance_info[sksh-argos-p-sol-sear-ec2-2c-01], False
>>>>>instance_info[sksh-argos-p-eks-cna-worker-2], True
>>>>>instance_info[sksh-argos-p-eks-ui-worker-1], True
>>>>>instance_info[sksh-argos-p-eks-ui-mgmt-1], True
>>>>>instance_info[sksh-argos-p-eks-ui-worker-2], True
>>>>>instance_info[sksh-argos-p-eks-igp-worker-2], True
>>>>>instance_info[sksh-argos-p-eks-cna-worker-1], True
>>>>>instance_info[sksh-argos-p-eks-ui-worker-8], True
>>>>>instance_info[sksh-argos-p-gw-blbk-ec2-2c-03], False
>>>>>instance_info[sksh-argos-p-gw-icms-ec2-2c-02], False
>>>>>instance_info[sksh-argos-p-eks-igp-worker-3], True
>>>>>instance_info[sksh-argos-p-eks-igp-worker-4], True
>>>>>instance_info[sksh-argos-p-eks-ui-worker-3], True
>>>>>instance_info[sksh-argos-p-eks-ui-worker-4], True
>>>>>instance_info[sksh-argos-p-cad-mig-ec2-2b-09], False
>>>>>instance_info[sksh-argos-p-cad-mig-ec2-2b-10], False
>>>>>instance_info[sksh-argos-p-eks-cna-worker-3], True
>>>>>instance_info[sksh-argos-p-eks-ui-ng-worker-1], True
>>>>>instance_info[sksh-argos-p-mob-cad-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-gw-blbk-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-icms-rrs-panel-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-icms-rrs-ec2-2a-03], False
>>>>>instance_info[sksh-argos-p-pt-whatap-ec2], False
>>>>>instance_info[sksh-argos-p-eks-ui-worker-5], True
>>>>>instance_info[sksh-argos-p-eks-cna-mgmt-1], True
>>>>>instance_info[sksh-argos-p-eks-ui-worker-7], True
>>>>>instance_info[sksh-argos-p-eks-igp-worker-5], True
>>>>>instance_info[sksh-argos-p-eks-igp-worker-1], True
>>>>>instance_info[sksh-argos-p-eks-igp-mgmt-1], True
>>>>>instance_info[sksh-argos-p-eks-cna-worker-4], True
>>>>>instance_info[sksh-argos-p-eks-cna-worker-5], True
>>>>>instance_info[sksh-argos-p-gw-icms-ec2-2a-01], False
>>>>>instance_info[sksh-argos-p-eks-ui-ng-worker-1], True
[{'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0cbcc929b34b6da3f',
  'name': 'sksh-argos-p-gw-sksig-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0c48fac11776b951d',
  'name': 'sksh-argos-p-gw-skali-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0bdf84db4cff57fcf',
  'name': 'sksh-argos-p-sol-msg-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-02338f30e868863c1',
  'name': 'sksh-argos-p-mob-arg-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0c748f61767de82ec',
  'name': 'sksh-argos-p-gw-blbi-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0b9c780927933e23e',
  'name': 'sksh-argos-p-mob-cap-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0aa556126cdde83aa',
  'name': 'sksh-argos-p-gw-rrs-ec2-2a-01'},
 {'autorecovery': False,
  'eks_node': False,
  'instance_id': 'i-0e09a8d21a16e1dec',
  'name': 'sksh-argos-p-gw-gwicms-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0126cebdd3e6876c8',
  'name': 'sksh-argos-p-gw-upali-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0e7a0c877666b9f7f',
  'name': 'sksh-argos-p-gw-upwlt-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-018e7e025e3d7e60a',
  'name': 'sksh-argos-p-gw-ktcdc-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-02b845a7f1bfc23fa',
  'name': 'sksh-argos-p-gw-ktcdc-ec2-2a-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-022ab6568304de22a',
  'name': 'sksh-argos-p-gw-skali-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0e8bb8af914e553b1',
  'name': 'sksh-argos-p-gw-upali-ec2'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-00f6a779330fda51b',
  'name': 'sksh-argos-p-mob-arg-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-093fbdb94bc0aa4e4',
  'name': 'sksh-argos-p-sol-msg-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0ddf43bf20a4a0d71',
  'name': 'sksh-argos-p-gw-sksig-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0eb56cb65646c008b',
  'name': 'sksh-argos-p-gw-upwlt-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0ebfb725bb97a4e2f',
  'name': 'sksh-argos-p-gw-rrs-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0abaf2b0139e4ce6f',
  'name': 'sksh-argos-p-gw-blbi-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-06025d9d8ac5e52f6',
  'name': 'sksh-argos-p-mob-cap-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0d24dc9975772e079',
  'name': 'sksh-argos-p-gw-moni-ec2-2b-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0126ed5c2b27cbc0f',
  'name': 'sksh-argos-p-gw-blbk-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-02904aaf51d275639',
  'name': 'sksh-argos-p-icms-rrs-ec2-2b-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0975e0d79731b849f',
  'name': 'sksh-argos-p-gw-moni-ec2-2c-02'},
 {'autorecovery': False,
  'eks_node': False,
  'instance_id': 'i-0e9d1b6496981a146',
  'name': 'sksh-argos-p-gw-gwicms-ec2-2c-02'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-078a4ecdf8ddca377',
  'name': 'sksh-argos-p-infra-ops-ec2-2c-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-04f5cbb3cc4a6da4a',
  'name': 'sksh-argos-p-sol-sear-ec2-2c-01'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-04dce8b63dadc9af4',
  'name': 'sksh-argos-p-eks-cna-worker-2'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-0207487b50a3dc271',
  'name': 'sksh-argos-p-eks-ui-worker-1'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-068046de807b103fc',
  'name': 'sksh-argos-p-eks-ui-mgmt-1'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-05b08adada38346ac',
  'name': 'sksh-argos-p-eks-ui-worker-2'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-084a46794f13e6038',
  'name': 'sksh-argos-p-eks-igp-worker-2'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-0dbe72b6060f601e0',
  'name': 'sksh-argos-p-eks-cna-worker-1'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-0aa9cff4a6134d67b',
  'name': 'sksh-argos-p-eks-ui-worker-8'},
 {'autorecovery': False,
  'eks_node': False,
  'instance_id': 'i-02d1cfc87ceb0c864',
  'name': 'sksh-argos-p-gw-blbk-ec2-2c-03'},
 {'autorecovery': False,
  'eks_node': False,
  'instance_id': 'i-0d16a369ac44f3279',
  'name': 'sksh-argos-p-gw-icms-ec2-2c-02'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-09b4550c4d6844a21',
  'name': 'sksh-argos-p-eks-igp-worker-3'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-0f6c06498d2282b68',
  'name': 'sksh-argos-p-eks-igp-worker-4'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-024bf234527c6251b',
  'name': 'sksh-argos-p-eks-ui-worker-3'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-06022894054013b49',
  'name': 'sksh-argos-p-eks-ui-worker-4'},
 {'autorecovery': False,
  'eks_node': False,
  'instance_id': 'i-0e479518c7fa4c359',
  'name': 'sksh-argos-p-cad-mig-ec2-2b-09'},
 {'autorecovery': False,
  'eks_node': False,
  'instance_id': 'i-0ca4280115663dca4',
  'name': 'sksh-argos-p-cad-mig-ec2-2b-10'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-04310200d201f3bf5',
  'name': 'sksh-argos-p-eks-cna-worker-3'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-055655602f325d2d3',
  'name': 'sksh-argos-p-eks-ui-ng-worker-1'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0a4de731b1d513707',
  'name': 'sksh-argos-p-mob-cad-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0b21b6d2fb7b7fac7',
  'name': 'sksh-argos-p-gw-blbk-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-0ace600ebe75ebd91',
  'name': 'sksh-argos-p-icms-rrs-panel-ec2-2a-01'},
 {'autorecovery': True,
  'eks_node': False,
  'instance_id': 'i-04244a2afc61ed164',
  'name': 'sksh-argos-p-icms-rrs-ec2-2a-03'},
 {'autorecovery': False,
  'eks_node': False,
  'instance_id': 'i-0b1e0a33ec3fcaa53',
  'name': 'sksh-argos-p-pt-whatap-ec2'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-064ba1c68ef76b714',
  'name': 'sksh-argos-p-eks-ui-worker-5'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-0300bbfae05f7e1c2',
  'name': 'sksh-argos-p-eks-cna-mgmt-1'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-02cf8dddc89356e0b',
  'name': 'sksh-argos-p-eks-ui-worker-7'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-08ae47416fef5e0af',
  'name': 'sksh-argos-p-eks-igp-worker-5'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-051da17f131a2d0f9',
  'name': 'sksh-argos-p-eks-igp-worker-1'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-0540c813ad32db14d',
  'name': 'sksh-argos-p-eks-igp-mgmt-1'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-07ca3e7827013e589',
  'name': 'sksh-argos-p-eks-cna-worker-4'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-0e5851c1299f06066',
  'name': 'sksh-argos-p-eks-cna-worker-5'},
 {'autorecovery': False,
  'eks_node': False,
  'instance_id': 'i-04893fb891bbd7e26',
  'name': 'sksh-argos-p-gw-icms-ec2-2a-01'},
 {'autorecovery': False,
  'eks_node': True,
  'instance_id': 'i-0ee1068391e87f588',
  'name': 'sksh-argos-p-eks-ui-ng-worker-1'}]
총갯수[60] - 알람설정 갯수[34], EKS Node 갯수[22]

[00] i-0e09a8d21a16e1dec:sksh-argos-p-gw-gwicms-ec2-2a-01
[01] i-0e9d1b6496981a146:sksh-argos-p-gw-gwicms-ec2-2c-02
[02] i-02d1cfc87ceb0c864:sksh-argos-p-gw-blbk-ec2-2c-03
[03] i-0d16a369ac44f3279:sksh-argos-p-gw-icms-ec2-2c-02
[04] i-0e479518c7fa4c359:sksh-argos-p-cad-mig-ec2-2b-09
[05] i-0ca4280115663dca4:sksh-argos-p-cad-mig-ec2-2b-10
[06] i-0b1e0a33ec3fcaa53:sksh-argos-p-pt-whatap-ec2
[07] i-04893fb891bbd7e26:sksh-argos-p-gw-icms-ec2-2a-01
추가알람설정 갯수[8]
Program execution time: 2.231924533843994 seconds
2023-07-03 18:57:33.409113
PS > 
```

```
PS D:\workspace\LCL-14\03.운영자료\EC2-Autorecovery> python ec2-autorecovery.py
CloudWatch Alarms
[1] sksh-argos-p-gw-gwicms-ec2-2a-01 (i-0e09a8d21a16e1dec)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-gwicms-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'ced118c9-038f-4ff9-bb48-c7e85080a48c', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'ced118c9-038f-4ff9-bb48-c7e85080a48c', 'content-type': 'text/xml', 'content-length': '214', 'date': 'Tue, 04 Jul 2023 01:50:13 GMT'}, 'RetryAttempts': 0}}
[2] sksh-argos-p-gw-gwicms-ec2-2c-02 (i-0e9d1b6496981a146)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-gwicms-ec2-2c-02
{'ResponseMetadata': {'RequestId': '63771efa-674c-4001-9b14-b62a6d630e35', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '63771efa-674c-4001-9b14-b62a6d630e35', 'content-type': 'text/xml', 'content-length': '214', 'date': 'Tue, 04 Jul 2023 01:50:13 GMT'}, 'RetryAttempts': 0}}
[3] sksh-argos-p-gw-blbk-ec2-2c-03 (i-02d1cfc87ceb0c864)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-blbk-ec2-2c-03
{'ResponseMetadata': {'RequestId': '9526e726-5dcf-4152-a7c3-787fbfc71fa5', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '9526e726-5dcf-4152-a7c3-787fbfc71fa5', 'content-type': 'text/xml', 'content-length': '214', 'date': 'Tue, 04 Jul 2023 01:50:13 GMT'}, 'RetryAttempts': 0}}
[4] sksh-argos-p-gw-icms-ec2-2c-02 (i-0d16a369ac44f3279)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-icms-ec2-2c-02
{'ResponseMetadata': {'RequestId': '39f1a220-5712-4db5-83b2-167be04fea54', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '39f1a220-5712-4db5-83b2-167be04fea54', 'content-type': 'text/xml', 'content-length': '214', 'date': 'Tue, 04 Jul 2023 01:50:13 GMT'}, 'RetryAttempts': 0}}
[5] sksh-argos-p-gw-icms-ec2-2a-01 (i-04893fb891bbd7e26)
     StatusCheckFailedSystem-Alarm-for-sksh-argos-p-gw-icms-ec2-2a-01
{'ResponseMetadata': {'RequestId': 'ca49785b-dc58-4f4c-83d0-92faa5b1cc5d', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'ca49785b-dc58-4f4c-83d0-92faa5b1cc5d', 'content-type': 'text/xml', 'content-length': '214', 'date': 'Tue, 04 Jul 2023 01:50:13 GMT'}, 'RetryAttempts': 0}}
총 5 개 EC2 Instance 에 대해서 Auto Recover 설정 함
Program execution time: 0.6406443119049072 seconds
2023-07-04 10:50:12.130817
PS D:\workspace\LCL-14\03.운영자료\EC2-Autorecovery> 
```