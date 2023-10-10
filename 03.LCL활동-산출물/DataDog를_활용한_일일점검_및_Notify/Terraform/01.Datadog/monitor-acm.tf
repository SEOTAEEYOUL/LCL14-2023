resource "datadog_monitor" "acm_expiry" {
    name          = "[P4][CSP] ACM Expiry - {{name.name}} - {{value}}"
    type          = "query alert"
    query         = "min(last_1d):min:aws.certificatemanager.days_to_expiry{*} by {name} < 30"
    message       = <<EOF
## ACM 만료 경고 발생
- ACM 메뉴를 통해 남은 기간을 확인 후 연장신청한다.

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람
EOF
    priority                 = 4
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    new_group_delay         = 60
    renotify_interval = 0    


    notify_no_data           = false
    escalation_message       = "ACM이 만료까지 30일 남았습니다. "
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P5", "CSP", "ACM", "Expiry", "team:skcc",  "monitor:CSP-ACM-Expiry-01"]


    monitor_thresholds {
        critical = 30
        warning = 45
    }
}