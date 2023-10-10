# -*- coding: utf-8 -*-
import boto3_helper
from boto3_helper import convert_bytes_to_string

import botocore

# import boto3
import jmespath
import xlsxwriter
import argparse
from   datetime import datetime, timezone, timedelta, date
import pandas as pd
import time

import json
from pprint import pprint
import re

import warnings
warnings.filterwarnings('ignore', category=FutureWarning, module='botocore.client')

now = datetime.now()
now_time = now.strftime("%y%m%d")
excel_name = now_time + '_resource_report_' + boto3_helper.getName( ) + '.xlsx'

xlsx = xlsxwriter.Workbook(excel_name, {'remove_timezone': True})

title_format            = xlsx.add_format({'bold':True, 'font_size':13, 'align': 'left'})
coltitle_format         = xlsx.add_format({'bold':True, 'font_color':'white', 'bg_color':'#393839', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
colname_format          = xlsx.add_format({'bold':True, 'font_color':'white', 'bg_color':'#1E4E79', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
colname_left_format     = xlsx.add_format({'bold':True, 'font_color':'white', 'bg_color':'#1E4E79', 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
center_alignment_format = xlsx.add_format({'align': 'center', 'valign': 'vcenter'})
url_format              = xlsx.add_format({'align': 'left', 'valign': 'vcenter', 'underline': True, 'color': 'blue', 'font_color': 'blue'})
string_format           = xlsx.add_format({'align': 'left', 'valign': 'vcenter'})
wrap_format             = xlsx.add_format({'text_wrap': True, 'valign': 'vcenter'})
nextline_format         = xlsx.add_format({'bg_color':'#BFBFBF', 'valign': 'vcenter'})
date_format             = xlsx.add_format({'num_format': 'yyyy/mm/dd hh:mm', 'valign': 'vcenter', 'align': 'left'})
currency_format         = xlsx.add_format({'num_format': '$#,##0.00'})
number_format           = xlsx.add_format({'num_format': '#,##0.00', 'align': 'right', 'valign': 'vcenter'})
integer_format          = xlsx.add_format({'num_format': '#,##0', 'align': 'right', 'valign': 'vcenter'})



def report_basic( ):
  arch_img = boto3_helper.get_arch_img( )
  # pprint(arch_img)

  if arch_img == "":
    return 

  arch_sheet = xlsx.add_worksheet('Architect')
  arch_sheet.write(0, 1, "아키텍처", title_format)
  
  # print(boto3_helper.get_arch_img( ))

  arch_sheet.insert_image('B2', arch_img)

  # connect_sheet = xlsx.add_worksheet('접속 정보')
  # connect_sheet.write(0, 1, "접속정보", title_format)


def report_resource( ):
    global summary_sheet
    summary_sheet = xlsx.add_worksheet('자원 요약')
  

    global resource_col
    resource_col = 1

    global sub_resource_col
    sub_resource_col = 2
    
    global summary_col
    summary_col = 3

    global cost_col
    cost_col = 4

    global exchange_rate_col
    exchange_rate_col = 'G1'


    ColTitle = [ "구분", "자원명", "개수", "USD", "원화"]

    Columns_B = [
        "IAM",
        "Direct Connect",
        "VPC",
        "Resource Access Manager",
        "Security Group",
        "ELB",
        "EC2",
        "Storage",
        "Container Service",
        "DB",
        "Streams",
        "Serverless",
        "Secrity",    
        "Code Series",
        "Logging/Monitoring",
        "AWS Backup",    
        "Network Security",
        "Edge Networking"]
    Columns_B_CNT = {
        "IAM": 2,
        "Direct Connect": 1,
        "VPC": 9,
        "Resource Access Manager": 1,
        "Security Group": 1,
        "ELB": 2,
        "EC2": 1,
        "Storage": 3,
        "Container Service": 3,
        "DB" : 5,
        "Streams" : 4,
        "Serverless" : 1,
        "Secrity" : 3,
        "AWS Certificate Manager" : 1,
        "Code Series" : 5,
        "Logging/Monitoring" : 5,
        "AWS Backup" : 1,     
        "Network Security" : 3,
        "Edge Networking": 2}


    Columns_C = ["User", "Group", "Direct Connect", "VPC", "Subnets", "Routes", "Internet Gateway", "NAT Gateway", "VPN Connection", "VPC Peering", "Transit Gateway", "Attachment", "Resource Access Manager", "Security Group", "NLB", "ALB", "Instance", "EBS", "EFS", "S3", "ECR", "ECS Cluster", "EKS Cluster", "RDS Instance", "RDS Proxy", "DynamoDB Tables", "ElastiCache", "REDSHIFT", "Kafka", "Amazon Simple Queue Service", "Kinesis Firehose", "SNS Topics", "Lambda", "Secrets Manager", "AWS Certificate Manager", "AWS Key Management Service", "CodeCommit", "CodeBuild", "CodeDeploy", "CodePipeline", "CodeArtifact", "CloudWatch Metrics", "CloudWatch Logs", "CloudWatch Alarms", "CloudWatch Events", "CloudTrail", "AWS Backup", "Web Application Firewall", "Network Firewall", "Shield Protection", "Route53 Hosted Zone", "CloudFront"]

    global Columns_C_POS
    Columns_C_POS = {
        "User": 2,
        "Group": 3,
        "Direct Connect": 4,
        "VPC": 5,
        "Subnets": 6,
        "Routes": 7,
        "Internet Gateway": 8,
        "NAT Gateway": 9,
        "VPN Connection": 10,
        "VPC Peering" : 11,
        "Transit Gateway" : 12,
        "Attachment" : 13,
        "Resource Access Manager" : 14,
        "Security Group": 15,
        "NLB" : 16,
        "ALB" : 17,
        "Instance" : 18,
        "EBS" : 19,
        "EFS" : 20,
        "S3" : 21,
        "ECR" : 22,
        "ECS Cluster" : 23,
        "EKS Cluster" : 24,
        "RDS Instance" : 25,
        "RDS Proxy" : 26,
        "DynamoDB Tables" : 27,
        "ElastiCache" : 28,
        "REDSHIFT" : 29,
        "Kafka" : 30,
        "Amazon Simple Queue Service" : 31,
        "Kinesis Firehose" : 32,
        "SNS Topics" : 33, 
        "Lambda" : 34,
        "Secrets Manager" : 35,
        "AWS Certificate Manager" : 36,
        "AWS Key Management Service" : 37,
        "CodeCommit" : 38,
        "CodeBuild" : 39,
        "CodeDeploy" : 40,
        "CodePipeline" : 41,
        "CodeArtifact" : 42,
        "CloudWatch Metrics" : 43,
        "CloudWatch Logs" : 44,
        "CloudWatch Alarms" : 45,
        "CloudWatch Events" : 46,
        "CloudTrail": 47,
        "AWS Backup" : 48,
        "Web Application Firewall" : 49,
        "Network Firewall" : 51,
        "Shield Protection" : 51,
        "Route53 Hosted Zone" : 52, 
        "CloudFront" : 53}

    global Columns_C_LINK
    Columns_C_LINK = {
        "User": "IAM",
        "Group": "IAM",
        "Direct Connect": "Direct Connect",
        "VPC": "VPC",
        "Subnets": "VPC",
        "Routes": "VPC",
        "Internet Gateway": "VPC",
        "NAT Gateway": "VPC",
        "VPN Connection": "VPC",
        "VPC Peering" : "VPC",
        "Transit Gateway" : "VPC",
        "Attachment" : "VPC",
        "Resource Access Manager" : "RAM",
        "Security Group": "Security Group",
        "NLB" : "ELB",
        "ALB" : "ELB",
        "Instance" : "EC2 Instance",
        "EBS" : "EBS",
        "EFS" : "EFS",
        "S3" : "S3",
        "ECR" : "ECR",
        "ECS Cluster" : "ECS",
        "EKS Cluster" : "EKS",
        "RDS Instance" : "RDS",
        "RDS Proxy" :  "RDS Proxy",
        "DynamoDB Tables" : "DynamoDB",
        "ElastiCache" : "ElastiCache",
        "REDSHIFT" : "REDSHIFT",
        "Kafka" : "Kafka(MSK)",
        "Amazon Simple Queue Service" : "SQS",
        "Kinesis Firehose" : "Kinesis Firehose",
        "SNS Topics" : "SNS Topics",
        "Lambda" : "Lambda",
        "Secrets Manager" : "Secrets Manager",
        "AWS Certificate Manager" : "AWS Certificate Manager",
        "AWS Key Management Service" : "AWS Key Management Service",
        "CodeCommit" : "CodeCommit",
        "CodeBuild" : "CodeBuild",
        "CodeDeploy" : "CodeDeploy",
        "CodePipeline" :  "CodePipeline",
        "CodeArtifact" :  "CodeArtifact",
        "CloudWatch Metrics" : "CloudWatch Metrics",
        "CloudWatch Logs" : "CloudWatch Logs",
        "CloudWatch Alarms" : "CloudWatch Alarms",
        "CloudWatch Events" : "CloudWatch Events",
        "CloudTrail" : "CloudTrail",  
        "AWS Backup" : "AWS Backup",
        "Web Application Firewall" : "WAF",
        "Network Firewall" : "Network Firewall",
        "Shield Protection" : "Shield Protection",
        "Route53 Hosted Zone" : "Route53",
        "CloudFront" : "CloudFront"
    }


    global Columns_E_C_Mapping
    Columns_E_C_Mapping = {
        "User": "",
        "Group": "",
        "AWS Direct Connect": "Direct Connect",
        "Amazon Virtual Private Cloud": "VPC",
        "Subnets": 6,
        "Routes": 7,
        "Internet Gateway": 8,
        "NAT Gateway": 9,
        "VPN Connection": 10,
        "VPC Peering" : 11,
        "Transit Gateway" : 12,
        "Attachment" : 13,
        "AWS Resource Access Manager" : "Resource Access Manager",
        "Security Group": 14,
        "Amazon Elastic Load Balancing": "NLB",
        "ALB" : 16,
        "Amazon Elastic Compute Cloud - Compute": "Instance",
        "EC2 - Other" : "EBS",
        "Amazon Elastic File System": "EFS",
        "Amazon Simple Storage Service": "S3",
        "Amazon EC2 Container Registry (ECR)": "ECR",
        "Amazon Elastic Container Service": "ECS Cluster",
        "Amazon Elastic Container Service for Kubernetes": "EKS Cluster",
        "Amazon Relational Database Service": "RDS Instance",
        "RDS Proxy" : 25,
        "Amazon DynamoDB": "DynamoDB Tables",
        "Amazon ElastiCache": "ElastiCache",
        "REDSHIFT" : 28,
        "Amazon Managed Streaming for Apache Kafka": "Kafka",
        "Amazon Simple Queue Service": "Amazon Simple Queue Service",
        "Amazon Kinesis Firehose": "Kinesis Firehose",
        "Amazon Simple Notification Service": "SNS Topics", 
        "AWS Lambda" : "Lambda",
        "AWS Secrets Manager": "Secrets Manager",
        "AWS Certificate Manager" : "AWS Certificate Manager",
        "AWS Key Management Service" : "AWS Key Management Service",
        "AWS CodeCommit": "CodeCommit",
        "CodeBuild": "CodeBuild",
        "AWS CodeDeploy" : "CodeDeploy",
        "AWS CodePipeline" : "CodePipeline",
        "AWS CodeArtifact": "CodeArtifact",
        "AmazonCloudWatch" : "CloudWatch Metrics",
        "CloudWatch Logs" : 43,
        "CloudWatch Alarms" : 44,
        "CloudWatch Events": "CloudWatch Events",
        "AWS CloudTrail" : "CloudTrail",
        "AWS Backup" : "AWS Backup",
        "AWS WAF" : "Web Application Firewall",
        "AWS Network Firewall": "Network Firewall",
        "Shield Protection" : 50,
        "Amazon Route 53": "Route53 Hosted Zone", 
        "Amazon CloudFront" : "CloudFront"}

    summary_sheet.write(0, 1, "자원요약", title_format)

    col = 1 
    for ColName in ColTitle:
        coltitle_format.set_border(1)
        coltitle_format.set_border_color('#393839')
        summary_sheet.write(1, col, ColName, coltitle_format)
        col += 1


    col = 2 
    row = 3
    for ColName in Columns_B:
        # summery_sheet.write(row, col, ColName, colname_format)
   
        range_ = 'B' + str(row) + ':' + 'B' + str(row + Columns_B_CNT[ColName] - 1)
        # print(ColName, " - ",  range_)
        colname_format.set_border(1)
        colname_format.set_border_color('white')
        if  Columns_B_CNT[ColName] == 1:
            summary_sheet.write(row-1, col-1, ColName, colname_format)
            row += 1
        else:
            summary_sheet.merge_range(range_, ColName, colname_format)
            row += Columns_B_CNT[ColName]

    col = 2 
    row = 2
    for ColName in Columns_C:
        colname_format.set_border(1)
        colname_format.set_border_color('gray')
        summary_sheet.write(row, col, ColName, colname_format)
        # print(ColName)
        # sheetlink_pos = 'internal:' + Columns_C_LINK[ColName] + '!' + 'C' + str(row + 1)
        sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A1"
        # print(sheetlink_pos)
        summary_sheet.write_url(row, col, sheetlink_pos, url_format, string=ColName)
        # summary_sheet.write_url(row, col, sheetlink_pos)
        row += 1

    summary_sheet.set_column('B:B', 20) # 구분
    summary_sheet.set_column('C:C', 20) # 자원명
    summary_sheet.set_column('D:D', 15) # 갯수
    summary_sheet.set_column('E:E', 42) # Cost
    summary_sheet.set_column('F:F', 20) # 환율 Title
    summary_sheet.set_column('G:G', 10) # 환율 값

    summary_sheet.write(0, 5, "환율", title_format)
    exchange_rate = boto3_helper.get_forex( )
    exchange_rate_float = float(exchange_rate.replace(',', ''))
    summary_sheet.write(0, 6, exchange_rate_float, number_format)

    summary_sheet.activate( )
    summary_sheet.autofit( )


def report_instance(ec2):
    instance_list = ec2.describe_instances()
    # pprint(instance_list)

    output = jmespath.search("Reservations[*].Instances[*].[Tags[?Key=='Name'].Value, InstanceId, InstanceType, Placement.AvailabilityZone, State.Name, PrivateIpAddress, PublicIpAddress, SecurityGroups[*].[GroupName, GroupId], VpcId, SubnetId, Tags]", instance_list)

    result_sheet = xlsx.add_worksheet('EC2 instance')

    Columns = ["Name", "Instance ID", "Instance Type", "Availability Zone", "State", "Private IP", "Public IP", "VPC ID", "Subnet ID", "Security Groups", "Tags"]

    # result_sheet.write(0, 0, "EC2 Instance List", title_format)

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1

    result_sheet.set_column('A:A', 72) # Name
    result_sheet.set_column('B:B', 20) # Instance ID
    result_sheet.set_column('C:C', 15) # Instance Type
    result_sheet.set_column('D:D', 17) # Availability Zone
    result_sheet.set_column('E:E', 12) # Status
    result_sheet.set_column('F:F', 17) # Private IP
    result_sheet.set_column('G:G', 17) # Public IP
    result_sheet.set_column('H:H', 25) # VPC ID
    result_sheet.set_column('I:I', 25) # Subnet ID
    result_sheet.set_column('J:J', 135)  # Security Groups
    result_sheet.set_column('K:K', 172)  # Tags

    # pprint(output)

    row = 2
    cnt = 0
    for instance in output:
        # instance = instance[0]
        # pprint(instance)
        for Name, InstanceId, InstanceType, AvailabilityZone, State, PrivateIpAddress, PublicIpAddress, SecurityGroups, VpcId, SubnetId, Tags in instance:
            if (Name == None) | (Name == []):
                Name=['-']
            if State != 'terminated':

                result_sheet.write(row, 0, Name[0], string_format)
                result_sheet.write(row, 1, InstanceId, string_format)
                result_sheet.write(row, 2, InstanceType, string_format)
                result_sheet.write(row, 3, AvailabilityZone, string_format)
                result_sheet.write(row, 4, State, string_format)
                result_sheet.write(row, 5, PrivateIpAddress, string_format)
                result_sheet.write(row, 6, PublicIpAddress, string_format)
                result_sheet.write(row, 7, VpcId, string_format)
                result_sheet.write(row, 8, SubnetId, string_format)
                slist = []
                for sgname, sgid in SecurityGroups:
                    slist.append(sgname + " (" + sgid + ")")
                result_sheet.write(row, 9, '\n'.join(slist), wrap_format)
                
                tag_str = ""
                tag_cnt = 0
                if Tags != '[]':
                    for tag in Tags:
                        for key in tag.keys( ):
                            # print(key, ":", tag[key])
                            if key == "Key":
                                if tag_cnt == 0:
                                    tag_str = (tag[key] + "=")
                                else:              
                                    tag_str += ("\n" + tag[key] + "=")
                            elif key == "Value":
                                tag_str += tag[key]
                            tag_cnt += 1
                result_sheet.write(row, 10, tag_str, wrap_format) # "tags"
            
            
                row += 1
                cnt += 1

    print(f"-Instance [{str(len(output))}] cnt[{cnt}]")


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    # print(sheetlink_pos)
    # row, col
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

    global summary_col
    # summary_sheet.write(Columns_C_POS['Instance'], summary_col, len(output), integer_format)
    # result_sheet.write(0, 1, f"EC2 Instance List({str(len(output))})", title_format)
    summary_sheet.write(Columns_C_POS['Instance'], summary_col, cnt, integer_format)
    result_sheet.write(0, 1, f"EC2 Instance List({cnt})", title_format)
    
    # ColName = '자원 요약'
    # sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    # print(sheetlink_pos)
    # summary_sheet.write_url(row, col, sheetlink_pos, string=ColName)
    
    print("Done.\n")

def report_directconnect_connections(directconnect):
    global result_sheet
    result_sheet = xlsx.add_worksheet('Direct Connect')

    Columns = ["No.", "Connection Name", "Connection Id", "Location", "Bandwidth", "Connection State", "AWS Device", "AWS DeviceV2", "AWS LogicalDeviceId", "Encryption Mode", "Has Logical Redundancy", "Jumbo Frame Capable", "MacSec Capable", "Owner Account", "Partner Name", "Port Encryption Status", "Region", "vlan", "Tags"]

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 34)  # connectionName
    result_sheet.set_column('C:C', 16)  # connectionId
    result_sheet.set_column('D:D', 12)  # location
    result_sheet.set_column('E:E', 12)  # bandwidth
    result_sheet.set_column('F:F', 12)  # connectionState
    result_sheet.set_column('G:G', 22)  # awsDevice
    result_sheet.set_column('H:H', 22)  # awsDeviceV2
    result_sheet.set_column('I:I', 22)  # awsLogicalDeviceId
    result_sheet.set_column('J:J', 12)  # encryptionMode
    result_sheet.set_column('K:K', 7)  # hasLogicalRedundancy
    result_sheet.set_column('L:L', 7)  # jumboFrameCapable
    result_sheet.set_column('M:M', 7)  # macSecCapable
    result_sheet.set_column('N:N', 18)  # ownerAccount
    result_sheet.set_column('O:O', 32)  # partnerName
    result_sheet.set_column('P:P', 22)  # portEncryptionStatus
    result_sheet.set_column('Q:Q', 12)  # region
    result_sheet.set_column('R:R', 12)  # vlan
    result_sheet.set_column('S:S', 32)  # tags
    
    
    # Direct Connect 연결 목록 가져오기
    response = directconnect.describe_connections()
    connections = response['connections']

    row = 2
    for connection in connections:
        # print(f"- Connection ID: {connection['connectionId']}")
        # print(f"  Location: {connection['location']}")
        # print(f"  Bandwidth: {connection['bandwidth']} Mbps")
        # print(f"  Connection State: {connection['connectionState']}")
        # print("-" * 50)
        row = write_directconnect_to_excel(row, connection, result_sheet)


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, string=ColName)


    result_sheet.write(0, 1, f"Direct Connect Connections List({str(row - 2)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['Direct Connect'], summary_col, row - 2, integer_format)
    print(f'-Direct Connect Connections List({str(row - 2)})')
    print("Done.\n")

def write_directconnect_to_excel(row, connection, result_sheet):
    result_sheet.write(row, 0, row - 1, integer_format)
    result_sheet.write(row, 1, connection['connectionName'], wrap_format)
    result_sheet.write(row, 2, connection['connectionId'], date_format)
    result_sheet.write(row, 3, connection['location'], date_format)
    result_sheet.write(row, 4, connection['bandwidth'], string_format)
    
    result_sheet.write(row, 5, connection['connectionState'], string_format)
    
    result_sheet.write(row, 6, connection['awsDevice'], string_format)
    result_sheet.write(row, 7, json.dumps(connection['awsDeviceV2'],indent=2), wrap_format)
    result_sheet.write(row, 8, json.dumps(connection['awsLogicalDeviceId'],indent=2), wrap_format)
    result_sheet.write(row, 9, connection['encryptionMode'], string_format)
    result_sheet.write(row, 10, connection['hasLogicalRedundancy'], string_format)
    result_sheet.write(row, 11, connection['jumboFrameCapable'], string_format)
    result_sheet.write(row, 12, connection['macSecCapable'], string_format)
    result_sheet.write(row, 13, connection['ownerAccount'], string_format)
    result_sheet.write(row, 14, connection['partnerName'], string_format)
    result_sheet.write(row, 15, connection['portEncryptionStatus'], string_format)
    result_sheet.write(row, 16, connection['region'], string_format)
    result_sheet.write(row, 17, connection['vlan'], string_format)
    result_sheet.write(row, 18, ', '.join(connection['tags']) if connection['tags'] else '-', string_format)
  
    
    row += 1

    return row

def report_vpc(ec2):
  vpc_list = ec2.describe_vpcs()

  vpc_output = jmespath.search("Vpcs[*].[Tags[?Key=='Name'].Value, VpcId, CidrBlock, DhcpOptionsId]", vpc_list)
  result_sheet = xlsx.add_worksheet('VPC')

  Columns = ["Name", "VPC ID", "CIDR", "DHCP options set"]
  # result_sheet.write(0, 0, "VPC List", title_format)

  col = 0
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 46) # NAME
  result_sheet.set_column('B:B', 25) # VPC ID, SUBNET ID
  result_sheet.set_column('C:C', 25) # CIDR, STATE, Subnet Associations
  result_sheet.set_column('D:D', 25) # DHCP, VPC ID
  result_sheet.set_column('E:E', 25) # CIDR
  result_sheet.set_column('F:F', 25) # Available IPv4 Address, Target
  result_sheet.set_column('G:G', 20) # Availability Zone
  result_sheet.set_column('H:H', 25) # Availability Zone ID
  result_sheet.set_column('I:I', 15) # Requester Region

  row = 2
  for Name, VpcId, Cidr, DhcpOptions in vpc_output:
    if Name == None:
      Name = ['-']
    result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 1, VpcId, string_format)
    result_sheet.write(row, 2, Cidr, string_format)
    result_sheet.write(row, 3, DhcpOptions, string_format)
    row += 1 

  print("-Vpc ["+str(len(vpc_output))+"]")


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  summary_sheet.write(Columns_C_POS['VPC'], summary_col, len(vpc_output), integer_format)
  result_sheet.write(0, 1, "VPC List("+str(len(vpc_output))+")", title_format)

  ##########################VPC#############################

  subnet_list = ec2.describe_subnets()
  subnet_output = jmespath.search("Subnets[*].[Tags[?Key=='Name'].Value, SubnetId, State, VpcId, CidrBlock, AvailableIpAddressCount, AvailabilityZone, AvailabilityZoneId]", subnet_list)

  row += 1

  Columns = ["Name", "Subnet ID", "State", "VPC ID", "CIDR", "Available IPv4 Addresses", "Availability Zone", "Availability Zone ID"]
  # result_sheet.write(row, 0, "Subnet List", title_format)
  subnet_title_row = row
  row += 1

  col = 0
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1
  row += 1

  # pprint(subnet_output)

  #print(subnet_output)
  for Name, SubnetId, State, VpcId, Cidr, AvailableIpAddressCount, AvailabilityZone, AvailabilityZoneId in subnet_output:
    if Name in [None, []]:
      Name = ['-']
    result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 1, SubnetId, string_format)
    result_sheet.write(row, 2, State, string_format)
    result_sheet.write(row, 3, VpcId, string_format)
    result_sheet.write(row, 4, Cidr, string_format)
    result_sheet.write(row, 5, AvailableIpAddressCount, string_format)
    result_sheet.write(row, 6, AvailabilityZone, string_format)
    result_sheet.write(row, 7, AvailabilityZoneId, string_format)
    row += 1

  print("-Subnets ["+str(len(subnet_output))+"]")


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(subnet_title_row, 0, sheetlink_pos, url_format, string=ColName)

  # 결과 값
  ColName = 'Subnets'
  result_sheet.write(subnet_title_row, 1, "Subnet List("+str(len(subnet_output))+")", title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(subnet_output), integer_format)

  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(subnet_title_row + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)

  ##########################SUBNET#############################

  rt_list = ec2.describe_route_tables()
  rt_output = jmespath.search("RouteTables[*].[Tags[?Key=='Name'].Value, RouteTableId, Associations[*].SubnetId, VpcId, Routes[*].[DestinationCidrBlock, [EgressOnlyInternetGatewayId, GatewayId, NatGatewayId, InstanceOwnerId, InstanceId, TransitGatewayId, LocalGatewayId, CarrierGatewayId, NetworkInterfaceId, VpcPeeringConnectionId], State]]", rt_list)
  
  row += 1 
  Columns = ["Name", "Route Table ID", "Subnet Associations", "VPC", "Destination", "Target", "Status"]
  # result_sheet.write(row, 0, "Route Table List", title_format)
  route_table_list_title_row = row
  row += 1
  
  col = 0
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1
  row += 1

  # print(rt_output)
  for Name, RouteTableId, Subnets, VpcId, Routes in rt_output:
    if Name == []:
      Name = ['-']
    result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 1, RouteTableId, string_format)
    result_sheet.write(row, 2, '\n'.join(Subnets), wrap_format)
    result_sheet.write(row, 3, VpcId, string_format)
    rCnt = row
    for destCidr, tgtId, State in Routes:
      cleanTgtId = list(filter(lambda x: x is not None, tgtId))
      result_sheet.write(rCnt, 4, destCidr, string_format)
      result_sheet.write(rCnt, 5, cleanTgtId[0], string_format)
      result_sheet.write(rCnt, 6, State, string_format)
      rCnt += 1
    row = rCnt 

  print("-Routes ["+str(len(rt_output))+"]")

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(route_table_list_title_row, 0, sheetlink_pos, url_format, string=ColName)

  # 결과 값
  ColName = 'Routes'
  result_sheet.write(route_table_list_title_row, 1, "Route Table List("+str(len(rt_output))+")", title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(rt_output), integer_format)

  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(route_table_list_title_row + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)

#########################ROUTE TABLE#############################

  igw_list = ec2.describe_internet_gateways()
  igw_output = jmespath.search("InternetGateways[*].[Tags[?Key=='Name'].Value, InternetGatewayId, Attachments[*].VpcId]", igw_list)

  row += 1
  Columns = ["Name", "igw-id", "Attached VPC"]
  # result_sheet.write(row, 0, "IGW List", title_format)
  igw_list_title_row = row
  row += 1

  col = 0 
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1
  row += 1

  #print(igw_output)
  for Name, igwid, VpcId in igw_output:
    if Name==[]:
      Name = ['-']
    result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 1, igwid, string_format)
    result_sheet.write(row, 2, '\n'.join(VpcId), wrap_format)
    row += 1

  print("-Internet Gateway ["+str(len(igw_output))+"]")

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(igw_list_title_row, 0, sheetlink_pos, string=ColName)

  # 결과 작성
  ColName = 'Internet Gateway'
  result_sheet.write(igw_list_title_row, 1, "IGW List("+str(len(igw_output))+")", title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(igw_output), integer_format)

  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(igw_list_title_row + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)
