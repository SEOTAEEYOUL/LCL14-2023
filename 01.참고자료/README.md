# 참고 프로젝트 및 자료

> [[SecuPy]Python 을 이용한 보안점검 Agent 개발 Phase - I](./SecuPy.md)  
> [[전사 TCL] Python 을 활용한 CRUD Matrix 자동분석 연구](./CRUD-Matrix%20-%EC%9E%90%EB%8F%99%EB%B6%84%EC%84%9D.md)  
> [Alert Now 소개 자료](./AlertNow_intro.pdf)  
> [[무한 경쟁 MSP ④] 관리 솔루션 ‘CMP’ 부상…MSP 대상 솔루션 판매도](http://www.itdaily.kr/news/articleView.html?idxno=207257)  
  - 컨설팅
    - 엔지니어링
    - 구축/운영
> [Multi-Cloud Management Platform](https://mcmp.cloudz.co.kr/main)  
> [Morpheus Data](http://www.softworks.co.kr/cmp/sub0101.html)  
> [CMP 비교](https://www.whatmatrix.com/comparison/Cloud-Management-Platforms)  
> [MSP](./MSP.md)  
> [Multi-Tenancy](./Multi-Tenant.md)  
> [DevOps](./DevOps.md), [SRE](./SRE.md), [DevOps vs SRE](./DevOPS-SRE.md)  
> [IaC](./IaC.md)  


`CSP`는 반재료에 해당하는 방대한 인프라단 서비스와 제품을 개발하고, `MSP`는 이들 반재료들을 완제품으로 만들어주는 역할을 한다

## 용어

### CSP(Cloud Service Provider, 클라우드 서비스 제공업체)  
기업에서 네트워크를 통해 주문형으로 액세스할 수 있는 클라우드 기반 컴퓨팅, 스토리지, 플랫폼, 애플리케이션 서비스 등의 확장 가능한 컴퓨팅 리소스를 제공하는 제3자 회사입니다.
-  AWS, MS Azure, GCP ...

### MSP(Managed Service Provider, 클라우드 매니지드 서비스 기업)  
- 네트워크를 통해 여러 기업들에게 network, application, system 그리고 e-management 서비스를 제공하는 사업자
- `pay-as-yo-go(종량제)` 형태의 가격 정책을 서비스를 제공해야 함
- 메가존 클라우드, 베스핀글로벌, 클루커스  ... 
  - Monitoring
  - Management
  - Service


### CMP(Cloud Management Platform, 클라우드 관리 플랫폼)
- 관리 솔루션
- CMP 활용한 운영 효율화와 역량강화
#### 가트너가 정의한 클라우드 관리 영역(7가지)
![가트너가-정의한-클라우드-관리-영역7가지.png](./img/%EA%B0%80%ED%8A%B8%EB%84%88%EA%B0%80-%EC%A0%95%EC%9D%98%ED%95%9C-%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C-%EA%B4%80%EB%A6%AC-%EC%98%81%EC%97%AD7%EA%B0%80%EC%A7%80.png)  
- 프로비저닝
- 코스트관리
- 클라우드 마이그레이션
- 보안관리
- 딜리버리
- 모니터링&분석
- 인벤토리관리
- 셀프서비스

#### 제공하는 서비스
- Multi-Cloud
- IT Automation
  - Administration
    - Multi-tenant support
    - Published API
  - Configuration Management
    - Chef
    - Puppet
    - `Ansible`
  - Network
    - SDN Support
    - Public cloud networking
  - User-Defined Actions
    - Conditional Actions
    - Pre-and Post-Install Actions
    - `Scheduled Actions`
  - Orchestration & Workflow
    - Natvie Workflow
    - 3rd Party Orchestration
    - `Webhooks`
  - 3rd Party Automation
    - ServiceNow
    - 3rd Party Atomation
    - CMDB Integration
  - User-Defined Properties
    - Automatic hostname creation
    - Configuration tags
  - Placement
    - Best Execution Venue - Performance
    - Best Execution Venue - Security
    - Best Execution Venue - Cost
    - Runtime polices
  - Provisioning
    - Bare-metal provisioning
  - Reconfiguration & expiration
    - Ability to change VM configuration
    - Live change VM resources
    - Scheduled expiration
  - Uptime management
    - Continous Infrastructure Testing
    - HA/DR fetures
- User Self-Service
- Chargeback
- Governance
- Security
- DevOps

### 프로덕트 팀



## 요건
### 정기 PM or 배포 등으로 발생하는 Alert 에 대해서 L1 에 미리 공지하여 무시할 수 있도록 대응할 수 있는 체계 확보
#### 현황
- 회사 MCMP 시스템은 회사에서 제공하는 CSP 사와의 계약으로 만들어진 시스템에 대한 MSP 를 위해 만들어서 일부 Ticket 올리는 기능만 사용 가능

####  해결 방안
- Ticket (정기 PM 작업)을 올릴 때 해당 내용을 Slack 의 `#comm_shieldus_argos`에 내용을 보내서 L1, L2 간의 작업 내용 공유 및 발생할 수 있는 P1 레벨의 Alert 를 특정 시점에 무시할 수 있도록 함
- Support Portal 를 통해 정기 작업를 입력시 위와 같은 작업이 가능
- Service Flow 가 기본사용이며, Servic Flow 와 Support Portal 은 연동이 안됨