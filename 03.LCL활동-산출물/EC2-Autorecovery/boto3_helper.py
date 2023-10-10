import os
import boto3
import pprint
from dotenv import load_dotenv
from datetime import date, datetime

from botocore.client import Config
config = Config(connect_timeout=15, read_timeout=15) # 기본값인 60초 대신 15초로 설정

def getName( ):
  load_dotenv()  
  return os.getenv('NAME')

def get_arch_img( ):
  return os.getenv('ARCH_IMG')

def get_s3_object( ):
  return os.getenv('S3_OBJECT')

# ENV 파일(위에 표시된 대로) 에서 데이터(액세스, 비밀 키 및 영역 이름)를 가져와 Python 메모리로 읽습니다.
def get_aws_keys():
  # load .env
  load_dotenv()  
  # return os.getenv('AWS_ACCESS_KEY'), os.getenv('AWS_SECRET_KEY')
  return os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY'), os.getenv('AWS_SESSION_TOKEN')

# Boto3 세션 을 초기화하고 객체를 사용자에게 반환
def init_aws_session():
  access_key, secret_key, session_token = get_aws_keys()
  if session_token is None:
    return boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=os.getenv('AWS_REGION'))
  else:
    return boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token, region_name=os.getenv('AWS_REGION'))


def ec2_get_vpc_list():
  session = init_aws_session()
  ec2 = session.client('ec2')
  response = ec2.describe_vpcs()
  return response['Vpcs']

def ec2_add_vpc(ip_block):
  session = init_aws_session()
  ec2 = session.client('ec2')
  response = ec2.create_vpc(CidrBlock = ip_block, InstanceTenancy='default')
  return response['Vpc']

def ec2_delete_vpc(vpc_id):
  session = init_aws_session()
  ec2 = session.client('ec2')
  response = ec2.delete_vpc(VpcId=vpc_id)
  return response

def ec2_get_subnet_list():
  session = init_aws_session()
  ec2 = session.client('ec2')
  response = ec2.describe_subnets()
  return response['Subnets']

def ec2_add_subnet(vpc_id, ip_block):
  session = init_aws_session()
  ec2 = session.client('ec2')
  response = ec2.create_subnet(VpcId=vpc_id, CidrBlock=ip_block)
  return response['Subnet']

def ec2_delete_subnet(subnet_id):
  session = init_aws_session()
  ec2 = session.client('ec2')
  response = ec2.delete_subnet(SubnetId=subnet_id)
  return response

if __name__ == "__main__":
  # region_args, profile_args = get_arguments()
  # main(region_args, profile_args)
  access_key, secret_key = get_aws_keys( )
  print("AWS_ACCESS_KEY : {0}, AWS_SECRET_KEY : {1}".format(access_key, secret_key))


def listToString(str_list):
  result = ''
  for s in str_list:
    result += s + ' '
  return (result.strip( ))

def iListToString(int_list):
  result = ''
  for i in int_list:
    result += str(i) + ' '
  return (result.strip( ))

# Helper method to serialize datetime fields
def json_datetime_serializer(obj):
  if isinstance(obj, (datetime, date)):
    return obj.isoformat()
  raise TypeError ("Type %s not serializable" % type(obj))

def unique_list(lst):
  return list(set(lst))