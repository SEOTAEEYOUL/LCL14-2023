# 알림 생성
resource "datadog_monitor" "mysql_lock_10m" {
    name          = "[P4][DB] MySQL Lock 10분 이상 지속"
    type          = "query alert"
    query         = "sum(last_5m):sum:mysql.innodb.row_lock_time{*} by {dbclusterinstance} > 1800"
    message = <<EOF
## MySQL Lock 10분 이상 지속
{{#is_alert}}
{{override_priority 'P3'}}
[P3][DB] MySQL ({{dbinstanceidentifier.name}})  MySQL Lock 30분 이상 지속 
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}

{{#is_warning}}
{{override_priority 'P4'}}
[P4][DB] MySQL ({{dbinstanceidentifier.name}})  MySQL Lock 15분 이상 지속 
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_info @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["MySQL", "Lock", "team:skcc", "monitor:DB-MySQL-Lock-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "Aurora MySQL Lock 10분 이상 지속 원인 파악 및 조치가 필요합니다."
    priority                 = 3

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1800
        warning  = 900
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "mysql_max_cpu_90" {
    name          = "[P1][DB] 최근 5분 동안 MySQL {{dbinstanceidentifier.name}} MAX CPU 사용율이 90% 입니다"
    type          = "query alert"
    query         = "avg(last_5m):max:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-aurora-mysql-*} by {name} >= 90"
    message = <<EOF
## 최근 5분 동안 MySQL {{dbinstanceidentifier.name}} MAX CPU 사용율이 90% 

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["MySQL", "Lock", "team:skcc", "monitor:DB-MySQL-MAX_CPU_90-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "최근 5분 동안 MySQL {{dbinstanceidentifier.name}} MAX CPU 사용율이 90% 이상 지속 원인 파악 및 조치가 필요합니다."
    priority                 = 1

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 90
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mysql_tempspace_90" {
    name          = "[P1][DB] Aurora MySQL ({{dbinstanceidentifier.name}} Temporary storage > 90%"
    type          = "query alert"
    query         = "min(last_10m):avg:aws.rds.free_local_storage{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {dbinstanceidentifier} / 1024 / 1024 / 1024 < 3"
    message = <<EOF
## Aurora MySQL ({{dbinstanceidentifier.name}} Temporary storage 사용율이 90% 이상 지속

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["MySQL", "TempSpace", "team:skcc", "monitor:DB-MySQL-TempSpace_90-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "MySQL {{dbinstanceidentifier.name}} Temporary Storage 사용율이 90% 이상 지속 원인 파악 및 조치가 필요합니다."
    priority                 = 1

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 3
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mysql_memory_low" {
    name          = "[P2][DB] MySQL {{hostname.name}} 사용 가능한 메모리가 너무 적습니다.(10% 미만)"
    type          = "query alert"
    query         = "min(last_10m):avg:aws.rds.freeable_memory{dbinstanceidentifier:sksh-argos-p-aurora-mysql-*} by {hostname} < 10737418240"
    message = <<EOF
## MySQL {{hostname.name}} 사용 가능한 메모리가 너무 적습니다(10% 미만)  

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] MySQL ({{hostname.name}} )  사용 가능한 메모리가  약 2.6% 입니다. ( 전체 384 중 GiB 10 GiB 미만  )
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}

{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] MySQL ({{hostname.name}})  사용 가능한 메모리가  약 5.2% 미만 입니다. ( 전체 384 GiB 중 20 GiB 미만 )
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["P2", "MySQL", "UsableMemory", "TooLow", "team:skcc", "monitor:DB-UsableMemory-TooLow-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "Aurora MySQL 사용 가능한 메모리가 너무 적습니다. 원인 파악 및 조치가 필요합니다."
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 10737418240
        warning  = 21474836480
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mysql_query_long_run" {
    name          = "[P5][DB] MySQL 에서 30초 이상 수행되는 Query 가 발생함"
    type          = "query alert"
    query         = "sum(last_5m):sum:mysql.queries.lock_time{*} by {query,dbclusteridentifier}.as_count() > 60000000000"
    message = <<EOF
## MySQL 느린 Query 가 발생함  

{{#is_alert}}
{{override_priority 'P4'}}
### [P4][DB] MySQL({{dbclusteridentifier.name}}) slow queries 최근 5분 동안 60초 이상의 queries 발생
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p4 @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}

{{#is_warning}}
{{override_priority 'P5'}}
### [P5][DB] MySQL({{dbclusteridentifier.name}}) slow queries 최근 5분 동안 30초 이상의 queries 발생
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p5 @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

`dbclusteridentifier: {{dbclusteridentifier.name}}`   
`query: {{query.name}}`   
`time: {{value}}`  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["P2", "MySQL", "Query", "LongRun", "team:skcc", "monitor:DB-MySQL-Query-LongRun-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "최근 5분 동안 Aurora MySQL 30초 이상 수행된 Query 발생. 원인 파악 및 조치가 필요합니다."
    priority                 = 4

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 60000000000
        warning  = 30000000000
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mysql_max_cpu_utilization_high" {
    name          = "[P1][DB] MySQL {{dbinstanceidentifier.name}} CPU 사용율이 너무 높음"
    type          = "query alert"
    query         = "avg(last_5m):max:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {name} >= 80"
    message = <<EOF
## MAX CPU Utilization is too high  

{{#is_alert}}
{{override_priority 'P1'}}
### [P1][DB] MySQL({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}% 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}


{{#is_warning}}
{{override_priority 'P2'}}
### [P2][DB] MySQL({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}% 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

`dbclusteridentifier: {{dbclusteridentifier.name}}`   
`time: {{value}}`  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}

EOF
    tags                     = ["P1", "MySQL", "CPU", "TooHigh", "team:skcc", "monitor:DB-MySQL-CPU-TooHigh-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "MySQL({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}%,  원인 파악 및 조치가 필요합니다."
    priority                 = 1

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 80
        warning  = 60
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mysql_temporary_storage_usage_high" {
    name          = "[P2][DB] MySQL {{dbinstanceidentifier.name}} Local Temporary storage  사용율이 너무 높음"
    type          = "query alert"
    query         = "min(last_10m):avg:aws.rds.free_local_storage{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {dbinstanceidentifier} < 1073741824"
    message = <<EOF
## MySQL {{dbinstanceidentifier.name}} Local Temporary storage 사용율이 너무 높음

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] MySQL({{dbinstanceidentifier.name}}) 최근 10분 동안 Local Temporary storage 사용률이 1 GB({{value}} 이하임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}


{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] MySQL({{dbinstanceidentifier.name}}) 최근 10분 동안 Local Temporary storage 사용률이 2 GB({{value}}) 이하임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

`dbclusteridentifier: {{dbinstanceidentifier.name}}`   
`time: {{value}}`  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["P2", "MySQL", "TemporaryStorage", "TooLow", "team:skcc", "monitor:DB-MySQL-Temporary-TooLow-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "MySQL({{dbinstanceidentifier.name}}) 최근 10분 동안 Local Temporary storage 사용률이 2 GB({{value}}) 이하임,  원인 파악 및 조치가 필요합니다."
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1073741824  # 1GB
        warning  = 2147483648  # 2GB
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mysql_engine_uptime_alarm" {
    name          = "[P2][DB] MySQL {{dbinstanceidentifier.name}} Aurora engine uptime alarm"
    type          = "query alert"
    query         = "min(last_15m):avg:aws.rds.engine_uptime{hostname:sksh-argos-p-aurora-mysql*} by {hostname} <= 90"
    message = <<EOF
## Aurora MySQL {{hostname.name}} engine uptime alarm

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] Aurora MySQL({{hostname.name}}) 의 기동시간이 90 초 ({{value}}) 이하임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos _p2 @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}


{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] Aurora MySQL({{hostname.name}}) 의 기동시간이 360 초 ({{value}}) 이하임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

`dbclusteridentifier: {{hostname.name}}`   
`time: {{value}}`  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["P2", "MySQL", "Engine", "UptimeAlarm", "team:skcc", "monitor:DB-MySQL-Engine-UptimeAlarm-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "Aurora MySQL({{hostname.name}}) engine uptime alarm,  원인 파악 및 조치가 필요합니다."
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 90   # 1m 30s
        warning  = 360  # 6m
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mysql_dml_latency_alarm" {
    name          = "[P2][DB] MySQL DML latency over 1800 seconds"
    type          = "query alert"
    query         = "max(last_10m):avg:aws.rds.dmllatency{dbclusteridentifier:sksh-argos-p-aurora-mysql*} by {name} > 1800000"
    message = <<EOF
## 최근 10분동안 MySQL {{dbclusteridentifier.name}} DML 대기시간이 1800 초 이상임

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] 최근 10분동안 MySQL({{dbclusteridentifier.name}}) 의 DML 대기시간이 1800 초 ({{value}}) 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}


{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] 최근 10분동안 MySQL({{dbclusteridentifier.name}}) 의 DML 대기시간이 1500 초 ({{value}}) 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

`dbclusteridentifier: {{dbclusteridentifier.name}}`   
`time: {{value}}`  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["P2", "MySQL", "DML", "Latency", "team:skcc", "monitor:DB-MySQL-DML-Latency-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = " 최근 10분동안 MySQL({{dbclusteridentifier.name}}) 의 DML 대기시간이 1800 초 ({{value}}) 이상임,  원인 파악 및 조치가 필요합니다."
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1800000   # 30m
        warning  = 1500000   # 25m
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mysql_ddl_latency_alarm" {
    name          = "[P2][DB] MySQL({{name.name}}) ddl latency over 600 seconds"
    type          = "query alert"
    query         = "max(last_10m):avg:aws.rds.ddllatency{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {name} > 600000"
    message = <<EOF
## 최근 10분동안 MySQL {{dbinstanceidentifier.name}} DDL 대기시간이 600 초 이상임

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] 최근 10분동안 MySQL({{dbinstanceidentifier.name}}) 의 DDL 대기시간이 600(10분) 초 ({{value}}) 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}


{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] 최근 10분동안 MySQL({{dbinstanceidentifier.name}}) 의 DDL 대기시간이 480(8분) 초 ({{value}}) 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

`dbinstanceidentifier: {{dbinstanceidentifier.name}}`   
`ddllatency: {{value}}`  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["P2", "MySQL", "DDL", "Latency", "team:skcc", "monitor:DB-MySQL-DDL-Latency-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = " 최근 10분동안 MySQL({{dbinstanceidentifier.name}}) 의 DDL 대기시간이 6000 초 ({{value}}) 이상임,  원인 파악 및 조치가 필요합니다."
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 600000    # 10m
        warning  = 480000    # 8m
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}