###############################IGW######################

  nat_list = ec2.describe_nat_gateways()
  nat_output = jmespath.search("NatGateways[*].[Tags[?Key=='Name'].Value, NatGatewayId, NatGatewayAddresses[*].[PublicIp, PrivateIp], VpcId, SubnetId]", nat_list)

  row += 1 
  Columns = ["Name", "NAT GW ID", "Public IP", "Private IP", "VPC ID", "Subnet ID"]
  # result_sheet.write(row, 0, "NAT Gateway List",  title_format)
  nat_gateway_list_row = row
  row += 1 

  col = 0 
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1
  row += 1

  for Name, natid, ip, VpcId, subnet in nat_output:
    if Name==[]:
      Name = ['-']
    result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 1, natid, string_format)
    result_sheet.write(row, 2, ip[0][0], string_format)
    result_sheet.write(row, 3, ip[0][1], string_format)
    result_sheet.write(row, 4, VpcId, string_format)
    result_sheet.write(row, 5, subnet, string_format)		
    row += 1

  print("-NAT Gateway ["+str(len(nat_output))+"]")

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(nat_gateway_list_row, 0, sheetlink_pos, url_format, string=ColName)

  # 결과 작성
  ColName = 'NAT Gateway'
  result_sheet.write(nat_gateway_list_row, 1, "NAT Gateway List("+str(len(nat_output))+")",  title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(nat_output), integer_format)


  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(nat_gateway_list_row + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)
#############################NAT########################

  vpn_list = ec2.describe_vpn_connections()
  vpn_output = jmespath.search("VpnConnections[*].[Tags[?Key=='Name'].Value, VpnConnectionId, State, VpnGatewayId, CustomerGatewayId]", vpn_list)

  row += 1

  Columns = ["Name", "VPN ID", "State", "Virtual Private Gateway", "Customer Gateway"]
  # result_sheet.write(row, 0, "VPN List", title_format)
  vpn_list_title_row = row
  row += 1

  col = 0
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1
  row += 1	

  # print(vpn_output)
  # Name = []
  for Name, VpnId, State, VGW, CGW in vpn_output:
    print(Name, len(Name))
    
    # if Name == None:
    #   Name = ['-', '.']
    # elif not Name:
    #   Name = ['-', '.']
    # elif len(Name) == 0:
    #   Name = ['-', '.']
    # print(Name, len(Name), Name[0])
    # result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 0, Name[0] if Name else '-', string_format)
    result_sheet.write(row, 1, VpnId, string_format)
    result_sheet.write(row, 2, State, string_format)
    result_sheet.write(row, 3, VGW, string_format)
    result_sheet.write(row, 4, CGW, string_format)
    row += 1

  print("-VPN Connection ["+str(len(vpn_output))+"]")

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(vpn_list_title_row, 0, sheetlink_pos, url_format, string=ColName)

  # 결과 값
  ColName = 'VPN Connection'
  result_sheet.write(vpn_list_title_row, 1, "VPN List("+str(len(vpn_output))+")", title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(vpn_output), integer_format)

  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(vpn_list_title_row + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)
  ##########################VPN#############################

  vpcpeering_list = ec2.describe_vpc_peering_connections()
  vpcpeering_output = jmespath.search("VpcPeeringConnections[*].[Tags[?Key=='Name'].Value, VpcPeeringConnectionId, Status.Message, AccepterVpcInfo.CidrBlock, AccepterVpcInfo.VpcId, AccepterVpcInfo.Region, RequesterVpcInfo.CidrBlock, RequesterVpcInfo.VpcId, RequesterVpcInfo.Region]", vpcpeering_list)

  row += 1

  Columns = ["Name", "Peering ID", "State", "Accepter CIDR", "Accepter VPC", "Accepter Region", "Requester CIDR", "Requester VPC", "Requester Region"]
  # result_sheet.write(row, 0, "VPC Peering List", title_format)
  vpc_peering_list_title_row = row
  row += 1

  col = 0
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1
  row += 1	

  #print(vpcpeering_output)
  for Name, PeeringId, State, AcpCIDR, AcpVPC, AcpRegion, ReqCIDR, ReqVPC, ReqRegion in vpcpeering_output:
    if Name == None:
      Name = ['-']
    # result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 0, Name[0] if Name else '-', string_format)
    result_sheet.write(row, 1, PeeringId, string_format)
    result_sheet.write(row, 2, State, string_format)
    result_sheet.write(row, 3, AcpCIDR, string_format)
    result_sheet.write(row, 4, AcpVPC, string_format)
    result_sheet.write(row, 5, AcpRegion, string_format)
    result_sheet.write(row, 6, ReqCIDR, string_format)
    result_sheet.write(row, 7, ReqVPC, string_format)
    result_sheet.write(row, 8, ReqRegion, string_format)
    row += 1

  print("-VPC Peering ["+str(len(vpcpeering_output))+"]")

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(vpc_peering_list_title_row, 0, sheetlink_pos, url_format, string=ColName)

  # 결과 값
  ColName = 'VPC Peering'
  result_sheet.write(vpc_peering_list_title_row, 1, "VPC Peering List("+str(len(vpcpeering_output))+")", title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(vpcpeering_output), integer_format)


  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(vpc_peering_list_title_row + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)
  #######################Peering##########################

  ## Transit Gateway 1 개로 가정 # 
  tgw_list = ec2.describe_transit_gateways()
  tgw_output = jmespath.search("TransitGateways[*].[Tags[?Key=='Name'].Value, TransitGatewayId, OwnerId, Description]", tgw_list)

  row += 1
  
  Columns = ["Name", "TGW ID", "Owner ID", "Description"]
  # result_sheet.write(row, 0, "Transit Gateway - Gateway List", title_format)
  transit_gateway_list_title_row = row
  row += 1

  col = 0
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1
  row += 1

  for Name, tgwId, OwnId, tgwDesc in tgw_output:
    #print(Name, type(Name))
    if Name==[]:
      Name = ['-']
    result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 1, tgwId, string_format)
    result_sheet.write(row, 2, OwnId, string_format)
    result_sheet.write(row, 3, tgwDesc, string_format)
    row += 1

  row += 1
  # result_sheet.write(row, 0, "Transit Gateway - Attachment List", title_format)
  transit_gateway_attachment_list_title_row = row
  

  tgw_att_list = ec2.describe_transit_gateway_attachments()
  tgw_att_output = jmespath.search("TransitGatewayAttachments[*].[Tags[?Key=='Name'].Value, TransitGatewayAttachmentId, ResourceType, ResourceId]",tgw_att_list)

  row+=1 
  Columns = ["Name", "Attachment Id", "ResourceType", "ResourceId"]
  col = 0
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1
  row += 1

  for Name, attId, resType, resId in tgw_att_output:
    if Name == []:
      Name = ['-']
    result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 1, attId, string_format)
    result_sheet.write(row, 2, resType, string_format)
    result_sheet.write(row, 3, resId, string_format)
    row += 1



  print("-Trangsit Gateway ["+str(len(tgw_output))+"], Attachment ["+str(len(tgw_att_output))+"]")

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(transit_gateway_list_title_row, 0, sheetlink_pos, url_format, string=ColName)

  # 결과 값 1 - Transit Gateway
  ColName = 'Transit Gateway'
  result_sheet.write(transit_gateway_list_title_row, 1, "Transit Gateway - Gateway List(" + str(len(tgw_output)) + ")", title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(tgw_output), integer_format)

  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(transit_gateway_list_title_row + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)

  # 결과 값 2 - Attachment

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(transit_gateway_attachment_list_title_row, 0, sheetlink_pos, url_format, string=ColName)


  ColName = 'Attachment'
  result_sheet.write(transit_gateway_attachment_list_title_row, 1, "Transit Gateway - Attachment List(" + str(len(tgw_att_output)) + ")", title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(tgw_att_output), integer_format)


  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(transit_gateway_attachment_list_title_row + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)

  print("Done.\n")	


def report_resource_shares(ram):
    global result_sheet
    result_sheet = xlsx.add_worksheet('RAM')

    Columns = ["No.", "name", "Owning Account Id", "Allow External Principals", "status", "Creation Time", "LastUpdated Time", "tags", "Resource Share Arn"]

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 34)  # name
    result_sheet.set_column('C:C', 16)  # owningAccountId
    result_sheet.set_column('D:D', 12)  # allowExternalPrincipals
    result_sheet.set_column('E:E', 7)   # status
    result_sheet.set_column('F:F', 16)  # creationTime
    result_sheet.set_column('G:G', 16)  # lastUpdatedTime
    result_sheet.set_column('H:H', 37)  # tags
    result_sheet.set_column('I:I', 72)  # resourceShareArn

    # Direct Connect 연결 목록 가져오기
    response = ram.get_resource_shares(resourceOwner='SELF')  # resourceOwner를 명시해야 합니다.

    row = 2
    for share in response['resourceShares']:
        # print("리소스 공유 이름:", share['name'])
        # print("리소스 공유 ARN:", share['resourceShareArn'])
        # print("상태:", share['status'])
        row = write_resource_shares(row, share, result_sheet)

        try:
            if 'principals' in share:  # principals 필드가 있는 경우에만 출력
                # print("공유 대상:")
                principals = share['principals']
                for principal in principals:
                    print("  - ID:", principal['id'])
                    print("    유형:", principal['type'])
                    # row = write_resource_shares(row, principal, result_sheet)
                    # if 'principals' in share:  # principals 필드가 있는 경우에만 출력
                    #      for principal in share['principals']:
                    #          row = write_resource_shares(row, principal, result_sheet)
        except KeyError:
            print("공유 대상 정보 없음")
        print("-" * 50)



    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"Resource Access Manager (RAM) List({str(row - 2)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['Resource Access Manager'], summary_col, row - 2, integer_format)
    print(f'-Resource Access Manager (RAM) List({str(row - 2)})')
    print("Done.\n")

def write_resource_shares(row, share, result_sheet):
    # pprint(share)
    result_sheet.write(row, 0, row - 1, integer_format)
    result_sheet.write(row, 1, share['name'], string_format)
    result_sheet.write(row, 2, share['owningAccountId'], string_format)
    result_sheet.write(row, 3, share['allowExternalPrincipals'], string_format)
    result_sheet.write(row, 4, share['status'], string_format)
    
    result_sheet.write(row, 5, share['creationTime'], date_format)    
    result_sheet.write(row, 6, share['lastUpdatedTime'], date_format)
    # result_sheet.write(row, 7, '\n'.join(json.dumps(share['tags'],indent=2)) if 'tags' in share else '-', wrap_format)   
    result_sheet.write(row, 7, json.dumps(share['tags'],indent=2) if 'tags' in share else '-', wrap_format)   
        
    result_sheet.write(row, 8, share['resourceShareArn'], string_format)
  
    
    row += 1

    return row


def report_sg(ec2):
  sg_list = ec2.describe_security_groups()
  sg_output = jmespath.search("SecurityGroups[*].[Tags[?Key=='Name'].Value, GroupName, GroupId, Description, VpcId, IpPermissions[*].[FromPort, ToPort, IpProtocol, IpRanges[*].{range:CidrIp, desc:Description}, UserIdGroupPairs[*].{range:GroupId, desc:Description}], IpPermissionsEgress[*].[FromPort, ToPort, IpProtocol, IpRanges[*].{range:CidrIp, desc:Description}, UserIdGroupPairs[*].{range:GroupId, desc:Description}]]", sg_list)
  result_sheet = xlsx.add_worksheet("Security Group")

  Columns = ["Name", "Group ID", "Group Name", "VPC ID", "Description", "In/Out", "Type", "Protocol", "Port Range", "Source/Destination", "Description"]

  # result_sheet.write(0,0,"Security Group List", title_format)

  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 50) # NAME
  result_sheet.set_column('B:B', 25) # Group Id
  result_sheet.set_column('C:C', 52) # Group Name
  result_sheet.set_column('D:D', 25) # VPC ID
  result_sheet.set_column('E:E', 52) # Description
  result_sheet.set_column('F:F', 7) # In/Out
  result_sheet.set_column('G:G', 7) # Type
  result_sheet.set_column('H:H', 10) # Protocol
  result_sheet.set_column('I:I', 10) # Port Range
  result_sheet.set_column('J:J', 20) # Source/Destination
  result_sheet.set_column('K:K', 80) # Descrition


  row = 2
  for Name, GName, Id, Description, VpcId, inbound, outbound in sg_output:
    if (Name == None) | (Name == []):
      Name = ['-']
    #print(Name)
    result_sheet.write(row, 0, Name[0], string_format)
    result_sheet.write(row, 1, Id, string_format)
    result_sheet.write(row, 2, GName, string_format)
    result_sheet.write(row, 3, VpcId, string_format)
    result_sheet.write(row, 4, Description, string_format)
    inCnt = row
    for inFromPort, inToPort, inProtocol, inCidr, inSg in inbound:
      inIpRange = inCidr + inSg
      if inFromPort==inToPort:
        inPort = inFromPort
      else:
        inPort = str(inFromPort)+"-"+str(inToPort)
      if (inPort == None) | (inPort == -1):
        inPort = '-'			
      for inRg in inIpRange:
        result_sheet.write(inCnt, 5, "IN", string_format)
        result_sheet.write(inCnt, 8, inPort, string_format)
        if inProtocol=='-1':
          inProtocol='-'
        result_sheet.write(inCnt, 7, inProtocol, string_format)
        result_sheet.write(inCnt, 9, inRg['range'], string_format)
        result_sheet.write(inCnt, 10, inRg['desc'], string_format)
        inCnt += 1
    outCnt = inCnt	
    for outFromPort, outToPort, outProtocol, outCidr, outSg in outbound:
      outIpRange = outCidr + outSg
      if outFromPort==outToPort:
        outPort = outFromPort
      else:
        outPort = str(outFromPort)+"-"+str(outToPort)			
      if (outPort == None) | (outPort == -1):
        outPort = '-'
      for outRg in outIpRange:
        result_sheet.write(outCnt, 5, "OUT", string_format)
        result_sheet.write(outCnt, 8, outPort, string_format)
        if outProtocol=='-1':
          outProtocol='-'
        result_sheet.write(outCnt, 7, outProtocol, string_format)
        result_sheet.write(outCnt, 9, outRg['range'], string_format)
        result_sheet.write(outCnt, 10, outRg['desc'], string_format)
        outCnt += 1

    row = outCnt


  print("-Security group ["+str(len(sg_output))+"]")


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  summary_sheet.write(Columns_C_POS['Security Group'], summary_col, len(sg_output), integer_format)
  result_sheet.write(0, 1, "Security Group List("+str(len(sg_output))+")", title_format)
  print("Done.\n")

def report_rds(rds):
  rds_instance_list = rds.describe_db_instances()
  instance_output = jmespath.search("DBInstances[*].[DBInstanceIdentifier, Engine, EngineVersion, DBInstanceClass, DBInstanceStatus, Endpoint.Address, Endpoint.Port, AvailabilityZone, DBSubnetGroup.Subnets[*].SubnetIdentifier, MultiAZ, StorageType, VpcSecurityGroups[*].VpcSecurityGroupId, DBParameterGroups[*].DBParameterGroupName]",rds_instance_list)

  result_sheet = xlsx.add_worksheet('RDS')

  Columns = ["Name", "Engine", "Type", "State", "Storage Type", "Endpoint", "Port", "Availability Zone", "Multi AZ", "Subnets", "Security Groups", "Parameter Group"]

  result_sheet.write(0, 0, "RDS DB Instance List", title_format)

  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 42) # NAME
  result_sheet.set_column('B:B', 32) # Egine
  result_sheet.set_column('C:C', 12) # Type
  result_sheet.set_column('D:D', 12) # State
  result_sheet.set_column('E:E', 12) # Storage Type
  result_sheet.set_column('F:F', 82) # Endpoint
  result_sheet.set_column('G:G', 7)  # Port
  result_sheet.set_column('H:H', 17) # Availability Zone
  result_sheet.set_column('I:I', 10) # Multi AZ
  result_sheet.set_column('J:J', 30) # Subnets
  result_sheet.set_column('K:K', 22) # Security Groups
  result_sheet.set_column('L:L', 32) # Parameter Group

  row = 2
  for DBName, Engine, EngineVersion, Type, Status, Endpoint, Port, AvailabilityZone, Subnets, MultiAZ, StorageType, SecurityGroupId, ParameterGroup in instance_output:    	
    result_sheet.write(row, 0, DBName, string_format)
    result_sheet.write(row, 1, Engine+" ("+EngineVersion+")", string_format)
    result_sheet.write(row, 2, Type, string_format)
    result_sheet.write(row, 3, Status, string_format)
    result_sheet.write(row, 4, StorageType, string_format)
    result_sheet.write(row, 5, Endpoint, string_format)
    result_sheet.write(row, 6, Port, integer_format)
    result_sheet.write(row, 7, AvailabilityZone, string_format)
    result_sheet.write(row, 8, MultiAZ, string_format)
    result_sheet.write(row, 9, '\n'.join(Subnets), wrap_format)
    result_sheet.write(row, 10, '\n'.join(SecurityGroupId), wrap_format)
    result_sheet.write(row, 11, '\n'.join(ParameterGroup), wrap_format)
    row += 1

  print("-Instance ["+str(len(instance_output))+"]")


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  summary_sheet.write(Columns_C_POS['RDS Instance'], summary_col, len(instance_output), integer_format)
  result_sheet.write(0, 1, "RDS DB Instance List(" + str(len(instance_output)) + ")", title_format)
  print("Done.\n")


def report_rds_db_proxy(rds):
  rds_db_proxy_list = rds.describe_db_proxies()
  # pprint(rds_db_proxy_list)

  dbproxies_output = jmespath.search("DBProxies[*].[Auth, CreatedDate, DBProxyArn, DBProxyName, DebugLogging, Endpoint, EngineFamily, IdleClientTimeout, RequireTLS, RoleArn, Status, UpdatedDate, VpcId, VpcSecurityGroupIds, VpcSubnetIds]", rds_db_proxy_list)

  global result_sheet
  result_sheet = xlsx.add_worksheet('RDS Proxy')

  Columns = ["DBProxy Name", "Engine Family", "Status", "Idle Client Timeout", "Debug Logging", "Endpoint", "Require TLS", "Role Arn", "Created Date", "Update dDate", "Vpc Id", "Vpc Security Groups Ids", "Vpc Subnet Ids", "DBProxy Arn", "Auth"]

  result_sheet.write(0, 0, "RDS DB Proxy List", title_format)

  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 32) # DBProxy Name
  result_sheet.set_column('B:B', 12) # Engine Family
  result_sheet.set_column('C:C', 7)  # Status
  result_sheet.set_column('D:D', 9) # Idle Client Timeout
  result_sheet.set_column('E:E', 12) # Debug Logging
  result_sheet.set_column('F:F', 72) # Endpoint
  result_sheet.set_column('G:G', 7)  # Require TLS
  result_sheet.set_column('H:H', 52) # Role Arn
  result_sheet.set_column('I:I', 17) # Created Date
  result_sheet.set_column('J:J', 17) # Update dDate
  result_sheet.set_column('K:K', 25) # Vpc Id
  result_sheet.set_column('L:L', 25) # Vpc Security Groups Ids
  result_sheet.set_column('M:M', 25) # Vpc Subnet Ids
  result_sheet.set_column('N:N', 102) # DBProxy Arn
  result_sheet.set_column('O:O', 172) # Auth

  row = 2
  auth_cnt = 0
  for auth, createdDate, dbProxyArn, dbProxyName, debugLogging, endpoint, engineFamily, idleClientTimeout, requireTLS, roleArn, status, updatedDate, vpcId, vpcSecurityGroupIds, vpcSubnetIds in dbproxies_output:    	
    result_sheet.write(row, 0, dbProxyName, string_format)
    result_sheet.write(row, 1, engineFamily, string_format)
    result_sheet.write(row, 2, status, string_format)
    result_sheet.write(row, 3, idleClientTimeout, integer_format)
    result_sheet.write(row, 4, debugLogging, string_format)
    result_sheet.write(row, 5, endpoint, string_format)
    result_sheet.write(row, 6, requireTLS, string_format)
    result_sheet.write(row, 7, roleArn, string_format)
    result_sheet.write(row, 8, createdDate, date_format)
    result_sheet.write(row, 9, updatedDate, date_format)
    result_sheet.write(row, 10, vpcId, string_format)
    result_sheet.write(row, 11, '\n'.join(vpcSecurityGroupIds), wrap_format)
    result_sheet.write(row, 12, '\n'.join(vpcSubnetIds), wrap_format)
    result_sheet.write(row, 13, dbProxyArn, string_format)
    auth_col_name = "Auth("
    auth_str = ""
    auth_cnt_ = 0
    for auth_ in auth:
      for key, value in auth_.items( ):
        # print(key, ":", value)
        auth_str += key + '=' + value + ','
      if auth_cnt_ == 0:
        auth_col_name += ",".join(auth_.keys( ))
      auth_cnt += 1
      auth_cnt_ += 1
      if auth_cnt_ < len(auth):
        auth_str += '\n'
    auth_col_name += ")"
    result_sheet.write(1, 14, auth_col_name, colname_format)
    result_sheet.write(row, 14, auth_str,  wrap_format)

    row += 1

  # print("auth_cnt[" + str(auth_cnt) + "]")

  print("-Instance ["+str(len(dbproxies_output))+"] , Auth(" + str(auth_cnt) + ")")


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


  result_sheet.write(0, 1, "RDS Proxy List(" + str(len(dbproxies_output)) + "), Auth(" + str(auth_cnt) + ")", title_format)
  global summary_col
  summary_sheet.write(Columns_C_POS['RDS Proxy'], summary_col, len(dbproxies_output), integer_format)
  print("Done.\n")

def report_s3(s3client, s3):
  is_report_object = False
  if boto3_helper.get_s3_object( ) == "True":
    is_report_object = True

  Columns = ["Name", "Region", "Creation Time", "Object Count", "Size(KB)", "Size(GB)"]

  result_sheet = xlsx.add_worksheet('S3')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "S3 Bucket List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1
  bucket_list = s3client.list_buckets()
  # pprint(bucket_list)

  result_sheet.set_column('A:A', 42) # Name
  result_sheet.set_column('B:B', 16) # Region
  result_sheet.set_column('C:C', 17) # Creation Time
  result_sheet.set_column('D:D', 10) # Object Count
  result_sheet.set_column('E:E', 20) # Size(KB)
  result_sheet.set_column('F:F', 10) # Size(GB)


  row = 2
  bucket_cnt = 0
  for bucket_name, create_date in jmespath.search("Buckets[*].[Name, CreationDate]", bucket_list):
    # print(bucket_name, create_date)
    region_info = s3client.get_bucket_location(Bucket=bucket_name)
    region = jmespath.search("LocationConstraint", region_info)

    # pprint(region_info)
    size_byte    = 0
    obj_cnt      = 0
    totalsize_gb = 0
    if is_report_object == True:
      my_bucket = s3.Bucket(bucket_name)
      for my_bucket_object in my_bucket.objects.all( ):
        # print(my_bucket_object.key)
        size_byte = size_byte+my_bucket_object.size
        obj_cnt += 1
      totalsize_gb=size_byte/1000./1024./1024.
    # print("\tObject Count[{2}] Size(Bytes[{3}], GB[{4})]".format(bucket_name, create_date, obj_cnt, size_byte, totalsize_gb)) 
    # print('---')
    result_sheet.write(row, 0, bucket_name, string_format)
    result_sheet.write(row, 1, region, string_format)
    result_sheet.write(row, 2, create_date, date_format)
    if is_report_object == True:
      result_sheet.write(row, 3, obj_cnt, integer_format)
      result_sheet.write(row, 4, size_byte, integer_format)
      result_sheet.write(row, 5, totalsize_gb, number_format)
    row += 1
    bucket_cnt += 1

  print("-S3 Bucket [" + str(bucket_cnt) + "]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


  # print("-Bucket ["+str(len(bucket_info))+"]")
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['S3'], summary_col, bucket_cnt, integer_format)
  result_sheet.write(0, 1, "S3 Bucket List(" + str(bucket_cnt) + ")", title_format)
  print("Done.\n") 


def report_ebs(ec2client, ec2):
    Columns = ["Volume Id", "Volume Type", "Size(GiB)", "IOPS", "State", "Create Time", "Attachment Time", "Attachment Device", "Attachment Instance Id", "Attachment State", "Attachment Delete On Termination", "AvailabilityZone", "Snapshot Id", "Encrypted", "KMS Key Id"]

    result_sheet = xlsx.add_worksheet('EBS')
    # result_sheet.set_column('A:Z', cell_format=wrap_format)

    # result_sheet.write(0, 0, "EBS List", title_format)
    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 25) # Volume ID
    result_sheet.set_column('B:B', 7)  # Volume Type
    result_sheet.set_column('C:C', 10) # Size(GiB)
    result_sheet.set_column('D:D', 10) # IOPS
    result_sheet.set_column('E:E', 10) # Status
    result_sheet.set_column('F:F', 17) # Create Time
    result_sheet.set_column('G:G', 17) # Attachment Times
    result_sheet.set_column('H:H', 12) # Attachment Devices
    result_sheet.set_column('I:I', 20) # Attachment Instance ID
    result_sheet.set_column('J:J', 12) # Attachment State
    result_sheet.set_column('K:K', 12) # Attachment Delete On Termination
    result_sheet.set_column('L:L', 17) # AvailabilityZone
    result_sheet.set_column('M:M', 25) # Snapshot Id
    result_sheet.set_column('N:N', 10) # Encrypted
    result_sheet.set_column('O:O', 77) # KMS Key Id

    volumes = ec2.volumes.all() # If you want to list out all volumes
    # pprint(volumes)
    # volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['in-use']}]) # if you want to list out only attached volumes
    cnt = 0
    row = 2
    for volume in volumes:
        # pprint(volume.id)
        # pprint(volume)
        # print(f'Volume {volume.id} ({volume.size} GiB) -> {volume.state}')
        describe_response = ec2client.describe_volumes(VolumeIds=[ volume.id ])
        describe_output = jmespath.search("Volumes[*].[Attachments[?Attachments.VolumeId==volume.id].AttachTime, Attachments[?Attachments.VolumeId==volume.id].Device, Attachments[?Attachments.VolumeId==volume.id].InstanceId, Attachments[?Attachments.VolumeId==volume.id].State, Attachments[?Attachments.VolumeId==volume.id].DeleteOnTermination, AvailabilityZone, CreateTime, Encrypted, KmsKeyId, Size, SnapshotId, State, VolumeId, VolumeType, Iops]", describe_response)

        # print(json.dumps(
        #   describe_response,
        #   indent=2,
        #   default=boto3_helper.json_datetime_serializer))    

        for attachTime, attachDevice, attachInstanceId, attachState, attachDeleteOnTermination, availabilityZone, createTime, encrypted, kmsKeyId, size, snapshotId, state, volumeId, volumeType, iops in describe_output:

        # if attachTime != []:
        #   print(attachTime[0], attachDevice[0], attachInstanceId[0], attachState[0], attachDeleteOnTermination[0], availabilityZoneDeleteOnTermination, encrypted, kmsKeyId, size, snapshotId, state, volumeId, volumeType, iops )
        # else:
        #   print(availabilityZoneDeleteOnTermination, encrypted, kmsKeyId, size, snapshotId, state, volumeId, volumeType, iops )

            result_sheet.write(row, 0, volumeId, string_format) # "Volume Id"
            result_sheet.write(row, 1, volumeType, string_format) # "Volume Type"
            result_sheet.write(row, 2, size, integer_format) # "size(GiB)"
            result_sheet.write(row, 3, iops, integer_format) # "iops"
            result_sheet.write(row, 4, state, string_format) # "State"
            result_sheet.write(row, 5, createTime, date_format) # "CreateTime"

            if attachTime != []:
                result_sheet.write(row, 6, attachTime[0], date_format) # "Attachment Time"
                result_sheet.write(row, 7, attachDevice[0], string_format) # "Attachment Device"
                result_sheet.write(row, 8, attachInstanceId[0], string_format) # "Attachment Instance Id"
                result_sheet.write(row, 9, attachState[0], string_format) # "Attachment State"
                result_sheet.write(row, 10, attachDeleteOnTermination[0], string_format) # "Attachment Delete On Termination"
            result_sheet.write(row, 11, availabilityZone, string_format) # "Availability Zone"
            result_sheet.write(row, 12, snapshotId, string_format) # "Snapshot Id"
            result_sheet.write(row, 13, encrypted, string_format) # "Encrypted"
            result_sheet.write(row, 14, kmsKeyId, string_format) # "KMS Key Id"
            row += 1

            cnt += 1


    print("-EBS ["+ str(cnt) +"]")

    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    # print(sheetlink_pos)
    # row, col
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

    global summary_col
    global Columns_C_POS
    summary_sheet.write(Columns_C_POS['EBS'], summary_col, cnt, integer_format)
    result_sheet.write(0, 1, "EBS List("+ str(cnt) +")", title_format)
    print("Done.\n")  

