# EC2 Check

## `aws.ec2.status_check_failed_system` vs `aws.ec2.status_check_failed_instance`

AWS.EC2.status_check_failed_system 및 AWS.EC2.status_check_failed_instance 메트릭은 Amazon Elastic Compute Cloud(EC2) 인스턴스의 상태 검사 실패를 추적합니다.

### AWS.EC2.status_check_failed_system
- EC2 인스턴스의 시스템 상태 검사가 실패한 수를 추적
- 시스템 상태 검사는 하드웨어 오류 또는 네트워크 연결 문제와 같은 인스턴스의 시스템 수준 문제를 식별하는 데 사용
- 시스템 상태 검사가 실패하면 인스턴스는 여전히 실행 중일 수 있지만 기본 하드웨어 또는 소프트웨어 문제로 인해 제대로 작동하지 않을 수 있음
- [P1][System] Host OS 사용 불가 {{host.name}}
- avg(last_15m):anomalies(avg:aws.ec2.status_check_failed_system{aws_account:123456789012}, 'basic', 2, direction='both', interval=60, alert_window='last_15m', count_default_zero='true') >= 1


### AWS.EC2.status_check_failed_instance
- 인스턴스 상태 검사가 실패한 수를 추적
- 인스턴스 상태 검사는 인스턴스 운영 체제 또는 애플리케이션과 같은 인스턴스 수준 문제를 식별하는 데 사용
- 인스턴스 상태 검사가 실패하면 인스턴스가 중지
- [P1][SYSTEM] {{name.name}} - EC2 instance status failed
- avg(last_5m):avg:aws.ec2.status_check_failed_instance{name:sksh-argos-p-*} by {name} > 0

두 메트릭 모두 인스턴스의 상태를 모니터링하고 문제를 식별하는 데 사용할 수 있습니다. 그러나 AWS.EC2.status_check_failed_system 메트릭은 더 중요한 것으로 간주되며 시스템 수준 문제를 식별하는 데 사용됩니다.