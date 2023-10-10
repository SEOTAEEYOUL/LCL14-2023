# 알림 생성
resource "datadog_monitor" "msk_response_rate" {
    name          = "[P4][CSP] MSK (Kafka) Response Rate"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.msk.kafka.server.replica.fetcher.metrics.response.rate{cluster_arn:arn:aws:kafka:ap-northeast-2:123456789012:cluster/sksh-argos-p-vpc-msk/98840637-0c22-4e47-83f7-f039b5f91c7a-3} > 9"
    message = <<EOF
# [AWS] 최근 5분 동안의 ARGOS MSK Response Rate (메시지큐 이상) {{name}} : {{value}}  

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                    = ["P4", "CSP", "MSK", "Response Rate", "team:skcc", "monitor:CSP-MSK-Response_Rate-01"]
    notify_audit            = false
    # restricted_roles    = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    # new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "최근 5분 동안의 MSK(Kafka) Response Rate (메시지큐 이상) 원인 파악 및 조치가 필요합니다."
    priority                 = 4

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"

    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 9
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "msk_under_replicated_partitions" {
    name          = "[P3][CSP] MSK Under Replicated Partitions - Broker : {{broker_id.name}} - {{value}}"
    type          = "query alert"
    query         = "sum(last_5m):sum:aws.kafka.under_replicated_partitions{cluster_name:sksh-argos-p-vpc-msk} by {broker_id} > 0"
    message       = <<EOF
## Kafka Under Replicated Partitions 발생 점검
- 현재 복제가 되지 않고 있는 파티션 수를 확인.
- 0 초과의 경우 점검 필요

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람
EOF
    priority                 = 3
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "Under Replicated Partitions가 발생했습니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P3", "CSP", "MSK", "UnderReplicatedPartitions", "team:skcc",  "monitor:CSP-MSK-UnderReplicatedPartitions-01"]


    monitor_thresholds {
        critical = 0        
    }
}


resource "datadog_monitor" "msk_offline_partition_count" {
    name          = "[P3][CSP] MSK Offline Partition Count - {{value}}"
    type          = "query alert"
    query         = "max(last_1h):max:aws.kafka.offline_partitions_count{cluster_name:sksh-argos-p-vpc-msk} > 0"
    message       = <<EOF
## Kafka Offline Partition Count 발생 점검
- 활성화된 리더가 없는 Partition 확인
- 0 초과의 경우 점검 필요

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 3
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    #new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "Offline Partition이 발생했습니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P3", "CSP", "MSK", "OfflinePartionCount", "team:skcc",  "monitor:CSP-MSK-OfflinePartitionCount-01"]


    monitor_thresholds {
        critical = 0        
    }
}


resource "datadog_monitor" "msk_disk_usage" {
    name          = "[P2][CSP] MSK 디스크 사용률이 85% 이상 ({{value}})"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.kafka.kafka_data_logs_disk_used{*} > 85"
    message       = <<EOF
## MSK Disk 사용률 점검
- 85% 초과 점검 필요

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 2
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    #new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "MSK Disk 사용률이 85% 이상입니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P2", "CSP", "MSK", "Disk", "team:skcc",  "monitor:CSP-MSK-DiskUsage-01"]


    monitor_thresholds {
        critical = 85
        warning = 70
    }
}


resource "datadog_monitor" "msk_max_partition_count" {
    name          = "[P3][CSP] MSK Max Partition Count - {{value}}"
    type          = "query alert"
    query         = "max(last_1h):max:aws.kafka.partition_count{cluster_name:sksh-argos-p-vpc-msk} > 1500"
    message       = <<EOF
## Kafka Max Partition Count 초과 점검
- 브로커 Spec 대비 권고 파티션 수 초과
- 1000 초과의 경우 점검 필요

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람
EOF
    priority                 = 3
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    #new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "Max Partition Count 권고 수를 초과했습니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P3", "CSP", "MSK", "MaxPartionCount", "team:skcc",  "monitor:CSP-MSK-MaxPartitionCount-01"]


    monitor_thresholds {
        critical = 1500
        warning = 1000
    }
}


resource "datadog_monitor" "msk_consumer_lag" {
    name          = "[P2][CSP] MSK Consumer Lag - {{groupid.name}} - {{value}}"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.msk.kafka.consumer.group.ConsumerLagMetrics.Value{cluster_arn:arn:aws:kafka:ap-northeast-2:123456789012:cluster/sksh-argos-p-vpc-msk/180e0a3b-1d0d-4994-8272-8c80bc96cc27-3} by {groupid} > 1000"
    message       = <<EOF
## Kafka Consumer Lag 발생 점검
- Consumer Application 점검 필요

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 2
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "Kafka Consumer Lag이 발생했습니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P2", "CSP", "MSK", "ConsumerLag", "team:skcc",  "monitor:CSP-MSK-ConsumerLag-01"]


    monitor_thresholds {
        critical = 1000
        warning = 500
    }
}

resource "datadog_monitor" "msk_active_controller_count" {
    name          = "[P2][CSP] MSK Active Controller Count - {{value}}"
    type          = "query alert"
    query         = "max(last_5m):max:aws.kafka.active_controller_count{cluster_name:sksh-argos-p-vpc-msk} > 0.34"
    message       = <<EOF
## MSK Active Controller Count 비정상 점검
- Active Controller Count 가 1 유지 해야함

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 2
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    #new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "Kafka Active Controller Count가 비정상입니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P2", "CSP", "MSK", "ActiveControllerCount", "team:skcc",  "monitor:CSP-MSK-ActiveControllerCount-01"]


    monitor_thresholds {
        critical = 0.34
    }
}