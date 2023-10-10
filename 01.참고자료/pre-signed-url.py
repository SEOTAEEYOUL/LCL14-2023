import boto3

s3_client = boto3.client('s3')

url = s3_client.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 's3-bucket-lcl14',
        'Key': 'system_check.html'
    },
    ExpiresIn=360
)

print(url)