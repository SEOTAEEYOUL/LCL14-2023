# 알림 생성
resource "datadog_monitor" "s3_bucket_size" {
    name          = "[P5][System] S3 Bucket Size Bytes"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.s3.bucket_size_bytes{bucketname:*} by {bucketname} > 5544950733150"
    message = <<EOF
# [P5][System] S3 Bucket Size Bytes 
ARGOS S3 Bucket Size Bytes
{{name}} : {{value}}
Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}  @webhook-alert_collect

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                = ["P5", "SYSTEM", "S3", "Bucket", "team:skcc", "monitor:SYSTEM-S3-Bucket-Size-01"]
    notify_audit        = false
    # restricted_roles    = ["write"]
    timeout_h           = 0
    include_tags        = true
    require_full_window = false
    new_group_delay      = 60
    notify_no_data      = false
    escalation_message  = "[P5][System] S3 Bucket 사용율이 높음"
    priority            = 5
    
    # 알림 조건 설정
    monitor_thresholds  {
        critical = 5544950733150
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}
