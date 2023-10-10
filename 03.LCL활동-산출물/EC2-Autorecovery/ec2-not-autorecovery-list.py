# -*- coding: utf-8 -*-
import boto3_helper

# import boto3
import jmespath
import argparse
import datetime
import time

import json
from pprint import pprint

import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='botocore.client')

now = datetime.datetime.now()
now_time = now.strftime("%y%m%d")


def report_cloudwatch_alarms_autorecover(cloudwatch, metric_name):
    ec2_instances = []

    next_token = ''
    cloudwatch_alarms_cnt = 0
    while True:
        alarms = cloudwatch.describe_alarms(MaxRecords=10, NextToken=next_token)
        for alarm in alarms['MetricAlarms']:
            # print(alarm['AlarmName'])

            alarm_output = jmespath.search('[ActionsEnabled, AlarmActions, AlarmArn, AlarmConfigurationUpdatedTimestamp, AlarmDescription, AlarmName, Dimensions, EvaluationPeriods, InsufficientDataActions, MetricName, Namespace, Period, StateReason, StateReasonData, StateUpdatedTimestamp, StateValue, Statistic, Threshold, Unit]', alarm)




            actionsEnabled, alarmActions, alarmArn, alarmConfigurationUpdatedTimestamp, alarmDescription, alarmName, dimensions, evaluationPeriods, insufficientDataActions, metricName, namespace, period, stateReason, stateReasonData, stateUpdatedTimestamp, stateValue, statistic, threshold, unit = alarm_output

            # pprint(f'{alarmName} : {alarmDescription}')
            # print("-------")

            if metricName == metric_name:
                if cloudwatch_alarms_cnt == 0:
                    pprint(alarm)
                ec2_instances.append(dimensions[0]['Value'])
                # ec2_instances.append(True)
                cloudwatch_alarms_cnt += 1

        if 'NextToken' not in alarms:
            break
        next_token = alarms['NextToken']

    print(f"{ec2_instances}\n총갯수[{cloudwatch_alarms_cnt}]\n")

    return cloudwatch_alarms_cnt, ec2_instances


def report_autorecover_not_set_ec2_list(ec2, autorecovery_cnt, autorecovery_instances):
    ec2_instances = []

    instance_list = ec2.describe_instances()
    # pprint(instance_list)

    output = jmespath.search("Reservations[*].Instances[*].[Tags[?Key=='Name'].Value, InstanceId, InstanceType, Placement.AvailabilityZone, State.Name, PrivateIpAddress, PublicIpAddress, SecurityGroups[*].[GroupName, GroupId], VpcId, SubnetId, Tags]", instance_list)

    instance_cnt = 0
    eks_node_cnt = 0
    for instance in output:
        # instance = instance[0]
        # pprint(instance)
        for Name, InstanceId, InstanceType, AvailabilityZone, State, PrivateIpAddress, PublicIpAddress, SecurityGroups, VpcId, SubnetId, Tags in instance:
            if (Name == None) | (Name == []):
                Name=['-']

            is_autorecovery = False
            for autorecovery_instance in autorecovery_instances:
                if autorecovery_instance == InstanceId:
                    is_autorecovery = True
                    break
        
            instance_info = {
                "name" : Name[0],
                "instance_id": InstanceId,
                "autorecovery": is_autorecovery,
                "eks_node": True if "eks" in Name[0] else False
            }

            # print(f'>>>>>instance_info[{Name[0]}], {True if "eks" in Name[0] else False}')
            if instance_info["eks_node"] == True:
                eks_node_cnt += 1

            ec2_instances.append(instance_info)    
            
            instance_cnt += 1

    pprint(ec2_instances)
    print(f"총갯수[{instance_cnt}] - 알람설정 갯수[{autorecovery_cnt}], EKS Node 갯수[{eks_node_cnt}]\n")
    

    additional_cnt = 0
    for instance_info in ec2_instances:
        if instance_info["eks_node"] == False:
            if instance_info["autorecovery"] == False:
                print(f'[{additional_cnt:02}] {instance_info["instance_id"]}:{instance_info["name"]}')
                additional_cnt += 1
    print(f"추가알람설정 갯수[{additional_cnt}]")


    return instance_cnt, ec2_instances

    
def main( ):
    

  session = boto3_helper.init_aws_session()

  print("CloudWatch Alarms")
  start_time = time.time()
  # codeartifact = session.client('codeartifact')
  cloudwatch = session.client('cloudwatch', region_name='ap-northeast-2')
  cloudwatch_alarms_cnt, ec2_instances = report_cloudwatch_alarms_autorecover(cloudwatch, 'StatusCheckFailed_System')

  ec2 = session.client('ec2')
  report_autorecover_not_set_ec2_list(ec2, cloudwatch_alarms_cnt, ec2_instances)
  

  end_time = time.time()
  print(f"Program execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
  # region_args, profile_args = get_arguments()
  # main(region_args, profile_args)
  main( )
  now = datetime.datetime.now()

  print(now) 