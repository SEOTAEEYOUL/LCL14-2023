#  Pre-signed URL(미리 서명된 URL) 

> [미리 서명된 URL을 통해 객체 공유](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)  
> [미리 서명된 URL로 작업](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/using-presigned-url.html)  


- Pre-signed URL은 AWS 서명된 요청(Signed Request)
- 임시적인 인증과 권한을 제공하기 위해 사용
- URL에 포함된 서명 정보를 통해 인증 및 권한을 증명하고, S3 객체를 다운로드하거나 업로드할 수 있음

## python 으로 미리 서명된 URL 만들기
### boto3 설치
```
pip install boto3
```

### presigned usrl 생성 코드
```
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
````

## 수행결과
### presigned url 생성
```
PS > python pre-signed-url.py
https://s3-bucket-lcl14.s3.amazonaws.com/**********
PS > 
```
#### chrome 에서 열기
```
<Error>
<script id="youtube-hd-fjdmkanbdloodhegphphhklnjfngoffa">var ythdlog = () => {};;var ythderror = () => {};</script>
<Code>InvalidAccessKeyId</Code>
<Message>The AWS Access Key Id you provided does not exist in our records.</Message>
<AWSAccessKeyId>**********</AWSAccessKeyId>
<RequestId>**********</RequestId>
<HostId>**********</HostId>
</Error>
````

### CLI 만들기
#### presigned url 만들기
```
aws s3 presign s3://s3-bucket-lcl14/system_check.html --expires-in 1800
```
#### 실행결과
```
PS > aws s3 presign s3://s3-bucket-lcl14/system_check.html --expires-in 60
https://s3-bucket-lcl14.s3.ap-northeast-2.amazonaws.com/**********
PS > 
```

#### browser 에서 결과 보기
```
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<Error>
<script id="youtube-hd-fjdmkanbdloodhegphphhklnjfngoffa">var ythdlog = () => {};;var ythderror = () => {};</script>
<Code>InvalidAccessKeyId</Code>
<Message>The AWS Access Key Id you provided does not exist in our records.</Message>
<AWSAccessKeyId>**********</AWSAccessKeyId>
<RequestId>**********</RequestId>
<HostId>**********</HostId>
</Error>
```


## Terraform
```
provider "aws" {
  region = "ap-northeast-2"
}

data "aws_s3_bucket_object" "system_check" {
  bucket = "s3-bucket-lcl14"
  key    = "system_check.html"
}

resource "aws_s3_bucket_object_presigned_url" "presigned_url" {
  bucket       = data.aws_s3_bucket_object.system_check.bucket
  key          = data.aws_s3_bucket_object.system_check.key
  expires      = "1800"
  allowed_methods = ["GET"]
}
```
