# EC2 GW 서버에 Tag 추가
- 임의 or 자동 생성된 VM의 경우 필수 Tag 가 누락된 경우 붙여주는 Util. 

## 표준 Tag

- 8 종이 표준 Tag
  - 5종 필수 Tag
  - 3종 사용자 정의 Tag

### 표준 Tag 활용
| 구분 | Cloud Z 화면에 노출되는 키 | CSP Tag Key | Tag 값 사용 예 |  
|:---|:---|:---|:---|  
| 필수 | 프로젝트 | cz-project | hr, mobile, ... |  
| | 담당자 | cz-owner | 홍길동, jack, ... |  
| | 운영환경 | cz-stage | prod, dev, staging, ... |  
| | 팀/조직 | cz-org | myteam, ops, ... |  
| | 서비스용도 | cz-appl | phone, 조직도, ... |  
| 사용자 정의 | 사용자정의1(변경가능) | cz-ext1 |  |  
| | 사용자정의2(변경가능) | cz-ext2 |  |  
| | 사용자정의3(변경가능) | cz-ext3 |  |  
- Cloud Z Tag에서 지정한 Tag 는 CSP 에도 자동 연동됩니다. CSP 콘솔에서는 CSP Tag Key 값으로 표시됩니다.  

### Tag 값 제약사항
- Tag key별로 1개의 Tag 값만 가질 수 있습니다.
- Tag 값은 소문자, 한글, 숫자, 대시(-), 언더바(_)만 사용 가능하며, 최대 63자까지만 허용 됩니다.
- Tag 값의 시작과 끝은 특수문자를 사용 할 수 없습니다.


### 환경 설정
```
$Env:AWS_PROFILE="lcl14"
aws sts get-caller-identity
```

#### 실행 결과
```
PS > $Env:AWS_PROFILE="lcl14"
PS > aws sts get-caller-identity
{
    "UserId": "**********",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/argos_py"
}
```


### EC2 Tag 처리 프로그램
| program | 설명 |  
|:---|:---|  
| ec2type-tag.py | EC2Type Tag 를 Name 의 문자열을 보고 붙이는 프로그램 |  
| ec2-tag-check.py | EC2 의 필수 Tag 가 빠져 있는 경우 붙이는 프로그램 |  

#### `EC2Type` Tag 값 
| Name | EC2Type Tag 값 |  
|:---|:---|  
| mob | Mobile |  
| gw | GW |  
| sol | Solution |  
| infra | Infra |  
| eks | EKSNode |  

#### 수행방법
```
python ec2type-tag.py
python ec2-tag-check.py
```

