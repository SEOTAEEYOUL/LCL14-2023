import boto3

def get_s3_bucket_list():
    # AWS 인증 정보 설정
    # session = boto3.Session(
    #     aws_access_key_id='YOUR_ACCESS_KEY',
    #     aws_secret_access_key='YOUR_SECRET_KEY',
    # )
    
    # S3 클라이언트 생성
    # s3_client = session.client('s3')
    s3_client = boto3.client('s3')

    try:
        # 버킷 목록 가져오기
        response = s3_client.list_buckets()

        # 각 버킷의 이름과 생성일자 출력
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            creation_date = bucket['CreationDate']
            print(f'Bucket: {bucket_name}, Creation Date: {creation_date}')
            # get_s3_bucket_object_list(bucket_name)
    except Exception as e:
        print(f'Error: {str(e)}')

def get_s3_bucket_object_list(bucket_name):
    # AWS 인증 정보 설정
    # session = boto3.Session(
    #     aws_access_key_id='YOUR_ACCESS_KEY',
    #     aws_secret_access_key='YOUR_SECRET_KEY',
    # )

    # S3 클라이언트 생성
    # s3_client = session.client('s3')
    s3_client = boto3.client('s3')

    try:
        # 버킷 안의 객체 목록 가져오기
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        # 객체 속성 출력
        if 'Contents' in response:
            for obj in response['Contents']:
                obj_key = obj['Key']
                obj_size = obj['Size']
                obj_last_modified = obj['LastModified']
                print(f'Object Key: {obj_key}, Size: {obj_size} bytes, Last Modified: {obj_last_modified}')
        else:
            print(f'Bucket[{bucket_name}] is empty.')
    except Exception as e:
        print(f'Error: {str(e)}')


def s3_upload_file(bucket_name, file_name):
    # S3 클라이언트 생성
    s3_client = boto3.client('s3')

    try:
        # index.html 파일 업로드
        with open(file_name, 'rb') as file:
            s3_client.upload_fileobj(file, bucket_name, file_name)
        
        print('index.html uploaded successfully.')
    except Exception as e:
        print(f'Error uploading index.html: {str(e)}')

def s3_read_file(bucket_name, file_name):
    # S3 클라이언트 생성
    s3_client = boto3.client('s3')

    try:
        # index.html 파일 읽기
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        html_content = response['Body'].read().decode('utf-8')
        
        print('index.html content:')
        print(html_content)
    except Exception as e:
        print(f'Error reading index.html: {str(e)}')

if __name__ == "__main__":
    # 함수 호출
    get_s3_bucket_list()

    # 버킷 이름을 입력하세요.
    bucket_name = 's3-bucket-argos'
    # file_name = 'index.html'
    # file_name = 'system_check.html'
    file_names = [
        'template/index.html',
        'template/resource_check.html',
        'template/system_check.html',
        'template/error.html',
        'template/404.html',
        'template/alert_list.html'
    ]
    
    # get_s3_bucket_object_list(bucket_name)

    for file_name in file_names:
        # index.html 파일을 저장합니다.
        s3_upload_file(bucket_name, file_name)

    # 버킷 목록을 확인하고 index.html 파일의 내용을 출력합니다.
    get_s3_bucket_object_list(bucket_name)

    for file_name in file_names:
        s3_read_file(bucket_name, file_name)
