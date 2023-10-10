# DevOps

사일로를 허물고 소프트웨어 개발 팀과 IT 운영 팀 의 작업을 결합 및 자동화하여 소프트웨어 개발 수명 주기를 단축하고 고품질 소프트웨어 제공 속도를 높이는 것을 목표로 하는 일련의 관행입니다.

## GitOps
> PaaS 환경화에서 CI, CD 를 Git 를 통해 관리하는 시스템을 구축하여, blue/green 과 같은 무중단 배포를 기반으로 한 상시 배포 환경을 구축하여 업무의 민첩성을 확보함을 목표로 함  

## 사용도구
### OSS
- Gitea    : Git Repository
- Jenkins  : CI Pipeline, 소스가 Git에 배포되면 빌드하여 Container Image 를 만들어 Image Repository 에 저장하는 Pipeline 을 수행
- Harbor   : Container Image Repository
- ArgoCD   : Git 에 Manifest 가 배포 됨을 확인하여 동기화 및 배포하는 도구

### AWS Managed Service
- CodeCommit : 안전한 Git 기반 리포지토리를 호스팅하는 완전관리형 소스 제어 서비스  
- CodeBuild : 소스 코드를 컴파일하는 단계부터 테스트 실행 후 소프트웨어 패키지를 개발하여 배포하는 단계까지 마칠 수 있는 완전관리형의 지속적 통합 서비스  
- CodeDeploy : Amazon EC2, AWS Fargate, AWS Lambda 및 온프레미스 서버와 같은 다양한 컴퓨팅 서비스에 대한 소프트웨어 배포를 자동화하는 완전관리형 배포 서비스  
- CodePipeline : 빠르고 안정적인 애플리케이션 및 인프라 업데이트를 위해 릴리스 파이프라인을 자동화하는 데 도움이 되는 완전관리형 지속적 전달 서비스  

[Link]  
[AWS CodeCommit란 무엇인가요?](https://docs.aws.amazon.com/ko_kr/codecommit/latest/userguide/welcome.html)  
[AWS CodeBuild(이)란 무엇입니까?](https://docs.aws.amazon.com/ko_kr/codebuild/latest/userguide/welcome.html)  
[AWS CodeDeploy란 무엇입니까?](https://docs.aws.amazon.com/ko_kr/codedeploy/latest/userguide/welcome.html)  
[AWS CodePipeline란 무엇인가요?](https://docs.aws.amazon.com/ko_kr/codepipeline/latest/userguide/welcome.html)  

### [DevOps와 SRE의 세 가지 차이점](https://www.ibm.com/blog/three-differences-between-devops-and-sre/)  


| 항목 | DevOps | SRE |  
|:---|:---|:---|  
| 개발 및 구현 | 핵심 개발에 관한 것 | 핵심 구현에 관한 것  |  
| | 속도, 품질 및 제어 기능으로 애플리케이션을 구축, 테스트, 배포 및 모니터링하는 데 도움이 되는 소프트웨어 개발에 민첩한 접근 방식을 취함 |  운영 데이터 및 소프트웨어 엔지니어링을 활용하여 IT 운영 작업을 자동화하고 소프트웨어 제공을 가속화하는 동시에 IT 위험을 최소화 |  
| 기술 | 소프트웨어 작성 | 왜 무엇이 잘못되었는지 찾기 위한 분석 |  
| | 코드를 작성하고 테스트하고 문제를 해결하는 데 도움이 되는 애플리케이션 라인을 얻기 위해 노력| 같은 문제가 계속 발생하지 않도록 보장하기를 원함 |  
| 오토메이션 | 배포를 자동화 </br> 작업과 기능을 자동화 | 중복성을 자동화 </BR> 수동 작업을 자동화 |  




