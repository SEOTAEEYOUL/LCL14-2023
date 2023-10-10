# 알림 생성
resource "datadog_monitor" "eks_node_not_ready" {
    name          = "[P2][Container] EKS({{kube_cluster_name.name}}) - Work Node({{event.host.name}})가 준비되지 않았습니다"
    type          = "event-v2 alert"
    # query         = "events(\"kube_cluster_name:sksh-argos-p-eks-*\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") > 0" 
    # events("kube_cluster_name:sksh-argos-p-eks-* source:kubernetes status is \"now:\" NodeNotReady").rollup("count").by("kube_cluster_name").last("1m") > 0
    # events("kube_cluster_name:sksh-argos-p-eks-* source:kubernetes status is \"now:\" NodeNotReady").rollup("count").by("kube_cluster_name").last("1m") > 0
    query         = "events(\"kube_cluster_name:sksh-argos-p-eks-* source:kubernetes status is \\\"now:\\\" NodeNotReady\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") > 0"
    # query         = 'events(\"kube_cluster_name:sksh-argos-p-eks-*\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") > 0" 
    message = <<EOF
## EKS({{kube_cluster_name.name}}) - Work Node({{event.host.name}})가 준비되지 않았습니다
- NotReday 상태의 Node 을 확인한다.
- Node 를 Describe 로 문제 원인을 확인하여, 필요시 조치 바랍니다.
```
kubectl get nodes 
kubectl describe nodes ...
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "Node", "NOT_READY", "team:skcc", "monitor:Container-EKS-Node-Not_Ready-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS NODE 가 준비되지 않은 원인 확인 필요"
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 0.0
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

# ...
resource "datadog_monitor" "eks_node_memory_usage" {
    name          = "[P5][Container] EKS({{cluster_name.name}}) - Node({{name.name}}) 최근 메모리 사용률이 높음"
    type          = "query alert"
    query         = "avg(last_1m):1 - avg:system.mem.pct_usable{cluster_name:sksh-argos-p-eks-*} by {cluster_name,eksnode,name,host} > 0.9"
    # query         = "avg(last_5m):avg:kubernetes_state.node.memory_allocatable{eks_nodegroup-name:sksh-argos-p-eks-*} by {cluster_name,node} / avg:kubernetes_state.node.memory_capacity{eks_nodegroup-name:sksh-argos-p-eks-*} by {cluster_name,node} * 100 > 95"
    # query         = "avg(last_5m):avg:kubernetes.memory.usage_pct{kube_namespace:argos} by {eks_nodegroup-name,name} * 100 > 95"
    message = <<EOF
# EKS({{cluster_name.name}}) Check nodeNode({{host.name}}) memory usage
- cluster_name : {{cluster_name.name}} 
- eksnode: {{eksnode.name}} 
- name: {{name.name}} 
- host : {{host.name}} 
- value : {{value}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info @webhook-sendSKCCTeams @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P5", "EKS", "Node", "Memory", "team:skcc", "monitor:Container-EKS-Node-Memory-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "최근 5분동안에 EKS({{cluster_name.name}}) - Node({{name.name}}) 의 메모리 사용이 90% 이상이므로 확인이 필요합니다"
    priority                 = 5

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 0.9
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "eks_node_disk_usage" {
    name          = "[P2][Container] EKS({{cluster_name.name}}) - Node {{host.name_tag}} disk 사용이 90% 이상"
    type          = "query alert"
    query         = "max(last_5m):avg:system.disk.in_use{cluster_name:sksh-argos-p-eks-*} by {name,host,device,cluster_name} > 0.9"
    message = <<EOF
# EKS({{cluster_name.name}}) - Node {{host.name_tag}} disk 사용이 90% 이상이므로 확인이 필요합니다

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "Node", "Disk", "team:skcc", "monitor:Container-EKS-Node-Disk-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "Node 의 Disk 사용이 90% 이상이므로 확인이 필요합니다"
    priority                 = 2

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 0.9
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

# resource "datadog_monitor" "eks_node_memory_usage" {
#     name          = "[P2][Container] EKS({{cluster_name.name}}) - Node {{host.name_tag}} memory usage over 90%"
#     type          = "query alert"
#     query         = "avg(last_1m):1 - avg:system.mem.pct_usable{cluster_name:sksh-argos-p-eks-*} by {host,name,cluster_name} > 0.9"
#     message = <<EOF
#     @slack-SKCC_Digital_Service-ict_shieldus_argos @webhook-alert_collect @webhook-alert_collect2
# EOF
#     tags                = ["P2", "EKS", "Node", "Memory", "team:skcc", "monitor:Container-EKS-Node-Memory-01"]
#     notify_audit        = false
#     # restricted_roles    = ["write"]
#     timeout_h           = 0
#     include_tags        = true
#     require_full_window = false
#     new_group_delay      = 60
#     notify_no_data      = false
#     escalation_message  = "Node 의 Memory 사용이 90% 이상이므로 확인이 필요합니다"
#     priority            = 2

#     notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


#     # 알림 조건 설정
#     monitor_thresholds  {
#         critical = 0.9
#     }

#     # monitor_threshold_windows {
#     #     trigger_window  = "last_30m"
#     #     recovery_window = "last_30m"
#     # }

#     renotify_interval = 60
# }


resource "datadog_monitor" "eks_node_scale-in" {
    name          = "[P5][Container] EKS({{kube_cluster_name.name}}) - Node Scale-In - {{message.name}}"
    type          = "event-v2 alert"
    # query         = "events(\"kube_cluster_name:sksh-argos-p-eks-*\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") > 0" 
    # events("kube_cluster_name:sksh-argos-p-eks-* source:kubernetes status is \"now:\" NodeNotReady").rollup("count").by("kube_cluster_name").last("1m") > 0
    # events("kube_cluster_name:sksh-argos-p-eks-* source:kubernetes status is \"now:\" NodeNotReady").rollup("count").by("kube_cluster_name").last("1m") > 0
    query         = "events(\"cluster_name:sksh-argos-p-eks-* source:kubernetes message:ScaleDownEmpty\").rollup(\"count\").by(\"message\").last(\"1m\") > 0"
    message = <<EOF
# EKS({{kube_cluster_name.name}}) - Node Scale-In - {{message.name}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_info @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P5", "EKS", "Node", "Scale-In", "team:skcc", "monitor:Container-EKS-Node-Scale-In-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS NODE 가 Scale-In 됨"
    priority                 = 5

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 0.0
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

resource "datadog_monitor" "eks_node_scale-out" {
    name          = "[P5][Container] EKS({{kube_cluster_name.name}}) - Node Scale-Out {{message.name}}"
    type          = "event-v2 alert"
    # query         = "events(\"kube_cluster_name:sksh-argos-p-eks-*\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") > 0" 
    # events("kube_cluster_name:sksh-argos-p-eks-* source:kubernetes status is \"now:\" NodeNotReady").rollup("count").by("kube_cluster_name").last("1m") > 0
    # events("kube_cluster_name:sksh-argos-p-eks-* source:kubernetes status is \"now:\" NodeNotReady").rollup("count").by("kube_cluster_name").last("1m") > 0
    query         = "events(\"cluster_name:sksh-argos-p-eks-* source:kubernetes message:ScaledupGroup\").rollup(\"count\").by(\"message\").last(\"1m\") > 0"
    message = <<EOF
# EKS({{kube_cluster_name.name}}) - Node Scale-Out {{message.name}}

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-SKCC_Digital_Service-ict_shieldus_argos_info @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P5", "EKS", "Node", "Scale-Out", "team:skcc", "monitor:Container-EKS-Node-Scale-Out-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "EKS NODE 가 Scale-Out 됨"
    priority                 = 5

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 0.0
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}


resource "datadog_monitor" "degraded_hardware_event" {
    name                     = "[P2][Container] EKS({{kube_cluster_name.name}}) - 노드 인스턴스가 성능이 저하된 하드웨어에서 실행 중입니다."
    type                     = "event-v2 alert"
    query                    = "events(\"The instance is running on degraded hardware\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") >= 1"
    message       = <<EOF
# EKS({{kube_cluster_name.name}}) - 노드 인스턴스가 성능이 저하된 하드웨어에서 실행 중
- EKS 클러스터 "{{kube_cluster_name.name}}"에 있는 하나 이상의 노드가 성능이 저하된 하드웨어에서 실행 중입니다. 노드 상태를 확인하고 문제를 해결합니다. 

Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 2


    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"

    # notify_audit             = false
    # timeout_h                = 0
    include_tags             = true
    # require_full_window      = false
    # new_group_delay          = 60
    
    notify_no_data           = false
    escalation_message       = "EKS NODE가 성능이 저하된 하드웨어에서 실행 중"


    tags                     = ["P2", "EKS", "Node", "degraded", "team:skcc", "team:skcc", "monitor:Container-EKS-Node-degraded-01"]


    monitor_thresholds {
        critical = 1
    }

    renotify_interval = 60
}












