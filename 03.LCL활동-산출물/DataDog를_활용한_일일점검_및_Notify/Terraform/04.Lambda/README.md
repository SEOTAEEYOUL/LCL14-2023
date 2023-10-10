# Lambda

> [Terraform 으로 aws lambda & function url 만들기 (단일 람다 함수에 API GW 없이 URL 붙이기)](https://www.binaryflavor.com/terraform-euro-aws-lambda-url-gwa-hamgge-olrigi/)  
> [AWS Lambda Function URLs with Terraform](https://github.com/byunjuneseok/aws-lambda-function-urls-with-terraform)   
- 지금까지는 aws lambda를 URL로 서빙하려면 API Gateway 없이는 불가능했다.
- 하지만, 이제는 하나의 lambda에 하나의 url을 붙일 수 있다. 그리고 이 프로비저닝을 코드로 관리할 수도 있게 되었다.

> [Announcing AWS Lambda Function URLs: Built-in HTTPS Endpoints for Single-Function Microservices](https://aws.amazon.com/ko/blogs/aws/announcing-aws-lambda-function-urls-built-in-https-endpoints-for-single-function-microservices/)  
> [Create a AWS Lambda function using Terraform and Python](https://medium.com/@haissamhammoudfawaz/create-a-aws-lambda-function-using-terraform-and-python-4e0c2816753a)  
> [Resource: aws_cloudwatch_event_rule](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule.html#schedule_expression)  
> [AWS Lambda 함수 URL을 이용하여 편리하고 안전한 API 서버와 클라이언트 만들기](https://aws.amazon.com/ko/blogs/tech/creating-api-server-using-aws-lambda-function-url/)  
> [Slack - 메시지 서식 지정](https://slack.com/intl/ko-kr/help/articles/202288908-%EB%A9%94%EC%8B%9C%EC%A7%80-%EC%84%9C%EC%8B%9D-%EC%A7%80%EC%A0%95)  
> [Slack api - chat.postMessage](https://api.slack.com/methods/chat.postMessage)  
> [Slack - Block Bit Builder](https://app.slack.com/block-kit-builder/T04DZ0646#%7B%22blocks%22:%5B%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22Hey%20there%20%F0%9F%91%8B%20I'm%20TaskBot.%20I'm%20here%20to%20help%20you%20create%20and%20manage%20tasks%20in%20Slack.%5CnThere%20are%20two%20ways%20to%20quickly%20create%20tasks:%22%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22*1%EF%B8%8F%E2%83%A3%20Use%20the%20%60/task%60%20command*.%20Type%20%60/task%60%20followed%20by%20a%20short%20description%20of%20your%20tasks%20and%20I'll%20ask%20for%20a%20due%20date%20(if%20applicable).%20Try%20it%20out%20by%20using%20the%20%60/task%60%20command%20in%20this%20channel.%22%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22*2%EF%B8%8F%E2%83%A3%20Use%20the%20_Create%20a%20Task_%20action.*%20If%20you%20want%20to%20create%20a%20task%20from%20a%20message,%20select%20%60Create%20a%20Task%60%20in%20a%20message's%20context%20menu.%20Try%20it%20out%20by%20selecting%20the%20_Create%20a%20Task_%20action%20for%20this%20message%20(shown%20below).%22%7D%7D,%7B%22type%22:%22image%22,%22title%22:%7B%22type%22:%22plain_text%22,%22text%22:%22image1%22,%22emoji%22:true%7D,%22image_url%22:%22https://api.slack.com/img/blocks/bkb_template_images/onboardingComplex.jpg%22,%22alt_text%22:%22image1%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22%E2%9E%95%20To%20start%20tracking%20your%20team's%20tasks,%20*add%20me%20to%20a%20channel*%20and%20I'll%20introduce%20myself.%20I'm%20usually%20added%20to%20a%20team%20or%20project%20channel.%20Type%20%60/invite%20@TaskBot%60%20from%20the%20channel%20or%20pick%20a%20channel%20on%20the%20right.%22%7D,%22accessory%22:%7B%22type%22:%22conversations_select%22,%22placeholder%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Select%20a%20channel...%22,%22emoji%22:true%7D%7D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22%F0%9F%91%80%20View%20all%20tasks%20with%20%60/task%20list%60%5Cn%E2%9D%93Get%20help%20at%20any%20time%20with%20%60/task%20help%60%20or%20type%20*help*%20in%20a%20DM%20with%20me%22%7D%5D%7D%5D%7D)  


```
$Env:SLACK_WEBHOOK_URL="https://hooks.slack.com/services/**********"
$Env:SLACK_CHANNEL="lcl14"
$Env:LAMBDA_URL="https://app.datadoghq.com/dashboard/**********"
```

## Terraform

1. terraform init - 초기화 (provider 설치)
2. terraform plan - 생성 및 수정, 삭제할 자원을 보여줌
3. terraform apply - 자원 생성 및 backend(S3) 에 현재 자원 상태(tfstate) 저장
4. terraform state list - 상태 보기
5. terraform output - output.tf 에 지정된 자원에 대해 보여줌
6. terraform destroy - 생성된 자원을 삭제 (주의)

## [01. 발생된 Alert 저장](./00.colletion/README.md)  

## [02. 일일점검 - Datadog Alert 이용, Slack 에 결과 통보](./01.daily-check/README.md)

## [03. 일일점검 결과 Slack 에 통보](./02.notification/README.md)