def report_IAM(iam):
  user_list = iam.list_users(MaxItems=1000)
  user_output = jmespath.search("Users[*].[UserName, PasswordLastUsed]", user_list)

  user_info = []
  for name, console_last in user_output:    
    group_info = iam.list_groups_for_user(UserName=name)
    groups = jmespath.search("Groups[*].GroupName", group_info)

    #####get programing access####
    ak_list = iam.list_access_keys(UserName=name)
    ak_output = jmespath.search("AccessKeyMetadata[*].AccessKeyId", ak_list)
    date_list = []
    for access_key in ak_output:
      last = iam.get_access_key_last_used(AccessKeyId=access_key)
      pl = jmespath.search("AccessKeyLastUsed.LastUsedDate", last)
      date_list.append(pl)

    program_last = None  
    
    date_list = list(filter(None, date_list))
    if date_list != []:
      date_list.sort(reverse=True)
      program_last = date_list[0]

    #print(name, str(console_last), str(program_last))

    if (console_last == None) & (program_last == None):
      lasted_access = "-"
    elif console_last == None:
      lasted_access = str(program_last)
    elif program_last == None:
      lasted_access = str(console_last)
    else:
      lasted_access = str(console_last) if (console_last > program_last) else str(program_last)

    #print(lasted_access)
    user_info.append([name, groups, lasted_access])

  result_sheet = xlsx.add_worksheet('IAM')

  Columns = ["User", "Group", "Last Activity (Console or Programmatic)"]

  # result_sheet.write(0, 0, "IAM User List", title_format)

  col = 0
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 55)
  result_sheet.set_column('B:B', 55)
  result_sheet.set_column('C:C', 35)

  row = 2 
  for user, group, last_ac in user_info:
    result_sheet.write(row, 0, user, string_format)
    result_sheet.write(row, 1, '\n'.join(group), wrap_format)
    result_sheet.write(row, 2, last_ac, string_format)
    row += 1

  print("-User ["+str(len(user_info))+"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  global Columns_C_POS
  global Columns_C_LINK
  summary_sheet.write(Columns_C_POS['User'], summary_col, len(user_info), integer_format)
  result_sheet.write(0, 1, "IAM User List(" + str(len(user_info)) + ")", title_format)

  ################ USER ##################
  group_list = iam.list_groups()
  group_output = jmespath.search("Groups[*].GroupName", group_list)

  row += 1

  Columns = ["Group", "Managed Policy", "Inline Policy"]
  # result_sheet.write(row, 0, "IAM Group List", title_format)
  group_title_rows = row
  row += 1

  col = 0
  for ColName in Columns:
    result_sheet.write(row, col, ColName, colname_format)
    col += 1 

  row += 1 

  for groupName in group_output:
    managed = iam.list_attached_group_policies(GroupName=groupName)
    inline = iam.list_group_policies(GroupName=groupName)

    managed_policy = jmespath.search("AttachedPolicies[*].PolicyName", managed)
    inline_policy = jmespath.search("PolicyNames", inline)

    result_sheet.write(row, 0, groupName, string_format)
    result_sheet.write(row, 1, '\n'.join(managed_policy), wrap_format)
    result_sheet.write(row, 2, '\n'.join(inline_policy), wrap_format)
    row += 1

  print("-Group ["+str(len(group_output))+"]")


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(group_title_rows, 0, sheetlink_pos, url_format, string=ColName)

  # 결과 값
  ColName = 'Group'
  result_sheet.write(group_title_rows, 1, "IAM Group List(" + str(len(group_output)) + ")", title_format)
  summary_sheet.write(Columns_C_POS[ColName], summary_col, len(group_output), integer_format)

  # 링크 작성
  sheetsummary_pos = "C" + str(Columns_C_POS[ColName] + 1)
  print(sheetsummary_pos)
  sheetlink_pos = "internal:\'" + Columns_C_LINK[ColName] + "\'!" + "A" + str(group_title_rows + 1)
  print(sheetlink_pos)
  summary_sheet.write_url(sheetsummary_pos, sheetlink_pos, url_format, string=ColName)
  

  print("Done.\n")


def report_elb(elb, alb):
  elb_list = elb.describe_load_balancers()
  alb_list = alb.describe_load_balancers()

  result_sheet = xlsx.add_worksheet('ELB')

  elb_path = jmespath.search('LoadBalancerDescriptions[*].[LoadBalancerName, DNSName, VpcId, AvailabilityZones, Scheme]', elb_list)
  alb_path = jmespath.search('LoadBalancers[*].[LoadBalancerArn, LoadBalancerName, DNSName, VpcId, AvailabilityZones, Scheme, Type]', alb_list)


  Columns = ['Load Balancer Name', 'DNS Name', 'VPC Id', 'Availability Zones', 'Type', 'Scheme', 'Target Group', 'Port', 'Status']

  result_sheet.write(0, 0, "ELB List", title_format)

  col = 0
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1


  result_sheet.set_column('A:A', 30) # Load Balancer Name
  result_sheet.set_column('B:B', 72) # DNS Name
  result_sheet.set_column('C:C', 25) # VPC ID
  result_sheet.set_column('D:D', 20) # Avalilability Zones
  result_sheet.set_column('E:E', 12) # Type
  result_sheet.set_column('F:F', 17) # Scheme
  result_sheet.set_column('G:G', 35) # Target Group
  result_sheet.set_column('H:H', 7)  # Port
  result_sheet.set_column('I:I', 130) # Status

  row = 2 

  # elb list
  for LBName, DNSName, VpcId, AvailabilityZones, Scheme in elb_path:
    targetInstances = elb.describe_instance_health(LoadBalancerName=LBName)
    targetSt = jmespath.search("InstanceStates[*].[InstanceId, State]", targetInstances)

    result_sheet.write(row, 0, LBName, string_format)
    result_sheet.write(row, 1, DNSName, string_format)
    result_sheet.write(row, 2, VpcId, string_format)
    result_sheet.write(row, 3, '\n'.join(AvailabilityZones), wrap_format)
    result_sheet.write(row, 5, Scheme, string_format)
    targetList = []
    for target in targetSt:
      targetList.append(':'.join(target))
    result_sheet.write(row, 8, '\n'.join(targetList), wrap_format)
    row += 1

  # alb list
  alb_cnt = 0
  nlb_cnt = 0
  for LBArn, LBName, DNSName, VpcId, AvailabilityZones, Scheme, Type in alb_path:
    targetlist = alb.describe_target_groups(LoadBalancerArn=LBArn)

    result_sheet.write(row, 0, LBName, string_format)
    result_sheet.write(row, 1, DNSName, string_format)
    result_sheet.write(row, 2, VpcId, string_format)
    result_sheet.write(row, 3, '\n'.join(d['ZoneName'] for d in AvailabilityZones), wrap_format)
    result_sheet.write(row, 5, Scheme, string_format)
    
    cnt = row
    for targetgp in targetlist['TargetGroups']:
      tgarn = targetgp['TargetGroupArn']
      tgname = targetgp['TargetGroupName']
      tgport = targetgp['Port']
      targethealth = alb.describe_target_health(TargetGroupArn=tgarn)
      targetSt = jmespath.search("TargetHealthDescriptions[*].[Target.Id, TargetHealth.State]", targethealth)

      targetList = []
      for target in targetSt:
        targetList.append(':'.join(target))

      result_sheet.write(cnt, 6, tgname, string_format)
      result_sheet.write(cnt, 7, tgport, string_format)
      result_sheet.write(cnt, 8, '\n'.join(targetList), wrap_format)
      cnt += 1
    
    result_sheet.write(row, 4, Type, string_format)
    if Type == 'network':
      nlb_cnt += 1
    elif Type == 'application':
      alb_cnt += 1

    if cnt > row :
      row = cnt
    else:
      row += 1

  print("-ELB ["+str(len(elb_path)+len(alb_path))+"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


  sub_title = "ELB List[ NLB(" + str(nlb_cnt) + "), ALB(" + str(alb_cnt) + ")]"
  result_sheet.write(0, 1, sub_title, title_format)
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['ALB'], summary_col, alb_cnt, integer_format)
  summary_sheet.write(Columns_C_POS['NLB'], summary_col, nlb_cnt, integer_format)
  print("Done.\n")


def report_redshift(redshift):
  rs_cluster_list = redshift.describe_clusters()
  cluster_output = jmespath.search("Clusters[*].[ClusterIdentifier, NodeType, Endpoint.Address, Endpoint.Port, VpcId, NumberOfNodes, MasterUsername]", rs_cluster_list)

  result_sheet = xlsx.add_worksheet('Redshift')

  Columns = ["Name", "Type", "Node", "Endpoint Address", "Endpoint Port", "Master User", "VPC"]

  # result_sheet.write(0, 0, "Redshift Cluster List", title_format)

  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  row = 2
  for ClusterName, NodeType, ep_address, ep_port, VpcId, Nodes, MasterUser in cluster_output:    	
    result_sheet.write(row, 0, ClusterName, string_format)
    result_sheet.write(row, 1, NodeType, string_format)
    result_sheet.write(row, 2, Nodes, string_format)
    result_sheet.write(row, 3, ep_address, string_format)
    result_sheet.write(row, 4, ep_port, string_format)
    result_sheet.write(row, 5, MasterUser, string_format)
    result_sheet.write(row, 6, VpcId, string_format)
    row += 1

  print("-Clusters ["+str(len(cluster_output))+"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['REDSHIFT'], summary_col, len(cluster_output), integer_format)
  result_sheet.write(0, 1, "Redshift Cluster List("+str(len(cluster_output))+")", title_format)
  print("Done.\n")


def report_ecr_repositories(ecr):
    global result_sheet
    result_sheet = xlsx.add_worksheet('ECR')

    Columns = ["No.", "repository Name", "createdAt", "repository Uri", "registry Id", "imageTag Mutability", "imageScanning Configuration", "encryption Configuration", "repository Arn"]

    # result_sheet.write(0, 0, "CloudWatch Events List", title_format)

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 27)  # repositoryName
    result_sheet.set_column('C:C', 16)  # createdAt
    result_sheet.set_column('D:D', 52)  # repositoryUri
    result_sheet.set_column('E:E', 12)  # registryId
    result_sheet.set_column('F:F', 10)  # imageTagMutability
    result_sheet.set_column('G:G', 22)  # imageScanningConfiguration
    result_sheet.set_column('H:H', 22)  # encryptionConfiguration
    result_sheet.set_column('I:I', 72)  # repositoryArn
    
    
    # CloudWatch Events 규칙 목록 가져오기
    response = ecr.describe_repositories()
    repositories = response['repositories']

    print("ECR Repositories")
    row = 2
    for repo in repositories:
        # print(f"- Repository Name: {repo['repositoryName']}")
        # print(f"  Repository URI: {repo['repositoryUri']}")
        # print("-" * 50)
        # pprint(repo)
        row = write_ecr_to_excel(row, repo, result_sheet)

    # nextToken을 사용하여 추가 목록 조회
    while 'nextToken' in response:
        next_token = response['nextToken']
        response = ecr.describe_repositories(maxResults=100, nextToken=next_token)
        repositories = response['repositories']

        print("Additional ECR Repositories:")
        for repo in repositories:
            # print(f"- Repository Name: {repo['repositoryName']}")
            # print(f"  Repository URI: {repo['repositoryUri']}")
            # print("-" * 50)
            # pprint(repo)

            row = write_ecr_to_excel(row, repo, result_sheet)



    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"ECR List({str(row - 2)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['ECR'], summary_col, row - 2, integer_format)
    print(f'-ECR List [{row - 2}]')
    print("Done.\n")

def write_ecr_to_excel(row, repo, result_sheet):
    result_sheet.write(row, 0, row - 1, integer_format)
    result_sheet.write(row, 1, repo['repositoryName'], wrap_format)
    result_sheet.write(row, 2, repo['createdAt'], date_format)
    result_sheet.write(row, 3, repo['repositoryUri'], string_format)
    
    result_sheet.write(row, 4, repo['registryId'], string_format)
    
    result_sheet.write(row, 5, repo['imageTagMutability'], string_format)
    result_sheet.write(row, 6, json.dumps(repo['imageScanningConfiguration'],indent=2), wrap_format)
    result_sheet.write(row, 7, json.dumps(repo['encryptionConfiguration'],indent=2), wrap_format)
    result_sheet.write(row, 8, repo['repositoryArn'], string_format)
    
    row += 1

    return row


def report_ecs(ecs):

  Columns = ["Cluster Name", "Status", "Registered Container Instances Count", "Running Tasks Count", "Pending Tasks Count", "Active Services Count", "Statistics", "Settings", "Capacity Providers", "Default Capacity Provider Strategy (weight, base)", "Services", "Tags", "Cluster ARN", ]

  result_sheet = xlsx.add_worksheet('ECS')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "ECS Cluster List", title_format)
  col = 0 
  for ColName in Columns:
    if col in (5, 6):
      result_sheet.write(1, col, ColName, colname_left_format)
    else:
      result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 32)  # Cluster Name
  result_sheet.set_column('B:B', 10)  # k8s version
  result_sheet.set_column('C:C', 10)  # Platform Version
  result_sheet.set_column('D:D', 17)  # createdAt
  result_sheet.set_column('E:E', 10)  # Status
  result_sheet.set_column('F:F', 22)  # Kubernetes Network Config(IP Family\nService Ipv4 Cidr)
  result_sheet.set_column('G:G', 152) # VPC(Cluster Security Group Id\nSecurity Group Id\nPrivate Access\nPublic Access\nPublic Access CIDRs\nsubnet ids\nVPC ID)
  result_sheet.set_column('H:H', 92)  # Tags
  result_sheet.set_column('I:I', 72)  # Cluster ARN
  result_sheet.set_column('J:J', 72)  # Role ARN
  result_sheet.set_column('K:K', 82)  # endpoint
  result_sheet.set_column('L:L', 82)  # identity.oidc.issuer

  clusters = ecs.list_clusters(maxResults=100)
  # print(clusters)

  clusters_arns = clusters["clusterArns"]
  # print(clusters_arns)
  clusters_descriptions = ecs.describe_clusters(clusters=clusters_arns)
  # print(clusters_descriptions)
  cluster_output = jmespath.search("clusters[*].[clusterArn, clusterName, status, registeredContainerInstancesCount, runningTasksCount, pendingTasksCount, activeServicesCount, statistics[*], tags[*], settings[*], capacityProviders[*], defaultCapacityProviderStrategy[*].weight, defaultCapacityProviderStrategy[*].base]", clusters_descriptions)

  row = 2
  for clusterArn, clusterName, status, registeredContainerInstancesCount, runningTasksCount, pendingTasksCount, activeServicesCount, statistics, tags, settings, capacityProviders, weight, base in cluster_output:    
    result_sheet.write(row, 0, clusterName, string_format)
    result_sheet.write(row, 1, status, string_format)
    result_sheet.write(row, 2, registeredContainerInstancesCount, integer_format)
    result_sheet.write(row, 3, runningTasksCount, integer_format)
    result_sheet.write(row, 4, pendingTasksCount, integer_format)
    result_sheet.write(row, 5, activeServicesCount, integer_format)
    result_sheet.write(row, 6, ', '.join(statistics), string_format)
    result_sheet.write(row, 7, ', '.join(settings), string_format)
    result_sheet.write(row, 8, ', '.join(capacityProviders), string_format)
    
    if len(capacityProviders) > 0:
      # for w in weight:
        
      # result_sheet.write(row, 11, '(' + ', '.join(str(weight)) + ', ' + ', '.join(str(base)) + ')')
      # result_sheet.write(row, 11, str(weight) + ', ' + str(base))
      ws = boto3_helper.iListToString(weight)
      bs = boto3_helper.iListToString(base)
      result_sheet.write(row, 9, ws + ', ' + bs, string_format)
    response = ecs.list_services(cluster=clusterName, maxResults=100)
    # pprint(response['serviceArns'])
    services = []
    for serivceArn in response['serviceArns']:
      # print(serivceArn.split('/')[2])
      services.append(serivceArn.split('/')[2])
    
    result_sheet.write(row, 10, ', \n'.join(services), wrap_format)
    result_sheet.write(row, 11, '\n'.join(tags), wrap_format)
    result_sheet.write(row, 12, clusterArn, string_format)

    row += 1
  
  print("-ECS Cluster ["+str(len(cluster_output))+"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['ECS Cluster'], summary_col, len(cluster_output), integer_format)
  result_sheet.write(0, 1, "ECS Cluster List(" + str(len(cluster_output)) + ")", title_format)
  print("Done.\n")


def report_eks(eks):

  # Columns = ["Cluster Name", "k8s Version", "Platform Version", "Created At", "Status", "Kubernetes Network Config :: \n- IP Family\n- Service Ipv4 Cidr", "VPC Config ::\n- Cluster Security Group Id\n- Endpoint Private Access\n- Endpoint Public Access\n- Public Access CIDRs\n- subnet ids\n- VPC ID", "Tags", "Cluster ARN", "Role ARN", "Endpoint", "identity.oidc.issuer"]

  Columns = ["No.", "Cluster Name", "k8s Version", "Platform Version", "Created At", "Status", "Kubernetes Network Config", "VPC Config", "Tags", "Cluster ARN", "Role ARN", "Endpoint", "identity.oidc.issuer"]

  result_sheet = xlsx.add_worksheet('EKS')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "EKS Cluster List", title_format)
  col = 0 
  for ColName in Columns:
    if col in (5, 6, 7, 8, 9):
      result_sheet.write(1, col, ColName, colname_left_format)
    else:
      result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 32)  # Cluster Name
  result_sheet.set_column('B:B', 32)  # Cluster Name
  result_sheet.set_column('C:C', 10)  # k8s version
  result_sheet.set_column('D:D', 10)  # Platform Version
  result_sheet.set_column('E:E', 17)  # createdAt
  result_sheet.set_column('F:F', 10)  # Status
  result_sheet.set_column('G:G', 42)  # Kubernetes Network Config(IP Family\nService Ipv4 Cidr)
  result_sheet.set_column('H:H', 152) # VPC(Cluster Security Group Id\nSecurity Group Id\nPrivate Access\nPublic Access\nPublic Access CIDRs\nsubnet ids\nVPC ID)
  result_sheet.set_column('I:I', 92)  # Tags
  result_sheet.set_column('J:J', 72)  # Cluster ARN
  result_sheet.set_column('K:K', 72)  # Role ARN
  result_sheet.set_column('L:L', 82)  # endpoint
  result_sheet.set_column('M:M', 82)  # identity.oidc.issuer


  cluster = eks.list_clusters(maxResults=100)
  clusters = cluster.get('clusters')
  # print(clusters)
  # print(json.dumps(clusters, indent=2))

  # ekss = client.describe_cluster(clusters)
  
  row = 2
  cluster_cnt = 0
  for cluster in clusters:
    # print("##################\n{0}\n##################".format(cluster))
    cluster_info = eks.describe_cluster(name=cluster)
    # pprint(cluster_info)
    # cluster_dic = cluster_info["cluster"]
    # pprint(cluster_dic)

    cluster_output = jmespath.search("cluster.[arn, createdAt, endpoint, identity.oidc.issuer, kubernetesNetworkConfig, kubernetesNetworkConfig.ipFamily, kubernetesNetworkConfig.serviceIpv4Cidr, name, platformVersion, resourcesVpcConfig, resourcesVpcConfig.endpointPrivateAccess, resourcesVpcConfig.endpointPublicAccess, resourcesVpcConfig.publicAccessCidrs, resourcesVpcConfig.securityGroupIds, resourcesVpcConfig.subnetIds, resourcesVpcConfig.vpcId, roleArn, status, tags, version]", cluster_info)
    # print('cluster_output')
    # pprint(cluster_output)

    clusterArn, createdAt, clusterEndpoint, oidcIssuer, kubernetesNetworkConfig, k8sIpFamily, k8sSvcIPv4Cidr, clusterName, platformVersion, resourcesVpcConfig, privateAccess, publicAccess, publicAccessCidrs, securityGroupIds, subnetIds, vpcId, roleArn, status, tags, k8sVersion = cluster_output
    result_sheet.write(row, 0, cluster_cnt + 1, integer_format) # "cluster name", 
    result_sheet.write(row, 1, clusterName, string_format) # "cluster name", 
    result_sheet.write(row, 2, k8sVersion, string_format) # "k8s version", 
    result_sheet.write(row, 3, platformVersion, string_format) # "platformVersion",
    result_sheet.write(row, 4, createdAt, date_format) # "createdAt"
    result_sheet.write(row, 5, status, string_format) # "status",
    kubernetesNetworkConfig_str = json.dumps(kubernetesNetworkConfig, indent=2)
    # result_sheet.write(row, 5, k8sIpFamily + '\n' + k8sSvcIPv4Cidr, wrap_format) # 4. 
    result_sheet.write(row, 6, kubernetesNetworkConfig_str, wrap_format) # 4. "kubernetesNetworkConfig(ipFamily, serviceIpv4Cidr)",
    # 9. "VPC(Cluster Security Group Id, Security Group Id, Private Access, Public Access, Public Access CIDRs, subnet ids)",
    # result_sheet.write(row, 6,
    #       ', '.join(securityGroupIds) + '\n' +
    #       str(privateAccess) + '\n' +
    #       str(publicAccess) + '\n' +
    #       ', '.join(publicAccessCidrs) + '\n' + 
    #       ', '.join(subnetIds) + '\n' + 
    #       vpcId, wrap_format)
    resourcesVpcConfig_str = json.dumps(resourcesVpcConfig, indent=2)
    result_sheet.write(row, 7, resourcesVpcConfig_str, wrap_format)
    tag_str = ""
    tag_cnt = 0
    for key in tags.keys( ):
      # print(key, ":", tags[key])    

      if tag_cnt == 0:
        tag_str = (key + "=" + tags[key])
      else:              
        tag_str += ("\n" + key + "=" + tags[key])
      tag_cnt += 1
    result_sheet.write(row, 8, tag_str, wrap_format) # "tags"
    result_sheet.write(row, 9, clusterArn, string_format) # "cluster arn",
    result_sheet.write(row, 10, roleArn, string_format) # "role arn",
    result_sheet.write(row, 11, clusterEndpoint, string_format) # endpoint",
    result_sheet.write(row, 12, oidcIssuer, string_format) # "identity.oidc.issuer",

    row += 1
    cluster_cnt += 1

  # result_sheet.autofit( )
  print("-EKS Cluster ["+ str(cluster_cnt) +"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['EKS Cluster'], summary_col, cluster_cnt, integer_format)
  result_sheet.write(0, 1, "EKS Cluster List("+ str(cluster_cnt) + ")", title_format)
  print("Done.\n") 

def report_efs(efs):
  Columns = ["No.", "Name", "Size(Bytes)", "File System Id", "Creation Time", "Number Of Mount Targets", "Performance Mode", "Throughput Mode", "Life Cycle State", "Encrypted", "KMS Key Id", "File System ARN"]

  result_sheet = xlsx.add_worksheet('EFS')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "EFS List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1


  result_sheet.set_column('A:A', 10) # Name
  result_sheet.set_column('B:B', 32) # Name
  result_sheet.set_column('C:C', 20)  # Size(Bytes)
  result_sheet.set_column('D:D', 20) # File System Id
  result_sheet.set_column('E:E', 17) # Creation Time
  result_sheet.set_column('F:F', 10) # Number Of Moun targets
  result_sheet.set_column('G:G', 17) # Performance Mode
  result_sheet.set_column('H:H', 12) # Throughput Mode
  result_sheet.set_column('I:I', 12) # Life Cycle State
  result_sheet.set_column('J:J', 10) # Encrypted
  result_sheet.set_column('K:K', 75) # KMS Key Id
  result_sheet.set_column('L:L', 95) # File System ARN

  efss = efs.describe_file_systems()['FileSystems'] # 리스트를 가져옴
  # pprint(efss)
  efss_output = jmespath.search("[*].[CreationTime, CreationToken, Encrypted, FileSystemArn, FileSystemId, KmsKeyId, LifeCycleState, Name, NumberOfMountTargets, OwnerId, PerformanceMode, SizeInBytes.Value, Tags, ThroughputMode]", efss)
  # print(".")
  # print(".")
  # print('efss_output')
  # pprint(efss_output)



  row = 2
  efs_cnt = 0
  for creationTime, creationToken, encrypted, fileSystemArn, fileSystemId, kmsKeyId, lifeCycleState, name, numberOfMountTargets, ownerId, performanceMode, sizeInBytes, tags, throughputMode in efss_output:    
    
    result_sheet.write(row, 0, efs_cnt + 1, integer_format) # No, 
    result_sheet.write(row, 1, name, string_format) # Name", 
    result_sheet.write(row, 2, sizeInBytes, integer_format) # "Size(Bytes)"
    result_sheet.write(row, 3, fileSystemId, string_format) # "FileSystemId"
    result_sheet.write(row, 4, creationTime, date_format) # "CreationTime"
    result_sheet.write(row, 5, numberOfMountTargets, integer_format) # "NumberOfMountTargets"
    result_sheet.write(row, 6, performanceMode, string_format) # "PerformanceMode"
    result_sheet.write(row, 7, throughputMode, string_format) # "ThroughputMode"
    result_sheet.write(row, 8, lifeCycleState, string_format) # "LifeCycleState
    result_sheet.write(row, 9, encrypted, string_format) # "Encrypted"
    result_sheet.write(row, 10, kmsKeyId, string_format) # "KmsKeyId"
    result_sheet.write(row, 11, fileSystemArn, string_format) # "FileSystemArn"
    row += 1
    efs_cnt += 1

  print("-EFS ["+ str(efs_cnt) +"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global Columns_C_POS
  global summary_col
  summary_sheet.write(Columns_C_POS['EFS'], summary_col, efs_cnt, integer_format)
  result_sheet.write(0, 1, "EFS List("+ str(efs_cnt) +")", title_format)

  print("Done.\n") 


def report_dynamodb(dynamodb):
  Columns = ["No.", "Name", "Item Count", "Key schema (AttributeName, KeyType)", "Item( < 10)"]

  result_sheet = xlsx.add_worksheet('DynamoDB')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "DynamoDB List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10) # No
  result_sheet.set_column('B:B', 32) # Name
  result_sheet.set_column('C:C', 7)  # Item Count
  result_sheet.set_column('D:D', 18) # Key schema (AttributeName, KeyType)
  result_sheet.set_column('E:E', 72) # Item( < 10)

  row = 2
  table_cnt = 0
  tables = list(dynamodb.tables.all())
  for table in tables:
    result_sheet.write(row, 0, table_cnt + 1, integer_format)     # Np. 
    result_sheet.write(row, 1, table.table_name, string_format)   # Name", 
    # print('----')
    # print ('Table Name: ', table.table_name) # 1
    result_sheet.write(row, 2, table.item_count, integer_format)  # "Item Count"
    schema_str = ""
    AttributeName = ""
    for schema in table.key_schema:
      AttributeName = schema['AttributeName']
      schema_str += schema['AttributeName'] + ', ' + schema['KeyType'] + '\n'
    result_sheet.write(row, 3, schema_str, string_format)        # "Key schema(AttributeName, KeyType)"
    
    resp = table.scan( )
    # pprint(resp)
    items = resp['Items']
    count = resp['Count']
    # print('\t', items)
    # print('\t', count)
    # print(AttributeName)
    item_str = ""
    item_cnt = 0
    for item in items:
      # print('\t', item[AttributeName])
      item_str += item[AttributeName] + ('\n' if (item_cnt + 1) < count else ' ')
      item_cnt += 1
      if item_cnt >= 10:
        item_str += '.\n'
        item_str += '.\n'
        item_str += '.'
        break
    result_sheet.write(row, 4, item_str, wrap_format) # 3 "Item( < 10)"

    row += 1
    table_cnt += 1

  print("-DynamoDB Table ["+ str(table_cnt) +"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['DynamoDB Tables'], summary_col, table_cnt, integer_format)
  result_sheet.write(0, 1, "DynamoDB List("+ str(table_cnt) + ")", title_format)

  print("Done.\n")  


def report_elasticaches(elasticache):
  Columns = ["No.", "Group ID", "Subnet Group Name", "Cluster Id", "Engine", "Engine Version", "Network Type", "Node Type", "Status", "Transit Encryption Enabled", "Auto Minor Version Upgrade", "Auth Token Enabled", "Cache Cluster Create Time", "Security Group Id", "ARN"]

  result_sheet = xlsx.add_worksheet('ElastiCache')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "ElastiCache List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10) # No.
  result_sheet.set_column('B:B', 32) # Group ID
  result_sheet.set_column('C:C', 32)  # Subnet Group Name
  result_sheet.set_column('D:D', 32) # Cluster Id
  result_sheet.set_column('E:E', 10) # Engine
  result_sheet.set_column('F:F', 10) # Engine Version
  result_sheet.set_column('G:G', 10) # Network Type
  result_sheet.set_column('H:H', 15) # Node Type
  result_sheet.set_column('I:I', 12) # Status
  result_sheet.set_column('J:J', 12) # Transit Encryption Enabled
  result_sheet.set_column('K:K', 10)  # Auto Minor Version Upgrade
  result_sheet.set_column('L:L', 10) # Auth Token Enabled
  result_sheet.set_column('M:M', 20) # Cache Cluster Create Time
  result_sheet.set_column('N:N', 25) # Security Group Id
  result_sheet.set_column('O:O', 72) # ARN



  # clusters = elasticache.describe_cache_clusters(MaxRecords=100,ShowCacheNodeInfo=True, ShowCacheClustersNotInReplicationGroups=True)
  clusters = elasticache.describe_cache_clusters( )
  # pprint(clusters)

  cluster_output = jmespath.search("CacheClusters[*].[ARN, AtRestEncryptionEnabled, AuthTokenEnabled, AutoMinorVersionUpgrade, CacheClusterCreateTime, CacheClusterId, CacheClusterStatus, CacheNodeType, CacheParameterGroup.CacheParameterGroupName, CacheParameterGroup.ParameterApplyStatus, CacheSecurityGroups, CacheSubnetGroupName, ClientDownloadLandingPage, Engine, EngineVersion, NetworkType, NumCacheNodes, PreferredAvailabilityZone, ReplicationGroupId, ReplicationGroupLogDeliveryEnabled, SecurityGroups[*].SecurityGroupId, SnapshotRetentionLimit, SnapshotWindow, TransitEncryptionEnabled]", clusters)

  row = 2
  cluster_cnt = 0
  for arn, atRestEncryptionEnabled, authTokenEnabled, autoMinorVersionUpgrade, cacheClusterCreateTime, cacheClusterId, cacheClusterStatus, cacheNodeType, cacheParameterGroupName, cacheParameterGroupParameterApplyStatus, cacheSecurityGroups, cacheSubnetGroupName, clientDownloadLandingPage, engine, engineVersion, networkType, numCacheNodes, preferredAvailabilityZone, replicationGroupId, replicationGroupLogDeliveryEnabled, securityGroupsId, snapshotRetentionLimit, snapshotWindow, transitEncryptionEnabled in cluster_output:    
    result_sheet.write(row, 0, cluster_cnt + 1, integer_format)
    result_sheet.write(row, 1, replicationGroupId, string_format)
    result_sheet.write(row, 2, cacheSubnetGroupName, string_format)
    result_sheet.write(row, 3, cacheClusterId, string_format)
    result_sheet.write(row, 4, engine, string_format)
    result_sheet.write(row, 5, engineVersion, string_format)
    result_sheet.write(row, 6, networkType, string_format)
    result_sheet.write(row, 7, cacheNodeType, string_format)
    result_sheet.write(row, 8, cacheClusterStatus, string_format)
    result_sheet.write(row, 9, transitEncryptionEnabled, string_format)
    result_sheet.write(row, 10, autoMinorVersionUpgrade, string_format)
    result_sheet.write(row, 11, authTokenEnabled, string_format)
    result_sheet.write(row, 12, cacheClusterCreateTime, date_format)
    if securityGroupsId is not None:
      result_sheet.write(row, 13, '\n'.join(securityGroupsId), wrap_format)
    result_sheet.write(row, 14, arn, string_format)
    row += 1
    cluster_cnt += 1

  print("-ElastiCache Cluster ["+ str(cluster_cnt) +"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['ElastiCache'], summary_col, cluster_cnt, integer_format)
  result_sheet.write(0, 1, "ElastiCache List("+ str(cluster_cnt) +")", title_format)
  print("Done.\n") 



def report_kafka(kafka):
    Columns = ["No.", "Cluster Name", "State", "Creation Time", "Kafka Version, ConfigurationVersion", "Client Subnets", "Instance Type", "Number Of Broker Nodes", "Broker Node Security Groups", "Storage Mode", "EBS -\nProvisioned Troughtput Enabled\nVolume Size", "Encryption In Transit", "Cluster ARN", "Zookeeper Connect String", "Zookeeper Connect String Tls", "List of Broker"]

    result_sheet = xlsx.add_worksheet('Kafka(MSK)')
    # result_sheet.set_column('A:Z', cell_format=wrap_format)

    # result_sheet.write(0, 0, "Kafka(MSK) List", title_format)
    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1

    result_sheet.set_column('A:A', 10) # No.
    result_sheet.set_column('B:B', 32) # Cluster Name
    result_sheet.set_column('C:C', 10) # State
    result_sheet.set_column('D:D', 20) # Creation Time
    result_sheet.set_column('E:E', 10) # Kafka Version, ConfigurationVersion
    result_sheet.set_column('F:F', 30) # Client Subnets
    result_sheet.set_column('G:G', 20) # Instance Type
    result_sheet.set_column('H:H', 7)  # Number Of Broker Nodes
    result_sheet.set_column('I:I', 22) # Broker Node Security Groups
    result_sheet.set_column('J:J', 8)  # Storage Mode
    result_sheet.set_column('K:K', 10) # EBS -\nProvisioned Troughtput Enabled\nVolume Size
    result_sheet.set_column('L:L', 15) # Encryption In Transit
    result_sheet.set_column('M:M', 102) # Cluster ARN
    result_sheet.set_column('N:N', 72) # Zookeeper Connect String
    result_sheet.set_column('O:O', 72) # Zookeeper Connect String Tls
    result_sheet.set_column('P:P', 72) # Cluster ARN

    # clusters = elasticache.describe_cache_clusters(MaxRecords=100,ShowCacheNodeInfo=True, ShowCacheClustersNotInReplicationGroups=True)
    cluster_list = kafka.list_clusters(MaxResults=100)
    # pprint(cluster_list)

    cluster_output = jmespath.search("ClusterInfoList[*].[BrokerNodeGroupInfo.ClientSubnets, BrokerNodeGroupInfo.InstanceType, BrokerNodeGroupInfo.SecurityGroups, BrokerNodeGroupInfo.StorageInfo.EbsStorageInfo.ProvisionedThroughput.Enabled, BrokerNodeGroupInfo.StorageInfo.EbsStorageInfo.VolumeSize, ClusterArn, ClusterName, CreationTime, CurrentBrokerSoftwareInfo.KafkaVersion, CurrentBrokerSoftwareInfo.ConfigurationRevision, CurrentVersion, EncryptionInfo.EncryptionInTransit.ClientBroker, EnhancedMonitoring, LoggingInfo, NumberOfBrokerNodes, OpenMonitoring, State, StorageMode, Tags, ZookeeperConnectString, ZookeeperConnectStringTls]", cluster_list)

    row = 2
    cluster_cnt = 0
    for brokerNodeGroupInfoClientSubnets, brokerNodeGroupInfoInstanceType, brokerNodeGroupInfoSecurityGroups, brokerNodeGroupInfoStorageInfoEbsStorageInfoProvisionedThroughput, brokerNodeGroupInfoStorageInfoEbsStorageInfoVolumeSize, clusterArn, clusterName, creationTime, kafkaVersion, kafkaConfigurationRevision, currentVersion, encryptionInfo, enhancedMonitoring, loggingInfo, numberOfBrokerNodes, openMonitoring, state, storageMode, tags, zookeeperConnectString, ZookeeperConnectStringTls in cluster_output:    
        result_sheet.write(row, 0, cluster_cnt + 1, integer_format)
        result_sheet.write(row, 1, clusterName, integer_format)
        result_sheet.write(row, 2, state, string_format)
        result_sheet.write(row, 3, creationTime, date_format)
        result_sheet.write(row, 4, kafkaVersion + ', ' + str(kafkaConfigurationRevision), string_format)
        result_sheet.write(row, 5, '\n'.join(brokerNodeGroupInfoClientSubnets), wrap_format)
        result_sheet.write(row, 6, brokerNodeGroupInfoInstanceType, string_format)
        result_sheet.write(row, 7, numberOfBrokerNodes, integer_format)
        result_sheet.write(row, 8, '\n'.join(brokerNodeGroupInfoSecurityGroups), wrap_format)
        result_sheet.write(row, 9, storageMode, string_format)
        result_sheet.write(row, 10, str(brokerNodeGroupInfoStorageInfoEbsStorageInfoProvisionedThroughput) + ', ' + str(brokerNodeGroupInfoStorageInfoEbsStorageInfoVolumeSize), string_format)
        result_sheet.write(row, 11, encryptionInfo, string_format)
        result_sheet.write(row, 12, clusterArn, string_format)
        zookeeperConnectString_ = zookeeperConnectString.split(',')
        # pprint(zookeeperConnectString_)
        result_sheet.write(row, 13, '\n'.join(zookeeperConnectString_), wrap_format)
        ZookeeperConnectStringTls_ = ZookeeperConnectStringTls.split(',')
        # pprint(ZookeeperConnectStringTls_)
        result_sheet.write(row, 14, '\n'.join(ZookeeperConnectStringTls_), wrap_format)
        
        replication = kafka.get_bootstrap_brokers(ClusterArn=clusterArn)
        replication_info = replication['BootstrapBrokerString']
        # pprint(replication_info)
        result_sheet.write(row, 15, '\n'.join(replication_info.split(',')), wrap_format)
        
        row += 1
        cluster_cnt += 1

    print("-Kafka(MSK) Cluster ["+ str(cluster_cnt) +"]")

    # 자원요약으로 가기
    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    # print(sheetlink_pos)
    # row, col
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

    result_sheet.write(0, 1, "Kafka(MSK) List("+ str(cluster_cnt) +")", title_format)
    global summary_col
    global Columns_C_POS
    summary_sheet.write(Columns_C_POS['Kafka'], summary_col, cluster_cnt, integer_format)

    print("Done.\n") 


def report_sqs(sqs):

  Columns = ["No.", "Queue Urls"]

  result_sheet = xlsx.add_worksheet('SQS')

  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10)   # No.
  result_sheet.set_column('B:B', 132)  # Queue Urls


  # https://sqs.us-west-2.amazonaws.com
  sqs_list = sqs.list_queues( )
  # pprint(sqs_list)
  # print("QUEUE - URLS ", sqs_list.get("QueueUrls"))

  row = 2
  sqs_cnt = 0
  try:
    sqs_output = sqs_list['QueueUrls']
    # pprint(sqs_list['QueueUrls'])

    for queueUrls in sqs_output:
      # print(queueUrls)
      result_sheet.write(row, 0, sqs_cnt + 1, integer_format) # No.
      result_sheet.write(row, 1, queueUrls, string_format)    # Domain Name

      row += 1
      sqs_cnt += 1
  except KeyError as e:
    print(e)


  print("-Amazon Simple Queue Service List ["+ str(sqs_cnt) +"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  result_sheet.write(0, 1, "Amazon Simple Queue Service("+ str(sqs_cnt) +")", title_format)
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['Amazon Simple Queue Service'], summary_col, sqs_cnt, integer_format)
  print("Done.\n")  


def report_kinesis_firehose_streams(firehose):    
    global result_sheet
    result_sheet = xlsx.add_worksheet('Kinesis Firehose')

    Columns = ["No.", "Delivery Stream Name", "Delivery Stream Status", "Delivery Stream Type", "Create Timestamp", "Delivery Stream Encryption Configuration", "Destinations"]

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 52) # DeliveryStreamName
    result_sheet.set_column('C:C', 9)  # DeliveryStreamStatus
    result_sheet.set_column('D:D', 9)  # DeliveryStreamType
    result_sheet.set_column('E:E', 16) # CreateTimestamp
    result_sheet.set_column('F:F', 36) # DeliveryStreamEncryptionConfiguration
    result_sheet.set_column('G:G', 102)  # Destinations

    try:
        # Kinesis Data Firehose 스트림 목록 조회
        response = firehose.list_delivery_streams()
        # pprint(response)
        if 'DeliveryStreamNames' in response:
            streams = response['DeliveryStreamNames']
            
            if not streams:
                print("No Kinesis Data Firehose streams found.")
                row = 2
            else:
                # print("Kinesis Data Firehose streams:")
                row = 2
                for stream in streams:
                    # print("- " + stream)
                    # 선택한 스트림의 상세 정보 출력
                    describe_kinesis_firehose_stream(firehose, row, stream)
                    row += 1
            ColName = '자원 요약'
            sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
            # print(sheetlink_pos)
            # row, col
            result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


            result_sheet.write(0, 1, f"Kinesis firehose List({str(row - 2)})", title_format)
            global summary_col
            summary_sheet.write(Columns_C_POS['Kinesis Firehose'], summary_col, row - 2, integer_format)
            # print(f'-Kinesis Firehose [{row - 2}]')
            print("Done.\n")
        else:
            print("Failed to retrieve Kinesis Data Firehose streams.")
            
    except Exception as e:
        print("An error occurred:", e)

"""
- sksh-argos-p-an2-kinesis-firehose-msk-broker-logs-stream
{'CreateTimestamp': datetime.datetime(2022, 10, 7, 14, 32, 32, 347000, tzinfo=tzlocal()), 'DeliveryStreamARN': 'arn:aws:firehose:ap-northeast-2:123456789012:deliverystream/sksh-argos-p-an2-kinesis-firehose-msk-broker-logs-stream',
 'DeliveryStreamEncryptionConfiguration': {'Status': 'DISABLED'},
 'DeliveryStreamName': 'sksh-argos-p-an2-kinesis-firehose-msk-broker-logs-stream',       
 'DeliveryStreamStatus': 'ACTIVE',
 'DeliveryStreamType': 'DirectPut',
 'Destinations': [{'DestinationId': 'destinationId-000000000001',
                   'ExtendedS3DestinationDescription': {'BucketARN': 'arn:aws:s3:::sksh-argos-p-an2-msk-broker-logs',
                                                        'BufferingHints': {'IntervalInSeconds': 300,
                                                                           'SizeInMBs': 5},
                                                        'CloudWatchLoggingOptions': {'Enabled': False},
                                                        'CompressionFormat': 'UNCOMPRESSED',
                                                        'EncryptionConfiguration': {'NoEncryptionConfig': 'NoEncryption'},
                                                        'Prefix': '',
                                                        'RoleARN': 'arn:aws:iam::123456789012:role/sksh-argos-p-firehose-role',
                                                        'S3BackupMode': 'Disabled'},     
                   'S3DestinationDescription': {'BucketARN': 'arn:aws:s3:::sksh-argos-p-an2-msk-broker-logs',
                                                'BufferingHints': {'IntervalInSeconds': 300,
                                                                   'SizeInMBs': 5},      
                                                'CloudWatchLoggingOptions': {'Enabled': False},
                                                'CompressionFormat': 'UNCOMPRESSED',     
                                                'EncryptionConfiguration': {'NoEncryptionConfig': 'NoEncryption'},
                                                'Prefix': '',
                                                'RoleARN': 'arn:aws:iam::123456789012:role/sksh-argos-p-firehose-role'}}],
 'HasMoreDestinations': False,
 'VersionId': '1'}
Kinesis Data Firehose stream details:
Stream Name: sksh-argos-p-an2-kinesis-firehose-msk-broker-logs-stream
Delivery Stream ARN: arn:aws:firehose:ap-northeast-2:123456789012:deliverystream/sksh-argos-p-an2-kinesis-firehose-msk-broker-logs-stream
Delivery Stream Status: ACTIVE
"""

def describe_kinesis_firehose_stream(firehose, row, stream_name):

    # print(f"row:[{row}]")

    try:
        # Kinesis Data Firehose 스트림 상세 정보 조회
        response = firehose.describe_delivery_stream(DeliveryStreamName=stream_name)
        
        if 'DeliveryStreamDescription' in response:
            description = response['DeliveryStreamDescription']
  
            # pprint(description)


            # print("Kinesis Data Firehose stream details:")
            # print("Stream Name:", description['DeliveryStreamName'])
            # print("Delivery Stream ARN:", description['DeliveryStreamARN'])
            # print("Delivery Stream Status:", description['DeliveryStreamStatus'])
            # 기타 상세 정보들도 필요에 따라 출력합니다.
            # firehose_output = jmespath.search("[*].{CreateTimestamp, DeliveryStreamEncryptionConfiguration, DeliveryStreamName, DeliveryStreamStatus, DeliveryStreamType, Destinations}", description)
            # print("before jmespath")
            query = {
                "CreateTimestamp": "CreateTimestamp",
                "DeliveryStreamEncryptionConfiguration": "DeliveryStreamEncryptionConfiguration",
                "DeliveryStreamName": "DeliveryStreamName",
                "DeliveryStreamStatus": "DeliveryStreamStatus",
                "DeliveryStreamType": "DeliveryStreamType",
                "Destinations": "Destinations"
            }

            result_sheet.write(row, 0, row - 1, integer_format)
            result_sheet.write(row, 1, description['DeliveryStreamName'], string_format)
            result_sheet.write(row, 2, description['DeliveryStreamStatus'], string_format)
            result_sheet.write(row, 3, description['DeliveryStreamType'], string_format)
            result_sheet.write(row, 4, description['CreateTimestamp'], date_format)
            result_sheet.write(row, 5, json.dumps(description['DeliveryStreamEncryptionConfiguration']), wrap_format)
            result_sheet.write(row, 6, json.dumps(description['Destinations'], indent=2), wrap_format)

            # for key, value in query.items():
            #     result = jmespath.search(value, description)
            #     print(f"{key}: {result}")
            #     if key == 'DeliveryStreamName':
            #         result_sheet.write(row, 1, result, string_format)
            #     elif key == 'DeliveryStreamStatus':
            #         result_sheet.write(row, 2, result, string_format)
            #     elif key == 'DeliveryStreamType':
            #         result_sheet.write(row, 3, result, string_format)
            #     elif key == 'CreateTimestamp':
            #         result_sheet.write(row, 4, result, string_format)
            #     elif key == 'DeliveryStreamEncryptionConfiguration':
            #         result_sheet.write(row, 5, json.dumps(result,indent=2), wrap_format)
            #     elif key == 'Destinations':
            #         result_sheet.write(row, 6, json.dumps(result, indent=2), wrap_format)                    
        else:
            print(f"Failed to retrieve details for the stream: {stream_name}")            
            
    except Exception as e:
        print(f"An error occurred: {e}")
        


def report_sns_topics(sns):
    global result_sheet
    result_sheet = xlsx.add_worksheet('SNS Topics')

    Columns = ["No.", "TopicArn"]
    Columns_Attributes = ["DisplayName", "Effective Delivery Policy", "Owner", "Policy", "Subscriptions Confirmed", "Subscriptions Deleted", "Subscriptions Pending"]


    col = 0 
    for ColName in Columns:
        # 수직 병합 (2:3)     
        result_sheet.merge_range(f'{chr(65 + col)}2:{chr(65 + col)}3', ColName, colname_format)
        # result_sheet.write(1, col, ColName, colname_format)
        col += 1

    # Rules Column - 수평 병합
    result_sheet.merge_range(f'{chr(65 + col)}2:{chr(65 + col + len(Columns_Attributes) - 1)}2', "Attributes", colname_format)

    for AttributesName in Columns_Attributes:
        result_sheet.write(f'{chr(65 + col)}3', AttributesName, colname_format)
        col += 1


    # SNS Topics
    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 132) # TopicArn
    result_sheet.set_column('C:C', 72)  # DisplayName
    result_sheet.set_column('D:D', 52)  # EffectiveDeliveryPolicy
    result_sheet.set_column('E:E', 12)  # Owner
    result_sheet.set_column('F:F', 142) # Policy
    result_sheet.set_column('G:G', 12)  # SubscriptionsConfirmed
    result_sheet.set_column('H:H', 12)  # SubscriptionsDeleted
    result_sheet.set_column('I:I', 12)  # SubscriptionsPending

    
    # SNS 목록 가져오기
    response = sns.list_topics()
    topics = response['Topics']

    row = 3
    for topic in topics:
        topic_arn  = topic['TopicArn']
        response   = sns.get_topic_attributes(TopicArn=topic_arn)
        attributes = response['Attributes']
        # print(f"ID: {id}")
        row = write_sns_topic_attributes_to_excel(row, attributes, result_sheet)


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"AWS SNS Topics List({str(row - 3)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['SNS Topics'], summary_col, row - 3, integer_format)
    print(f'-AWS Shield Protection List({str(row - 2)})')
    print("Done.\n")

def write_sns_topic_attributes_to_excel(row, attributes, result_sheet):
    result_sheet.write(row, 0, row - 2, integer_format)
    result_sheet.write(row, 1, attributes['TopicArn'], string_format)
    result_sheet.write(row, 2, attributes['DisplayName'], string_format)
    
    effectiveDeliveryPolicy = json.loads(attributes['EffectiveDeliveryPolicy'])
    result_sheet.write(row, 3, json.dumps(effectiveDeliveryPolicy, indent=2), wrap_format)
    
    result_sheet.write(row, 4, attributes['Owner'], string_format)
    
    policy = json.loads(attributes['Policy'])
    result_sheet.write(row, 5, json.dumps(policy, indent=2), wrap_format)
    
    result_sheet.write(row, 6, attributes['SubscriptionsConfirmed'], integer_format)    
    result_sheet.write(row, 7, attributes['SubscriptionsDeleted'], integer_format)
    result_sheet.write(row, 8, attributes['SubscriptionsPending'], integer_format)

  
    
    row += 1

    return row


def report_lambda(client):
  Columns = ["No.", "Function Name", "Handler", "Architectures", "Code Size", "Last Modified", "Memory Size", "Ephemeral Storage Size", "Package Type", "Runtime", "Timeout", "Tracing Config", "Role", "Function Arn"]

  result_sheet = xlsx.add_worksheet('Lambda')

  # result_sheet.write(0, 0, "Lambda Function List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10)  # No.
  result_sheet.set_column('B:B', 82)  # Function Name
  result_sheet.set_column('C:C', 30)  # Handler
  result_sheet.set_column('D:D', 15)  # Architectures
  result_sheet.set_column('E:E', 10)  # Code Size
  result_sheet.set_column('F:F', 30)  # Last Modified
  result_sheet.set_column('G:G', 10)  # Memory Size
  result_sheet.set_column('H:H', 10)  # Ephemeral Storage Size
  result_sheet.set_column('I:I', 10)   # Package Type
  result_sheet.set_column('J:J', 12) # Runtime
  result_sheet.set_column('K:K', 10) # "Timeout"
  result_sheet.set_column('L:L', 12) # "Tracing Config"
  result_sheet.set_column('M:M', 102) # "Role"
  result_sheet.set_column('N:N', 130) # "Function Arn"

  # response = lambda.publish_version(
  #     FunctionName='helloWorldLambda',
  # )


  lambda_function_list = client.list_functions(
    # MasterRegion='ap-northeast-2',
    FunctionVersion='ALL',
    # Marker='string',
    MaxItems=123
  )
  # pprint(lambda_function_list)

  lambda_function_output = jmespath.search("Functions[*].[Architectures, CodeSize, Description, EphemeralStorage.Size, FunctionArn, FunctionName, Handler, LastModified, MemorySize, PackageType, RevisionId, Role, Runtime, Timeout, TracingConfig.Mode, Version]", lambda_function_list)

  row = 2
  function_cnt = 0
  for architectures, codeSize, description, ephemeralStorageSize, functionArn, functionName, handler, lastModified, memorySize, packageType, revisionId, role, runtime, timeout, tracingConfigMode, version in lambda_function_output:
    result_sheet.write(row, 0, function_cnt + 1, integer_format)         # No.
    result_sheet.write(row, 1, functionName, string_format)             # FunctionName
    result_sheet.write(row, 2, handler, string_format)                  # Handler
    result_sheet.write(row, 3, ", ".join(architectures), string_format) # Architectures
    result_sheet.write(row, 4, codeSize, integer_format)                # CodeSize
    result_sheet.write(row, 5, lastModified, date_format)               # LastModified
    result_sheet.write(row, 6, memorySize, integer_format)              # MemorySize
    result_sheet.write(row, 7, ephemeralStorageSize, integer_format)    # EphemeralStorageSize
    result_sheet.write(row, 8, packageType, string_format)              # PackageType
    result_sheet.write(row, 9, runtime,  string_format)                 # Runtime
    result_sheet.write(row, 10, timeout,  integer_format)               # Timeout
    result_sheet.write(row, 11, tracingConfigMode, string_format)       # TracingConfig
    result_sheet.write(row, 12, role, string_format)                    # Role
    result_sheet.write(row, 13, functionArn, string_format)             # FunctionArn
    row += 1
    function_cnt += 1

  print("-Lambda Function["+ str(function_cnt) + "]")

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['Lambda'], summary_col, function_cnt, integer_format)
  result_sheet.write(0, 1, "Lambda Function List("+ str(function_cnt) + ")", title_format)
  print("Done.\n") 

