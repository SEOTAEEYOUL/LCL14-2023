# 알림 생성
resource "datadog_monitor" "eks_daemonset_desired" {
    name          = "[P2][Container] EKS({{kube_cluster_name.name}}) - Deploy Daemonset Check {{kube_namespace.name}}/{{kube_daemon_set.name}}"
    type          = "query alert"
    query         = "avg(last_5m):avg:kubernetes_state.daemonset.desired{kube_cluster_name:*} by {kube_daemon_set,kube_namespace,kube_cluster_name} - avg:kubernetes_state.daemonset.ready{kube_cluster_name:*} by {kube_daemon_set,kube_namespace,kube_cluster_name} > 0"
    message = <<EOF
## DaemonSet 기동 상태 확인
- pod 를 식별한 후 log 를 보거나 daemonset 를 describe 해서 조치를 취함
```
kubectl -n argos get pods | grep -v Running
kubectl -n argos describe pods ...
kubectl -n argos logs -f ...
kubectl -n argos get ds
kubectl -n argos get ds ... -o yaml
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "DaemonSet", "Desired", "team:skcc", "monitor:Container-EKS-DaemonSet-Desired-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "DaemonSet 배포 상태 확인이 필요합니다"
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


resource "datadog_monitor" "eks_statefulset_desired" {
    name          = "[P2][Container] EKS Cluster({{kube_cluster_name.name}}) - Deploy Statefulset Check {{kube_namespace.name}}/{{kube_stateful_set.name}}"
    type          = "query alert"
    query         = "avg(last_5m):avg:kubernetes_state.statefulset.replicas_desired{kube_cluster_name:*} by {kube_cluster_name,kube_namespace,kube_stateful_set} - avg:kubernetes_state.statefulset.replicas_ready{kube_cluster_name:*} by {kube_cluster_name,kube_namespace,kube_stateful_set} > 0"
    message = <<EOF
## StatefulSet 기동 상태 확인
```
kubectl -n argos get pods | grep -v Running
kubectl -n argos describe pods ...
kubectl -n argos get sts
kubectl -n argos get sts ... -o yaml
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "StatefulSet", "Desired", "team:skcc", "monitor:Container-EKS-StatefulSet-Desired-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "StatefulSet 배포 상태 확인이 필요합니다"
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


resource "datadog_monitor" "eks_deploy_deployment" {
    name          = "[P2][Container] EKS({{kube_cluster_name.name}}) - Deploy Deployment Check {{kube_namespace.name}}/{{kube_replica_set.name}}"
    type          = "query alert"
    query         = "avg(last_5m):avg:kubernetes_state.replicaset.replicas_ready{kube_cluster_name:*} by {kube_replica_set,kube_namespace,kube_cluster_name} / avg:kubernetes_state.replicaset.replicas_desired{kube_cluster_name:*} by {kube_replica_set,kube_namespace,kube_cluster_name} <= 0"
    message = <<EOF
## Deployment 기동 상태 확인
```
kubectl -n argos get pods | grep ...
kubectl -n argos describe pods ...
kubectl -n argos get deploy
kubectl -n argos get deploy ... -o yaml
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["P2", "EKS", "Deployment", "Deploy", "team:skcc", "monitor:Container-EKS-Deployment-Deploy-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 60
    notify_no_data           = false
    escalation_message       = "Deployment 배포 상태 확인이 필요합니다"
    priority                 = 3
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

resource "datadog_monitor" "eks_pod_abnormal" {
    name          = "[P2][Container] EKS({{kube_cluster_name.name}}) - POD Phase Abnormal {{kube_namespace.name}}/({{pod_name.name}}.{{value}}"
    type          = "query alert"
    query         = "avg(last_5m):sum:kubernetes_state.pod.status_phase{kube_cluster_name:*,!kube_namespace:management,!pod_phase:running} by {pod_phase,kube_namespace,kube_cluster_name,pod_name} > 2"
    message       = <<EOF
## 비정상 상태 Pod 확인
```
kubectl -n argos get pods | grep -v Running
kubectl -n argos describe pods ...
kubectl -n argos logs ...
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 2
         
    # notify_audit             = false
    # timeout_h                = 0
    include_tags             = true
    # require_full_windo     w = false
    # new_group_delay          = 60
         
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"
    
    notify_no_data           = false
    escalation_message       = "EKS Pod 의 상태가 Abnormal 인 Pod 를 확인 및 조치 해 주세요"


    tags                     = ["P2", "EKS", "Pods", "Abnormal", "team:skcc",  "monitor:Container-EKS-Pods-Abnormal-01"]
    

    monitor_thresholds {
        critical = 2
    }

    renotify_interval = 60
}

resource "datadog_monitor" "eks_pod_unschedulable" {
    name          = "[P2][Container] EKS({{kube_cluster_name.name}}) - POD Unschedulable ({{namespace.name}}/{{pod_name.name}})"
    type          = "query alert"
    query         = "avg(last_1m):avg:kubernetes_state.pod.scheduled{kube_cluster_name:*} by {pod_name,kube_namespace,kube_cluster_name} >= 1"
    message       = <<EOF
## 비정상 상태(Unscheduled) Pod 확인 필요
```
kubectl -n argos get pods | grep -v Running
kubectl -n argos describe pods ...
kubectl top nodes  
kubectl describe node ...
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 2
         
    # notify_audit             = false
    # timeout_h                = 0
    include_tags             = true
    # require_full_windo       = false
    # new_group_delay          = 60
         
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"
    
    notify_no_data           = false
    escalation_message       = "EKS Pod 의 상태가 Unscheduled 인 Pod 를 확인 및 조치 해 주세요"


    tags                     = ["P2", "EKS", "Pods", "Unschduled", "team:skcc",  "monitor:Container-EKS-Pods-Unschduled-01"]
    

    monitor_thresholds {
        critical = 1
    }

    renotify_interval = 60
}

resource "datadog_monitor" "eks_pod_restart" {
    name          = "[P3][Container] EKS({{cluster_name.name}}) Pod({{kube_namespace.name}}/{{pod_name.name}}) - 재시작 발생"
    type          = "query alert"
    query         = "avg(last_1m):diff(sum:kubernetes_state.container.restarts{kube_namespace:argos} by {pod_name,kube_namespace,cluster_name}.rollup(min,60)) >= 1"
    message       = <<EOF
## 재시작 상태 Pod 확인 및 조치
- 재시작이 잦은 Pod 을 확인한다.
- describe 와 log 로 해당 문제점을 파악하여 조치해 준다.
```
kubectl -n argos get pods | grep -v Running
kubectl -n argos describe pods ...
kubectl -n argos logs -f ...
kubectl -n argos edit deploy ...
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 3
    
    # notify_audit            = false
    # timeout_h               = 0
    include_tags             = true
    # require_full_window     = false
    # new_group_delay         = 60
    
    notify_no_data           = false
    escalation_message       = "잦은 재기동 상태인 EKS Pod 의 상태를 describe 와 log 로 확인 및 조치 해 주세요"
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    tags                     = ["P3", "EKS", "Pods", "Restart", "team:skcc",  "monitor:Container-EKS-Pods-Restart-01"]


    monitor_thresholds {
        critical = 1
    }

    renotify_interval = 60
}


resource "datadog_monitor" "eks_pod_oom_killed" {
    name          = "[P2][Container]EKS({{event.tags.kube_cluster_name}} POD OOMKilled ({{event.tags.kube_namespace}}/{{event.tags.pod_name}})"
    type          = "event-v2 alert"
    query         = "events(\"tags:\"kube_cluster_name:*\" source:docker OOM\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") >= 1"
    message       = <<EOF
## Pod 가 메모리 부족으로 죽었습니다. 확인 후 조치 부탁 드립니다.
- OOM Killed 는 메모리 limit 를 올려 주시면 통상 조치가 됩니다.
- describe 와 log 로 해당 문제점을 파악하여 조치해 준다.
```
kubectl -n argos get pods 
kubectl -n argos describe pods ...
kubectl -n argos logs -f ...
kubectl -n argos edit deploy ...
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 2
    
    # notify_audit        = false
    # timeout_h           = 0
    include_tags             = true
    # require_full_window = false
    # new_group_delay     = 60
    
    notify_no_data           = false
    escalation_message       = "OOM Killed 로 죽은 EKS Pod 의 상태를 describe 와 log 로 확인 및 조치 해 주세요"


    tags                     = ["P2", "EKS", "Pods", "OOMKilled", "team:skcc",  "monitor:Container-EKS-Pods-OOMKilled-01"]
    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    monitor_thresholds {
        critical = 1
    }

    renotify_interval = 60
}


resource "datadog_monitor" "eks_pod_cpu" {
    name          = "[P5][Container] EKS({{cluster_name.name}}) Pod({{kube_deployment.name}} ) CPU 사용률 이 높음(100% 이상으로 Pod CPU 자원을 늘리는 것을 고려 필요)"
    type          = "query alert"
    query         = "avg(last_5m):(avg:kubernetes.cpu.user.total{eks_nodegroup-name:sksh-argos-p-eks-*} by {kube_deployment,name,cluster_name,eks_nodegroup-name} / avg:kubernetes.cpu.limits{eks_nodegroup-name:sksh-argos-p-eks-*} by {kube_deployment,name,cluster_name,eks_nodegroup-name}) * 100 > 100"
    message       = <<EOF
## CUP 100% 이상을 사용하는 Pod 확인 및 조치
- 업무상 사용량이 많은 것은 CPU 할당을 늘려 재 배포함
- describe 로 해당 문제점을 파악하여 조치해 준다.
```
kubectl -n argos get pods | grep ...
kubectl -n argos describe pods ...
kubectl -n argos edit deploy ...
```

Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify: @slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_info @webhook-alert_collect @webhook-alert_collect2
EOF
    priority                 = 5
         
    # notify_audit             = false
    # timeout_h                = 0
    include_tags             = true
    # require_full_window      = false
    # new_group_delay          = 60
    
    notify_no_data           = false
    escalation_message       = "잦은 재기동 상태인 EKS Pod 의 상태를 describe 와 log 로 확인 및 조치 해 주세요"


    tags                     = ["P5", "EKS", "Pods", "CPU", "100", "team:skcc",  "monitor:Container-EKS-Pods-CPU-100-01"]


    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    monitor_thresholds {
        critical = 100
    }

    renotify_interval = 60
}