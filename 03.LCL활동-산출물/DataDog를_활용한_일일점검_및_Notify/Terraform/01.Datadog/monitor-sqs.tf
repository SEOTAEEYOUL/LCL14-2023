resource "datadog_monitor" "sqs_dlq_occur" {
    name          = "[P5][CSP] SQS Dead Letter Queue Occurred - {{queuename.name}} - {{value}}"
    type          = "query alert"
    query         = "max(last_5m):max:aws.sqs.approximate_number_of_messages_visible{queuename:dlq-*} by {queuename} >= 100"
    message       = <<EOF
## SQS Dead Letter Queue 데이터 발생
- 발생 사유를 확인한다.

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람
EOF
    priority                 = 5
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "SQS DLQ에 데이터가 적재되었습니다. 확인 및 조치 해주세요"
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P5", "CSP", "SQS", "DLQ", "team:skcc",  "monitor:CSP-SQS-DLQ-Occured-01"]


    monitor_thresholds {
        critical = 100
        warning = 1
    }
}

resource "datadog_monitor" "sqs_queue_congestion" {
    name          = "[P2][CSP] SQS Queue Congestion - {{queuename.name}} - {{value}}"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.sqs.approximate_number_of_messages_visible{queuename:sdq-*} by {queuename} > 3000"
    message       = <<EOF
## SQS Queue 적체 발생
- 발생 사유를 확인한다.

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
    escalation_message       = "SQS Queue에 데이터가 적체되고 있습니다. 확인 및 조치 해주세요"
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P2", "CSP", "SQS", "QUEUE", "team:skcc",  "monitor:CSP-SQS-QUEUE-Congestion-01"]

    monitor_thresholds {
        critical = 3000
        warning = 1000
    }
}