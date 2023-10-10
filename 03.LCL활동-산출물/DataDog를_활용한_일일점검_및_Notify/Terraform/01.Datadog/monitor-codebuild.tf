resource "datadog_monitor" "codebuild_build_failed" {
    name          = "[P5][CSP] CodeBuild 빌드실패 - {{projectname.name}}"
    type          = "query alert"
    query         = "sum(last_5m):sum:aws.codebuild.failed_builds{projectname:prd_pipeline_*} by {projectname}.as_count() >= 1"
    message       = <<EOF
## Codebuild Build Failed 발생
- Build Log를 통해 발생 사유를 확인한다.

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
    escalation_message       = "CodeBuild 수행 시 Build실패가 발생했습니다."
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P5", "CSP", "CodeBuild", "BuildFailed", "team:skcc",  "monitor:CSP-CodeBuild-BuildFailed-01"]


    monitor_thresholds {
        critical = 1
    }
}