resource "datadog_monitor" "log_smsagent_dbconnection" {
    name          = "[P3][CSP] SMS AGENT DB Connection ERROR"
    type          = "log alert"
    query         = "logs(\"service:SMS-agent status:error JDBC\").index(\"*\").rollup(\"count\").by(\"service\").last(\"5m\") > 1"
    message       = <<EOF
## SMS Agent DB Connection Error 발생
- 정상적으로 재접속되는지 확인 필요함
- 간혹 재접속되지 않는 경우가 있으며, Agent Restart가 필요함

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람
EOF
    priority                 = 3
    
    enable_logs_sample = true
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true    
    require_full_window = false
    new_group_delay         = 60
    renotify_interval = 10    
    renotify_statuses = ["alert"]
    
    notify_by = [ "*" ]
    on_missing_data = "default"
    
    escalation_message       = "SMS Agent에 DB Connection Error가 발생했습니다. 확인해주세요"
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P3", "CSP", "LOG", "SMS", "team:skcc",  "monitor:CSP-LOG-SMS-DBConnectionError-01"]


    monitor_thresholds {
        critical = 1
    }
}