def report_secretsmanager(secretsmanager):

  Columns = ["No.", "Name", "CreatedDate", "LastChangedDate", "LastAccessedDate", "Tags", "ARN"]

  result_sheet = xlsx.add_worksheet('Secrets Manager')
  # # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "Secrets Manager List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10)  # No.
  result_sheet.set_column('B:B', 32)  # Name
  result_sheet.set_column('C:C', 17)  # CreatedDate
  result_sheet.set_column('D:D', 17)  # LastChangedDate
  result_sheet.set_column('E:E', 17)  # LastAccessedDate
  result_sheet.set_column('F:F', 32)  # Tags
  result_sheet.set_column('G:G', 102) # ARN

  secrets_list = secretsmanager.list_secrets(MaxResults=100)
  # pprint(secrets_list)
  # pprint(secrets_list['SecretList'])

  secrets_output = jmespath.search("[*].[Name, CreatedDate, LastChangedDate, LastAccessedDate, Tags, ARN]", secrets_list['SecretList'])
  # pprint(secrets_output)

  row = 2
  secrets_cnt = 0
  for name, createdDate, lastChangedDate, lastAccessedDate, tags, ARN in secrets_output:
    result_sheet.write(row, 0, secrets_cnt + 1, integer_format) # "Name", 
    result_sheet.write(row, 1, name, string_format)             # "Name", 
    result_sheet.write(row, 2, createdDate, date_format)        # "CreatedDate"
    result_sheet.write(row, 3, lastChangedDate, date_format)    # LastChangedDate
    result_sheet.write(row, 4, lastAccessedDate, date_format)   # LastAccessedDate
    tag_str = ""
    tag_cnt = 0
    if tags != '[]' and tags is not None:
      for tag in tags:
        # if tag_cnt > 1:
        #   tag_str += "\n"
        for key in tag.keys( ):
          # print(key, ":", tag[key])
          if key == "Key":
            if tag_cnt == 0:
              tag_str = (tag[key] + "=")
            else:              
              tag_str += ("\n" + tag[key] + "=")
          elif key == "Value":
            tag_str += tag[key]
        tag_cnt += 1

          # tag_str += (key + "=" + tag[key] + "\n")
          
    result_sheet.write(row, 5, tag_str, wrap_format)             # LTags
    result_sheet.write(row, 6, ARN, string_format)            # ARN

    row += 1
    secrets_cnt += 1

  print("-SecretsManager List ["+ str(secrets_cnt) +"]")

  # 자원요약으로 가기
  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


  result_sheet.write(0, 1, "Secrets Manager List("+ str(secrets_cnt) +")", title_format)
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['Secrets Manager'], summary_col, secrets_cnt, integer_format)
  print("Done.\n")  


