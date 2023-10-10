# 알림 생성
resource "datadog_monitor" "eks_job_fail" {
    name          = "[P2][Container] EKS({{kube_cluster_name.name}} ) - Job Failed ({{job_name.name}})"
    type          = "query alert"
    query         = "avg(last_5m):avg:kubernetes_state.job.failed{kube_cluster_name:*} by {kube_job,kube_namespace,kube_cluster_name} > 1"
    message = <<EOF
## "EKS({{kube_cluster_name.name}} ) Job({{job_name.name}}) 이 실패, 확인 필요합니다"

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "JOB", "Fail", "team:skcc", "monitor:Container-EKS-JOB-Fail-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS Job 이 실패, 확인 필요합니다"
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "eks_alb_2xx" {
    name          = "[P2][Container] EKS ALB({{name.name}}) 2XX 응답 코드가 30분 내에 0 건 발생, 확인 필요"
    type          = "query alert"
    query         = "sum(last_30m):sum:aws.applicationelb.httpcode_target_2xx{elbv2.k8s.aws/cluster:*,ingress.k8s.aws/resource:loadbalancer,loadbalancer:*,!loadbalancer:app/sksh-argos-p-eks-mcaps-alb-pub/730c080d2603b283,!loadbalancer:app/sksh-argos-p-eks-cna-alb-pri/75b3cb3b9edb9fe1} by {loadbalancer,name}.as_count() <= 0"
    message = <<EOF
## EKS ALB({{name.name}}) 의 2XX 응답 코드가 30분 내에 0 건 발생, 확인 필요

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "ALB", "2XX", "team:skcc", "monitor:Container-EKS-ALB-2XX-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "Ingress Controller(ALB)의 응답코드 2XX 가 3분동안 0개, 확인 필요합니다"
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 0
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "eks_alb_4xx" {
    name          = "[P3][Container] EKS ALB ({{loadbalancer.name}} ) 응답코드 4XX 가 분당 300개 이상이며 확인 필요합니다"
    type          = "query alert"
    query         = "sum(last_1m):sum:aws.applicationelb.httpcode_target_4xx{loadbalancer:app/sksh-argos-p-eks-*} by {name,loadbalancer}.as_count() > 300"
    message = <<EOF
## EKS ALB ({{loadbalancer.name}} ) 응답코드 4XX 가 분당 300개 이상이며 확인 필요합니다

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P3", "EKS", "ALB", "4XX", "team:skcc", "monitor:Container-EKS-ALB-4XX-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "Ingress Controller(ALB)의 응답코드 4XX 가 분당 300개 이상이며 확인 필요합니다"
    priority                 = 3


    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"

    # 알림 조건 설정
    monitor_thresholds  {
        critical = 300
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "eks_alb_5xx" {
    name                = "[P2][Container] EKS ALB ({{loadbalancer.name}}) 응답코드 5XX 가 분당 50개 이상"
    type                = "query alert"
    query               = "sum(last_1m):sum:aws.applicationelb.httpcode_target_5xx{loadbalancer:app/sksh-argos-p-eks-*} by {name,loadbalancer}.as_count() > 50"
    message = <<EOF
## EKS ALB ({{loadbalancer.name}}) 응답코드 5XX 가 분당 50개 이상 확인 필요합니다

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "ALB", "5XX", "team:skcc", "monitor:Container-EKS-ALB-5XX-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "Ingress Controller(ALB)의 응답코드 5XX 가 분당 50개 이상, 확인 필요합니다"
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 50
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "eks_network_tx_error" {
    name                = "[P2][Container] EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network TX 오류"
    type                = "query alert"
    query               = "avg(last_5m):avg:kubernetes.network.tx_errors{cluster_name:sksh-argos-p-*} by {eks_nodegroup-name,cluster_name} >= 1"
    message = <<EOF
## EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network TX 오류, 확인 필요합니다

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "Network", "TX", "Error", "team:skcc", "monitor:Container-EKS-TX-Error-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network TX 오류, 확인 필요합니다"
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "eks_network_tx_drop" {
    name                = "[P2][Container] EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}} ) Network TX Drop"
    type                = "query alert"
    query               = "avg(last_5m):avg:kubernetes.network.tx_dropped{cluster_name:sksh-argos-p-*} by {eks_nodegroup-name,name,cluster_name} >= 1"
    message = <<EOF
## EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network TX Drop 발생, 확인 필요합니다

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "Network", "TX", "Drop", "team:skcc", "monitor:Container-EKS-TX-Drop-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network TX Drop 발생, 확인 필요합니다"     
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "eks_network_rx_error" {
    name                = "[P2][Container] EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network RX 오류"
    type                = "query alert"
    query               = "avg(last_5m):sum:kubernetes.network.rx_dropped{cluster_name:*} by {eks_nodegroup-name,name,cluster_name} > 10"
    message = <<EOF
## EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network RX 오류, 확인 필요합니다

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "Network", "RX", "Error", "team:skcc", "monitor:Container-EKS-RX-Error-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network RX 오류, 확인 필요합니다"
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 10
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "eks_network_rx_drop" {
    name                = "[P2][Container] EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}} ) Network RX Drop"
    type                = "query alert"
    query               = "avg(last_5m):avg:kubernetes.network.rx_dropped{cluster_name:sksh-argos-p-*} by {name,eks_nodegroup-name,cluster_name} > 10"
    message = <<EOF
## EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network RX Drop 발생, 확인 필요합니다

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "Network", "RX", "Drop", "team:skcc", "monitor:Container-EKS-RX-Drop-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network RX Drop 발생, 확인 필요합니다"     
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 10
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "eks_network_alb_abnormal_target_group" {
    name                = "[P3][Container] EKS ALB({{name.name}}) - 비정상적인 Target Group({{targetgroup.name}})"
    type                = "query alert"
    query               = "avg(last_5m):sum:aws.applicationelb.un_healthy_host_count{elbv2.k8s.aws/cluster:*,ingress.k8s.aws/resource:loadbalancer,loadbalancer:app/sksh-argos-p-eks-*} by {targetgroup,name} >= 1"
    message = <<EOF
## EKS({{name.name}} - ALB({{name.name}}) - 비정상적인 Target Group({{targetgroup.name}})이 존재함, 확인 필요합니다

{{#is_alert}}
### ALERT: 비정상 ELB 감지됨!

#### 비정상 ELB 목록: 
- 이름: {{name.name}}
- 타겟 그룹: {{targetgroup.name}}

{{/is_alert}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P3", "EKS", "ALB", "TargetGroup", "Unhealthy", "team:skcc", "monitor:Container-EKS-ALB-TargetGroup-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS({{name.name}} - ALB({{name.name}}) - 비정상적인 Target Group({{targetgroup.name}})이 존재함, 확인 필요합니다"     
    priority                 = 3

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 1
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 1440
}