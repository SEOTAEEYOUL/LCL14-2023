# Datadog


## L1 표준 모니터링 항목

## Datadog Priority 별 Slack 채널
| Slack 채널 | 설명 | Datadog Priority |  
|:---|:---|:---|  
| #ict_shieldus_argos_l1 | Critical (l1 channel) - 바로 확인 후 처리 | P1 |  
| #ict_shieldus_argos_p2 | 일과중 바로 확인 (p2 channel) | P2 |  
| #ict_shieldus_argos_p3 | 일과중 확인 (p3 channel) | P3 |   
| #ict_shieldus_argos_info | 주간 확인 (info channel) | P4 |
| #ict_shieldus_argos_info | 월간 확인 (info channel) | P5 |  

### EC2
| Monitor ID | 구분 | 항목 | Datadog Metric | 설명 | Alert Rule |  
|:---|:---|:---|:---|:---|:---|  
|| Status | Server Down | aws.ec2.status_check_failed_system | System Fail(OS 사용불가) | 해당 Metric 값이 0이 아닌 1 인 경우 |  
|| Status | EBS Fail | aws.ebs.status.ok | EBS(DISK) 사용불가 | 해당 Metric 값이 1이 아닌 0 인 경우 |  
|| Resource | CPU 사용률 | system.cpu.idle | CPU 과다사용 | 각 서버별 특성에 맞는 고정 임계치 사용 |  
|| Resource | MEM 사용률 | system.mem.usagable </br> system.mem.total | MEM 과다사용 | 각 서버별 특성에 맞는 고정 임계치 사용 |  
|| Resource | Disk 사용률 | system.disk.used </br> system.disk.total | Disk 과다사용 | 각 서버별 특성에 맞는 고정 임계치 사용 |  
|| Resource | inode 사용률 | system.fs.inodes.in_use | inode 과다사용 | 각 서버별 특성에 맞는 고정 임계치 사용 |  
|| Log | Linux Syslog| Filename : messages | System Error 발생 | [Keyword] </br> - critical </br> - alert </br> - error: Operation </br> - kernel:err |  

### EKS
| 구분 | 항목 | Datadog Metric | 설명 | Alert Rule |  
|:---|:---|:---|:---|:---|  
| Status | Pod Restarted |  kubernetes.containers.restarts | | | 
| Status | OOM Killed |  Log/Events : "OOM" 키워드 | | | 
| Status | Node NotReeady |  Log/Events : "NodeNotReady" | | | 
| Status | Pod 생성오류 |  Log/Events : "CrashLoopBackOff" | | | 
| Status | damonset |  kubernetes._state.daemonset.desired | | | 
| Resource | MEM 사용율 | system.mem.usable </br> system.mem.total | | | 
| Resource | Disk 사용율 | system.disk.used </br> system.disk.total | | | 
| Resource | Network Drop | kubernetes.network.tx_dropped </br> kubernetes.network.rx_dropped | | | 

### RDS
| 구분 | 항목 | Datadog Metric | 설명 | Alert Rule |  
|:---|:---|:---|:---|:---|  
| Status | 처리량 (쿼리) | trace.mysql.query.hits | | |  
| Status | 응답지연 (쿼리) | trace.mysql.query | | |  
| Status | 응답지연 (DML) | aws.rds.dmllatency | | max(last_10m):avg:aws.rds.dmllatency{dbclusteridentifier:sksh-argos-p-aurora-mysql*} by {name} > 1800000 |  
| Status | Restarted | aws.rds.engine_uptime |  Aurora engine uptime alarm | min(last_15m):avg:aws.rds.engine_uptime{hostname:sksh-argos-p-aurora-mysql*} by {hostname} <= 90 |  
| Status | Connection 과다 사용 | aws.rds.database_connections | | max(last_10m):avg:aws.rds.database_connections{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {dbinstanceidentifier} > 15000 |  
| Resource | CPU사용률 | aws.rds.cpuutilization | | avg(last_5m):max:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {name} >= 80 |  
| Resource | MEM 사용률 | aws.rds.freeable_memory | | avg(last_5m):avg:aws.rds.freeable_memory{dbinstanceidentifier:*,dbinstanceclass:db.t3.medium,engine:mariadb,!dbinstanceidentifier:sksh-argos-p-aurora-mysql-master-rci,!dbinstanceidentifier:sksh-argos-p-aurora-mysql-reader-rci} by {name} < 210000000 |  
| Resource | Disk사용률 | aws.rds.free_local_storage | Temporary storage  | min(last_10m):avg:aws.rds.free_local_storage{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {dbinstanceidentifier} < 1073741824 |  
| Resource | Disk사용률 | aws.rds.free_storage_space | 저장소 사용량  | avg(last_5m):(avg:aws.rds.free_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-*} by {dbinstanceidentifier} / avg:aws.rds.total_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-*} by {dbinstanceidentifier}) * 100 < 4 |  



## 일일 체크
- Datadog Alarm 을 입력하여 이중 Priority 1, 2 를 09, 22 시에 수행하여 결과 Report 함
- Terraform 으로 Alarm 데이터를 입력함

### [Python](./Python/README.md)  
#### Datadog Alert 목록 가져오기
- `python datadog-alert-list.py` 수행
  - 산출물
    - [alert_list.py](./Python/alert_list.py) : daily check lambda 에서 사용하기 위한 `P1`, `P2` 의 Datadog Alarm 목록

### [Terraform](./Terraform/README.md)  
- 공동작업을 위한 Backend 생성([S3](./Terraform//02.S3/README.md), [DynamoDB](./Terraform/03.DynamoDB/README.md))
- [Datadog Alarm 생성](./Terraform/01.Datadog/README.md)
- [AWS Lambda 생성](./Terraform/04.Lambda/README.md)
  - Python 함수, URL 생성 접근 가능
  - [`collection`:발생한 Alert 를 DynamoDB에 저장 및 테이블 형태로 보여주기](./Terraform/04.Lambda/00.colletion/)
    - Datadog 에서 Lambda URL 를 webhook 으로 등록하여 수집함
  - [`daily-check`:입력되어 있는 Datadog Alarm 의 `P1`, `P2` 를 09, 22 시에 수행, DynamoDB 에 저장]
  - [`notification`:09시 5분, 20시 5분에 시스템 체크 결과를 Slack 에 알림](./Terraform/04.Lambda/02.notification/README.md)
