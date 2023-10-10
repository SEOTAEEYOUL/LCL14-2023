resource "datadog_monitor" "lambda_error" {
    name          = "[P5][CSP] Lambda Errors - {{functionname.name}} {{value}}"
    type          = "query alert"
    query         = "sum(last_1h):sum:aws.lambda.errors{aws_account:123456789012} by {functionname}.as_count() >= 1"
    message       = <<EOF
## Lambda Error 발생
- 발생 사유를 확인한다.

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @jellyfishlove@sk.com @slack-SKCC_Digital_Service-ict_shieldus_argos @teams-ARGOS-ITOSS @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 5
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "Lambda Function 수행 시 Error가 발생했습니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P5", "CSP", "Lambda", "ERROR", "team:skcc",  "monitor:CSP-Lambda-Error-01"]


    monitor_thresholds {
        critical = 1
    }
}