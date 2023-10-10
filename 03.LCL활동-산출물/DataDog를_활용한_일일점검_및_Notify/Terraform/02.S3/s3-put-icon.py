import os
import boto3
from datetime import datetime

# AWS S3 정보
# aws_access_key = 'YOUR_AWS_ACCESS_KEY'
# aws_secret_key = 'YOUR_AWS_SECRET_KEY'
bucket_name = 's3-bucket-argos'

# S3 클라이언트 생성
# s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
s3_client = boto3.client('s3')

# def upload_to_s3(file_path, file_name):
#     try:
#         # 파일 업로드
#         s3_client.upload_file(file_path, bucket_name, file_name)
#         return True
#     except Exception as e:
#         print(f"파일 업로드 오류: {e}")
#         return False

def s3_upload_file(bucket_name, file_name):
    # S3 클라이언트 생성
    s3_client = boto3.client('s3')

    try:
        # index.html 파일 업로드
        with open(file_name, 'rb') as file:
            s3_client.upload_fileobj(file, bucket_name, file_name)
        
        return True
    except Exception as e:
        print(f"파일 업로드 오류: {e}")
        return False

def list_uploaded_files():
    try:
        # S3 버킷 내 파일 리스트업
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            uploaded_files = response['Contents']
            return uploaded_files
        else:
            print("업로드된 파일 없음")
            return []
    except Exception as e:
        print(f"파일 리스트업 오류: {e}")
        return []

def get_file_info(file_object):
    # 파일 정보 추출 (이름, 크기, 업로드 날짜)
    file_name = file_object['Key']
    file_size = file_object['Size']
    upload_date = file_object['LastModified']
    return file_name, file_size, upload_date

def main():
    # 현재 디렉토리 파일 리스트업
    current_directory = os.getcwd()
    current_directory = 'icon'
    # print(f'current_directory[{current_directory}]')
    files = os.listdir(current_directory)


    # S3에 파일 업로드
    for file_name in files:
        # print(f'file_name[{file_name}]')
        # file_path = os.path.join(current_directory, file_name)
        file_path = f'{current_directory}/{file_name}' 
        # print(f'file_path[{file_path}]')
        # if upload_to_s3(file_path, file_name):
        if s3_upload_file(bucket_name, file_path):
            print(f"{file_name}을(를) S3에 성공적으로 업로드하였습니다.")
        else:
            print(f"{file_name} 업로드 실패")    

    # 업로드된 파일 리스트업 및 정보 출력
    uploaded_files = list_uploaded_files()
    if uploaded_files:
        print("\n업로드된 파일 리스트:")
        for file_object in uploaded_files:
            file_name, file_size, upload_date = get_file_info(file_object)
            print(f"파일명: {file_name}, 크기: {file_size} 바이트, 업로드 날짜: {upload_date}")

if __name__ == "__main__":
    main()