#### 실행 결과
```
PS > python ec2-gw-tag.py
name[sksh-argos-p-gw-sksig-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-skali-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-sol-msg-ec2-2a-01] -> Tag: EC2Type=Solution
name[sksh-argos-p-mob-arg-ec2-2a-01] -> Tag: EC2Type=Mobile
name[sksh-argos-p-gw-blbi-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-mob-cap-ec2-2a-01] -> Tag: EC2Type=Mobile
name[sksh-argos-p-gw-rrs-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-gwicms-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-upali-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-upwlt-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-ktcdc-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-ktcdc-ec2-2a-02] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-skali-ec2-2b-02] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-upali-ec2] -> Tag: EC2Type=GW
name[sksh-argos-p-mob-arg-ec2-2b-02] -> Tag: EC2Type=Mobile
name[sksh-argos-p-sol-msg-ec2-2b-02] -> Tag: EC2Type=Solution
name[sksh-argos-p-gw-sksig-ec2-2b-02] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-upwlt-ec2-2b-02] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-rrs-ec2-2b-02] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-blbi-ec2-2b-02] -> Tag: EC2Type=GW
name[sksh-argos-p-mob-cap-ec2-2b-02] -> Tag: EC2Type=Mobile
name[sksh-argos-p-gw-moni-ec2-2b-01] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-blbk-ec2-2b-02] -> Tag: EC2Type=GW
name[sksh-argos-p-icms-rrs-ec2-2b-02] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-moni-ec2-2c-02] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-gwicms-ec2-2c-02] -> Tag: EC2Type=GW
name[sksh-argos-p-infra-ops-ec2-2c-01] -> Tag: EC2Type=Infra
name[sksh-argos-p-sol-sear-ec2-2c-01] -> Tag: EC2Type=Solution
name[sksh-argos-p-eks-cna-worker-2] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-ui-worker-1] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-ui-mgmt-1] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-ui-worker-2] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-igp-worker-2] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-cna-worker-1] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-ui-worker-8] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-gw-blbk-ec2-2c-03] -> Tag: EC2Type=GW
name[sksh-argos-p-gw-icms-ec2-2c-02] -> Tag: EC2Type=GW
name[sksh-argos-p-eks-igp-worker-3] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-igp-worker-4] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-ui-worker-3] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-ui-worker-4] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-cna-worker-3] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-ui-ng-worker-1] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-mob-cad-ec2-2a-01] -> Tag: EC2Type=Mobile
name[sksh-argos-p-gw-blbk-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-icms-rrs-panel-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-icms-rrs-ec2-2a-03] -> Tag: EC2Type=GW
name[sksh-argos-p-eks-ui-worker-5] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-cna-mgmt-1] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-igp-worker-5] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-igp-worker-1] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-igp-mgmt-1] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-cna-worker-4] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-cna-worker-5] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-gw-icms-ec2-2a-01] -> Tag: EC2Type=GW
name[sksh-argos-p-eks-ui-ng-worker-1] -> Tag: EC2Type=EKSNode
name[sksh-argos-p-eks-ui-ng-worker-1] -> Tag: EC2Type=EKSNode
EC2Type Tag 수정된 총 EC2 개수[57] 개
PS > 
```
```
PS > python ec2-tag-check.py
sksh-argos-p-gw-sksig-ec2-2a-01
sksh-argos-p-gw-skali-ec2-2a-01 
sksh-argos-p-sol-msg-ec2-2a-01  
sksh-argos-p-mob-arg-ec2-2a-01  
sksh-argos-p-gw-blbi-ec2-2a-01  
sksh-argos-p-mob-cap-ec2-2a-01  
sksh-argos-p-gw-rrs-ec2-2a-01   
sksh-argos-p-gw-gwicms-ec2-2a-01
sksh-argos-p-gw-upali-ec2-2a-01 
sksh-argos-p-gw-upwlt-ec2-2a-01 
sksh-argos-p-gw-ktcdc-ec2-2a-01
sksh-argos-p-gw-ktcdc-ec2-2a-02
sksh-argos-p-gw-skali-ec2-2b-02
sksh-argos-p-gw-upali-ec2
sksh-argos-p-mob-arg-ec2-2b-02
sksh-argos-p-sol-msg-ec2-2b-02
sksh-argos-p-gw-sksig-ec2-2b-02
sksh-argos-p-gw-upwlt-ec2-2b-02
sksh-argos-p-gw-rrs-ec2-2b-02
sksh-argos-p-gw-blbi-ec2-2b-02
sksh-argos-p-mob-cap-ec2-2b-02
sksh-argos-p-gw-moni-ec2-2b-01
sksh-argos-p-gw-blbk-ec2-2b-02
sksh-argos-p-icms-rrs-ec2-2b-02
sksh-argos-p-gw-moni-ec2-2c-02
sksh-argos-p-gw-gwicms-ec2-2c-02
sksh-argos-p-infra-ops-ec2-2c-01
sksh-argos-p-sol-sear-ec2-2c-01
sksh-argos-p-eks-cna-worker-2
sksh-argos-p-eks-ui-worker-1
sksh-argos-p-eks-ui-mgmt-1
sksh-argos-p-eks-ui-worker-2
sksh-argos-p-eks-igp-worker-2
sksh-argos-p-eks-cna-worker-1
sksh-argos-p-eks-ui-worker-8
sksh-argos-p-gw-blbk-ec2-2c-03
sksh-argos-p-gw-icms-ec2-2c-02
sksh-argos-p-eks-igp-worker-3
sksh-argos-p-eks-igp-worker-4
sksh-argos-p-eks-ui-worker-3
sksh-argos-p-eks-ui-worker-4
sksh-argos-p-cad-mig-ec2-2b-09
sksh-argos-p-cad-mig-ec2-2b-10
sksh-argos-p-eks-cna-worker-3
sksh-argos-p-eks-ui-ng-worker-1
sksh-argos-p-mob-cad-ec2-2a-01
sksh-argos-p-gw-blbk-ec2-2a-01
sksh-argos-p-icms-rrs-panel-ec2-2a-01
sksh-argos-p-icms-rrs-ec2-2a-03
sksh-argos-p-pt-whatap-ec2
sksh-argos-p-eks-ui-worker-5
sksh-argos-p-eks-cna-mgmt-1
sksh-argos-p-eks-igp-worker-5
sksh-argos-p-eks-igp-worker-1
sksh-argos-p-eks-igp-mgmt-1
sksh-argos-p-eks-cna-worker-4
sksh-argos-p-eks-cna-worker-5
sksh-argos-p-gw-icms-ec2-2a-01
sksh-argos-p-eks-ui-ng-worker-1
        Environment 를 추가함
        ServiceName 를 추가함
        Personalinformation 를 추가함
sksh-argos-p-eks-ui-ng-worker-1
        Environment 를 추가함
        ServiceName 를 추가함
        Personalinformation 를 추가함
PS >
```

