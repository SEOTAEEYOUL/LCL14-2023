alert_list      = [
    {
        "no": 1,
        "monitor_id": 125194486,
        "name": "[P2][Container] EKS({{cluster_name.name}}) - Node {{host.name_tag}} disk 사용이 90% 이상",
        "dynamodb_key": "Container-EKS-Node-Disk-01",
        "query": "max(last_5m):avg:system.disk.in_use{cluster_name:sksh-argos-p-eks-*} by {name,host,device,cluster_name} > 0.9"
    },
    {
        "no": 2,
        "monitor_id": 125194491,
        "name": "[P2][Container] EKS({{kube_cluster_name.name}}) - 노드 인스턴스가 성능이 저하된 하드웨어에서 실행 중입니다.",
        "dynamodb_key": "Container-EKS-Node-degraded-01",
        "query": "events(\"The instance is running on degraded hardware\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") >= 1"
    },
    {
        "no": 3,
        "monitor_id": 125194492,
        "name": "[P2][Container] EKS({{kube_cluster_name.name}}) - Work Node({{event.host.name}})가 준비되지 않았습니다",
        "dynamodb_key": "Container-EKS-Node-Not_Ready-01",
        "query": "events(\"kube_cluster_name:sksh-argos-p-eks-* source:kubernetes status is \\\"now:\\\" NodeNotReady\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") > 0"
    },
    {
        "no": 4,
        "monitor_id": 125194493,
        "name": "[P1][SYSTEM] {{name.name}} - EC2 인스턴스 상태 실패",
        "dynamodb_key": "SYSTEM-EC2-Instance-Fail-01",
        "query": "avg(last_5m):avg:aws.ec2.status_check_failed_instance{!name:sksh-argos-p-eks*} by {name} > 0"
    },
    {
        "no": 5,
        "monitor_id": 125194495,
        "name": "[P2][Container] EKS {{cluster_name.name}}  Service({{service.name}}) Full GC 과다발생",
        "dynamodb_key": "Service-EKS-FullGC-01",
        "query": "avg(last_3m):avg:jvm.gc.major_collection_count{service:*} by {service,cluster_name} > 0.5"
    },
    {
        "no": 6,
        "monitor_id": 125790395,
        "name": "[P2][Container] EKS({{kube_cluster_name.name}} ) - Job Failed ({{job_name.name}})",
        "dynamodb_key": "Container-EKS-JOB-Fail-01",
        "query": "avg(last_5m):avg:kubernetes_state.job.failed{kube_cluster_name:*} by {kube_job,kube_namespace,kube_cluster_name} > 1"
    },
    {
        "no": 7,
        "monitor_id": 125793793,
        "name": "[P1][DB] 최근 5분 동안 MySQL {{dbinstanceidentifier.name}} MAX CPU 사용율이 90% 입니다",
        "dynamodb_key": "DB-MySQL-MAX_CPU_90-01",
        "query": "avg(last_5m):max:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-aurora-mysql-*} by {name} >= 90"
    },
    {
        "no": 8,
        "monitor_id": 125796552,
        "name": "[P1][DB] Aurora MySQL ({{dbinstanceidentifier.name}} Temporary storage > 90%",
        "dynamodb_key": "DB-MySQL-TempSpace_90-01",
        "query": "min(last_10m):avg:aws.rds.free_local_storage{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {dbinstanceidentifier} / 1024 / 1024 / 1024 < 3"
    },
    {
        "no": 9,
        "monitor_id": 125797703,
        "name": "[P1][DB] 최근 5분 동안 MariaDB({{name.name}}) CPU 사용율이 90% 이상 입니다.",
        "dynamodb_key": "DB-MariaDB-CPU_90-01",
        "query": "avg(last_5m):avg:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-rds-mariadb-*} by {name} > 90"
    },
    {
        "no": 10,
        "monitor_id": 125840804,
        "name": "[P1][Network] DX Connection Down ({{connectionid.name}})",
        "dynamodb_key": "Network-DX-Down-01",
        "query": "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1"
    },
    {
        "no": 11,
        "monitor_id": 125843135,
        "name": "[P2][SYSTEM] 최근 5분동안 EC2[{{host.name}}] 의 CPU 사용률이 {{threshold}}% 이상 입니다",
        "dynamodb_key": "SYSTEM-EC2-CPU-High-01",
        "query": "avg(last_5m):100 - avg:system.cpu.idle{host:sksh*} by {host} >= 90"
    },
    {
        "no": 12,
        "monitor_id": 125851731,
        "name": "[P2][Container] EKS({{kube_cluster_name.name}}) - Deploy Daemonset Check {{kube_namespace.name}}/{{kube_daemon_set.name}}",
        "dynamodb_key": "Container-EKS-DaemonSet-Desired-01",
        "query": "avg(last_5m):avg:kubernetes_state.daemonset.desired{kube_cluster_name:*} by {kube_daemon_set,kube_namespace,kube_cluster_name} - avg:kubernetes_state.daemonset.ready{kube_cluster_name:*} by {kube_daemon_set,kube_namespace,kube_cluster_name} > 0"
    },
    {
        "no": 13,
        "monitor_id": 125852634,
        "name": "[P1][System] Host {{name.name}} - FS inode 사용량이 높습니다",
        "dynamodb_key": "SYSTEM-EC2-FS-inode-01",
        "query": "avg(last_5m):avg:system.fs.inodes.in_use{name:sksh-argos-p*,device:/*} by {name,device} * 100 >= 90"
    },
    {
        "no": 14,
        "monitor_id": 125853923,
        "name": "[P2][Container] EKS({{kube_cluster_name.name}}) - POD Phase Abnormal {{kube_namespace.name}}/({{pod_name.name}}.{{value}}",
        "dynamodb_key": "Container-EKS-Pods-Abnormal-01",
        "query": "avg(last_5m):sum:kubernetes_state.pod.status_phase{kube_cluster_name:*,!kube_namespace:management,!pod_phase:running} by {pod_phase,kube_namespace,kube_cluster_name,pod_name} > 2"
    },
    {
        "no": 15,
        "monitor_id": 125855351,
        "name": "[P2][Container] EKS ALB ({{loadbalancer.name}}) 응답코드 5XX 가 분당 50개 이상",
        "dynamodb_key": "Container-EKS-ALB-5XX-01",
        "query": "sum(last_1m):sum:aws.applicationelb.httpcode_target_5xx{loadbalancer:app/sksh-argos-p-eks-*} by {name,loadbalancer}.as_count() > 50"
    },
    {
        "no": 16,
        "monitor_id": 125863486,
        "name": "[P2][Container] EKS Cluster({{kube_cluster_name.name}}) - Deploy Statefulset Check {{kube_namespace.name}}/{{kube_stateful_set.name}}",
        "dynamodb_key": "Container-EKS-StatefulSet-Desired-01",
        "query": "avg(last_5m):avg:kubernetes_state.statefulset.replicas_desired{kube_cluster_name:*} by {kube_cluster_name,kube_namespace,kube_stateful_set} - avg:kubernetes_state.statefulset.replicas_ready{kube_cluster_name:*} by {kube_cluster_name,kube_namespace,kube_stateful_set} > 0"
    },
    {
        "no": 17,
        "monitor_id": 125904868,
        "name": "[P2][Container]EKS({{event.tags.kube_cluster_name}} POD OOMKilled ({{event.tags.kube_namespace}}/{{event.tags.pod_name}})",
        "dynamodb_key": "Container-EKS-Pods-OOMKilled-01",
        "query": "events(\"tags:\"kube_cluster_name:*\" source:docker OOM\").rollup(\"count\").by(\"kube_cluster_name\").last(\"1m\") >= 1"
    },
    {
        "no": 18,
        "monitor_id": 126011514,
        "name": "[P2][DB] MySQL {{hostname.name}} 사용 가능한 메모리가 너무 적습니다.(10% 미만)",
        "dynamodb_key": "DB-UsableMemory-TooLow-01",
        "query": "min(last_10m):avg:aws.rds.freeable_memory{dbinstanceidentifier:sksh-argos-p-aurora-mysql-*} by {hostname} < 10737418240"
    },
    {
        "no": 19,
        "monitor_id": 126239710,
        "name": "[P2][Container] EKS ALB({{name.name}}) 2XX 응답 코드가 30분 내에 0 건 발생, 확인 필요",
        "dynamodb_key": "Container-EKS-ALB-2XX-01",
        "query": "sum(last_30m):sum:aws.applicationelb.httpcode_target_2xx{elbv2.k8s.aws/cluster:*,ingress.k8s.aws/resource:loadbalancer,loadbalancer:*,!loadbalancer:app/sksh-argos-p-eks-mcaps-alb-pub/730c080d2603b283,!loadbalancer:app/sksh-argos-p-eks-cna-alb-pri/75b3cb3b9edb9fe1} by {loadbalancer,name}.as_count() <= 0"
    },
    {
        "no": 20,
        "monitor_id": 126242214,
        "name": "[P2][DB] MariaDB02(CAD) {{hostname.name}} 사용 가능한 메모리({{value}})가 최근 5분동안 10% 미만 입니다.",
        "dynamodb_key": "DB-MariaDB02-FreeableMemory-01",
        "query": "avg(last_5m):avg:aws.rds.freeable_memory{dbinstanceidentifier:*,dbinstanceclass:db.t3.medium,engine:mariadb,dbinstanceidentifier:sksh-argos-p-rds-mariadb-02} by {name} < 805306368"
    },
    {
        "no": 21,
        "monitor_id": 126242215,
        "name": "[P2][DB] MariaDB01(IGP) {{hostname.name}} 사용 가능한 메모리({{value}})가 최근 5분동안 10% 미만 입니다.",
        "dynamodb_key": "DB-MariaDB01-FreeableMemory-01",
        "query": "avg(last_5m):avg:aws.rds.freeable_memory{dbinstanceidentifier:*,dbinstanceclass:db.t3.medium,engine:mariadb,dbinstanceidentifier:sksh-argos-p-rds-mariadb-01} by {name} < 214748364"
    },
    {
        "no": 22,
        "monitor_id": 126286121,
        "name": "[P2][Container] EKS({{kube_cluster_name.name}}) - POD Unschedulable ({{namespace.name}}/{{pod_name.name}})",
        "dynamodb_key": "Container-EKS-Pods-Unschduled-01",
        "query": "avg(last_1m):avg:kubernetes_state.pod.scheduled{kube_cluster_name:*} by {pod_name,kube_namespace,kube_cluster_name} >= 1"
    },
    {
        "no": 23,
        "monitor_id": 126335039,
        "name": "[P2][Container] EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network TX 오류",
        "dynamodb_key": "Container-EKS-TX-Error-01",
        "query": "avg(last_5m):avg:kubernetes.network.tx_errors{cluster_name:sksh-argos-p-*} by {eks_nodegroup-name,cluster_name} >= 1"
    },
    {
        "no": 24,
        "monitor_id": 126335040,
        "name": "[P2][Container] EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}} ) Network TX Drop",
        "dynamodb_key": "Container-EKS-TX-Drop-01",
        "query": "avg(last_5m):avg:kubernetes.network.tx_dropped{cluster_name:sksh-argos-p-*} by {eks_nodegroup-name,name,cluster_name} >= 1"
    },
    {
        "no": 25,
        "monitor_id": 126339370,
        "name": "[P2][Container] EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}} ) Network RX Drop",
        "dynamodb_key": "Container-EKS-RX-Drop-01",
        "query": "avg(last_5m):avg:kubernetes.network.rx_dropped{cluster_name:sksh-argos-p-*} by {name,eks_nodegroup-name,cluster_name} > 10"
    },
    {
        "no": 26,
        "monitor_id": 126339371,
        "name": "[P2][Container] EKS({{cluster_name.name}} - {{eks_nodegroup-name.name}}.{{name.name}}) Network RX 오류",
        "dynamodb_key": "Container-EKS-RX-Error-01",
        "query": "avg(last_5m):sum:kubernetes.network.rx_dropped{cluster_name:*} by {eks_nodegroup-name,name,cluster_name} > 10"
    },
    {
        "no": 27,
        "monitor_id": 126352965,
        "name": "[P2][DB] 최근 5분 동안 MariaDB {{dbinstanceidentifier.name}} 최대 접속이 200 이상(Max:450)",
        "dynamodb_key": "DB-MariaDB-MaxConnecton-01",
        "query": "avg(last_5m):avg:aws.rds.database_connections{dbinstanceidentifier:sksh-argos-p-rds-mariadb*} by {name} > 200"
    },
    {
        "no": 28,
        "monitor_id": 127492672,
        "name": "[P2][CSP] SQS Queue Congestion - {{queuename.name}} - {{value}}",
        "dynamodb_key": "CSP-SQS-QUEUE-Congestion-01",
        "query": "avg(last_5m):avg:aws.sqs.approximate_number_of_messages_visible{queuename:sdq-*} by {queuename} > 3000"
    },
    {
        "no": 29,
        "monitor_id": 127496531,
        "name": "[P2][CSP] MSK Active Controller Count - {{value}}",
        "dynamodb_key": "CSP-MSK-ActiveControllerCount-01",
        "query": "max(last_5m):max:aws.kafka.active_controller_count{cluster_name:sksh-argos-p-vpc-msk} > 0.34"
    },
    {
        "no": 30,
        "monitor_id": 127496535,
        "name": "[P2][CSP] MSK Consumer Lag - {{groupid.name}} - {{value}}",
        "dynamodb_key": "CSP-MSK-ConsumerLag-01",
        "query": "avg(last_5m):avg:aws.msk.kafka.consumer.group.ConsumerLagMetrics.Value{cluster_arn:arn:aws:kafka:ap-northeast-2:123456789012:cluster/sksh-argos-p-vpc-msk/180e0a3b-1d0d-4994-8272-8c80bc96cc27-3} by {groupid} > 1000"
    },
    {
        "no": 31,
        "monitor_id": 127496536,
        "name": "[P2][CSP] MSK 디스크 사용률이 85% 이상 ({{value}})",
        "dynamodb_key": "CSP-MSK-DiskUsage-01",
        "query": "avg(last_5m):avg:aws.kafka.kafka_data_logs_disk_used{*} > 85"
    },
    {
        "no": 32,
        "monitor_id": 127530050,
        "name": "[P1][DB] MySQL {{dbinstanceidentifier.name}} CPU 사용율이 너무 높음",
        "dynamodb_key": "DB-MySQL-CPU-TooHigh-01",
        "query": "avg(last_5m):max:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {name} >= 80"
    },
    {
        "no": 33,
        "monitor_id": 127532869,
        "name": "[P2][DB] MySQL {{dbinstanceidentifier.name}} Local Temporary storage  사용율이 너무 높음",
        "dynamodb_key": "DB-MySQL-Temporary-TooLow-01",
        "query": "min(last_10m):avg:aws.rds.free_local_storage{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {dbinstanceidentifier} < 1073741824"
    },
    {
        "no": 34,
        "monitor_id": 127563959,
        "name": "[P2][DB] MySQL {{dbinstanceidentifier.name}} Aurora engine uptime alarm",
        "dynamodb_key": "DB-MySQL-Engine-UptimeAlarm-01",
        "query": "min(last_15m):avg:aws.rds.engine_uptime{hostname:sksh-argos-p-aurora-mysql*} by {hostname} <= 90"
    },
    {
        "no": 35,
        "monitor_id": 127565605,
        "name": "[P2][DB] MySQL DML latency over 1800 seconds",
        "dynamodb_key": "DB-MySQL-DML-Latency-01",
        "query": "max(last_10m):avg:aws.rds.dmllatency{dbclusteridentifier:sksh-argos-p-aurora-mysql*} by {name} > 1800000"
    },
    {
        "no": 36,
        "monitor_id": 127581937,
        "name": "[P2][DB] MySQL({{name.name}}) ddl latency over 600 seconds",
        "dynamodb_key": "DB-MySQL-DDL-Latency-01",
        "query": "max(last_10m):avg:aws.rds.ddllatency{dbinstanceidentifier:sksh-argos-p-aurora-mysql*} by {name} > 600000"
    },
    {
        "no": 37,
        "monitor_id": 127821964,
        "name": "[P1][System] Host {{host.name}} - EBS failed - {{volume-name.name}}",
        "dynamodb_key": "SYSTEM-EC2-EBS-Fail-01",
        "query": "min(last_1m):max:aws.ebs.status.ok{volume-name:*} by {volume-name} < 1"
    },
    {
        "no": 38,
        "monitor_id": 127822718,
        "name": "[P1][System] Host [{{name.name}}] - 메모리 사용량이 90 %  이상입니다.",
        "dynamodb_key": "SYSTEM-EC2-MEM-High-01",
        "query": "avg(last_5m):(1 - avg:system.mem.pct_usable{name:sksh-argos-p*} by {name}) * 100 >= 90"
    },
    {
        "no": 39,
        "monitor_id": 127822912,
        "name": "[P2][System] Host [{{host.name}}]- Alert messages log[{{log.message}}] 발생",
        "dynamodb_key": "SYSTEM-EC2-Alert-Message-01",
        "query": "events(\"Name:sksh-argos-p* filename:messages (\":emerg\" OR \":crit\" OR \":alert\" OR \"error: Operation\" OR \"kernel:err\")\").rollup(\"count\").by(\"host\").last(\"1m\") >= 1"
    },
    {
        "no": 40,
        "monitor_id": 130834458,
        "name": "[P2][DB] 최근 5분 동안 CAD MariaDB ({{dbinstanceidentifier.name}}) 여유 저장소 공간이 낮음",
        "dynamodb_key": "DB-MariaDB-FreeStorageSpace-01",
        "query": "avg(last_5m):(avg:aws.rds.free_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-02} by {dbinstanceidentifier} / avg:aws.rds.total_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-02} by {dbinstanceidentifier}) * 100 < 4"
    },
    {
        "no": 41,
        "monitor_id": 130834459,
        "name": "[P2][DB] 최근 5분 동안 IGP MariaDB ({{dbinstanceidentifier.name}}) 여유 저장소 공간이 낮음",
        "dynamodb_key": "DB-ICP-MariaDB-FreeStorageSpace-01",
        "query": "avg(last_5m):(avg:aws.rds.free_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-01} by {dbinstanceidentifier} / avg:aws.rds.total_storage_space{dbinstanceidentifier:sksh-argos-p-rds-mariadb-01} by {dbinstanceidentifier}) * 100 < 4"
    },
    {
        "no": 42,
        "monitor_id": 130834460,
        "name": "[P2][DB] CAD MariaDB {{dbinstanceidentifier.name}} CPU 사용율이 너무 높음",
        "dynamodb_key": "DB-MariaDB-CPU-TooHigh-01",
        "query": "avg(last_5m):avg:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-rds-mariadb-02} by {name} > 80"
    },
    {
        "no": 43,
        "monitor_id": 130834461,
        "name": "[P2][DB] IGP MariaDB {{dbinstanceidentifier.name}} CPU 사용율이 너무 높음",
        "dynamodb_key": "DB-MariaDB-CPU-TooHigh-01",
        "query": "avg(last_5m):avg:aws.rds.cpuutilization{dbinstanceidentifier:sksh-argos-p-rds-mariadb-01} by {name} > 80"
    },
    {
        "no": 44,
        "monitor_id": 131024355,
        "name": "[P2][Network] TGW PacketDropCountNoRoute ({{transitgatewayattachment.name}})",
        "dynamodb_key": "Network-TGW-PacketDrop-01",
        "query": "sum(last_5m):sum:aws.transitgateway.packet_drop_count_no_route{transitgateway:tgw-055c4967d80e517e2} by {transitgatewayattachment}.as_count() > 100"
    },
]
