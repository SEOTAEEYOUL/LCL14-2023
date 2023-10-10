# CLI

> [구성 기본 사항](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds)  

## AWS CLI
### Linux
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
./aws/install -i /usr/local/aws-cli -b /usr/local/bin
```
```bash
sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update
which aws
ls -l /usr/local/bin/aws
```

### Windows
[AWSCLIV2](https://awscli.amazonaws.com/AWSCLIV2.msi)
```powershell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
aws --version
```
```
PS C:\workspace\AWSBasic> aws --version
aws-cli/2.4.24 Python/3.8.8 Windows/10 exe/AMD64 prompt/off
PS C:\workspace\AWSBasic> 
```



## aws-iam-authenticator
```powershell
choco install -y aws-iam-authenticator
aws-iam-authenticator help
```
```powershell
curl -o aws-iam-authenticator.exe https://amazon-eks.s3.us-west-2.amazonaws.com/1.21.2/2021-07-05/bin/windows/amd64/aws-iam-authenticator.exe
aws-iam-authenticator help
```

## 액세스 키 ID 및 보안 액세스 키  
### 키 페어 생성
![IAM-사용자-Security credentials(IAM-사용자-SecurityCredentials(보안자격증명)-CreateAccessKey(액세스키생성).png.png](./img/IAM-사용자-SecurityCredentials(보안자격증명)-CreateAccessKey(액세스키생성).png)


### aws cli 구성
```
PS C:\workspace\AWSBasic> aws configure
AWS Access Key ID [****************GWEC]: **IA**OR**3K**OEWDIC
AWS Secret Access Key [****************/N4/]: ****************KZW0ywudbmbSvIysCLqz/UFi 
Default region name [ap-northeast-2]:
Default output format [json]:
PS C:\workspace\AWSBasic> 
```


### .csv 파일을 통한 key pair 가져오기
```
aws configure import --csv file://ca07456_accessKeys.csv
```

## 프로파일
- 설정 모음을 프로파일이라고 함
- 여러개의 로그인을 사용할 경우 사용
### profile 생성
awd configure --profile ca07456
```
PS C:\workspace\AWSBasic> aws configure --profile ca07456
AWS Access Key ID [****************WDIC]: 
AWS Secret Access Key [****************CLqz]:
Default region name [None]: ap-northeast-2
Default output format [None]: json
PS C:\workspace\AWSBasic> 
```

### profile 생성 확인
aws configure list --profile ca07456
```
PS C:\workspace\AWSBasic> aws configure list --profile ca07456
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                  ca07456           manual    --profile
access_key     ****************WDIC shared-credentials-file
secret_key     ****************/UFi shared-credentials-file
    region           ap-northeast-2      config-file    ~/.aws/config
PS C:\workspace\AWSBasic> 
```

### 구성 목록 보기
aws configure list
```
PS C:\workspace\AWSBasic> aws configure list         
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************WDIC shared-credentials-file
secret_key     ****************/UFi shared-credentials-file
    region           ap-northeast-2      config-file    ~/.aws/config
```

### 프로파일 목록 보기
aws configure list-profiles
```
PS C:\workspace\AWSBasic> aws configure list-profiles
default
710984438158_CA_eks-admin
ca07456
PS C:\workspace\AWSBasic> 
```

### 프로파일 설정 보기
aws configure get region 
```
PS C:\workspace\AWSBasic\2.EKS\powershell> aws configure get access_key --profile ca07456
PS C:\workspace\AWSBasic\2.EKS\powershell> aws configure get secret_key --profile ca07456
PS C:\workspace\AWSBasic\2.EKS\powershell> aws configure get region --profile ca07456    
ap-northeast-2
PS C:\workspace\AWSBasic\2.EKS\powershell> aws configure get output --profile ca07456
json
PS C:\workspace\AWSBasic\2.EKS\powershell> 
```

### 설정된 profile로 AWS 서비스 접근되는지 확인
```
PS C:\workspace\AWSBasic> aws s3 ls --profile ca07456
2020-04-01 11:22:17 aws-landing-zone-s3-access-logs-520666629845-us-east-1
2022-01-12 15:13:24 cf-templates-1i9b4mx1ufiw7-ap-northeast-2
2022-01-18 10:02:13 cf-templates-1i9b4mx1ufiw7-ap-northeast-3
2022-01-12 14:51:07 edu-dev-an2-s3-mybucket-03124
2022-01-19 15:58:38 edu-dev-an2-s3-mybucket-05087
2022-01-19 15:58:36 edu-dev-an2-s3-mybucket-07297
2022-01-12 14:51:04 edu-dev-an2-s3-mybucket-08405
2022-03-11 10:52:50 edu-dev-an2-s3-mybucket-10565
PS C:\workspace\AWSBasic> 
```

```
export AWS_ACCESS_KEY_ID=**********
export AWS_SESSION_TOKEN=**********
export AWS_SECRET_ACCESS_KEY=**********
```
