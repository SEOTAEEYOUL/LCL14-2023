aws cloudwatch put-metric-alarm --alarm-name StatusCheckFailedSystem-Alarmfor-i-0a7cc129687581xxx --metric-name StatusCheckFailed_System --namespace
AWS/EC2 --statistic Minimum --dimensions Name=InstanceId,Value=i0a7cc129687581xxx --unit Count --period 60 --evaluation-periods 1 --threshold
1 --comparison-operator GreaterThanOrEqualToThreshold --alarm-actions
arn:aws:sns:ap-northeast-2:91902386xxxx:myMail arn:aws:automate:ap-northeast2:ec2:recover --region ap-northeast-2 