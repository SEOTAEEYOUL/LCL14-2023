import boto3
from pprint import pprint

ec2 = boto3.resource('ec2')

def get_value(dict_list, key):
    # pprint(dict_list)

    is_exist = False
    for dict in dict_list:
        if dict["Key"] == key:
            # print(dict["Value"])
            return dict['Value']

    return None

def is_exist(dict_list, key):
    # pprint(dict_list)

    is_exist = False
    for dict in dict_list:
        if dict["Key"] == key:
            # print(dict["Value"])
            is_exist = True
            break

    return is_exist


def check_required_tags( ):

    keys = [ 'Environment', 'ServiceName', 'Personalinformation']
    
    tag_cnt = 0

    for instance in ec2.instances.all():
        # pprint(instance.tags)
        # 키가 있는지 확인
        name = get_value(instance.tags, 'Name')
        print(f'{name}')
        for key in keys:
   
            if is_exist(instance.tags, key) == False:
                print(f'\t{key} 를 추가함')
                # print(f'Environment 키가 없음')
                if key == 'Environment':
                    instance.create_tags(Tags=[{'Key': 'Environment', 'Value': 'prd'}])
                elif key == 'Personalinformation':
                    instance.create_tags(Tags=[{'Key': 'Personalinformation', 'Value': 'yes'}])
                elif key == 'ServiceName':
                     instance.create_tags(Tags=[{'Key': 'ServiceName', 'Value': 'argos'}])       
        
       



if __name__ == "__main__":
    # region_args, profile_args = get_arguments()
    # main(region_args, profile_args)
    check_required_tags( )