def report_acm(acm):

  Columns = ["No.", "Domain Name", "Created At", "Imported At", "In Use", "Not After", "Not Before", "Key Algorithm", "Status", "Subject Alternative Name Summaries", "Type",  "Crtificate ARN"]

  result_sheet = xlsx.add_worksheet('AWS Certificate Manager')
  # # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "Secrets Manager List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10)  # No.
  result_sheet.set_column('B:B', 32)  # Domain Name
  result_sheet.set_column('C:C', 17)  # Created At
  result_sheet.set_column('D:D', 17)  # Imported At
  result_sheet.set_column('E:E', 12)  # In Use
  result_sheet.set_column('F:F', 17)  # Not After datetime
  result_sheet.set_column('G:G', 17)  # Not Before datetime
  result_sheet.set_column('H:H', 12)  # Key Algorithm
  result_sheet.set_column('I:I', 10)  # Status 
  result_sheet.set_column('J:J', 32)  # Subject Alternative Name Summaries 
  result_sheet.set_column('K:K', 15)  # Type
  result_sheet.set_column('L:L', 102) # Crtificate ARN

  acm_list = acm.list_certificates (
              CertificateStatuses = [
              'PENDING_VALIDATION', 'ISSUED', 'INACTIVE', 'EXPIRED', 'VALIDATION_TIMED_OUT', 'REVOKED', 'FAILED']
              )
  # pprint(acm_list)

  
  # pprint(acm_list['SecretList'])

  acm_output = jmespath.search("CertificateSummaryList[*].[CertificateArn, CreatedAt, DomainName, HasAdditionalSubjectAlternativeNames, ImportedAt, InUse, KeyAlgorithm, NotAfter, NotBefore, Status, SubjectAlternativeNameSummaries, Type]", acm_list)
  # pprint(acm_output)

  row = 2
  acm_cnt = 0
  for certificateArn, createdAt, domainName, hasAdditionalSubjectAlternativeNames, importedAt, inUse, keyAlgorithm, notAfter, notBefore, status, subjectAlternativeNameSummaries, type in acm_output:

    result_sheet.write(row, 0,  acm_cnt + 1, integer_format)    # No.
    result_sheet.write(row, 1,  domainName, string_format)      # Domain Name
    result_sheet.write(row, 2,  createdAt, date_format)         # Created At
    result_sheet.write(row, 3,  importedAt, date_format)        # Imported At
    result_sheet.write(row, 4,  inUse, string_format)           # In Use
    result_sheet.write(row, 5,  notAfter, date_format)          # Not After datetime
    result_sheet.write(row, 6,  notBefore, date_format)         # Not Before datetime
    result_sheet.write(row, 7,  keyAlgorithm, string_format)    # Key Algorithm
    result_sheet.write(row, 8,  status, string_format)          # Status 
    result_sheet.write(row, 9,  ", ".join(subjectAlternativeNameSummaries), string_format)  # Subject Alternative Name Summaries 
    result_sheet.write(row, 10,  type, string_format)           # Type
    result_sheet.write(row, 11, certificateArn, string_format)  # Crtificate ARN

    row += 1
    acm_cnt += 1
  print(f"-AWS Certificate Manager List [{str(acm_cnt)}]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


  result_sheet.write(0, 1, "AWS Certificate Manager("+ str(acm_cnt) +")", title_format)
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['AWS Certificate Manager'], summary_col, acm_cnt, integer_format)
  print("Done.\n")  



def report_kms_keys(kms):
    global result_sheet
    result_sheet = xlsx.add_worksheet('AWS Key Management Service')

    Columns = ["No.", "Key Arn", "Key Id", "Enabled", "Creation Date", "Customer Master Key Spec", "Encryption Algorithms", "Key Manager", "Key Spec", "Key State", "Key Usage", "Multi Region", "Origin", "Description"]

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 78)  # KeyArn
    result_sheet.set_column('C:C', 37)  # KeyId
    result_sheet.set_column('D:D', 10)  # Enabled
    result_sheet.set_column('E:E', 16)  # CreationDate
    result_sheet.set_column('F:F', 20)  # CustomerMasterKeySpec
    result_sheet.set_column('G:G', 22)  # EncryptionAlgorithms
    result_sheet.set_column('H:H', 12)   # KeyManager
    result_sheet.set_column('I:I', 22)  # KeySpec
    result_sheet.set_column('J:J', 12)  # KeyState
    result_sheet.set_column('K:K', 18)  # KeyUsage
    result_sheet.set_column('L:L', 7)   # MultiRegion
    result_sheet.set_column('M:M', 12)  # Origin
    result_sheet.set_column('N:N', 82)  # Description

    
    # KSM 목록 가져오기
    response = kms.list_keys()
    keys = response['Keys']

    row = 2
    for key in keys:
        key_id = key['KeyId']
        # print(f"Key ID: {key_id}")
        row = write_describe_key_to_excel(row, kms, key_id, result_sheet)


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"AWS Key Management Service List({str(row - 2)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['AWS Key Management Service'], summary_col, row - 2, integer_format)
    print(f'-AWS Key Management Service List({str(row - 2)})')
    print("Done.\n")

def write_describe_key_to_excel(row, kms, key_id, result_sheet):
    response = kms.describe_key(KeyId=key_id)
    key_metadata = response['KeyMetadata']
    result_sheet.write(row, 0, row - 1, integer_format)
    result_sheet.write(row, 1, key_metadata['Arn'], wrap_format)
    result_sheet.write(row, 2, key_metadata['KeyId'], string_format)
    result_sheet.write(row, 3, key_metadata['Enabled'], string_format)
    result_sheet.write(row, 4, key_metadata['CreationDate'], date_format)
    
    result_sheet.write(row, 5, key_metadata['CustomerMasterKeySpec'], string_format)
    
    result_sheet.write(row, 6, ", ".join(key_metadata['EncryptionAlgorithms']), string_format)
    result_sheet.write(row, 7, key_metadata['KeyManager'], wrap_format)
    result_sheet.write(row, 8, key_metadata['KeySpec'], wrap_format)
    result_sheet.write(row, 9, key_metadata['KeyState'], string_format)
    result_sheet.write(row, 10, key_metadata['KeyUsage'], string_format)
    result_sheet.write(row, 11, key_metadata['MultiRegion'], string_format)
    result_sheet.write(row, 12, key_metadata['Origin'], string_format)
    result_sheet.write(row, 13, key_metadata['Description'], string_format)
  
    
    row += 1

    return row




def report_codecommit(codecommit):

    Columns = ["No.", "Repository Name", "Default Branch", "Creation Date", "Last Modified Date", "Description", "Arn", "Account Id", "Clone Url Http", "Clone Url Ssh"]

    result_sheet = xlsx.add_worksheet('CodeCommit')
    # result_sheet.set_column('A:Z', cell_format=wrap_format)

    # result_sheet.write(0, 0, "EKS Cluster List", title_format)
    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1

    result_sheet.set_column('A:A', 10)  # No.
    result_sheet.set_column('B:B', 32)  # Repository Name
    result_sheet.set_column('C:C', 10)  # Default Branch
    result_sheet.set_column('D:D', 17)  # Creation Date
    result_sheet.set_column('E:E', 17)  # Last Modified Date
    result_sheet.set_column('F:F', 52)  # Description
    result_sheet.set_column('G:G', 82) # Arn
    result_sheet.set_column('H:H', 32)  # Account Id
    result_sheet.set_column('I:I', 82)  # Clone Url Http
    result_sheet.set_column('J:J', 82)  # Clone Url Ssh



    repositories = codecommit.list_repositories( )
    # pprint(repositories)


    # repositories = jmespath.search("repositories", repositories)
    # pprint(repositories)

    # repositories = jmespath.search("[*].repositoryName", repositories)
    # pprint(repositories)

    repositories = jmespath.search("repositories[*].repositoryName", repositories)
    # pprint(repositories)

    # repositories = jmespath.search("repositories[*].repositoryId, repositoryName]", repositories)
    # pprint(repositories)


  
    row = 2
    codecommit_cnt = 0
    for repository in repositories:
        # pprint(repository)
        # print("##################\n{0}\n##################".format(cluster))
        repository_info = codecommit.get_repository(repositoryName=repository)
        # pprint(repository_info)

        # pprint(repository_info['repositoryMetadata']['Arn'])
        repository_output = jmespath.search("repositoryMetadata.[Arn, accountId, cloneUrlHttp, cloneUrlSsh, creationDate, defaultBranch, lastModifiedDate, repositoryDescription, repositoryId, repositoryName]", repository_info)
    
        # repositoryMetadata = jmespath.search("*.repositoryMetadata", repository_info)
        # print("====")
        # pprint(repository_output)

        arn, accountId, cloneUrlHttp, cloneUrlSsh, creationDate, defaultBranch, lastModifiedDate, repositoryDescription, repositoryId, repositoryName = repository_output

        result_sheet.write(row, 0, codecommit_cnt + 1, integer_format)   # "No."" 
        result_sheet.write(row, 1, repositoryName, string_format)        # "repository Name", 
        result_sheet.write(row, 2, defaultBranch, string_format)         # "k8s version", 
        result_sheet.write(row, 3, creationDate, date_format)            # "platformVersion",
        result_sheet.write(row, 4, lastModifiedDate, date_format)        # "createdAt"
        result_sheet.write(row, 5, repositoryDescription, string_format) # "Description", 
        result_sheet.write(row, 6, arn, string_format)                   # "Arn", 
        result_sheet.write(row, 7, accountId, string_format)             # Account Id
        result_sheet.write(row, 8, cloneUrlHttp, string_format)          # Clone Url Http
        result_sheet.write(row, 9, cloneUrlSsh, string_format)           # Clone Url Ssh

        row += 1
        codecommit_cnt += 1

    print("-Code Commit ["+ str(codecommit_cnt) +"]")

    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    # print(sheetlink_pos)
    # row, col
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

    result_sheet.write(0, 1, "CodeCommit List("+ str(codecommit_cnt) + ")", title_format)
    global summary_col
    global Columns_C_POS
    summary_sheet.write(Columns_C_POS['CodeCommit'], summary_col, codecommit_cnt, integer_format)
    print("Done.\n") 


def report_codebuild(codebuild):

    Columns = ["No.", "Name", "Project Visibility", "Created", "Last Modified", "Description", "Arn", "Environment", "Service Role", "Source - type", "Source - location", "Source - BuildSpec"]

    result_sheet = xlsx.add_worksheet('CodeBuild')
    # result_sheet.set_column('A:Z', cell_format=wrap_format)

    # result_sheet.write(0, 0, "EKS Cluster List", title_format)
    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1

    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 32)  # Name
    result_sheet.set_column('C:C', 10)  # Project Visibility
    result_sheet.set_column('D:D', 17)  # Created
    result_sheet.set_column('E:E', 17)  # Last Modified
    result_sheet.set_column('F:F', 52)  # Description
    result_sheet.set_column('G:G', 82)  # Arn
    result_sheet.set_column('H:H', 82)  # Service Role
    result_sheet.set_column('I:I', 12)  # Source - type
    result_sheet.set_column('J:J', 82)  # Source - location
    result_sheet.set_column('K:K', 132)  # Source - BuildSpec
    result_sheet.set_column('L:L', 132)  # Environment




    # builds = codebuild.list_builds( )
    # pprint(builds)

    next_token = ''
    row = 2
    codebuild_cnt = 0
    while True:
        # response = client.list_projects(
        #   sortBy='NAME'|'CREATED_TIME'|'LAST_MODIFIED_TIME',
        #   sortOrder='ASCENDING'|'DESCENDING',
        #   nextToken='string'
        #   )
        if len(next_token) != 0:
            projects = codebuild.list_projects(sortBy='NAME', sortOrder='ASCENDING', nextToken=next_token)
        else:
            projects = codebuild.list_projects(sortBy='NAME', sortOrder='ASCENDING')
        # pprint(projects)
        # print("-------")


        for project in projects['projects']:
            # print(str(codebuild_cnt + 1), ' : ', project)
            project_details = codebuild.batch_get_projects(names=[project])
            # pprint(project_details)

            project_output = jmespath.search('projects[0].[arn, artifacts, badge, cache, created,  description, encryptionKey, environment, lastModified, logsConfig, name,  projectVisibility, queuedTimeoutInMinutes, secondaryArtifacts, secondarySourceVersions,  secondarySources, serviceRole, source, sourceVersion, tags, timeoutInMinutes]', project_details)
            # print("project_output: --")
            # pprint(project_output)

            arn, artifacts, badge, cache, created, description, encryptionKey, environment, lastModified, logsConfig, name,  projectVisibility, queuedTimeoutInMinutes, secondaryArtifacts, secondarySourceVersions, secondarySources, serviceRole, source, sourceVersion, tags, timeoutInMinutes = project_output

            # print("source ---")
            # pprint(source)

            source_output = jmespath.search("[buildspec,gitCloneDepth,gitSubmodulesConfig,insecureSsl,location,type]", source)
            # source_output = jmespath.search("buildspec", source)
            # print("soruce_output")
            # pprint(source_output)
            buildspec,gitCloneDepth,gitSubmodulesConfig,insecureSsl,location,type = source_output
            # print('buildspec ---')
            # print(buildspec)

            # environment_output = jmespath.search("[computeType,environmentVariables,image,imagePullCredentialsType,privilegedMode,type]", environment)

            result_sheet.write(row, 0, codebuild_cnt, integer_format)    # "No.",   
            result_sheet.write(row, 1, name, string_format)              # "Name", 
            result_sheet.write(row, 2, projectVisibility, string_format) # "Project Visibility", 
            result_sheet.write(row, 3, created, date_format)             # "Created",
            result_sheet.write(row, 4, lastModified, date_format)        # "Last Modified"
            result_sheet.write(row, 5, description, string_format)       # "Description", 
            result_sheet.write(row, 6, arn, string_format)               # "Arn", 
            result_sheet.write(row, 7, serviceRole, string_format)       # Service Role
            result_sheet.write(row, 8, type, string_format)              # Source - type
            result_sheet.write(row, 9, location, string_format)          # Source - location
            result_sheet.write(row, 10, buildspec, wrap_format)          # Source - BuildSpec
            environment_str = ''
            exclude_key = "environmentVariables"
            for key, value in environment.items():
                environment_str += f"{key}: {value}\n"
            result_sheet.write(row, 10, environment_str, wrap_format)  # Environment

            row += 1
            codebuild_cnt += 1

        if 'nextToken' in projects:
            next_token = projects['nextToken']
        else:
            break

    print("-Code Build ["+ str(codebuild_cnt) +"]")

    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    # print(sheetlink_pos)
    # row, col
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

    result_sheet.write(0, 1, "CodeBuild List("+ str(codebuild_cnt) + ")", title_format)
    global summary_col
    global Columns_C_POS
    summary_sheet.write(Columns_C_POS['CodeBuild'], summary_col, codebuild_cnt, integer_format)
    print("Done.\n") 


def report_codedeploy(codedeploy):

    Columns = ["No.", "Application Name", "Deployment Groups", "Deployment Style", "Compute Platform", "Deployment ConfigName", "Service Role ARN", "Last Attempted Deployment - createTime", "Last Attempted Deployment - endTime", "Last Attempted Deployment - status"]

    result_sheet = xlsx.add_worksheet('CodeDeploy')
    # result_sheet.set_column('A:Z', cell_format=wrap_format)

    # result_sheet.write(0, 0, "EKS Cluster List", title_format)
    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1

    result_sheet.set_column('A:A', 10)  # No.
    result_sheet.set_column('B:B', 32)  # Application Name
    result_sheet.set_column('C:C', 30)  # Deployment Groups
    result_sheet.set_column('D:D', 42)  # Deployment Style
    result_sheet.set_column('E:E', 17)  # Compute Platform
    result_sheet.set_column('F:F', 32)  # Deployment ConfigName
    result_sheet.set_column('G:G', 72)  # Service Role ARN
    result_sheet.set_column('H:H', 17)  # Last Attempted Deployment - createTime
    result_sheet.set_column('I:I', 17)  # Last Attempted Deployment - endTime
    result_sheet.set_column('J:J', 12)  # Last Attempted Deployment - status





    # builds = codebuild.list_builds( )
    # pprint(builds)

    next_token = ''
    row = 2
    codedeploy_cnt = 0
    while True:
        # response = client.list_projects(
        #   sortBy='NAME'|'CREATED_TIME'|'LAST_MODIFIED_TIME',
        #   sortOrder='ASCENDING'|'DESCENDING',
        #   nextToken='string'
        #   )
        if len(next_token) != 0:
            deployments = codedeploy.list_deployments(nextToken=next_token)
        else:
            deployments = codedeploy.list_deployments( )
        # pprint(deployments)
        # print("-------")


        if len(next_token) != 0:
            applications = codedeploy.list_applications(nextToken=next_token)
        else:
            applications = codedeploy.list_applications( )
        # pprint(applications)
        # print("-------")


        for application in applications['applications']:
            # print(str(codedeploy_cnt + 1), ' : ', application)
            deployment_groups_details = codedeploy.list_deployment_groups(applicationName=application)
            # pprint(deployment_groups_details)

            for deployment_group in deployment_groups_details['deploymentGroups']:
                # pprint(deployment_group)

                deployment_group_detail = codedeploy.get_deployment_group(
                    applicationName=application,
                    deploymentGroupName=deployment_group)

                # pprint(deployment_group_detail)

                deployment_group_output = jmespath.search('deploymentGroupInfo.[alarmConfiguration, applicationName, autoScalingGroups, computePlatform, deploymentConfigName,  deploymentGroupId, deploymentGroupName, deploymentStyle, ec2TagFilters, lastAttemptedDeployment, onPremisesInstanceTagFilters,  outdatedInstancesStrategy, serviceRoleArn, triggerConfigurationss]', deployment_group_detail)
                # print("deployment_group_output: --")
                # pprint(deployment_group_output)

                alarmConfiguration, applicationName, autoScalingGroups, computePlatform, deploymentConfigName,  deploymentGroupId, deploymentGroupName, deploymentStyle, ec2TagFilters, lastAttemptedDeployment, onPremisesInstanceTagFilters,  outdatedInstancesStrategy, serviceRoleArn, triggerConfigurationss = deployment_group_output

                if lastAttemptedDeployment is not None:
                # print("lastAttemptedDeployment ---")
                # pprint(lastAttemptedDeployment)

                    lastAttemptedDeployment_output = jmespath.search("[createTime,deploymentId,endTime,status]", lastAttemptedDeployment)
                    # source_output = jmespath.search("buildspec", source)
                    # print("soruce_output")
                    # pprint(source_output)
                    createTime, deploymentId, endTime, status = lastAttemptedDeployment_output
                    # print('createTime ---')
                    # print(createTime)

 
                result_sheet.write(row, 0, codedeploy_cnt + 1, string_format) # No. 
                result_sheet.write(row, 1, applicationName, string_format)            # Application Name 
                result_sheet.write(row, 2, deploymentGroupName, string_format)        # Deployment Groups 
                deploymentStyle_str = ''
                # exclude_key = "environmentVariables"
                for key, value in deploymentStyle.items():
                    deploymentStyle_str += f"{key}: {value}\n"

                result_sheet.write(row, 3, deploymentStyle_str, wrap_format) # Deployment Style
                result_sheet.write(row, 4, computePlatform, date_format) # Compute Platform        
                result_sheet.write(row, 5, deploymentConfigName, string_format) # Deployment ConfigName
                result_sheet.write(row, 6, serviceRoleArn, string_format) # Service Role ARN
                if lastAttemptedDeployment is not None:
                    result_sheet.write(row, 7, createTime, string_format)  # Last Attempted Deployment - createTime
                    result_sheet.write(row, 8, endTime, string_format)  # Last Attempted Deployment - endTime
                    result_sheet.write(row, 9, status, string_format)  # Last Attempted Deployment - status


            row += 1
            codedeploy_cnt += 1

        # if 'nextToken' in projects:
        #   next_token = projects['nextToken']
        # else:
        #   break
        break

    print("-Code Depoloy ["+ str(codedeploy_cnt) +"]")

    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    # print(sheetlink_pos)
    # row, col
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

    result_sheet.write(0, 1, "CodeDeploy List("+ str(codedeploy_cnt) + ")", title_format)
    global summary_col
    global Columns_C_POS
    summary_sheet.write(Columns_C_POS['CodeDeploy'], summary_col, codedeploy_cnt, integer_format)
    print("Done.\n") 


def report_codepipeline(codepipeline):

  Columns = ["No.", "Name", "Created", "Updated", "Version", "Stages", "Artifact Store", "Pipeline Arn", "Role ARN"]

  result_sheet = xlsx.add_worksheet('CodePipeline')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "EKS Cluster List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10)  # No.
  result_sheet.set_column('B:B', 32)  # Name
  result_sheet.set_column('C:C', 17)  # Created
  result_sheet.set_column('D:D', 17)  # Updated
  result_sheet.set_column('E:E',  7)  # Version
  result_sheet.set_column('F:F', 17)  # Stages
  result_sheet.set_column('G:G', 72)  # Artifact Store
  result_sheet.set_column('H:H', 72)  # Pipeline Arn
  result_sheet.set_column('I:I', 82)  # Role ARN




  # builds = codebuild.list_builds( )
  # pprint(builds)

  next_token = ''
  # row = 2
  row = 3 # merget write 시 사용하는 range format ('A1:A3') 을 쓸경우 row, cell 포맷과 달리 + 1 하여야 함
  codepipeline_cnt = 0
  while True:
    if len(next_token) != 0:
      pipelines = codepipeline.list_pipelines(nextToken=next_token, maxResults=100)
    else:
      pipelines = codepipeline.list_pipelines( )
    # pprint(pipelines)
    # print("-------")

    for pipeline in pipelines['pipelines']:
      pipeline_output = jmespath.search('[name, created, updated, version]', pipeline)
      name, created, updated, version = pipeline_output
      pipeline_name = pipeline['name']
      # print(str(codepipeline_cnt + 1), ' : ', pipeline_name)
      pipeline_info = codepipeline.get_pipeline(name=pipeline_name)
      # pprint(pipeline_info)

      metadata_info_output = jmespath.search('metadata.[created, pipelineArn, updated]', pipeline_info)
      created, pipelineArn, updated = metadata_info_output

      pipeline_info_output = jmespath.search('pipeline.[artifactStore, name, roleArn, stages, version]', pipeline_info)

      artifactStore, name, roleArn, stages, version = pipeline_info_output

      stage_cnt = len(stages)
      
      # xlsxwriter.exceptions.OverlappingRange: Merge range 'A6:A10' overlaps previous merge range 'A2:A6'.
      # row + stage_cnt 할 경우 위의 오류 발생
      
      range_ = 'A' + str(row) + ':' + 'A' + str(row + stage_cnt - 1)
      result_sheet.merge_range(range_, codepipeline_cnt + 1, integer_format) # No.
      
      # result_sheet.write(row, 0, name, string_format)  # Name 
      range_ = 'B' + str(row) + ':' + 'B' + str(row + stage_cnt - 1)
      result_sheet.merge_range(range_, name, string_format) # Name

      # result_sheet.write(row, 1, created, date_format)    # Created
      range_ = 'C' + str(row) + ':' + 'C' + str(row + stage_cnt - 1)
      result_sheet.merge_range(range_, created, date_format) # Created

      # result_sheet.write(row, 2, updated, date_format)    # Updated
      range_ = 'D' + str(row) + ':' + 'D' + str(row + stage_cnt - 1)
      result_sheet.merge_range(range_, updated, date_format)    # Updated


      # result_sheet.write(row, 3, version, string_format)  # Version
      range_ = 'E' + str(row) + ':' + 'E' + str(row + stage_cnt - 1)
      result_sheet.merge_range(range_, version, string_format)  # Version
      

      artifactStore_str = json.dumps(artifactStore,indent=2)
      # result_sheet.write(row + stage_cnt, 5, name, string_format)  # Artifact Store
      range_ = 'G' + str(row) + ':' + 'G' + str(row + stage_cnt - 1)
      result_sheet.merge_range(range_, artifactStore_str, wrap_format)  # Artifact Store

    
      # result_sheet.write(row + stage_cnt + 1, 6, pipelineArn, string_format)  # Pipeline Arn
      range_ = 'H' + str(row) + ':' + 'H' + str(row + stage_cnt - 1)
      result_sheet.merge_range(range_, pipelineArn, string_format)  # Pipeline Arn
      
      
      # result_sheet.write(row + stage_cnt + 2, 7, roleArn, string_format)  # Role ARN
      range_ = 'I' + str(row) + ':' + 'I' + str(row + stage_cnt - 1)
      result_sheet.merge_range(range_, roleArn, string_format)  # Role ARN

      # print(name)
      stage_str = ""
      offset = 0
      for stage in stages:
        # pprint(stage)
        # print("        ", stage['actions'][0]['name'])
        # print(stage_cnt, json.dumps(stage, indent=2))
        stage_str = json.dumps(stage, indent=2)
        pos = 'F' + str(row + offset)
        # result_sheet.write(row + offset, 4, "        " + stage['actions'][0]['name'] + "\n", wrap_format)    # Stages
        # result_sheet.write_comment(row + offset, 4, stage_str, wrap_format)
        result_sheet.write(pos, "        " + stage['actions'][0]['name'] + "\n", wrap_format)    # Stages
        result_sheet.write_comment(pos, stage_str)

        offset += 1

      # row += 1
      row += offset
      codepipeline_cnt += 1

    # if 'nextToken' in projects:
    #   next_token = projects['nextToken']
    # else:
    #   break
    break

  print("-Code Pipeline ["+ str(codepipeline_cnt) +"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  result_sheet.write(0, 1, "CodePipeline List("+ str(codepipeline_cnt) + ")", title_format)
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['CodePipeline'], summary_col, codepipeline_cnt, integer_format)
  print("Done.\n") 

