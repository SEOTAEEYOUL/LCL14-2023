resource "datadog_monitor" "elasticache_cpu_usage" {
    name          = "[P3][CSP] ElastiCache CPU Utilization - {{name.name}} - {{value}}"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.elasticache.cpuutilization{engine:redis} by {name} > 85"
    message       = <<EOF
## ElastiCache(REDIS) CPU 사용률 85% 초과
- 발생 사유를 확인한다.
- CloudWatch에서 ElastiCache Slow Query를 확인

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
    escalation_message       = "## ElastiCache(REDIS) CPU 사용률 85% 초과했습니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P3", "CSP", "ElastiCache", "CPU", "team:skcc",  "monitor:CSP-ElastiCache-CPU-Usage-01"]


    monitor_thresholds {
        critical = 85
        warning = 70
    }
}


resource "datadog_monitor" "elasticache_memory_usage" {
    name          = "[P3][CSP] ElastiCache Memory Usage - {{name.name}} - {{value}}"
    type          = "query alert"
    query         = "max(last_5m):max:aws.elasticache.database_memory_usage_percentage{*} by {name} > 90"
    message       = <<EOF
## ElastiCache(REDIS) Memory 사용률 90% 초과
- 발생 사유를 확인한다.
- CloudWatch에서 ElastiCache Metrics를 확인

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
    escalation_message       = "## ElastiCache(REDIS) Memory 사용률 90% 초과했습니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P3", "CSP", "ElastiCache", "Memory", "team:skcc",  "monitor:CSP-ElastiCache-Memory-Usage-01"]


    monitor_thresholds {
        critical = 90
        warning = 80
    }
}
