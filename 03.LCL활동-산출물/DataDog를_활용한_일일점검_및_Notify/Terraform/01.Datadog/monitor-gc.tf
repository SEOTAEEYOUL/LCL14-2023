# 알림 생성
resource "datadog_monitor" "jvm_fullgc" {
    name          = "[P2][Container] EKS {{cluster_name.name}}  Service({{service.name}}) Full GC 과다발생"
    type          = "query alert"
    query         = "avg(last_3m):avg:jvm.gc.major_collection_count{service:*} by {service,cluster_name} > 0.5"
    message = <<EOF
## EKS({{service.name}}) Full GC 과다발생  
- describe 로 해당 문제점을 파악하여 조치해 준다.
- 업무상 사용량이 많은 것은 Memory 할당을 늘려 재 배포함
```
kubectl -n argos get pods | grep ...
kubectl -n argos describe pods ...
kubectl -n argos logs -f ...
kubectl -n argos edit deploy ...
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "Service", "FullGC", "team:skcc", "monitor:Service-EKS-FullGC-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "Memory Leak 혹은 증설을 포함한 Full GC 과다발생 원인 파악 및 조치가 필요합니다."
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"

    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 0.5
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}