import boto3


ec2 = boto3.resource('ec2')

ec2_cnt = 0
for instance in ec2.instances.all():
  for tag in instance.tags:
    if tag['Key'] == 'Name':
      name = tag['Value']
      if 'mob' in name:
        print(f'name[{name}] -> Tag: EC2Type=Mobile')
        # instance.create_tags(Tags=[{'Key': 'EC2Type', 'Value': 'Mobile'}])
        ec2_cnt += 1
      #   elif ['gw', 'icms'] in name:
      elif any(tag in name for tag in ['gw', 'icms']):
        print(f'name[{name}] -> Tag: EC2Type=GW')
        # instance.create_tags(Tags=[{'Key': 'EC2Type', 'Value': 'GW'}])
        ec2_cnt += 1
      elif 'sol' in name:
        print(f'name[{name}] -> Tag: EC2Type=Solution')
        # instance.create_tags(Tags=[{'Key': 'EC2Type', 'Value': 'Solution'}])
        ec2_cnt += 1
      elif 'infra' in name:
        print(f'name[{name}] -> Tag: EC2Type=Infra')
        instance.create_tags(Tags=[{'Key': 'EC2Type', 'Value': 'Infra'}])
        ec2_cnt += 1
      elif 'eks' in name:
        print(f'name[{name}] -> Tag: EC2Type=EKSNode')
        instance.create_tags(Tags=[{'Key': 'EKSNode', 'Value': 'Infra'}])
        ec2_cnt += 1

        instance.create_tags(Tags=[{'Key': 'Environment', 'Value': 'prd'}])
        instance.create_tags(Tags=[{'Key': 'Personalinformation', 'Value': 'yes'}])
        instance.create_tags(Tags=[{'Key': 'ServiceName', 'Value': 'argos'}])

print(f'EC2Type Tag 수정된 총 EC2 개수[{ec2_cnt}] 개')

# PS D:\workspace\Project-S\3.Prod\98.Monitoring\Python> python ec2-gw-tag.py
# name[sksh-argos-p-gw-sksig-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-skali-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-cmliv-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-blbi-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-rrs-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-gwicms-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-upali-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-upwlt-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-ktcdc-ec2-2a-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-ktcdc-ec2-2a-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-skali-ec2-2b-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-upali-ec2] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-sksig-ec2-2b-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-upwlt-ec2-2b-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-rrs-ec2-2b-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-blbi-ec2-2b-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-moni-ec2-2b-01] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-cmliv-ec2-2b-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-blbk-ec2-2b-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-moni-ec2-2c-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-gwicms-ec2-2c-02] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-blbk-ec2-2c-03] -> Tag: EC2Type=GW
# name[sksh-argos-p-gw-blbk-ec2-2a-01] -> Tag: EC2Type=GW
# EC2Type Tag 추가된 총 EC2 개수[23] 개

# for instance in ec2.instances.all():
#   for tag in instance.tags:
#     if tag['Key'] == 'EC2Type':
#       name = tag['Value']
#       if name in ['GW', 'Mobile', 'Solution']:
#         print(f'name[{name}] -> Tag: Environment=prd, ServiceName=argos, Personalinformation=yes')
#         # instance.create_tags(Tags=[{'Key': 'EC2Type', 'Value': 'GW'}])
#         instance.create_tags(Tags=[{'Key': 'Environment', 'Value': 'prd'}])
#         instance.create_tags(Tags=[{'Key': 'ServiceName', 'Value': 'argos'}])
#         instance.create_tags(Tags=[{'Key': 'Personalinformation', 'Value': 'yes'}])
#         gw_cnt += 1

# print(f'[Environment, ServiceName, Personalinformation] Tag 추가된 총 EC2 개수[{gw_cnt}] 개')