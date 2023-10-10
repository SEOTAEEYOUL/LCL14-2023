# Datadog Alarm


> [Managing Datadog with Terraform](https://www.datadoghq.com/blog/managing-datadog-with-terraform/)  
> [Datadog 알람을 Terraform으로 만들어 보자.](https://tech.cloudmt.co.kr/2020/12/10/datadog-terraform/)  
> [Learn Terraform - Automate Monitoring with the Terraform Datadog Provider](https://github.com/hashicorp/learn-terraform-datadog-local)  
> [Monitor Types](https://docs.datadoghq.com/monitors/types/)  
> [Automate Monitoring with the Terraform Datadog Provider](https://developer.hashicorp.com/terraform/tutorials/applications/datadog-provider)  
> [Datadog Provider](https://registry.terraform.io/providers/DataDog/datadog/latest/docs)  
> [datadog_monitor (Resource)](https://registry.terraform.io/providers/DataDog/datadog/latest/docs/resources/monitor)  
> [datadog_api_key (Resource)](https://registry.terraform.io/providers/DataDog/datadog/latest/docs/resources/api_key)  

## Terraform Datadog Alert 예시 코드
| 소스명 | 설명 |  
|:---|:---|  
| provider.tf | provider 정의 |  
| variables.tf | 변수 선언 |  
| terraform.tfvars | 선언한 변수값 정의 |  
| monitor-ec2.tf | EC2 의 CPU 사용율 알람 |  


## 설정
### Notify your team
#### Title
```
[AROGS 관제] DB Performance 1분 이상 Slow Queries
```
```
[AWS 관제] DB dead lock 발생
```
```
[ARGOS 관제] ARGOS EC2 Host Down
```
```
[P2][SYSTEM] [{{host.name}}] EC2의 CPU Test 사용률이 역시 높습니다.
```
#### Body
```
■ 임계치 : ARGOS DB ( Aurora Mysql ) slow queries 최근 5분 동안 1분 이상의 queries
■ 알람 그룹 : {{query.name}} {{dbclusteridentifier.name}} 
■ 현재값 : {{value}}
■ 발생시간 : Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
■ 알람대상 : @slack-ARGOS-monitoring @webhook-AlertNow
```
```
■ 임계치 : ARGOS DB dead lock 발생
■ 알람 그룹 : {{engine}}
■ 호스트 : {{name}}
■ 현재값 : {{value}}
■ 발생시간 : Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}} 
■ 알람대상 : @slack-ARGOS-monitoring @webhook-AlertNow
```
```
■ 알람명 : ARGOS EC2 Host down
■ 알람 그룹 : {{host.argos}} 
■ 호스트 : {{host.name}}
■ 서버 IP : {{{{is_match "host.name" "sksh-argos-p-gw-blbi-ec2-2a-01"}}}} 10.70.35.61 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-blbi-ec2-2b-02"}}}} 10.70.36.61 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-blbk-ec2-2a-01"}}}} 10.70.35.58 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-blbk-ec2-2b-02"}}}} 10.70.36.58 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-blbk-ec2-2b-03"}}}} 10.70.37.58 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-ktcdc-ec2-2a-01"}}}} 10.50.25.2 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-ktcdc-ec2-2a-02"}}}} 10.50.25.10 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-moni-ec2-2b-01"}}}} 10.70.36.67 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-moni-ec2-2c-02"}}}} 10.70.37.67 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-rrs-ec2-2a-01"}}}} 10.70.35.55 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-rrs-ec2-2b-02"}}}} 10.70.36.55 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-skali-ec2-2a-01"}}}} 10.70.35.31 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-skali-ec2-2b-02"}}}} 10.70.36.31 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-sksig-ec2-2a-01"}}}} 10.70.35.43 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-sksig-ec2-2b-02"}}}} 10.70.36.43 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-upali-ec2-2a-01"}}}} 10.70.35.34 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-upali-ec2-2b-02"}}}} 10.70.36.34 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-upwlt-ec2-2a-01"}}}} 10.70.35.46 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-upwlt-ec2-2b-02"}}}} 10.70.36.46 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-icms-rrs-ec2-2a-03"}}}} 10.70.64.101 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-icms-rrs-ec2-2b-02"}}}} 10.70.64.52 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-icms-rrs-panel-ec2-2a-01"}}}} 10.70.64.40 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-icms-ec2-2a-01"}}}} 10.70.35.77 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-icms-ec2-2c-02"}}}} 10.70.37.77 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-infra-ops-ec2-2c-01"}}}} 10.70.37.10 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-arg-ec2-2a-01"}}}} 10.70.35.11 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-arg-ec2-2b-02"}}}} 10.70.36.11 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-cad-ec2-2a-01"}}}} 10.70.35.15 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-cap-ec2-2a-01"}}}} 10.70.35.13 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-cap-ec2-2b-02"}}}} 10.70.36.13 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-sol-msg-ec2-2a-01"}}}} 10.70.35.21 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-sol-msg-ec2-2b-02"}}}} 10.70.36.21 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-sol-sear-ec2-2c-01"}}}} 10.70.37.17 {{{{/is_match}}}}
■ 용도 : {{{{is_match "host.name" "sksh-argos-p-gw-blbi-ec2-2a-01"}}}} BlueLine, BlueIP, BlueNMS 신호 및 NMS정보 수집 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-blbi-ec2-2b-02"}}}} BlueLine, BlueIP, BlueNMS 신호 및 NMS정보 수집 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-blbk-ec2-2a-01"}}}} 금융기관(전용회선) 신호 송수신 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-blbk-ec2-2b-02"}}}} 금융기관(VPN) 신호 송수신 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-blbk-ec2-2b-02"}}}} 금융기관(X.25) 신호 송수신 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-ktcdc-ec2-2a-01"}}}} KT CDC 신호수신 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-ktcdc-ec2-2a-02"}}}} KT CDC 신호수신 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-moni-ec2-2b-01"}}}} 프로세스의 성능,에러,시스템메시지 출력을 위한 프로세스 운영 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-moni-ec2-2c-02"}}}} 프로세스의 성능,에러,시스템메시지 출력을 위한 프로세스 운영 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-rrs-ec2-2a-01"}}}} SKT,LG 무선망 원격제어/패널ID받기 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-rrs-ec2-2b-02"}}}} SKT,LG 무선망 원격제어/패널ID받기 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-skali-ec2-2a-01"}}}} SKT CAT.M1 Alive 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-skali-ec2-2b-02"}}}} SKT CAT.M1 Alive 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-sksig-ec2-2a-01"}}}} SKT CAT.M1 신호 수집 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-sksig-ec2-2b-02"}}}} SKT CAT.M1 신호 수집 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-upali-ec2-2a-01"}}}} LG U+ WLTE Alive서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-upali-ec2-2b-02"}}}} LG U+ WLTE Alive서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-upwlt-ec2-2a-01"}}}} LG WLTE 신호 수집 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-upwlt-ec2-2b-02"}}}} LG WLTE 신호 수집 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-icms-rrs-ec2-2a-03"}}}} I-CMS인터넷 주장치 원격제어 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-icms-rrs-ec2-2b-02"}}}} I-CMS인터넷 주장치 원격제어 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-icms-rrs-panel-ec2-2a-01"}}}} I-CMS인터넷 주장치 패널ID받기 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-icms-ec2-2a-01"}}}} 인터넷을 통하여 직접 신호 수집서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-gw-icms-ec2-2c-02"}}}} 인터넷을 통하여 직접 신호 수집서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-infra-ops-ec2-2c-01"}}}} EKS 관리 용 베스천 서버 (+ Datadog 설치 이미지 ) {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-arg-ec2-2a-01"}}}} 모바일ARGOS App의 WAS 서버 ( MQTT 서버 ) {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-arg-ec2-2b-02"}}}} 모바일ARGOS App의 WAS 서버 ( MQTT 서버 ) {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-cad-ec2-2a-01"}}}} ARGOS CAD WEB/WAS 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-cap-ec2-2a-01"}}}} 마이캡스 모바일 App WAS 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-mob-cap-ec2-2b-02"}}}} 마이캡스 모바일 App WAS 서버 {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-sol-msg-ec2-2a-01"}}}} SMS, 알림Talk, Email 메세징 서비스 WAS 서버, DRM 문서보안 서비스링크 Agent ( API )  {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-sol-msg-ec2-2b-02"}}}} SMS, 알림Talk, Email 메세징 서비스 WAS 서버, DRM 문서보안 서비스링크 Agent ( API ) {{{{/is_match}}}}{{{{is_match "host.name" "sksh-argos-p-sol-sear-ec2-2c-01"}}}} 지식관리 솔루션 WAS 서버 {{{{/is_match}}}}
■ 현재값 : {{value}}
■ 발생시간 : Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}} 
■ 알람대상 : @webhook-AlertNow @slack-ARGOS-monitoring
```
```
{{#is_alert}}
[P2][SYSTEM] ({{host.name}})의 CPU Test 사용률이 {{threshold}}% 이상입니다.
EC2 인스턴스의 상태를 확인해주세요.
{{/is_alert}}

{{#is_warning}}
[P3][SYSTEM] ({{host.name}})의 CPU Test 사용률이 {{warn_threshold}}% 이상입니다.
EC2 인스턴스의 상태를 확인해주세요.
{{/is_warning}}

{{#is_recovery}}
Alert 상태가 해제되었습니다.
{{/is_recovery}}
Noti: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @webhook-alert_collect
```

## 배포하기
```
terraform init
terraform plan
terraform apply
terraform state list
```

### terraform init
```powershell
PS > terraform init

Initializing the backend...

Initializing provider plugins...
- Finding latest version of datadog/datadog...
- Installing datadog/datadog v3.26.0...
- Installed datadog/datadog v3.26.0 (signed by a HashiCorp partner, key ID FB70BE941301C3EA)

Partner and community providers are signed by their developers.
If you'd like to know more about provider signing, you can read about it here:
https://www.terraform.io/docs/cli/plugins/signing.html

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
PS > 
```

#### terraform plan
```
PS > terraform plan 
datadog_monitor.ec2_cpu: Refreshing state... [id=122774605]

Terraform used the selected providers to generate the following execution plan. Resource        
actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # datadog_monitor.ec2_cpu will be updated in-place
  ~ resource "datadog_monitor" "ec2_cpu" {
        id                   = "122774605"
      ~ name                 = "[P2][SYSTEM] [{{host.service}}] EC2의 CPU 사용률이 높습니다." -> "[P2][SYSTEM] [{{host.name}}] EC2의 CPU 사용률이 높습니다."
        tags                 = [
            "EC2",
            "P2",
            "SYSTEM",
            "team:skcc",
        ]
        # (18 unchanged attributes hidden)

        # (1 unchanged block hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.

─────────────────────────────────────────────────────────────────────────────────────────────── 

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take    
exactly these actions if you run "terraform apply" now.
PS > 
```

#### terraform apply
```
PS > terraform apply
datadog_monitor.ec2_cpu: Refreshing state... [id=122774605]

Terraform used the selected providers to generate the following execution plan. Resource        
actions are indicated with the following symbols:
  ~ update in-place

Terraform will perform the following actions:

  # datadog_monitor.ec2_cpu will be updated in-place
  ~ resource "datadog_monitor" "ec2_cpu" {
        id                   = "122774605"
      ~ name                 = "[P2][SYSTEM] [{{host.service}}] EC2의 CPU 사용률이 높습니다." -> "[P2][SYSTEM] [{{host.name}}] EC2의 CPU 사용률이 높습니다."
        tags                 = [
            "EC2",
            "P2",
            "SYSTEM",
            "team:skcc",
        ]
        # (18 unchanged attributes hidden)

        # (1 unchanged block hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

datadog_monitor.ec2_cpu: Modifying... [id=122774605]
datadog_monitor.ec2_cpu: Modifications complete after 0s [id=122774605]

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
PS > 
```