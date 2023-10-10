# LCL 환경

> [choco - 윈도우즈 패키지 매니저](./choco.md)  
> [vscode - 에디터](./vscode.md)  
> [AWS CLI](./CLI.md)  
> [Docker](./Docker.md)  


## AWS Console
https://123456789012.signin.aws.amazon.com/console

```
$Env:AWS_PROFILE="lcl14" 
aws sts get-caller-identity
```

## AWS Account
| 계정 | Account I.D |  
|:---|:---|  
| IAM | 123456789012 |  
| Network | 123456789012 |  
| Dev | 123456789012 |  
| Stg | 123456789012 |  
| Prd | 123456789012 |  

## 사용자 계정 밑에 .aws 디렉토리
### config
```
[default]
region = ap-northeast-2
output = json
[profile lcl14]
region = ap-northeast-2
output = json
```


### credentials
```
[default]
aws_access_key_id = **********
aws_secret_access_key = **********
[lcl14]
aws_access_key_id = **********
aws_secret_access_key = **********
```