def report_codeartifact(codeartifact):

  Columns = ["No.", "Name", "Domain Name", "Domain Owner", "Administrator Account", "Description", "ARN", "End Point"]

  result_sheet = xlsx.add_worksheet('CodeArtifact')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "EKS Cluster List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10)  # No.
  result_sheet.set_column('B:B', 32)  # Name
  result_sheet.set_column('C:C', 17)  # Domain Name
  result_sheet.set_column('D:D', 13)  # Domain Owner
  result_sheet.set_column('E:E', 13)  # Administrator Account
  result_sheet.set_column('F:F', 52)  # Description
  result_sheet.set_column('G:G', 72)  # ARN
  result_sheet.set_column('H:H', 72)  # End Point



  # builds = codebuild.list_builds( )
  # pprint(builds)

  # List repositories
  next_token = ''
  row = 2
  codeartifact_cnt = 0
  while True:
    if len(next_token) != 0:
      repositories = codeartifact.list_repositories(nextToken=next_token, maxResults=100)
    else:
      # repositories = codeartifact.list_repositories(repositoryPrefix='nextoss', maxResults=100)
      repositories = codeartifact.list_repositories(maxResults=100)
    # pprint(repositories)
    # print("-------")


    for repository in repositories['repositories']:
      # pprint(repository)
      repository_output = jmespath.search('[administratorAccount, arn, description, domainName, domainOwner, name]', repository)

      administratorAccount, arn, description, domainName, domainOwner, name = repository_output
      
      # Get repository endpoint
      # response = client.get_repository_endpoint(
      #               domain='string',
      #               domainOwner='string',
      #               repository='string',
      #               format='npm'|'pypi'|'maven'|'nuget'|'generic')
      # print(f"{name}: {domainName}\n")
      endpoint = codeartifact.get_repository_endpoint(domain=domainName, repository=name, format='maven')
      # pprint(endpoint)

      endpoint_output = jmespath.search('[repositoryEndpoint]', endpoint)
      repositoryEndpoint = endpoint_output
      # print(repositoryEndpoint)
      

      # Get package version      
      # package_version_asset = codeartifact.get_package_version_readme(
      #               domain=domainName,
      #               repository=name,
      #               format='maven',
      #               package='*',
      #               packageVersion='*')
      #               # Unknown parameter in input: "package_version", must be one of: domain, domainOwner, repository, format, namespace, package, packageVersion, asset, packageVersionRevision
      #               # namespace='namespace',
      #               # package='package',
      #               # package_version='package-version')
      # pprint(package_version_asset)
      # break
      
      # name, created, updated, version = pipeline_output
      # pipeline_name = pipeline['name']
      # print(str(codepipeline_cnt + 1), ' : ', pipeline_name)
      # pipeline_info = codepipeline.get_pipeline(name=pipeline_name)
      # # pprint(pipeline_info)

      # metadata_info_output = jmespath.search('metadata.[created, pipelineArn, updated]', pipeline_info)
      # created, pipelineArn, updated = metadata_info_output

      # pipeline_info_output = jmespath.search('pipeline.[artifactStore, name, roleArn, stages, version]', pipeline_info)

      # artifactStore, name, roleArn, stages, version = pipeline_info_output

      result_sheet.write(row, 0, codeartifact_cnt + 1, integer_format) # "Name", 
      result_sheet.write(row, 1, name, string_format)                  # "Name", 
      result_sheet.write(row, 2, domainName, string_format)            # "Domain Name"
      result_sheet.write(row, 3, domainOwner, string_format)           # "Domain Owner"
      result_sheet.write(row, 4, administratorAccount, string_format)  # Administrator Account"
      result_sheet.write(row, 5, description, string_format)           # "Description",
      result_sheet.write(row, 6, arn, string_format)                   # "ARN"
      result_sheet.write(row, 7, repositoryEndpoint[0], string_format) # "End Point"


      row += 1
      # row += offset
      codeartifact_cnt += 1

    # if 'nextToken' in projects:
    #   next_token = projects['nextToken']
    # else:
    #   break
    break

  print("-Code Artifact ["+ str(codeartifact_cnt) +"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  result_sheet.write(0, 1, f"Code Artifact List({codeartifact_cnt})", title_format)
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['CodeArtifact'], summary_col, codeartifact_cnt, integer_format)
  print("Done.\n") 




def report_cloudwatch_alarms(cloudwatch):
  # {'ActionsEnabled': True,
  #  'AlarmActions': ['arn:aws:automate:ap-northeast-2:ec2:recover'],
  #  'AlarmArn': 'arn:aws:cloudwatch:ap-northeast-2:123456789012:alarm:StatusCheckFailedSystem-Alarm-for-sksh-argos-p-sol-sear-ec2-2c-01',
  #  'AlarmConfigurationUpdatedTimestamp': datetime.datetime(2023, 4, 7, 9, 8, 25, 691000, tzinfo=tzutc()),
  #  'AlarmDescription': 'Alarm when status check fails on '
  #                      'i-04f5cbb3cc4a6da4a(sksh-argos-p-sol-sear-ec2-2c-01) ',
  #  'AlarmName': 'StatusCheckFailedSystem-Alarm-for-sksh-argos-p-sol-sear-ec2-2c-01',
  #  'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
  #  'Dimensions': [{'Name': 'InstanceId', 'Value': 'i-04f5cbb3cc4a6da4a'}],
  #  'EvaluationPeriods': 1,
  #  'InsufficientDataActions': [],
  #  'MetricName': 'StatusCheckFailed_System',
  #  'Namespace': 'AWS/EC2',
  #  'OKActions': [],
  #  'Period': 60,
  #  'StateReason': 'Threshold Crossed: 1 datapoint [0.0 (07/04/23 09:08:00)] was '
  #                 'not greater than or equal to the threshold (1.0).',
  #  'StateReasonData': '{"version":"1.0","queryDate":"2023-04-07T09:09:36.306+0000","startDate":"2023-04-07T09:08:00.000+0000","unit":"Count","statistic":"Minimum","period":60,"recentDatapoints":[0.0],"threshold":1.0,"evaluatedDatapoints":[{"timestamp":"2023-04-07T09:08:00.000+0000","sampleCount":1.0,"value":0.0}]}',
  #  'StateTransitionedTimestamp': datetime.datetime(2023, 4, 7, 9, 9, 36, 311000, tzinfo=tzutc()),
  #  'StateUpdatedTimestamp': datetime.datetime(2023, 4, 7, 9, 9, 36, 311000, tzinfo=tzutc()),
  #  'StateValue': 'OK',
  #  'Statistic': 'Minimum',
  #  'Threshold': 1.0,
  #  'Unit': 'Count'}

  # {'ActionsEnabled': True,
  # 'AlarmActions': ['arn:aws:sns:ap-northeast-2:123456789012:PRD_Argos_Shield_Advanced'],
  # 'AlarmArn': 'arn:aws:cloudwatch:ap-northeast-2:123456789012:alarm:DDoSDetectedAlarmForProtection_2548fc3644f7bb5e',     
  # 'AlarmConfigurationUpdatedTimestamp': datetime.datetime(2023, 4, 14, 1, 52, 40, 978000, tzinfo=tzutc()),
  # 'AlarmDescription': 'Alarm for DDoS events detected on resource '
  #                     'arn:aws:elasticloadbalancing:ap-northeast-2:123456789012:loadbalancer/app/sksh-argos-p-ec2-arg-alb-pub/2548fc3644f7bb5e',
  # 'AlarmName': 'DDoSDetectedAlarmForProtection_2548fc3644f7bb5e',
  # 'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
  # 'DatapointsToAlarm': 1,
  # 'Dimensions': [{'Name': 'ResourceArn',
  #                 'Value': 'arn:aws:elasticloadbalancing:ap-northeast-2:123456789012:loadbalancer/app/sksh-argos-p-ec2-arg-alb-pub/2548fc3644f7bb5e'}],
  # 'EvaluationPeriods': 20,
  # 'InsufficientDataActions': [],
  # 'MetricName': 'DDoSDetected',
  # 'Namespace': 'AWS/DDoSProtection',
  # 'OKActions': [],
  # 'Period': 60,
  # 'StateReason': 'Threshold Crossed: no datapoints were received for 20 periods '
  #                 'and 20 missing datapoints were treated as [NonBreaching].',
  # 'StateReasonData': '{"version":"1.0","queryDate":"2023-04-14T01:54:24.794+0000","statistic":"Sum","period":60,"recentDatapoints":[],"threshold":1.0,"evaluatedDatapoints":[{"timestamp":"2023-04-14T01:53:00.000+0000"},{"timestamp":"2023-04-14T01:52:00.000+0000"},{"timestamp":"2023-04-14T01:51:00.000+0000"},{"timestamp":"2023-04-14T01:50:00.000+0000"},{"timestamp":"2023-04-14T01:49:00.000+0000"},{"timestamp":"2023-04-14T01:48:00.000+0000"},{"timestamp":"2023-04-14T01:47:00.000+0000"},{"timestamp":"2023-04-14T01:46:00.000+0000"},{"timestamp":"2023-04-14T01:45:00.000+0000"},{"timestamp":"2023-04-14T01:44:00.000+0000"},{"timestamp":"2023-04-14T01:43:00.000+0000"},{"timestamp":"2023-04-14T01:42:00.000+0000"},{"timestamp":"2023-04-14T01:41:00.000+0000"},{"timestamp":"2023-04-14T01:40:00.000+0000"},{"timestamp":"2023-04-14T01:39:00.000+0000"},{"timestamp":"2023-04-14T01:38:00.000+0000"},{"timestamp":"2023-04-14T01:37:00.000+0000"},{"timestamp":"2023-04-14T01:36:00.000+0000"},{"timestamp":"2023-04-14T01:35:00.000+0000"},{"timestamp":"2023-04-14T01:34:00.000+0000"}]}',
  # 'StateTransitionedTimestamp': datetime.datetime(2023, 4, 14, 1, 54, 24, 800000, tzinfo=tzutc()),
  # 'StateUpdatedTimestamp': datetime.datetime(2023, 4, 14, 1, 54, 24, 800000, tzinfo=tzutc()),
  # 'StateValue': 'OK',
  # 'Statistic': 'Sum',
  # 'Threshold': 1.0,
  # 'TreatMissingData': 'notBreaching'}

  Columns = ["No.", "Alarm Name", "Dimensions", "Actions Enabled", "Alarm Actions", "Alarm Configuration Updated Timestamp", "Namespace", "Metric Name", "Unit", "Threshold", "Statistic", "Alarm Description", "Alarm ARN"]

  result_sheet = xlsx.add_worksheet('CloudWatch Alarms')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "EKS Cluster List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10)  # No.
  result_sheet.set_column('B:B', 52)  # Alarm Name
  result_sheet.set_column('C:C', 32)  # Dimensions
  result_sheet.set_column('D:D', 7)   # Actions Enabled
  result_sheet.set_column('E:E', 62)  # Alarm Actions
  result_sheet.set_column('F:F', 17)  # Alarm Configuration Updated Timestamp
  result_sheet.set_column('G:G', 12)  # Namespace
  result_sheet.set_column('H:H', 32)  # Metric Name
  result_sheet.set_column('I:I', 32)  # Unit
  result_sheet.set_column('J:J', 7)   # Threshold
  result_sheet.set_column('K:K', 12)   # Statistic
  result_sheet.set_column('L:L', 35)  # Alarm Description
  result_sheet.set_column('M:M', 142)  # Alarm ARN



  next_token = ''
  cloudwatch_alarms_cnt = 0
  row = 2
  while True:
    alarms = cloudwatch.describe_alarms(MaxRecords=10, NextToken=next_token)
    for alarm in alarms['MetricAlarms']:
      # print(alarm['AlarmName'])

      alarm_output = jmespath.search('[ActionsEnabled, AlarmActions, AlarmArn, AlarmConfigurationUpdatedTimestamp, AlarmDescription, AlarmName, Dimensions, EvaluationPeriods, InsufficientDataActions, MetricName, Namespace, Period, StateReason, StateReasonData, StateUpdatedTimestamp, StateValue, Statistic, Threshold, Unit]', alarm)

      # if cloudwatch_alarms_cnt == 0:
      #   pprint(alarm)
        # alarm_json = json.dumps(alarm, indent=2)
        # print(alarm_json)
        # pprint(alarm_output)
      

      actionsEnabled, alarmActions, alarmArn, alarmConfigurationUpdatedTimestamp, alarmDescription, alarmName, dimensions, evaluationPeriods, insufficientDataActions, metricName, namespace, period, stateReason, stateReasonData, stateUpdatedTimestamp, stateValue, statistic, threshold, unit = alarm_output

      # pprint(f'{alarmName} : {alarmDescription}')
      # print("-------")



      # "Alarm Name", "Dimensions", "Actions Enabled", "Alarm Actions", "Alarm Configuration Updated Timestamp", "Namespace", "Metric Name", "Unit", "Threshold", "Statistic", "Alarm Description", "Alarm ARN"

      result_sheet.write(row,  0, cloudwatch_alarms_cnt + 1, integer_format)  # Alarm Name      
      result_sheet.write(row,  1, alarmName, string_format)  # Alarm Name      
      
      if dimensions is not None:
        if len(dimensions) > 0:
          result_sheet.write(row,  2, json.dumps(dimensions[0], indent=2), wrap_format)  # Dimensions
      
      result_sheet.write(row,  3, actionsEnabled, string_format)   # Actions Enabled
      # '.'.join(arr) if len(arr) > 1 else ' '
      # pprint(alarmActions)
      # print(f'alarmActions len[{len(alarmActions)}]')
      # string_list = ["apple", "banana", "cherry", "apple", "banana", "cherry"]
      # count = len(string_list) if isinstance(string_list, list) else 0
      # print(count)
      result_sheet.write(row,  4, alarmActions[0] if len(alarmActions)  >= 1 else '-', string_format)  # Alarm Actions
      # result_sheet.write(row,  3, alarmActions.join(', ') if isinstance(alarmActions, list)  >= 1 else '-', string_format)  # Alarm Actions
      result_sheet.write(row,  5, alarmConfigurationUpdatedTimestamp, date_format)  # Alarm Configuration Updated Timestamp
      result_sheet.write(row,  6, namespace, string_format)  # Namespace
      result_sheet.write(row,  7, metricName, string_format)  # Metric Name
      result_sheet.write(row,  8, unit, string_format)   # Unit
      result_sheet.write(row,  9, threshold, string_format)   # Threshold
      result_sheet.write(row, 10, statistic, string_format)  # Statistic
      result_sheet.write(row, 11, alarmDescription, wrap_format)  # Alarm Description
      result_sheet.write(row, 12, alarmArn, string_format)  # Alarm ARN

      cloudwatch_alarms_cnt += 1
      row += 1

    if 'NextToken' not in alarms:
      break
    next_token = alarms['NextToken']

      # if 'nextToken' in projects:
      #   next_token = projects['nextToken']
      # else:
      #   break


  print("-CodeWatch Alarms ["+ str(cloudwatch_alarms_cnt) +"]")

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  result_sheet.write(0, 1, "CloudWatch Alarms List("+ str(cloudwatch_alarms_cnt) + ")", title_format)
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['CloudWatch Alarms'], summary_col, cloudwatch_alarms_cnt, integer_format)
  print("Done.\n") 


def report_cloudwatch_metrics(cloudwatch):
    global result_sheet
    result_sheet = xlsx.add_worksheet('CloudWatch Metrics')

    # 제목 추가
    # result_sheet.write(0, 1, "CloudWatch Metrics", title_format)

    # 행 병합
    result_sheet.merge_range('A2:A3', 'No', colname_format)
    result_sheet.merge_range('B2:B3', 'Namespace', colname_format)
    result_sheet.merge_range('C2:C3', 'MetricName', colname_format)

    # 열 병합
    # worksheet.write('D1:E1', "Dimensions", bold_format)
    result_sheet.merge_range('D2:E2', 'Dimensions', colname_format)
    result_sheet.write('D3',    "Name", colname_format)
    result_sheet.write('E3',    "Value", colname_format)


    result_sheet.set_column('A:A', 9)  # No
    result_sheet.set_column('B:B', 32) # Namespace
    result_sheet.set_column('C:C', 32)  # MetricName
    result_sheet.set_column('D:D', 32)  # Dimensions - NAME
    result_sheet.set_column('E:E', 52)  # Dimensions - Value


    # CloudWatch 리소스 목록 가져오기
    response = cloudwatch.list_metrics()
    metrics = response['Metrics']

    # print("CloudWatch Metrics:")
    row = 3
    no  = 0
    for metric in metrics:
        # print(f"- {metric['Namespace']} - {metric['MetricName']}")
        # print(f"- [{no:10,d}]{metric['Namespace']} - {metric['MetricName']}")
        # pprint(metric)
        row, no = write_metrics_to_excel(row, no, result_sheet, metric)

        # 페이징 토큰 사용하여 추가 메트릭 가져오기
        while 'NextToken' in response:
            next_token = response['NextToken']
            response = cloudwatch.list_metrics(NextToken=next_token)
            metrics = response['Metrics']

            # print("Additional Metrics:")
            for metric in metrics:
                # print(f"- [{no:10,d}]{metric['Namespace']} - {metric['MetricName']}")
                row, no = write_metrics_to_excel(row, no, result_sheet, metric)


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    # print(sheetlink_pos)
    # row, col
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

    result_sheet.write(0, 1, f"CloudWatch Metrics List({str(no)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['CloudWatch Metrics'], summary_col, no, integer_format)

def write_metrics_to_excel(row, no, result_sheet, metric):
    dimensions = metric['Dimensions']
    dimension_cnt = 0
    for dimension in dimensions:            
        dimension_cnt += 1


    if dimension_cnt == 1 or dimension_cnt == 0:
        # print(f'row[{row}] dimension_cnt[{dimension_cnt}]')
        result_sheet.write(row, 0, no + 1, string_format)
        result_sheet.write(row, 1, metric['Namespace'], string_format)
        result_sheet.write(row, 2, metric['MetricName'], string_format)
    else:
        cell_row        = f'A{row + 1}:A{row + dimension_cnt}'
        cell_namespace  = f'B{row + 1}:B{row + dimension_cnt}'
        cell_metricname = f'C{row + 1}:C{row + dimension_cnt}'
        # print(f'row[{row}] dimension_cnt[{dimension_cnt}] [{cell_row}, {cell_namespace}, {cell_metricname}]')
        result_sheet.merge_range(cell_row, no + 1, string_format)
        result_sheet.merge_range(cell_namespace, metric['Namespace'], string_format)
        result_sheet.merge_range(cell_metricname, metric['MetricName'], string_format)             
    
    # dimensions = metric['Dimensions']
    for dimension in dimensions:
        result_sheet.write(row, 3, dimension['Name'], string_format)
        result_sheet.write(row, 4, dimension['Value'], string_format)
        row += 1
    if dimension_cnt == 0:
        row += 1
    no += 1    
    return row, no



def report_cloudwatch_logs(cloudwatch_logs):
  # {'arn': 'arn:aws:logs:ap-northeast-2:123456789012:log-group:/aws-glue/crawlers:*',
  # 'creationTime': 1659398509262,
  # 'logGroupName': '/aws-glue/crawlers',
  # 'metricFilterCount': 0,
  # 'storedBytes': 205779}

  Columns = ["No.", "Log Group Name", "Creation Time", "Metric Filter Count", "Stored Bytes", "ARN"]

  result_sheet = xlsx.add_worksheet('CloudWatch Logs')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # result_sheet.write(0, 0, "EKS Cluster List", title_format)
  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 10)   # No.
  result_sheet.set_column('B:B', 52)   # Log Group Name
  result_sheet.set_column('C:C', 17)   # Creation Time
  result_sheet.set_column('D:D', 7)    # Metric Filter Count
  result_sheet.set_column('E:E', 22)   # Stored Bytes
  result_sheet.set_column('F:F', 142)  # ARN


  logGroups = cloudwatch_logs.describe_log_groups()

  next_token = ''
  cloudwatch_logs_cnt = 0
  row = 2
  for logGroup in logGroups['logGroups']:
    # print(logGroup['logGroupName'])

    logGroup_output = jmespath.search('[arn, creationTime, logGroupName, metricFilterCount, storedBytes]', logGroup)

    # if cloudwatch_logs_cnt == 0:
    #   pprint(logGroup['logGroupName'])
      # alarm_json = json.dumps(alarm, indent=2)
      # print(alarm_json)
      # pprint(alarm_output)
      

    arn, creationTime, logGroupName, metricFilterCount, storedBytes = logGroup_output

    date = pd.to_datetime(creationTime, utc=True, unit='ms')

    # pprint(f"{logGroupName} : {(date + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}")
    # print("-------")



    result_sheet.write(row,  0, cloudwatch_logs_cnt + 1, integer_format)  # No.  
    result_sheet.write(row,  1, logGroupName, string_format)              # Log Group Name
    result_sheet.write(row,  2, (date + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S'), string_format)  # Creation Time
    result_sheet.write(row,  3, metricFilterCount, integer_format)        # Metric Filter Count
    result_sheet.write(row,  4, storedBytes, integer_format)              # Stored Bytes
    result_sheet.write(row,  5, arn, string_format)                       # Alarm Configuration Updated Timestamp


    cloudwatch_logs_cnt += 1
    row += 1


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  # print(sheetlink_pos)
  # row, col
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  print("-CodeWatch Logs ["+ str(cloudwatch_logs_cnt) +"]")
  result_sheet.write(0, 1, "CloudWatch Logs List("+ str(cloudwatch_logs_cnt) + ")", title_format)
  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['CloudWatch Logs'], summary_col, cloudwatch_logs_cnt, integer_format)
  print("Done.\n") 



def report_cloudwatch_events(events):
    global result_sheet
    result_sheet = xlsx.add_worksheet('CloudWatch Events')

    Columns = ["No.", "Name", "State", "EventBusName", "ManagedBy", "ScheduleExpression", "Description", "Arn", "EventPattern"]

    # result_sheet.write(0, 0, "CloudWatch Events List", title_format)

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 42)  # Name
    result_sheet.set_column('C:C', 9)   # State
    result_sheet.set_column('D:D', 15)  # EventBusName
    result_sheet.set_column('E:E', 32)  # ManagedBy
    result_sheet.set_column('F:F', 20)  # ScheduleExpression
    result_sheet.set_column('G:G', 42)  # Description
    result_sheet.set_column('H:H', 52)  # Arn
    result_sheet.set_column('I:I', 52) # EventPattern
    
    
    # CloudWatch Events 규칙 목록 가져오기
    response = events.list_rules()
    rules = response['Rules']

    print("CloudWatch Events Rules:")
    row = 2
    for rule in rules:
        # print(f"- {rule['Name']}")
        # pprint(rule)

        result_sheet.write(row, 0, row - 1, integer_format)
        result_sheet.write(row, 1, rule['Name'], wrap_format)
        result_sheet.write(row, 2, rule['State'], string_format)
        result_sheet.write(row, 3, rule['EventBusName'], string_format)
        
        if 'ManagedBy' in rule:
            result_sheet.write(row, 4, rule['ManagedBy'], string_format)
        else:
            result_sheet.write(row, 4, '-', string_format)
        
        if 'ScheduleExpression' in rule:
            result_sheet.write(row, 5, rule['ScheduleExpression'], string_format)
        else:
            result_sheet.write(row, 5, '-', string_format)
        
       
        if 'Description' in rule:
            result_sheet.write(row, 6, rule['Description'], wrap_format)
        else:
            result_sheet.write(row, 6, '-', string_format)
        
        result_sheet.write(row, 7, rule['Arn'], wrap_format)
        
        if 'EventPattern' in rule:
            json_data = json.loads(rule['EventPattern'])
            result_sheet.write(row, 9, json.dumps(json_data,indent=2), wrap_format)
            # result_sheet.write(row, 8, rule['EventPattern'], wrap_format)
        else:
            result_sheet.write(row, 9, '-', string_format)
        
        row += 1


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"CloudWatch Events List({str(row - 2)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['CloudWatch Events'], summary_col, row - 2, integer_format)
    print("Done.\n")



def report_cloudtrail_trails(cloudtrail):
    global result_sheet
    result_sheet = xlsx.add_worksheet('CloudTrail')

    Columns = ["No.", "Name", "S3 BucketName", "LogFile Validation Enabled", "Is Organization Trail", "Is Multi Region Trail", "Include Global Service Events", "Home Region", "Has Insight Selectors", "Has Custom Event Selectors", "Cloud WatchLogs Log Group Arn", "CloudWatchLogs Role Arn"]

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 82)  # Name
    result_sheet.set_column('C:C', 32)  # S3BucketName
    result_sheet.set_column('D:D', 7)   # LogFileValidationEnabled
    result_sheet.set_column('E:E', 7)   # IsOrganizationTrail
    result_sheet.set_column('F:F', 7)   # IsMultiRegionTrail
    result_sheet.set_column('G:G', 7)   # IncludeGlobalServiceEvents
    result_sheet.set_column('H:H', 17)  # HomeRegion
    result_sheet.set_column('I:I', 7)   # HasInsightSelectors
    result_sheet.set_column('J:J', 7)   # HasCustomEventSelectors
    result_sheet.set_column('K:K', 72)  # CloudWatchLogsLogGroupArn
    result_sheet.set_column('L:L', 92)  # CloudWatchLogsRoleArn

    
    
    #  # CloudTrail 추적 목록 가져오기
    response = cloudtrail.describe_trails()
    trails = response['trailList']

    row = 2
    for trail in trails:
        row = write_trail_to_excel(row, trail, result_sheet)


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"CloudTrail List({str(row - 2)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['CloudTrail'], summary_col, row - 2, integer_format)
    print(f'-CloudTrail List({str(row - 2)})')
    print("Done.\n")

def write_trail_to_excel(row, trail, result_sheet):
    result_sheet.write(row, 0, row - 1, integer_format)
    result_sheet.write(row, 1, trail['Name'], wrap_format)
    result_sheet.write(row, 2, trail['S3BucketName'], date_format)
    result_sheet.write(row, 3, trail['LogFileValidationEnabled'], date_format)
    result_sheet.write(row, 4, trail['IsOrganizationTrail'], string_format)
    
    result_sheet.write(row, 5, trail['IsMultiRegionTrail'], string_format)
    
    result_sheet.write(row, 6, trail['IncludeGlobalServiceEvents'], string_format)
    result_sheet.write(row, 7, trail['HomeRegion'], wrap_format)
    result_sheet.write(row, 8, trail['HasInsightSelectors'], wrap_format)
    result_sheet.write(row, 9, trail['HasCustomEventSelectors'], string_format)
    result_sheet.write(row, 10, trail['CloudWatchLogsLogGroupArn'] if 'CloudWatchLogsLogGroupArn' in trail else '-', string_format)
    result_sheet.write(row, 11, trail['CloudWatchLogsRoleArn'] if 'CloudWatchLogsRoleArn' in trail else '-', string_format)
    
    row += 1

    return row



