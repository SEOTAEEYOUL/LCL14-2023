# 알림 생성
resource "datadog_monitor" "ec2_cpu_high" {
    name          = "[P2][SYSTEM] 최근 5분동안 EC2[{{host.name}}] 의 CPU 사용률이 {{threshold}}% 이상 입니다"
    type          = "query alert"
    query         = "avg(last_5m):100 - avg:system.cpu.idle{host:sksh*} by {host} >= 90"
    message = <<EOF
# EC2[{{host.name}}] 의 {{threshold}}% 이상, 높은 CPU 사용률 확인 필요합니다. 
{{#is_alert}}  
[P2][SYSTEM] ({{host.name}})의 CPU 사용률이 {{threshold}}% 이상입니다.  
EC2 인스턴스의 상태를 확인해주세요.  
{{/is_alert}}  

{{#is_warning}}  
[P3][SYSTEM] ({{host.name}})의 CPU 사용률이 {{warn_threshold}}% 이상입니다.  
EC2 인스턴스의 상태를 확인해주세요.  
{{/is_warning}}  

{{#is_recovery}}  
Alert 상태가 해제되었습니다.  
{{/is_recovery}}  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                = ["P2", "SYSTEM", "EC2", "CPU", "team:skcc", "monitor:SYSTEM-EC2-CPU-High-01"]
    notify_audit        = false
    # restricted_roles    = ["write"]
    timeout_h           = 0
    include_tags        = true
    require_full_window = false
    new_group_delay      = 60
    notify_no_data      = false
    escalation_message  = "EC2[{{host.name}}] 의 {{threshold}}% 이상, 높은 CPU 사용률 확인 필요합니다."
    priority            = 2
    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 90
        warning = 80
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


# 알림 생성
resource "datadog_monitor" "ec2_instance_status_fail" {
    name                = "[P1][SYSTEM] {{name.name}} - EC2 인스턴스 상태 실패"
    type                = "query alert"
    query               = "avg(last_5m):avg:aws.ec2.status_check_failed_instance{!name:sksh-argos-p-eks*} by {name} > 0"
    message = <<EOF
[P1][SYSTEM] {{name.name}} - EC2 인스턴스 상태 실패 
EC2 인스턴스의 상태를 확인해주세요.  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                = ["P1", "SYSTEM", "EC2", "Instance", "Fail", "team:skcc", "monitor:SYSTEM-EC2-Instance-Fail-01"]
    notify_audit        = false
    # restricted_roles    = ["write"]
    timeout_h           = 0
    include_tags        = true
    require_full_window = false
    new_group_delay      = 300
    notify_no_data      = false
    escalation_message  = "EC2 인스턴스의 상태를 확인해주세요."
    priority            = 1
    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 0
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_5m"
    #     recovery_window = "last_5m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "ec2_fs_inode_usage_high" {
    name                = "[P1][System] Host {{name.name}} - FS inode 사용량이 높습니다"
    type                = "query alert"
    query               = "avg(last_5m):avg:system.fs.inodes.in_use{name:sksh-argos-p*,device:/*} by {name,device} * 100 >= 90"
    message = <<EOF
## EC2[{{name.name}}] 의 inode 를 확인해 주세요
### inode 수를 확인
```
df -i
```
- iused: 사용된 inode 수
- ifree: 사용 가능한 inode 수
- %iused: 사용된 inode의 백분율

### 식별하기
- ls -laShr <경로_디렉토리>

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                = ["P1", "SYSTEM", "EC2", "FS", "inode", "team:skcc", "monitor:SYSTEM-EC2-FS-inode-01"]
    notify_audit        = false
    # restricted_roles    = ["write"]
    timeout_h           = 0
    include_tags        = true
    require_full_window = false
    new_group_delay      = 60
    notify_no_data      = false
    escalation_message  = "EC2({{name.name}}) 파일시스템의 inode 사용량이 높습니다. 상태를 확인해주세요."
    priority            = 1
    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 90
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_5m"
    #     recovery_window = "last_5m"
    # }

    renotify_interval = 60
}

/*
resource "datadog_monitor" "ec2_os_unavailable" {
    name          = "[P1][System] Host {{name.name}} - FS inode 사용량이 높습니다"
    type          = "query alert"
    query         = "avg(last_5m):avg:system.fs.inodes.in_use{name:sksh-argos-p*,device:/*} by {name,device} * 100 >= 90"
    message = <<EOF
## EC2[{{name.name}}] 의 inode 를 확인해 주세요
### inode 수를 확인
```
df -i
```
- iused: 사용된 inode 수
- ifree: 사용 가능한 inode 수
- %iused: 사용된 inode의 백분율

### 식별하기
- ls -laShr <경로_디렉토리>

Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                = ["P1", "SYSTEM", "EC2", "FS", "inode", "team:skcc", "monitor:SYSTEM-EC2-FS-inode-01"]
    notify_audit        = false
    # restricted_roles    = ["write"]
    timeout_h           = 0
    include_tags        = true
    require_full_window = false
    new_group_delay      = 60
    notify_no_data      = false
    escalation_message  = "EC2({{name.name}}) 파일시스템의 inode 사용량이 높습니다. 상태를 확인해주세요."
    priority            = 1
    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 90
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_5m"
    #     recovery_window = "last_5m"
    # }

    renotify_interval = 60
}
*/

resource "datadog_monitor" "ec2_ebs_fail" {
    name                = "[P1][System] Host {{host.name}} - EBS failed - {{volume-name.name}}"
    type                = "query alert"
    query               = "min(last_1m):max:aws.ebs.status.ok{volume-name:*} by {volume-name} < 1"
    message = <<EOF
## [P2][System] Host {{host.name}} - EBS failed - {{volume-name.name}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                = ["P1", "SYSTEM", "EC2", "EBS", "Fail", "team:skcc", "monitor:SYSTEM-EC2-EBS-Fail-01"]
    notify_audit        = false
    # restricted_roles    = ["write"]
    timeout_h           = 0
    include_tags        = true
    require_full_window = false
    new_group_delay      = 300
    notify_no_data      = false
    escalation_message  = "EC2 EBS 상태를 확인해주세요."
    priority            = 1
    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_5m"
    #     recovery_window = "last_5m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "ec2_mem_high" {
    name                = "[P1][System] Host [{{name.name}}] - 메모리 사용량이 90 %  이상입니다."
    type                = "query alert"
    query               = "avg(last_5m):(1 - avg:system.mem.pct_usable{name:sksh-argos-p*} by {name}) * 100 >= 90"
    message = <<EOF
## [P2][System] 최근 5분 동안 Host [{{name.name}}] - 메모리 사용량이 {{value}} %  이상입니다.
상태 확인이 필요합니다.


Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                = ["P1", "SYSTEM", "EC2", "MEM", "High", "team:skcc", "monitor:SYSTEM-EC2-MEM-High-01"]
    notify_audit        = false
    # restricted_roles    = ["write"]
    timeout_h           = 0
    include_tags        = true
    require_full_window = false
    new_group_delay      = 300
    notify_no_data      = false
    escalation_message  = "EC2 Memory 사용량이 90% 이상, 상태를 확인해주세요."
    priority            = 1
    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 90
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_5m"
    #     recovery_window = "last_5m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "ec2_alert_message_log" {
    name                = "[P2][System] Host [{{host.name}}]- Alert messages log[{{log.message}}] 발생"
    type                = "event-v2 alert"
    query               = "events(\"Name:sksh-argos-p* filename:messages (\":emerg\" OR \":crit\" OR \":alert\" OR \"error: Operation\" OR \"kernel:err\")\").rollup(\"count\").by(\"host\").last(\"1m\") >= 1"
    message = <<EOF
## [P2][System] Host [{{host.name}}] - Alert messages log - {{log.message}} 발생
확인 부탁드립니다.
{{host.name}} :  {{log.message}} 


Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                = ["P2", "SYSTEM", "EC2", "Alert", "Message", "team:skcc", "monitor:SYSTEM-EC2-Alert-Message-01"]
    notify_audit        = false
    # restricted_roles    = ["write"]
    timeout_h           = 0
    include_tags        = true
    require_full_window = false
    new_group_delay      = 300
    notify_no_data      = false
    escalation_message  = "Host [{{host.name}}] Alert messages log 발생, 확인 부탁드립니다."
    priority            = 2
    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_5m"
    #     recovery_window = "last_5m"
    # }

    renotify_interval = 60
}