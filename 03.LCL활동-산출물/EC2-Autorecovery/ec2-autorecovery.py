import boto3_helper
import ec2_autorecovery_list

import time
import datetime

def set_autorecovery(cloudwatch):
    cnt = 0
    for ec2_instance, ec2_name in ec2_autorecovery_list.ec2_instances.items():
        print(f'[{cnt + 1}] {ec2_name} ({ec2_instance})')
        print(f'     StatusCheckFailedSystem-Alarm-for-{ec2_name}')

        response = cloudwatch.put_metric_alarm(
            AlarmName=f'StatusCheckFailedSystem-Alarm-for-{ec2_name}', 
            MetricName='StatusCheckFailed_System',
            Namespace='AWS/EC2',
            Statistic='Minimum',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': ec2_instance
                },
            ],
            Unit='Count',
            Period=60,
            EvaluationPeriods=1,
            Threshold=1, 
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            AlarmActions=[
                # f"arn:aws:sns:ap-northeast-2:91902386xxxx:myMail",
                # f"arn:aws:automate:{region}:ec2:reboot",
                f"arn:aws:automate:ap-northeast-2:ec2:recover"
            ],
            ActionsEnabled=True,
            AlarmDescription=f'Alarm when status check fails on {ec2_instance}({ec2_name}) '
            )
        print(response)


        cnt += 1


    print(f'총 {cnt} 개 EC2 Instance 에 대해서 Auto Recover 설정 함')


if __name__ == "__main__":
    session = boto3_helper.init_aws_session()

    print("CloudWatch Alarms")
    start_time = time.time()
    # codeartifact = session.client('codeartifact')
    cloudwatch = session.client('cloudwatch', region_name='ap-northeast-2')
    set_autorecovery(cloudwatch)

    end_time = time.time()
    print(f"Program execution time: {end_time - start_time} seconds")

    now = datetime.datetime.now()

    print(now) 