def report_backup_vaults(backup, row, result_sheet):

  # {'BackupVaultArn': 'arn:aws:backup:ap-northeast-2:123456789012:backup-vault:sksh-argos-p-ec2-backup-vault',
  #  'BackupVaultName': 'sksh-argos-p-ec2-backup-vault',
  #  'CreationDate': datetime.datetime(2022, 7, 25, 14, 49, 9, 655000, tzinfo=tzlocal()),
  #  'EncryptionKeyArn': 'arn:aws:kms:ap-northeast-2:123456789012:key/ac4f918d-ac87-4323-9dd1-7e565ed62bc5',
  #  'Locked': False,
  #  'NumberOfRecoveryPoints': 938}

  Columns = ["Backup Vault Name", "Creation Date", "Number Of RecoveryPoints", "EncryptionKeyArn"]

  col = 0 
  for ColName in Columns:
    result_sheet.write(1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 32)  # Backup Vault Name
  result_sheet.set_column('B:B', 17)  # Creatio Date
  result_sheet.set_column('C:C', 17)  # Number Of RecoveryPoints
  result_sheet.set_column('D:D', 82)  # EncryptionKeyArn


  response = backup.list_backup_vaults( )

  backup_vault_cnt = 0
  for backup_vault in response['BackupVaultList']:
    # print(f'backup_vault')
    # pprint(backup_vault)
    # print(f"Backup vault name: {backup_vault['BackupVaultName']}")
    result_sheet.write(row, 0, backup_vault['BackupVaultName'], string_format) # Backup Vault Name
    result_sheet.write(row, 1, backup_vault['CreationDate'], date_format) # Creatio Date
    result_sheet.write(row, 2, backup_vault['NumberOfRecoveryPoints'], integer_format) # "Number Of RecoveryPoints
    result_sheet.write(row, 3, backup_vault['EncryptionKeyArn'], string_format) # EncryptionKeyArn
    backup_vault_cnt += 1
    row += 1
    # print(f'--------------------------------------------------')


  print(f'-백업볼트 개수[{backup_vault_cnt}]')

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)

  result_sheet.write(0, 1, "AWS Backup Vault List("+ str(backup_vault_cnt) + ")", title_format)
  return backup_vault_cnt



def report_backup_plans(backup, row, result_sheet):
  Columns = ["Backup Plan Name", "Creation Date", "Last Execution Date", "Backup Plan Arn", "Advanced Backup Settings"] # , "Backup Plan Arn", "Backup Plan Id", "Version Id"]

  col = 0 
  for ColName in Columns:
    result_sheet.write(row + 1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 32)  # Backup Plan Name
  result_sheet.set_column('B:B', 17)  # Creatio Date
  result_sheet.set_column('C:C', 17)  # Last Execution Date
  result_sheet.set_column('D:D', 82)  # Backup Plan Arn
  result_sheet.set_column('E:E', 42)  # Advanced Backup Settings 


  # client = boto3.client('backup')
  backup_plans = backup.list_backup_plans()

  backup_plan_cnt = 0
  for plan in backup_plans['BackupPlansList']:
    # pprint(plan)
    # {'BackupPlanArn': 'arn:aws:backup:ap-northeast-2:123456789012:backup-plan:3257c407-b860-4d83-a60b-c1bf44c2e4d5',
    #  'BackupPlanId': '3257c407-b860-4d83-a60b-c1bf44c2e4d5',
    #  'BackupPlanName': 'sksh-argos-p-efs-backup-plan',
    #  'CreationDate': datetime.datetime(2023, 3, 31, 11, 16, 31, 307000, tzinfo=tzlocal()),
    #  'LastExecutionDate': datetime.datetime(2023, 4, 20, 2, 0, 11, 137000, tzinfo=tzlocal()),
    #  'VersionId': 'NWY1MDZkNWEtZGY2OC00MTlmLWE3MjgtMWZjZjAyNDk2Mzdh'}

    # print(f"Backup plan name: {plan['BackupPlanName']}")
    result_sheet.write(row + backup_plan_cnt + 2, 0, plan['BackupPlanName'], string_format)
    result_sheet.write(row + backup_plan_cnt + 2, 1, plan['CreationDate'], date_format)
    result_sheet.write(row + backup_plan_cnt + 2, 2, plan['LastExecutionDate'], date_format) # Last Execution Date
    result_sheet.write(row + backup_plan_cnt + 2, 3, plan['BackupPlanArn'], string_format)   # Backup Plan Arn
    # advancedBackupSettings = plan['AdvancedBackupSettings']
    # if AdvancedBackupSettings is not None:
    #   print(f"AdvancedBackupSettings: {plan['AdvancedBackupSettings']}")
    if 'AdvancedBackupSettings' in plan:
      # print(f"AdvancedBackupSettings: {plan['AdvancedBackupSettings']}")
      advancedBackupSettings = json.dumps(plan['AdvancedBackupSettings'], indent=2)
      # print(f'AdvancedBackupSettings: {advancedBackupSettings}')
      result_sheet.write(row + backup_plan_cnt + 2, 4, advancedBackupSettings, wrap_format)   # Backup Plan Arn
    else:
      result_sheet.write(row + backup_plan_cnt + 2, 4, '-', wrap_format) 
    # print(f"Backup plan ID: {plan['BackupPlanId']}")
    # print(f"Backup plan version: {plan['VersionId']}")
    backup_plan_cnt += 1
    # print(f'--------------------------------------------------')
  
  print(f'-백업플랜[{backup_plan_cnt}]\n.\n.\n.\n')

  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  result_sheet.write_url(row, 0, sheetlink_pos, url_format, string=ColName)


  result_sheet.write(row, 1, "AWS Backup Plan List("+ str(backup_plan_cnt) + ")", title_format)

  return backup_plan_cnt




def report_protected_resources(backup, row, result_sheet):
  # print('\n\n\n')
  # print(f'보호된 자원 목록 출력하기')
  # {'LastBackupTime': datetime.datetime(2023, 4, 19, 3, 0, tzinfo=tzlocal()),
  # 'ResourceArn': 'arn:aws:ec2:ap-northeast-2:123456789012:instance/i-0065d1b5fee3480bc',
  # 'ResourceName': 'sksh-argos-p-icms-icms-ec2-2b-08',
  # 'ResourceType': 'EC2'}
  # {'LastBackupTime': datetime.datetime(2023, 4, 24, 3, 0, tzinfo=tzlocal()),
  # 'ResourceArn': 'arn:aws:elasticfilesystem:ap-northeast-2:123456789012:file-system/fs-0047a5f34667f2924',
  # 'ResourceName': 'sksh-argos-p-an2-efs-application02',
  # 'ResourceType': 'EFS'}
  
  Columns = ["Resource Name", "Resource Type", "Last Backup Time", "Resource Arn"]

  col = 0 
  for ColName in Columns:
    result_sheet.write(row + 1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 32)  # Backup Plan Name
  result_sheet.set_column('B:B', 17)  # Creatio Date
  result_sheet.set_column('C:C', 17)  # Last Execution Date
  result_sheet.set_column('D:D', 82)  # Backup Plan Arn


  list_protected_resources = backup.list_protected_resources(MaxResults=123
      # BackupPlanId=backup_plan_id
  )
  # pprint(list_protected_resources)

  protected_resources_cnt = 0
  ec2_cnt = 0
  efs_cnt = 0
  for protected_resources in list_protected_resources['Results']:


    protected_resources_output = jmespath.search('[LastBackupTime, ResourceArn, ResourceName, ResourceType]', protected_resources)

    lastBackupTime, resourceArn, resourceName, resourceType = protected_resources_output
    result_sheet.write(row + ec2_cnt + efs_cnt + 2, 0, resourceName, string_format)  # Resource Name
    result_sheet.write(row + ec2_cnt + efs_cnt + 2, 1, resourceType, string_format)  # Resource Type
    result_sheet.write(row + ec2_cnt + efs_cnt + 2, 2, lastBackupTime, date_format)  # Last Execution Date
    result_sheet.write(row + ec2_cnt + efs_cnt + 2, 3, resourceArn, string_format)   # Backup Plan Arn

    # print(f'{resourceType}/{resourceName} - {lastBackupTime}')
    if 'EC2' in resourceType:
      # if ec2_cnt == 0:
      #   pprint(protected_resources)
      ec2_cnt += 1
    elif 'EFS' in resourceType:
      # if efs_cnt == 0:
      #   pprint(protected_resources)
      efs_cnt += 1

  print(f'-보호된 자원 목록[{str(ec2_cnt + efs_cnt)}]')
  print(f'\t-EC2 Backup 설정된 갯수{ec2_cnt}')
  print(f'\t-EFS Backup 설정된 갯수{efs_cnt}')

  # result_sheet.write(rows, 0, "Protected Resource List("+ str(ec2_cnt + efs_cnt) + ")", title_format)
  # result_sheet.write(rows + 1, 1, "EC2 Backup 설정된 갯수("+ str(ec2_cnt) + ")", title_format)
  # result_sheet.write(rows + 2, 1, "EFS Backup 설정된 갯수("+ str(efs_cnt) + ")", title_format)


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  result_sheet.write_url(row, 0, sheetlink_pos, url_format, string=ColName)

  result_sheet.write(row, 1, f"Protected Resource List(총[{ec2_cnt + efs_cnt}], EC2 Backup 설정된 갯수[{ec2_cnt}], EFS Backup 설정된 갯수[{efs_cnt}])", title_format)

  return (ec2_cnt + efs_cnt)


def report_backup_jobs(backup, row, result_sheet):
  print('\n\n\n')
  print(f'backup jobs 목록')

  # {'AccountId': '123456789012',
  # 'BackupJobId': 'E96A0995-C5F9-E49A-FE6B-2E46F689692D',
  # 'BackupSizeInBytes': 212398050502,
  # 'BackupVaultArn': 'arn:aws:backup:ap-northeast-2:123456789012:backup-vault:sksh-argos-p-ec2-backup-vault',
  # 'BackupVaultName': 'sksh-argos-p-ec2-backup-vault',
  # 'CompletionDate': datetime.datetime(2023, 4, 19, 3, 22, 46, 250000, tzinfo=tzlocal()),
  # 'CreatedBy': {'BackupPlanArn': 'arn:aws:backup:ap-northeast-2:123456789012:backup-plan:28455991-cf2b-40e9-b233-03ccb1f2479d',
  #               'BackupPlanId': '28455991-cf2b-40e9-b233-03ccb1f2479d',
  #               'BackupPlanVersion': 'NWY3ZTZiZmMtMDA0ZS00ZmFiLTg1OTktMTc5ZDMyMTliMDgx',
  #               'BackupRuleId': 'b0456b69-4a90-456a-9d9d-c16cd7a6a2a9'},
  # 'CreationDate': datetime.datetime(2023, 4, 19, 3, 0, tzinfo=tzlocal()),
  # 'IamRoleArn': 'arn:aws:iam::123456789012:role/EC2AWSBackupServiceRole',
  # 'IsParent': False,
  # 'PercentDone': '100.0',
  # 'RecoveryPointArn': 'arn:aws:backup:ap-northeast-2:123456789012:recovery-point:f49c6f49-b36c-461f-928b-a1039c5c7d5d',    
  # 'ResourceArn': 'arn:aws:elasticfilesystem:ap-northeast-2:123456789012:file-system/fs-04b05821552ecfc78',
  # 'ResourceName': 'sksh-argos-p-an2-efs-application01',
  # 'ResourceType': 'EFS',
  # 'StartBy': datetime.datetime(2023, 4, 19, 4, 0, tzinfo=tzlocal()),
  # 'State': 'COMPLETED'}

  # {backupVaultName} : {resourceType}/{resourceName} {startBy}-{completionDate} [{percentDone}% {state}]'
  # 'sksh-argos-p-ec2-backup-vault : EC2/sksh-argos-p-gw-gwicms-ec2-2c-02 '
  #  '2023-04-24 04:00:00+09:00-2023-04-24 03:32:00.659000+09:00 [100.0% '
  #  'COMPLETED]
  Columns = ["Resource Name", "Start By", "Percent Done", "Resource Arn", "Backup Vault Name", "ResourceType", "Completion Date", "State", ]

  col = 0 
  for ColName in Columns:
    result_sheet.write(row + 1, col, ColName, colname_format)
    col += 1

  result_sheet.set_column('A:A', 32)  # Resource Name
  result_sheet.set_column('B:B', 17)  # Start By
  result_sheet.set_column('C:C', 17)  # Percent Done
  result_sheet.set_column('D:D', 82)  # Resource Arn
  result_sheet.set_column('E:E', 42)  # Backup Vault Name
  result_sheet.set_column('F:F', 12)  # Resource Type
  result_sheet.set_column('G:G', 17)  # Completion Date
  result_sheet.set_column('H:H', 12)  # State


  today = date.today( )
  today_str = today.strftime('%Y-%m-%d')
  # yesterday = today - datetime.timedelta(days=1)
  # today.strftime('%Y-%m-%d') 
  # year = today.strftime('%Y')
  # month = today.strftime('%m')
  # day = today.strftime('%d')


  # backup_jobs = backup.list_backup_jobs(ByCreatedBefore=datetime(year, month, day))
  backup_jobs = backup.list_backup_jobs(MaxResults=123)
  # backup_jobs = backup.list_backup_jobs( )
  # pprint(backup_jobs)

  backup_job_cnt = 0
  ec2_cnt = 0
  efs_cnt = 0
  for backup_job in backup_jobs['BackupJobs']:
    # pprint(backup_job)

    # {'AccountId': '123456789012',
    # 'BackupJobId': 'E96A0995-C5F9-E49A-FE6B-2E46F689692D',
    # 'BackupSizeInBytes': 212398050502,
    # 'BackupVaultArn': 'arn:aws:backup:ap-northeast-2:123456789012:backup-vault:sksh-argos-p-ec2-backup-vault',
    # 'BackupVaultName': 'sksh-argos-p-ec2-backup-vault',
    # 'CompletionDate': datetime.datetime(2023, 4, 19, 3, 22, 46, 250000, tzinfo=tzlocal()),
    # 'CreatedBy': {'BackupPlanArn': 'arn:aws:backup:ap-northeast-2:123456789012:backup-plan:28455991-cf2b-40e9-b233-03ccb1f2479d',
    #               'BackupPlanId': '28455991-cf2b-40e9-b233-03ccb1f2479d',
    #               'BackupPlanVersion': 'NWY3ZTZiZmMtMDA0ZS00ZmFiLTg1OTktMTc5ZDMyMTliMDgx',
    #               'BackupRuleId': 'b0456b69-4a90-456a-9d9d-c16cd7a6a2a9'},
    # 'CreationDate': datetime.datetime(2023, 4, 19, 3, 0, tzinfo=tzlocal()),
    # 'IamRoleArn': 'arn:aws:iam::123456789012:role/EC2AWSBackupServiceRole',
    # 'IsParent': False,
    # 'PercentDone': '100.0',
    # 'RecoveryPointArn': 'arn:aws:backup:ap-northeast-2:123456789012:recovery-point:f49c6f49-b36c-461f-928b-a1039c5c7d5d',    
    # 'ResourceArn': 'arn:aws:elasticfilesystem:ap-northeast-2:123456789012:file-system/fs-04b05821552ecfc78',
    # 'ResourceName': 'sksh-argos-p-an2-efs-application01',
    # 'ResourceType': 'EFS',
    # 'StartBy': datetime.datetime(2023, 4, 19, 4, 0, tzinfo=tzlocal()),
    # 'State': 'COMPLETED'}
  
    backup_job_output = jmespath.search('[AccountId, BackupJobId, BackupSizeInBytes, BackupVaultArn, BackupVaultName, CompletionDate, CreatedBy, CreationDate, IamRoleArn, IsParent, PercentDone, RecoveryPointArn, ResourceArn, ResourceName, ResourceType, StartBy, State]', backup_job)


    accountId, backupJobId, backupSizeInBytes, backupVaultArn, backupVaultName, completionDate, createdBy, creationDate, iamRoleArn, isParent, percentDone, recoveryPointArn, resourceArn, resourceName, resourceType, startBy, state = backup_job_output
    

    # if today.strftime('%Y-%m-%d') == startBy.strftime('%Y-%m-%d'):
    if today_str == startBy.strftime('%Y-%m-%d'):
      # print('The date matches!')
      # pprint(f'{backupVaultName} : {resourceType}/{resourceName} {startBy}-{completionDate} [{percentDone}% {state}]')
      # print("-------")

      result_sheet.write(row + backup_job_cnt + 2, 0, resourceName, string_format)    # 0.Resource Name
      result_sheet.write(row + backup_job_cnt + 2, 1, startBy, date_format)         # 1.Start By
      result_sheet.write(row + backup_job_cnt + 2, 2, percentDone, string_format)       # 2.Percent Done
      result_sheet.write(row + backup_job_cnt + 2, 3, resourceArn, string_format)     # 3.Resource Arn
      result_sheet.write(row + backup_job_cnt + 2, 4, backupVaultName, string_format) # 4.Backup Vault Name
      result_sheet.write(row + backup_job_cnt + 2, 5, resourceType, string_format)    # 5.Resource Type
      result_sheet.write(row + backup_job_cnt + 2, 6, completionDate, date_format)    # 6.Completion Date
      result_sheet.write(row + backup_job_cnt + 2, 7, state, string_format)           # 7.State


      backup_job_cnt += 1
      if resourceType == 'EC2':
          ec2_cnt += 1
      elif resourceType == 'EFS':
          efs_cnt += 1

    else:
        # print('The date does not match -- break')
        break


  ColName = '자원 요약'
  sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
  result_sheet.write_url(row, 0, sheetlink_pos, url_format, string=ColName)
  
  print(f'-당일 수행된 AWS Backup Job Count[{backup_job_cnt}]')
  result_sheet.write(row, 1, "당일 수행된 AWS Backup Job Count("+ str(backup_job_cnt) + ")", title_format)

  return backup_job_cnt


# 1. list backup valuts
# 2. list backup plans
# 3. list protected resources
# 4. list backup jobs
def report_aws_backup(backup):

  result_sheet = xlsx.add_worksheet('AWS Backup')
  # result_sheet.set_column('A:Z', cell_format=wrap_format)

  # list backup valuts
  rows = 2
  backup_vault_cnt = report_backup_vaults(backup, rows, result_sheet)
  
  # list backup plans
  rows += backup_vault_cnt
  rows += 2
  backup_plan_cnt = report_backup_plans(backup, rows, result_sheet)



  # list protected resources
  rows += backup_plan_cnt
  rows += (2 + 2)
  protected_resource_cnt = report_protected_resources(backup, rows, result_sheet)


  # 당일 수행된 backup jobs
  rows += protected_resource_cnt
  rows += (2 + 2)
  backup_job_cnt = report_backup_jobs(backup, rows, result_sheet)
  

  # print("-AWS Backup ["+ str(backup_job_cnt) +"]")
  print(f'-AWS Backup [{backup_job_cnt}]')
  # result_sheet.write(0, 0, "AWS Backup List("+ str(backup_job_cnt) + ")", title_format)

  global summary_col
  global Columns_C_POS
  summary_sheet.write(Columns_C_POS['AWS Backup'], summary_col, backup_job_cnt, integer_format)

  print("Done.\n") 


def report_waf_web_acls(waf):
    global result_sheet
    result_sheet = xlsx.add_worksheet('WAF')

    Columns = ["No.", "Name", "Id", "Description", "ARN", "Capacity", "Default Action", "Label Namespace", "Managed By Firewall Manager"] 

    Columns_Rules = [
        "No",
        "Name",
        "Action",
        "OverrideAction",
        "Priority",
        "Statement",
        "VisibilityConfig"        
    ]

    col = 0 
    for ColName in Columns:   
        # 수직 병합 (2:3)     
        result_sheet.merge_range(f'{chr(65 + col)}2:{chr(65 + col)}3', ColName, colname_format)
        # result_sheet.merge_range('A2:A3', 'No', colname_format)
        # result_sheet.write(1, col, ColName, colname_format)
        col += 1
    
    # Rules Column - 수평 병합 
    result_sheet.merge_range(f'{chr(65 + col)}2:{chr(65 + col + len(Columns_Rules) - 1)}2', "Rules", colname_format)
    

    for RuleName in Columns_Rules:
        result_sheet.write(f'{chr(65 + col)}3', RuleName, colname_format)
        col += 1


    # Web ACL Info
    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 78)  # Name
    result_sheet.set_column('C:C', 37)  # Id
    result_sheet.set_column('D:D', 37)  # Description
    result_sheet.set_column('E:E', 37)  # ARN
    result_sheet.set_column('F:F', 16)  # Capacity
    result_sheet.set_column('G:G', 12)  # DefaultAction
    result_sheet.set_column('H:H', 32)  # LabelNamespace
    result_sheet.set_column('I:I', 12)  # ManagedByFirewallManager
    # - Rules ---
    result_sheet.set_column('J:J', 5)   # No
    result_sheet.set_column('K:K', 122)  # Name
    result_sheet.set_column('L:L', 12)  # Action
    result_sheet.set_column('M:M', 32)  # OverrideAction
    result_sheet.set_column('N:N', 9)   # Priority
    result_sheet.set_column('O:O', 10)  # Statement
    result_sheet.set_column('P:P', 152)  # VisibilityConfig

    
    # WAF ACL 목록 가져오기
    response = waf.list_web_acls(Scope='REGIONAL')  # 또는 CLOUDFRONT
    web_acls = response['WebACLs']

    
    row = 3
    web_acl_cnt = 1
    for web_acl in web_acls:
        web_acl_id   = web_acl['Id']
        web_acl_name = web_acl['Name']
        row = describe_waf_web_acl(row, web_acl_cnt, waf, web_acl_id, web_acl_name, result_sheet)
        web_acl_cnt += 1


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"AWS WAF(Web Application Firewall) ACL List({str(web_acl_cnt - 1)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['Web Application Firewall'], summary_col, web_acl_cnt - 1, integer_format)
    print(f'-AWS WAF(Web Application Firewall) ACL List({str(web_acl_cnt - 1)})')
    print("Done.\n")

def describe_waf_web_acl(row, web_acl_cnt, waf, web_acl_id, web_acl_name, result_sheet):
    response = waf.get_web_acl(
        Id=web_acl_id,
        Name=web_acl_name,
        Scope='REGIONAL'  # 또는 CLOUDFRONT
    )
    web_acl_info = response['WebACL']
    # pprint(web_acl_info)

    row = write_waf_web_acl_to_excel(row, web_acl_cnt, web_acl_info, result_sheet)
    
    return row

def write_waf_web_acl_to_excel(row, web_acl_cnt, web_acl_info, result_sheet):
    rules = web_acl_info['Rules']
    start_row = row + 1
    end_row   = row + len(rules) 

    # 수직 병합 
    col = 0; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', web_acl_cnt, integer_format)
    col = 1; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', web_acl_info['Name'], wrap_format)
    col = 2; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', web_acl_info['Id'], string_format)
    col = 3; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', web_acl_info['Description'], string_format)
    col = 4; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', web_acl_info['ARN'], string_format)
    col = 5; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', web_acl_info['Capacity'], date_format)
    col = 6; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', json.dumps(web_acl_info['DefaultAction'], indent=2), wrap_format)
    col = 7; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', web_acl_info['LabelNamespace'], string_format)
    col = 8; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', web_acl_info['ManagedByFirewallManager'], wrap_format)

    # result_sheet.merge_range(row, 0, web_acl_cnt, integer_format)
    # result_sheet.merge_range(row, 1, web_acl_info['Name'], wrap_format)
    # result_sheet.merge_range(row, 2, web_acl_info['Id'], string_format)
    # result_sheet.merge_range(row, 3, web_acl_info['Description'], string_format)
    # result_sheet.merge_range(row, 4, web_acl_info['ARN'], string_format)
    # result_sheet.merge_range(row, 5, web_acl_info['Capacity'], date_format)    
    # result_sheet.merge_range(row, 6, json.dumps(web_acl_info['DefaultAction'], indent=2), wrap_format)    
    # result_sheet.merge_range(row, 7, web_acl_info['LabelNamespace'], string_format)
    # result_sheet.wrimerge_rangete(row, 8, web_acl_info['ManagedByFirewallManager'], wrap_format)

    rule_cnt = 1
    webinfo_start_row = row
    for rule in rules:
        result_sheet.write(row, 9,  rule_cnt, integer_format)
        result_sheet.write(row, 10,  rule['Name'], wrap_format)
        result_sheet.write(row, 11, json.dumps(rule['Action'], indent=2) if 'Action' in rule else '-', wrap_format)    
        result_sheet.write(row, 12, json.dumps(rule['OverrideAction'], indent=2) if 'OverrideAction' in rule else '-', wrap_format)
        result_sheet.write(row, 13, rule['Priority'], string_format)
        rule_statement = convert_bytes_to_string(rule['Statement'])
        # result_sheet[row, 14].comment = Comment(json.dumps(rule_statement, indent=2))
        result_sheet.write(row, 14, json.dumps(rule_statement, indent=2), string_format)
        result_sheet.write(row, 15, json.dumps(rule['VisibilityConfig'], indent=2), wrap_format) 
        
        rule_cnt += 1
        row += 1

    return row



def report_network_firewalls(network_firewall):
    global result_sheet
    result_sheet = xlsx.add_worksheet('Network Firewall')

    Columns = ["No.", "Firewall Name", "Firewall Id", "Firewall Arn", "Vpc Id", "Delete Protection", "Encryption Configuration", "Firewall Policy Arn", "Firewall Policy Change Protection", "Subnet Change Protection", "Subnet Mappings", "Tags", "Description"] 

    col = 0 
    for ColName in Columns:   
        result_sheet.write(1, col, ColName, colname_format)
        col += 1
    

    # Web ACL Info
    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 30)  # FirewallName
    result_sheet.set_column('C:C', 40)  # FirewallId
    result_sheet.set_column('D:D', 82)  # FirewallArn
    result_sheet.set_column('E:E', 22)  # VpcId
    result_sheet.set_column('F:F', 7)   # DeleteProtection
    result_sheet.set_column('G:G', 32)  # EncryptionConfiguration
    result_sheet.set_column('H:H', 84)  # FirewallPolicyArn
    result_sheet.set_column('I:I', 12)  # FirewallPolicyChangeProtection
    result_sheet.set_column('J:J', 12)  # SubnetChangeProtection
    result_sheet.set_column('K:K', 42)  # SubnetMappings
    result_sheet.set_column('L:L', 32)  # Tags
    result_sheet.set_column('M:M', 32)  # Description

    
    # Network Firewall 목록 가져오기
    response = network_firewall.list_firewalls()
    firewalls = response['Firewalls']

    
    row = 2    
    for firewall in firewalls:
        firewall_name = firewall['FirewallName']
        response = network_firewall.describe_firewall(FirewallName=firewall_name)
        firewall_info = response['Firewall']
        # pprint(firewall_info)
        row = write_firewall_info_to_excel(row, firewall_info, result_sheet)
        # row = describe_network_firewall(row, firewall, firewall_name, result_sheet)


    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"AWS Network Firewall List({str(row - 2)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['Network Firewall'], summary_col, row - 2, integer_format)
    print(f'-AWS Network Firewall List({str(row - 2)})')
    print("Done.\n")



def write_firewall_info_to_excel(row, firewall_info, result_sheet):
    # pprint(firewall_info)
    result_sheet.write(row, 0, row - 1, integer_format) # No.
    result_sheet.write(row, 1, firewall_info['FirewallName'], string_format)                  # Firewall Name 
    result_sheet.write(row, 2, firewall_info['FirewallId'], string_format)                     # Firewall Id 
    result_sheet.write(row, 3, firewall_info['FirewallArn'], string_format)                    # Firewall Arn
    result_sheet.write(row, 4, firewall_info['VpcId'], string_format)                          # Vpc Id
    result_sheet.write(row, 5, firewall_info['DeleteProtection'], string_format)               # Delete Protection    
    result_sheet.write(row, 6, json.dumps(firewall_info['EncryptionConfiguration'], indent=2), wrap_format)  # Encryption Configuration
    result_sheet.write(row, 7, firewall_info['FirewallPolicyArn'], string_format)              # Firewall Policy Arn
    result_sheet.write(row, 8, firewall_info['FirewallPolicyChangeProtection'], string_format) # Firewall Policy Change Protection
    result_sheet.write(row, 9, firewall_info['SubnetChangeProtection'], string_format)         # Subnet Change Protection
    result_sheet.write(row, 10, json.dumps(firewall_info['SubnetMappings'], indent=2), wrap_format) # Subnet Mappings
    result_sheet.write(row, 11, json.dumps(firewall_info['Tags'], indent=2), wrap_format)       # Tags    
    result_sheet.write(row, 12, firewall_info['Description'] if 'Description' in firewall_info else '-' , string_format)                    # Description
    
    row += 1
    
    return row



