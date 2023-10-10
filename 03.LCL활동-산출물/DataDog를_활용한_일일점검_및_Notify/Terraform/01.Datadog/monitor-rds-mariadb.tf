resource "datadog_monitor" "mariadb_cpu_90" {
    name          = "[P1][DB] 최근 5분 동안 MariaDB({{name.name}}) CPU 사용율이 90% 이상 입니다."
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-rds-mariadb-*} by {name} > 90"
    message = <<EOF
## 최근 5분 동안 MariaDB({{name.name}}) CPU 사용율이 90% 이상

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["MariaDB", "CPU", "team:skcc", "monitor:DB-MariaDB-CPU_90-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "MariaDB {{name.name}} CPU 사용율이 90% 이상, 지속 원인 파악 및 조치가 필요합니다."
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


# db.t3.medium vCPU : 2, 메모리 : 4GiB
resource "datadog_monitor" "mariadb_01_freeable_memory_low" {
    name          = "[P2][DB] MariaDB01(IGP) {{hostname.name}} 사용 가능한 메모리({{value}})가 최근 5분동안 10% 미만 입니다."
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.rds.freeable_memory{dbinstanceidentifier:*,dbinstanceclass:db.t3.medium,engine:mariadb,dbinstanceidentifier:sksh-argos-p-rds-mariadb-01} by {name} < 214748364"
    message = <<EOF
# MariaDB01 {{hostname.name}} 사용 가능한 메모리({{value}})가 최근 5분동안 10% 미만, 확인 및 조치 필요합니다.
## Instance Type : db.t3.medium
## vCPU : 2
## 메모리 : 4GiB

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] MariaDB ({{hostname.name}} )  사용 가능한 메모리가  약 5% 미만 입니다. ( 전체 4 GiB 중 214.7 MiB  미만  )
{{/is_alert}}

{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] IGP MariaDB ({{hostname.name}})  사용 가능한 메모리가  약 10% 미만 입니다. ( 전체 4 GiB 중 429.5 MiB 미만 )
{{/is_warning}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["MariaDB", "FreeableMemory", "TooLow", "team:skcc", "monitor:DB-MariaDB01-FreeableMemory-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "MariaDB01(IGP)({{hostname.name}})의 사용 가능한 메모리({{value}})가 최근 5분동안 10% 미만, 확인 및 조치 필요합니다."
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 214748364 
        warning  = 429496729
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

#  db.t3.xlarge vCPU : 4, 메모리 : 16GiB
resource "datadog_monitor" "mariadb_02_freeable_memory_low" {
    name          = "[P2][DB] MariaDB02(CAD) {{hostname.name}} 사용 가능한 메모리({{value}})가 최근 5분동안 10% 미만 입니다."
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.rds.freeable_memory{dbinstanceidentifier:*,dbinstanceclass:db.t3.medium,engine:mariadb,dbinstanceidentifier:sksh-argos-p-rds-mariadb-02} by {name} < 805306368"
    message = <<EOF
# MariaDB02 {{hostname.name}} 사용 가능한 메모리({{value}})가 최근 5분동안 10% 미만, 확인 및 조치 필요합니다.
## Instance Type : db.t3.xlarge
## vCPU : 4
## 메모리 : 16GiB

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] MariaDB ({{hostname.name}} )  사용 가능한 메모리가  약 5% 미만 입니다. ( 전체 16 GiB 중 805 MiB  미만  )
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}

{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] MariaDB ({{hostname.name}})  사용 가능한 메모리가  약 10% 미만 입니다. ( 전체 16 GiB 중 1.6 GiB 미만 )
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["MariaDB", "FreeableMemory", "TooLow", "team:skcc", "monitor:DB-MariaDB02-FreeableMemory-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "CAD - MariaDB02({{hostname.name}})의 사용 가능한 메모리({{value}})가 최근 5분동안 10% 미만, 확인 및 조치 필요합니다."
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 805306368 
        warning  = 1610612736
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mariadb_01_free_storage_space_low" {
    name          = "[P2][DB] 최근 5분 동안 IGP MariaDB ({{dbinstanceidentifier.name}}) 여유 저장소 공간이 낮음"
    type          = "query alert"
    query         = "avg(last_5m):(avg:aws.rds.free_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-01} by {dbinstanceidentifier} / avg:aws.rds.total_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-01} by {dbinstanceidentifier}) * 100 < 4"
    message = <<EOF
# 최근 5분 동안 CAD MariaDB ({{dbinstanceidentifier.name}}) 여유 저장소 공간이 낮음, 확인 및 조치 필요합니다.

{{#is_alert}}
{{override_priority 'P1'}}
ALERT: [P1][DB] MariaDB ({{dbinstanceidentifier.name}})  저장소 사용량이 96% 이상입니다.
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_l1
{{/is_alert}}

{{#is_warning}}
{{override_priority 'P2'}}
ALERT: [P2][DB] MariaDB ({{dbinstanceidentifier.name}})  저장소 사용량이 90% 이상입니다.
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @slack-skshieldusnextossdev-prd알람 
{{/is_warning}} 

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "MariaDB", "IGP", "FreeStorageSpace", "Low", "team:skcc", "monitor:DB-ICP-MariaDB-FreeStorageSpace-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "최근 5분 동안 MariaDB ({{dbinstanceidentifier.name}}) 여유 저장소 공간이 낮음, 확인 및 조치 필요합니다."     
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 4 
        warning  = 10
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "mariadb_02_free_storage_space_low" {
    name          = "[P2][DB] 최근 5분 동안 CAD MariaDB ({{dbinstanceidentifier.name}}) 여유 저장소 공간이 낮음"
    type          = "query alert"
    query         = "avg(last_5m):(avg:aws.rds.free_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-02} by {dbinstanceidentifier} / avg:aws.rds.total_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-02} by {dbinstanceidentifier}) * 100 < 4"
    message = <<EOF
# 최근 5분 동안 CAD MariaDB ({{dbinstanceidentifier.name}}) 여유 저장소 공간이 낮음, 확인 및 조치 필요합니다.

{{#is_alert}}
{{override_priority 'P1'}}
ALERT: [P1][DB] MariaDB ({{dbinstanceidentifier.name}})  저장소 사용량이 96% 이상입니다.
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_l1
{{/is_alert}}

{{#is_warning}}
{{override_priority 'P2'}}
ALERT: [P2][DB] MariaDB ({{dbinstanceidentifier.name}})  저장소 사용량이 90% 이상입니다.
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @slack-skshieldusnextossdev-prd알람 
{{/is_warning}} 

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "MariaDB", "FreeStorageSpace", "Low", "team:skcc", "monitor:DB-MariaDB-FreeStorageSpace-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "최근 5분 동안 CAD MariaDB ({{dbinstanceidentifier.name}}) 여유 저장소 공간이 낮음, 확인 및 조치 필요합니다."     
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 4 
        warning  = 10
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "mariadb_max_connection_over_200" {
    name          = "[P2][DB] 최근 5분 동안 MariaDB {{dbinstanceidentifier.name}} 최대 접속이 200 이상(Max:450)"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.rds.database_connections{dbinstanceidentifier:sksh-argos-p-rds-mariadb*} by {name} > 200"
    message = <<EOF
# 최근 5분 동안 MariaDB {{dbinstanceidentifier.name}} Max connections over 200(Max:450) 이상, 확인 및 조치 필요
## {{name}} : {{value}}


{{#is_alert}}
{{override_priority 'P2'}}
ALERT: [P2][DB] 최근 5분 동안 MariaDB {{dbinstanceidentifier.name}} 최대 접속이 200 이상임(Max:450), 확인 및 조치 필요
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_l1
{{/is_alert}}

{{#is_warning}}
{{override_priority 'P3'}}
ALERT: [P3][DB] 최근 5분 동안 MariaDB {{dbinstanceidentifier.name}} 최대 접속이 100 이상임(Max:450), 확인 및 조치 필요
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @slack-skshieldusnextossdev-prd알람 
{{/is_warning}} 

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "MariaDB", "MaxConnection", "Over", "team:skcc", "monitor:DB-MariaDB-MaxConnecton-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "최근 5분 동안 MariaDB {{dbinstanceidentifier.name}} Max connections over 200(Max:450) 이상, 확인 및 조치 필요"     
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 200 
        warning  = 100
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "mariadb_01_max_cpu_utilization_high" {
    name          = "[P2][DB] IGP MariaDB {{dbinstanceidentifier.name}} CPU 사용율이 너무 높음"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-rds-mariadb-01} by {name} > 80"
    message = <<EOF
## MAX CPU Utilization is too high  

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] IGP MariaDB({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}% 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}


{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] IGP MariaDB({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}% 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

`dbclusteridentifier: {{dbclusteridentifier.name}}`   
`time: {{value}}`  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["P2", "IGP", "MariaDB", "CPU", "TooHigh", "team:skcc", "monitor:DB-MariaDB-CPU-TooHigh-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "IGP MariaDB({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}%,  원인 파악 및 조치가 필요합니다."
    priority                 = 2

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

resource "datadog_monitor" "mariadb_02_max_cpu_utilization_high" {
    name          = "[P2][DB] CAD MariaDB {{dbinstanceidentifier.name}} CPU 사용율이 너무 높음"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-rds-mariadb-02} by {name} > 80"
    message = <<EOF
## MAX CPU Utilization is too high  

{{#is_alert}}
{{override_priority 'P2'}}
### [P2][DB] CAD MariaDB({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}% 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
{{/is_alert}}


{{#is_warning}}
{{override_priority 'P3'}}
### [P3][DB] CAD MariaDB({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}% 이상임
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
{{/is_warning}}

`dbclusteridentifier: {{dbclusteridentifier.name}}`   
`time: {{value}}`  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
EOF
    tags                     = ["P2", "IGP", "MariaDB", "CPU", "TooHigh", "team:skcc", "monitor:DB-MariaDB-CPU-TooHigh-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "CAD MariaDB({{dbclusteridentifier.name}}) 최근 5분 동안 CPU 사용률이 {{value}}%,  원인 파악 및 조치가 필요합니다."
    priority                 = 2

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