def report_shield_protections(shield):
    global result_sheet
    result_sheet = xlsx.add_worksheet('Shield Protection')

    Columns = ["No.", "Name", "Id", "Application Layer Automatic Response Configuration", "Protection Arn", "Resource Arn", "Resource Type", "Health"]

    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1


    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 37)  # Name
    result_sheet.set_column('C:C', 40)  # Id
    result_sheet.set_column('D:D', 30)  # ApplicationLayerAutomaticResponseConfiguration
    result_sheet.set_column('E:E', 72)  # ProtectionArn
    result_sheet.set_column('F:F', 109) # ResourceArn
    result_sheet.set_column('G:G', 12)  # Resource Type
    result_sheet.set_column('H:H', 12)  # Health

    try:
        # Shield 목록 가져오기
        response = shield.list_protections()
        protections = response['Protections']

        row = 2
        for protection in protections:
            protection_id = protection['Id']
            response      = shield.describe_protection(ProtectionId=protection_id)
            protection    = response['Protection']
            # print(f"ID: {id}")
            row = write_shield_to_excel(row, protection, result_sheet)
    except botocore.exceptions.ClientError as e:
        print("An error occurred:", e)
        row = 2

    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"AWS Shield Protection List({str(row - 2)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['Shield Protection'], summary_col, row - 2, integer_format)
    print(f'-AWS Shield Protection List({str(row - 2)})')
    print("Done.\n")

def write_shield_to_excel(row, protection, result_sheet):
    result_sheet.write(row, 0, row - 1, integer_format)
    result_sheet.write(row, 1, protection['Name'], string_format)
    result_sheet.write(row, 2, protection['Id'], string_format)
    result_sheet.write(row, 3, json.dumps(protection['ApplicationLayerAutomaticResponseConfiguration'], indent=2), wrap_format)
    result_sheet.write(row, 4, protection['ProtectionArn'], string_format)
    
    result_sheet.write(row, 5, protection['ResourceArn'], string_format)
    
    result_sheet.write(row, 6, protection['ResourceType'] if 'ResourceType' in protection else '-', string_format)
    result_sheet.write(row, 7, protection['Health'] if 'Health' in protection else '-', string_format)

  
    
    row += 1

    return row



def report_route53_hosted_zones(route53):
    global result_sheet
    result_sheet = xlsx.add_worksheet('Route53')

    Columns = ["No.", "Id", "Name", "Resource Record Set Count", "Caller Reference", "Config", "Is Truncated", "Max Items"]
    Columns_RecordSets = ["Type", "TTL", "Resourc eRecords", "Alias Target"]


    col = 0 
    for ColName in Columns:
        # 수직 병합 (2:3)     
        result_sheet.merge_range(f'{chr(65 + col)}2:{chr(65 + col)}3', ColName, colname_format)
        # result_sheet.write(1, col, ColName, colname_format)
        col += 1

    # Rules Column - 수평 병합
    result_sheet.merge_range(f'{chr(65 + col)}2:{chr(65 + col + len(Columns_RecordSets) - 1)}2', "ResourceRecordSets", colname_format)

    for RecordSetsName in Columns_RecordSets:
        result_sheet.write(f'{chr(65 + col)}3', RecordSetsName, colname_format)
        col += 1


    # SNS Topics
    result_sheet.set_column('A:A', 10)  # No
    result_sheet.set_column('B:B', 42)  # Id
    result_sheet.set_column('C:C', 22)  # Name
    result_sheet.set_column('D:D', 10)  # ResourceRecordSetCount
    result_sheet.set_column('E:E', 32)  # CallerReference
    result_sheet.set_column('F:F', 52) # Config
    result_sheet.set_column('G:G', 12)  # IsTruncated
    result_sheet.set_column('H:H', 7)  # MaxItems

    result_sheet.set_column('I:I', 7)   # Type
    result_sheet.set_column('J:J', 7)   # TTL
    result_sheet.set_column('K:K', 92)  # ResourceRecords
    result_sheet.set_column('L:L', 92)  # AliasTarget

    try:
        # Route53 목록 가져오기
        response = route53.list_hosted_zones()
        hosted_zones = response['HostedZones']

        row = 3
        hosted_cnt = 1
        for hosted_zone in hosted_zones:
            hosted_zone_id = hosted_zone['Id']
            hosted_zone_name = hosted_zone['Name']
            record_sets = route53.list_resource_record_sets(HostedZoneId=hosted_zone_id)
           
            # print(f"ID: {id}")
            row = write_route53_hosted_zone_to_excel(row, hosted_cnt, hosted_zone, record_sets , result_sheet)
            hosted_cnt += 1

    except botocore.exceptions.ClientError as e:
        print("An error occurred:", e)

    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"AWS Route 53 Hosted Zones({str(hosted_cnt - 1)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['Route53 Hosted Zone'], summary_col, hosted_cnt - 1, integer_format)
    print(f'-AWS Route 53 Hosted Zones({str(hosted_cnt - 1)})')
    print("Done.\n")

def write_route53_hosted_zone_to_excel(row, hosted_cnt, hosted_zone, record_sets, result_sheet):   
    start_row = row + 1
    end_row   = row + len(record_sets['ResourceRecordSets'])
    
    # 수직 병합 
    col = 0; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', hosted_cnt, integer_format)
    col = 1; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', hosted_zone['Id'], string_format)
    col = 2; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', hosted_zone['Name'], string_format)    
    col = 3; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', hosted_zone['ResourceRecordSetCount'], wrap_format)
    col = 4; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', hosted_zone['CallerReference'], string_format)
    col = 5; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', json.dumps(hosted_zone['Config'], indent=2), wrap_format)

    col = 6; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', record_sets['IsTruncated'], string_format)
    col = 7; result_sheet.merge_range(f'{chr(65 + col)}{start_row}:{chr(65 + col)}{end_row}', record_sets['MaxItems'], integer_format)


    resource_record_sets = record_sets['ResourceRecordSets']
    for resource_record in resource_record_sets:
        # resource_record['ResourceRecords']
        result_sheet.write(row, 8,  resource_record['Type'], string_format)
        result_sheet.write(row, 9, resource_record['TTL'] if 'TTL' in resource_record else 0, integer_format)        
        result_sheet.write(row, 10, ",\n".join(record['Value'] for record in resource_record['ResourceRecords']) if 'ResourceRecords' in resource_record else '-', wrap_format)
        result_sheet.write(row, 11, ",\n".join(f"{key}: {value}" for key, value in resource_record['AliasTarget'].items( )) if 'AliasTarget' in resource_record else '-', wrap_format)

        row += 1

    return row



def report_cloudfront_distributions(cloudfront):
    global result_sheet
    result_sheet = xlsx.add_worksheet('CloudFront')

    Columns = ["No.", "Id", "Domain Name", "Status", "Last Modified Time", "Active Trusted Key Groups", "Active Trusted Signers", "Alias ICP Recordals", "ARN"]  
    Columns_DistributionConfig = ["Aliases", "Cache Behaviors", "Caller Reference", "Comment", "Continuous Deployment Policy Id", "Custom Error Responses", "Default Cache Behavior", "Default Root Object", "Enabled", "Http Version", "Is IPV6 Enabled", "Logging", "Origin Groups", "Origins", "PriceClass", "Restrictions", "Staging", "Viewer Certificate", "Web ACL Id"]


    col = 0 
    for ColName in Columns:
        # 수직 병합 (2:3)     
        result_sheet.merge_range(f'{chr(65 + col)}2:{chr(65 + col)}3', ColName, colname_format)
        # result_sheet.write(1, col, ColName, colname_format)
        col += 1

    # Rules Column - 수평 병합
    # print(f'{chr(65 + col)}2:{chr(65 + col + len(Columns_DistributionConfig) - 1)}2')
    _len = len(Columns_DistributionConfig) 
    # print(f'_len[{_len}] + col[{col}] - 1 => [{_len + col - 1}] >= 26')
    if (_len + col) >= 26:
        # (_len + col - 1) - 27
        _col = (_len + col - 1) - 26
        # print(f'_col[{_col}] -> {chr(65 + col)}2:A{chr(65 + _col)}2')
        result_sheet.merge_range(f'{chr(65 + col)}2:A{chr(65 + _col)}2', 'DistributionConfig', colname_format)
    else:
        # f'{chr(65 + col)}2:{chr(65 + col + len(Columns_DistributionConfig) - 1)}2'
        result_sheet.merge_range(f'{chr(65 + col)}2:{chr(65 + col + len(Columns_DistributionConfig) - 1)}2', 'DistributionConfig', colname_format)

    for DistributionConfigName in Columns_DistributionConfig:
        if col >= 26:
            _col = col - 26
            # print(f'1. {_col} : A{chr(65 + _col)}3')
            result_sheet.write(f'A{chr(65 + _col)}3', DistributionConfigName, colname_format)
        else:
            # print(f'2. {col} : {chr(65 + col)}3')
            result_sheet.write(f'{chr(65 + col)}3', DistributionConfigName, colname_format)
        col += 1


    # SNS Topics
    result_sheet.set_column('A:A', 10)   # No
    result_sheet.set_column('B:B', 17)   # Id
    result_sheet.set_column('C:C', 32)   # DomainName
    result_sheet.set_column('D:D', 10)   # Status
    result_sheet.set_column('E:E', 16)   # LastModifiedTime
    result_sheet.set_column('F:F', 17)   # ActiveTrustedKeyGroups
    result_sheet.set_column('G:G', 17)   # ActiveTrustedSigners
    result_sheet.set_column('H:H', 67)   # AliasICPRecordals
    result_sheet.set_column('I:I', 57)   # ARN

    result_sheet.set_column('J:J', 17)   # Aliases
    result_sheet.set_column('K:K', 37)   # CacheBehaviors
    result_sheet.set_column('L:L', 37)   # CallerReference
    result_sheet.set_column('M:M', 12)   # Comment
    result_sheet.set_column('N:N', 12)   # ContinuousDeploymentPolicyId 
    result_sheet.set_column('O:O', 12)   # CustomErrorResponses
    result_sheet.set_column('P:P', 85)   # DefaultCacheBehavior
    result_sheet.set_column('Q:Q', 12)   # DefaultRootObject 
    result_sheet.set_column('R:R', 7)    # Enabled
    result_sheet.set_column('S:S', 7)    # HttpVersion
    result_sheet.set_column('T:T', 7)    # IsIPV6Enabled
    result_sheet.set_column('U:U', 22)   # Logging
    result_sheet.set_column('V:V', 12)   # OriginGroups
    result_sheet.set_column('W:W', 82)   # Origins
    result_sheet.set_column('X:X', 12)   # PriceClass
    result_sheet.set_column('Y:Y', 27)   # Restrictions
    result_sheet.set_column('Z:Z',  7)   # Staging
    result_sheet.set_column('AA:AA', 92) # ViewerCertificate
    result_sheet.set_column('AB:AB', 122) # WebACLId"
    
    
    try:
        # CloudFront Distribution 목록 가져오기
        distribution_cnt = 1
        response = cloudfront.list_distributions()
        distributions = response['DistributionList'].get('Items', [])

        if not distributions:
            print("No CloudFront distributions found.")
            # return

        row = 3
        for distribution in distributions:
            distribution_id = distribution['Id']
            distribution_detail = cloudfront.get_distribution(Id=distribution_id)
            distribution_info = distribution_detail['Distribution']
           
            # print(f"ID: {id}")
            row = write_cloudfront_distribution_to_excel(row, distribution_cnt, distribution_info, result_sheet)
            distribution_cnt += 1

    except botocore.exceptions.ClientError as e:
        print("An error occurred:", e)

    ColName = '자원 요약'
    sheetlink_pos = "internal:\'" + ColName + "\'!" + "B1"
    result_sheet.write_url(0, 0, sheetlink_pos, url_format, string=ColName)


    result_sheet.write(0, 1, f"AWS CloudFront({str(distribution_cnt - 1)})", title_format)
    global summary_col
    summary_sheet.write(Columns_C_POS['CloudFront'], summary_col, distribution_cnt - 1, integer_format)
    print(f'-AWS CloudFront({str(distribution_cnt - 1)})')
    print("Done.\n")

def write_cloudfront_distribution_to_excel(row, distribution_cnt, distribution, result_sheet):   
    
    result_sheet.write(row, 0, distribution_cnt, integer_format)
    result_sheet.write(row, 1, distribution['Id'], string_format)
    result_sheet.write(row, 2, distribution['DomainName'], string_format)    
    result_sheet.write(row, 3, distribution['Status'], string_format)
    result_sheet.write(row, 4, distribution['LastModifiedTime'], date_format)
    result_sheet.write(row, 5, json.dumps(distribution['ActiveTrustedKeyGroups'], indent=2), wrap_format)
    result_sheet.write(row, 6, json.dumps(distribution['ActiveTrustedSigners'], indent=2), wrap_format)
    result_sheet.write(row, 7, json.dumps(distribution['AliasICPRecordals'] if 'AliasICPRecordals' in distribution else '-', indent=2), wrap_format)
    result_sheet.write(row, 8, distribution['ARN'], string_format)


    _config = distribution['DistributionConfig']    
    # resource_record['ResourceRecords']
    result_sheet.write(row, 9,  json.dumps(_config['Aliases'], indent=2), wrap_format)
    result_sheet.write(row, 10, json.dumps(_config['CacheBehaviors'], indent=2), wrap_format)        
    result_sheet.write(row, 11, _config['CallerReference'], wrap_format)
    result_sheet.write(row, 12, _config['Comment'], wrap_format)
    result_sheet.write(row, 13, _config['ContinuousDeploymentPolicyId'], wrap_format)
    result_sheet.write(row, 14, json.dumps(_config['CustomErrorResponses'], indent=2), wrap_format)
    # result_sheet.write(row, 15, recursive_print_dict(_config['DefaultCacheBehavior']), wrap_format)
    result_sheet.write(row, 15, json.dumps(_config['DefaultCacheBehavior'], indent=2), wrap_format)
    result_sheet.write(row, 16, _config['DefaultRootObject'], wrap_format)
    result_sheet.write(row, 17, _config['Enabled'], wrap_format)
    result_sheet.write(row, 18, _config['HttpVersion'], wrap_format)
    result_sheet.write(row, 19, _config['IsIPV6Enabled'], wrap_format)
    result_sheet.write(row, 20, json.dumps(_config['Logging'], indent=2), wrap_format)
    result_sheet.write(row, 21, json.dumps(_config['OriginGroups'], indent=2), wrap_format)
    result_sheet.write(row, 22, json.dumps(_config['Origins'], indent=2), wrap_format)
    result_sheet.write(row, 23, _config['PriceClass'], wrap_format)
    result_sheet.write(row, 24, json.dumps(_config['Restrictions'], indent=2), wrap_format)
    result_sheet.write(row, 25, _config['Staging'], wrap_format)
    result_sheet.write(row, 26, json.dumps(_config['ViewerCertificate'], indent=2), wrap_format)
    result_sheet.write(row, 27, _config['WebACLId'], wrap_format)


    row += 1

    return row




def get_monthly_usage_and_cost(ce, name, month, year):
    # 현재 날짜를 UTC로 가져옴
    today = datetime.now(timezone.utc)

    # 이번 달의 시작일과 종료일 계산
    # first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = (first_day_of_month.replace(month=first_day_of_month.month % 12 + 1) - timedelta(days=1)).replace(hour=23, minute=59, second=59)

    try:
        # AWS 비용 및 사용량 쿼리 실행
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': first_day_of_month.strftime('%Y-%m-%d'),
                'End': last_day_of_month.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )

        # 결과 출력
        global summary_col, resource_col, sub_resource_col, cost_col
        global Columns_C_POS, Columns_E_C_Mapping

        cost = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
        currency = response['ResultsByTime'][0]['Total']['UnblendedCost']['Unit']

        print(f'{"":=^80}')
        print(f"{name} : {year}년 {month}월 AWS 비용: {cost} {currency}")
        print(f'{"":=^80}')


        coltitle_format.set_border(1)
        coltitle_format.set_border_color('#393839')
        summary_sheet.write(1, cost_col, f'{name} : {year}년 {month}월 AWS 비용({currency})', coltitle_format)

        cost_sum_row = 2 + len(Columns_E_C_Mapping)
        # summary_sheet.write(cost_sum_row, resource_col, f'{name} : {year}년 {month}월 AWS 총비용({currency})', coltitle_format)    
        _col_range = f'{chr(65 + resource_col)}{cost_sum_row + 1}:{chr(65 + resource_col + 2)}{cost_sum_row + 1}'
        _col_title = f'{name} : {year}년 {month}월 AWS 비용 합계 (단위 : {currency})'
        summary_sheet.merge_range(_col_range, _col_title, coltitle_format)
        
        _number_format      = xlsx.add_format({'num_format': '#,##0.00', 'align': 'right', 'valign': 'vcenter', 'bg_color':'#BFBFBF', 'bold': True})
        _cost = float(cost)
        summary_sheet.write(cost_sum_row, cost_col, _cost, _number_format)

        # formula = '=G2*E17'
        cost_col_str = boto3_helper.convert_to_cell(cost_sum_row, cost_col)
        won_col_str  = boto3_helper.convert_to_cell(cost_sum_row, cost_col + 1)
        formula = f'={exchange_rate_col}*{cost_col_str}'
        # print(formula)
        summary_sheet.write_formula(won_col_str, formula, _number_format)




        # AWS 비용 및 사용량 쿼리 실행 (GroupBy 사용)
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': first_day_of_month.strftime('%Y-%m-%d'),
                'End': last_day_of_month.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                },
            ]
        )

        # 결과 출력
        print(f"{name} : {year}년 {month}월 AWS 자원별 비용:")

        print(f'{"":=^80}')
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                service_name = group['Keys'][0]            
                cost = group['Metrics']['UnblendedCost']['Amount']
                currency = group['Metrics']['UnblendedCost']['Unit']
                print(f"{service_name:50}: {cost} {currency}")
                if "Tax" == service_name:
                    cost_tax_row = cost_sum_row + 1
                    _col_range = f'{chr(65 + resource_col)}{cost_tax_row + 1}:{chr(65 + resource_col + 2)}{cost_tax_row + 1}'
                    _col_title = f'{name} : {year}년 {month}월 AWS 비용 Tax (단위 : {currency})'
                    summary_sheet.merge_range(_col_range, _col_title, coltitle_format)
                    
                    _number_format      = xlsx.add_format({'num_format': '#,##0.00', 'align': 'right', 'valign': 'vcenter', 'bg_color':'#BFBFBF', 'bold': True})
                    _cost = float(cost)
                    summary_sheet.write(cost_tax_row, cost_col, _cost, _number_format)

                    # formula = '=G2*E17'
                    cost_col_str = boto3_helper.convert_to_cell(cost_tax_row, cost_col)
                    won_col_str  = boto3_helper.convert_to_cell(cost_tax_row, cost_col + 1)
                    formula = f'={exchange_rate_col}*{cost_col_str}'
                    # print(formula)
                    summary_sheet.write_formula(won_col_str, formula, _number_format)

                elif service_name in Columns_E_C_Mapping:       
                    _service_name = Columns_E_C_Mapping[service_name]
                else:
                    continue

                # 비용 기록
                # print(f'currency[{currency} cost[{cost}]')
                _cost = float(cost)
                if _cost >= 10000:
                    _bg_color   = '#FF0000'
                    _font_color = '#FFFFFF'
                    _is_bold    = True
                elif _cost >= 1000:
                    _bg_color   = '#FF7F00'
                    _font_color = '#FFFFFF'
                    _is_bold    = True
                elif _cost >= 100:
                    _bg_color   = '#FFFF33'
                    _font_color = '#000000'
                    _is_bold    = True
                elif _cost >= 10:
                    _bg_color   = '#FFFFCC'
                    _font_color = '#000000'
                    _is_bold    = False
                else:
                    _bg_color   = '#EEEEEE'
                    _font_color = '#000000'
                    _is_bold    = False
                __number_format      = xlsx.add_format({'num_format': '#,##0.00', 'align': 'right', 'valign': 'vcenter', 'bg_color': _bg_color, 'font_color': _font_color, 'bold': _is_bold})
                
                _cost = float(cost)
                summary_sheet.write(Columns_C_POS[_service_name], cost_col, _cost, __number_format)
                # formula = '=G2*E17'
                cost_col_str = boto3_helper.convert_to_cell(Columns_C_POS[_service_name], cost_col)
                won_col_str  = boto3_helper.convert_to_cell(Columns_C_POS[_service_name], cost_col + 1)
                formula = f'={exchange_rate_col}*{cost_col_str}'
                # print(f'{won_col_str} -> {formula}')
                # summary_sheet.write_formula(won_col_str, formula, number_format)
                # cost 와 같은 format (색상 포함)으로 기록하기
                summary_sheet.write_formula(won_col_str, formula, __number_format)

                cell_format = xlsx.add_format()
                cell_format.set_bg_color(_bg_color)  # 배경색을 Cost Cell 과 동일하게 설정
                cell_format.set_font_color(_font_color)
                if _is_bold == True:
                    cell_format.set_bold( )
                
                # 자원명 셀에 색상 입히기
                _cell_range = f'{chr(65 + sub_resource_col)}{Columns_C_POS[_service_name] + 1}:{chr(65 + sub_resource_col)}{Columns_C_POS[_service_name] + 1}'
                # print(f'_cell_range[{_cell_range}]')
                summary_sheet.conditional_format(
                    _cell_range,
                    {'type': 'cell', 'format':cell_format, 'criteria': 'greater than', 'value': 10})            
                
                # 개수 셀에 색상 입히기
                _cell_range = f'{chr(65 + summary_col)}{Columns_C_POS[_service_name] + 1}:{chr(65 + summary_col)}{Columns_C_POS[_service_name] + 1}'      
                # print(f'_cell_range[{_cell_range}]')      
                summary_sheet.conditional_format(
                    _cell_range,
                    {'type': 'cell', 'format':cell_format, 'criteria': 'greater than or equal to', 'value': 0})
        print(f'{"":=^80}')
    except Exception as e:
        print("An error occurred:", e)


def main( ):
    
    report_basic( )
    report_resource( )

    session = boto3_helper.init_aws_session( )


    print("IAM")
    iam = session.client('iam')
    report_IAM(iam) #iam

    print("DirectConnect Connections")
    directconnect     = session.client('directconnect')
    report_directconnect_connections(directconnect) # directconnect connection 

    print("VPC")
    ec2client = session.client('ec2')
    ec2 = session.resource('ec2') 
    report_vpc(ec2client) #vpc #subnet 

    print("AWS Resource Access Manager (RAM):")
    ram = session.client('ram')
    report_resource_shares(ram)

    print("Security Group")
    #report_sg(ec2) #security group
    report_sg(ec2client) 


    elb = session.client('elb')
    alb = session.client('elbv2')
    print("ELB")
    report_elb(elb, alb) #lb

    print("EC2 Instance")
    report_instance(ec2client) #instance

    print("EC2 - EBS")
    report_ebs(ec2client, ec2)

    print("EFS")
    efs = session.client('efs')
    report_efs(efs)

    print("S3")
    s3client = session.client('s3')
    s3 = session.resource('s3')
    report_s3(s3client, s3)

    print("ECR")
    ecr = session.client('ecr')
    report_ecr_repositories(ecr)

    print("ECS")
    ecs = session.client('ecs')
    report_ecs(ecs)

    print("EKS")
    eks = session.client('eks')
    report_eks(eks)

    print("RDS")
    rds = session.client('rds')
    report_rds(rds) #rds

    print("RDS Proxy")
    report_rds_db_proxy(rds) # rds db proxy

    print("DynamoDB")
    dynamodb = session.resource('dynamodb')
    report_dynamodb(dynamodb)

    print("ElastiCache")
    elasticache = session.client('elasticache')
    report_elasticaches(elasticache)


    print("REDSHIFT")
    redshift = session.client('redshift')
    report_redshift(redshift)  


    print("Kafka")
    kafka = session.client('kafka')
    report_kafka(kafka)


    print("Amazon Simple Queue Service")
    sqs = session.client('sqs')
    report_sqs(sqs)


    print("Amazon Kinesis Firehose")
    # firehose = session.client(service_name, region_name=region_name)
    firehose = session.client('firehose')
    report_kinesis_firehose_streams(firehose)   


    print("AWS SNS Topics")
    sns = session.client('sns')
    report_sns_topics(sns)

    print("Lambda")
    client = session.client('lambda')
    report_lambda(client)


    print("Secrets Manager")
    secretsmanager = session.client('secretsmanager')
    # secretsmanager = session.resource('secretsmanager')
    report_secretsmanager(secretsmanager)

    print("AWS Certificate Manager")
    acm = session.client('acm')
    report_acm(acm)


    print("AWS Key Management Service")
    kms = session.client('kms')
    report_kms_keys(kms)


    print("Code Commit")
    codecommit = session.client('codecommit')
    report_codecommit(codecommit)

    print("Code Build")
    codebuild = session.client('codebuild')
    report_codebuild(codebuild)

    print("Code Deploy")
    codedeploy = session.client('codedeploy')
    report_codedeploy(codedeploy)


    print("Code Pipeline")
    codepipeline = session.client('codepipeline')
    report_codepipeline(codepipeline)

    print("Code Artifact")
    # session = boto3_helper.init_aws_session( )
    codeartifact = session.client('codeartifact', region_name='ap-northeast-1')
    report_codeartifact(codeartifact)

    print("CloudWatch Metric")
    cloudwatch = session.client('cloudwatch') 
    report_cloudwatch_metrics(cloudwatch)

    print("CloudWatch Logs")
    logs = session.client('logs', region_name='ap-northeast-2')
    report_cloudwatch_logs(logs)
    
    print("CloudWatch Alarms")
    cloudwatch = session.client('cloudwatch', region_name='ap-northeast-2')
    report_cloudwatch_alarms(cloudwatch)


    print("CloudWatch Events")
    events     = session.client('events')
    report_cloudwatch_events(events)

    print("CloudTrail")
    cloudtrail = session.client('cloudtrail')
    report_cloudtrail_trails(cloudtrail)

    print("AWS Backup")
    backup = session.client('backup', region_name='ap-northeast-2')
    report_aws_backup(backup)


    print("AWS WAF(WebApplication Firewall)")
    waf = session.client('wafv2')
    report_waf_web_acls(waf)
  
    print("AWS Network Firewall")
    network_firewall = session.client('network-firewall')            
    report_network_firewalls(network_firewall)

    print("AWS Shield Protections")
    shield = session.client('shield')
    report_shield_protections(shield)

    print("AWS Route 53 Hosted Zones")
    route53 = session.client('route53')
    report_route53_hosted_zones(route53)


    print("AWS CloudFront Distributions")
    cloudfront = session.client('cloudfront')
    report_cloudfront_distributions(cloudfront)



    name, target_year, target_month = boto3_helper.get_target_month( )
    print(f"[CostExplorer] {name}")
    # ce = session.client('ce', region_name=region_name)
    ce = session.client('ce')    
    get_monthly_usage_and_cost(ce, name, target_month, target_year)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', required=False, default='default', help='Account Credential Name')
    parser.add_argument('-r', required=False, default='ap-northeast-2', help='Region')
    args = parser.parse_args()

    return args.r, args.p

if __name__ == "__main__":
    # region_args, profile_args = get_arguments()
    # main(region_args, profile_args)
    start_time = time.time()
    main( )
    xlsx.close( )
    end_time = time.time()
    print(f"Program execution time: {end_time - start_time} seconds")

    now = datetime.now( )

    print(now) 