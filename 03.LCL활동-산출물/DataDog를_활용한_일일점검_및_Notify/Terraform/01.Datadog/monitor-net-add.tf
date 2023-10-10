# Channel List
# @slack-SKCC_Digital_Service-ict_shieldus_argos_l1
# @slack-SKCC_Digital_Service-ict_shieldus_argos_p2 
# @slack-SKCC_Digital_Service-ict_shieldus_argos_p3 
# @slack-SKCC_Digital_Service-ict_shieldus_argos_info

# 1
resource "datadog_monitor" "network_dx_down" {
  name = "[P1][Network] DX Connection Down ({{connectionid.name}})"
  type = "query alert"
  message = <<-EOF
    ## Data망
    - dxcon-fh5l0k7k : 1st VIF (KINX)
    - dxcon-fg6pdahf : 2nd VIF (LG U+)
    ## 신호수신망
    - dxcon-fh891mus : 1st VIF (KINX)
    - dxcon-fg44j36q : 2nd VIF (KINX)
    - dxcon-fg6a3n0g : 3rd VIF (LG U+)
    ## 고객센터망
    - dxcon-fgqxwnve : 1st VIF (SKCC / KINX)
    - dxcon-fh2s52kw : 2nd VIF (SKCC / KINX)
    ## 비고
    - Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_l1
  EOF
  tags = [
    "Network",
    "DX Conn Down",  
    "monitor:Network-DX-Down-01",
    "team:skcc",
  ]
  query = "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1"
  priority = 1
  restricted_roles = null
  escalation_message   = "AWS Direct Connect 가 Down 되었습니다. 원인 파악 및 조치가 필요합니다."
  include_tags         = true
  new_group_delay      = 60  
  notification_preset_name = "hide_query"
  notify_no_data       = false
  renotify_interval    = 60
  require_full_window  = false  
  notify_audit         = false  
}

# 2
resource "datadog_monitor" "network_tgw_packetdropnoroute" {
  name = "[P2][Network] TGW PacketDropCountNoRoute ({{transitgatewayattachment.name}})"
  type = "query alert"
  message = <<-EOF
    # Transit Gateway Attachment 별 라우팅 이상 여부 확인
    - Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p2
  EOF
  tags = [
    "TGW",
    "Drop",
    "Network",
    "monitor:Network-TGW-PacketDrop-01",
    "team:skcc",
  ]
  query = "sum(last_5m):sum:aws.transitgateway.packet_drop_count_no_route{transitgateway:tgw-055c4967d80e517e2} by {transitgatewayattachment}.as_count() > 100"
  priority = 2
  restricted_roles = null
  escalation_message   = "AWS TGW의 Attachment 라우팅 경로 변화가 감지 되었습니다. 원인 파악 및 조치가 필요합니다."
  include_tags         = true
  evaluation_delay     = 900
  new_group_delay      = 60
  notification_preset_name = "hide_query"
  notify_no_data       = false
  renotify_interval    = 60
  require_full_window  = false  
  notify_audit         = false  
}

# 3
resource "datadog_monitor" "network_tgw_packetdropblackhole" {
  name = "[P4][Network] TGW PacketDropCountBlackhole ({{transitgatewayattachment.name}})"
  type = "query alert"
  message = <<-EOF
    # Transit Gateway Attachment 별 패킷 유실 여부 확인
    - Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
  EOF
  tags = [
    "Network",
    "TGW",
    "DropBlackhole",    
    "monitor:Network-TGW-PacketBlackhole-01",
    "team:skcc",
  ]
  query = "sum(last_5m):sum:aws.transitgateway.packet_drop_count_blackhole{transitgateway:tgw-055c4967d80e517e2} by {transitgatewayattachment}.as_count() > 100"
  priority = 4
  restricted_roles = null
  escalation_message   = "AWS TGW의 Attachment Blackhole 상태가 감지 되었습니다. 원인 파악 및 조치가 필요합니다."
  include_tags         = true
  evaluation_delay     = 900
  new_group_delay      = 60
  notification_preset_name = "hide_query"
  notify_no_data       = false
  renotify_interval    = 60
  require_full_window  = false  
  notify_audit         = false  
}

# 4
resource "datadog_monitor" "network_natgw_packetdrop" {
  name = "[P3][Network] NAT Gateway drop 패킷 수 체크 : {{natgatewayid.name}}"
  type = "query alert"
  message = <<-EOF
    ## NAT 게이트웨이에서 Drop된 패킷 수 확인
    - 대상: {{natgatewayid.name}}
    - Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_p3
  EOF
  tags = [
    "monitor:Network-NATGW-PacketDrop-01",
    "team:skcc",
    "Network",
  ]
  query = "sum(last_5m):sum:aws.natgateway.packets_drop_count.sum{natgatewayid:nat-*} by {name}.as_count() > 10"
  priority = 3
  restricted_roles = null
  notify_audit         = false
  require_full_window  = false
  notify_no_data       = false
  renotify_interval    = 0
  include_tags         = true
  evaluation_delay     = 900
  new_group_delay      = 60    
}

# 5
resource "datadog_monitor" "network_natgw_error_port_allocation" {
  name = "[P5][Network] NAT Gateway 소스 포트 할당 불가 : {{natgatewayid.name}}"
  type = "query alert"
  message = <<-EOF
      ## NAT 게이트웨이가 소스 포트를 할당하지 못한 횟수
      - 대상: {{name.name}}
      - Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
      - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
      EOF        
  tags = [
    "monitor:Network-NATGW-ErrorPortAllocation-01",
    "team:skcc",
    "Network"        
    ]  
  query = "sum(last_5m):sum:aws.natgateway.error_port_allocation{natgatewayid:*} by {name}.as_count() > 1"
  priority         = 5
  notify_audit      = false
  require_full_window = false
  notify_no_data    = false
  renotify_interval = 0
  include_tags      = true
  evaluation_delay  = 900
  new_group_delay   = 60 
}

# 6
resource "datadog_monitor" "network_natgw_idle_timeout_count" {
  name = "[P5][Network] NAT Gateway Idle Timeout Count : {{natgatewayid.name}}"
  type = "query alert"
  message = <<-EOF
        ## NAT 게이트웨이가 활성 상태에서 유휴 상태로 전환되는 연결로 인해 발생하는 timeout 수
        - 대상: {{name.name}}
        - Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
        - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
        EOF        
  tags = [
        "monitor:Network-NATGW-IdleTimeoutCount-01",
        "team:skcc",
        "Network"        
    ]  
  query = "sum(last_5m):sum:aws.natgateway.idle_timeout_count{natgatewayid:*, !name:sksh-argos-p-ngw-pub-2c} by {name}.as_count() > 300"
  priority         = 5
  notify_audit      = false
  require_full_window = false
  notify_no_data    = false
  renotify_interval = 0
  include_tags      = true
  evaluation_delay  = 900
  new_group_delay   = 60 
}

# 7
resource "datadog_monitor" "network_dx_vif_egress_peak" {
  name = "[P5][Network] DX VIF EGRESS Traffic Peak 발생"
  type = "query alert"
  message = <<-EOF
        ## DX VIF Egress 트래픽이 100Mb 이상일 경우 체크
        - Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
        - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
        EOF        
  tags = [
        "monitor:Network-DX-VIF_Egress_Peak",
        "team:skcc",
        "Network"        
    ]  
  query = "max(last_5m):sum:aws.dx.virtual_interface_bps_egress{*} by {virtualinterfaceid}.as_rate() > 100000000"
  priority         = 5
  notify_audit      = false
  require_full_window = false
  notify_no_data    = false
  renotify_interval = 0
  include_tags      = true
  evaluation_delay  = 900
  new_group_delay   = 60 
}

# 8
resource "datadog_monitor" "network_dx_vif_ingress_peak" {
  name = "[P5][Network] DX VIF INGRESS Traffic Peak 발생"
  type = "query alert"
  message = <<-EOF
        ## DX VIF Ingress 트래픽이 100Mb 이상일 경우 체크
        - Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
        - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
        EOF        
  tags = [
        "monitor:Network-DX-VIF_Ingress_Peak",
        "team:skcc",
        "Network"        
    ]  
  query = "max(last_5m):avg:aws.dx.virtual_interface_bps_ingress{*} by {virtualinterfaceid}.as_rate() > 100000000"
  priority         = 5
  notify_audit      = false
  require_full_window = false
  notify_no_data    = false
  renotify_interval = 0
  include_tags      = true
  evaluation_delay  = 900
  new_group_delay   = 60 
}

# 9 Monitor NLB Request Count



resource "datadog_monitor" "network_nlb_processed_bytes" {
  name         = "[P5][Network] NLB processed bytes"
  type         = "metric alert"
  message = <<-EOF
    ## 1시간 동안 AWS NLB 처리량 100Mb 초과 시 체크 
    - Time(Asia/Seoul): {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
  EOF    
  tags = [    
    "monitor:Network-NLB-ProcessedBytes",
    "team:skcc",
    "Network"
  ]
  query        = "sum(last_1h):sum:aws.networkelb.processed_bytes{loadbalancer:*, !name:sksh-argos-p-eks-ui-ie-nlb-pri} by {name}.as_count() > 400000000"
  priority = 5
  notify_audit = false
  require_full_window = false
  notify_no_data = false
  renotify_interval = 0
  include_tags = true
  evaluation_delay = 900
  new_group_delay = 60 
}


# 10
resource "datadog_monitor" "network_ALB_target_unhealthy_count_monitor" {
  name = "[P5][Network] ALB Target Unhealthy Count"
  type = "query alert"
  message = <<-EOF
    ## Check if ALB Target Health Unhealthy Count is above 30
    - Time(Asia/Seoul): {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
  EOF
  tags = [    
    "monitor:Network-ALB-Target_Health_Unhealthy_Count",
    "team:skcc",
    "Network"
  ]
  query = "max(last_1h):sum:aws.applicationelb.unhealthy_routing_request_count{*} by {loadbalancer} > 30"
  priority = 5
  notify_audit = false
  require_full_window = false
  notify_no_data = false
  renotify_interval = 0
  include_tags = true
  evaluation_delay = 900
  new_group_delay = 60
}

# 11
resource "datadog_monitor" "network_ALB_request_count_high_monitor" {
  name = "[P5][Network] ALB Request Count High"
  type = "query alert"
  message = <<-EOF
    ## Check if ALB Request Count is consistently high
    - Time(Asia/Seoul): {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
  EOF
  tags = [    
    "monitor:Network-ALB-Request_Count_High",
    "team:skcc",
    "Network"
  ]
  query = "sum(last_1h):sum:aws.applicationelb.request_count{*} by {loadbalancer}.as_count() > 1000000"
  priority = 5
  notify_audit = false
  require_full_window = false
  notify_no_data = false
  renotify_interval = 0
  include_tags = true
  evaluation_delay = 900
  new_group_delay = 60
}

# 12
resource "datadog_monitor" "network_NLB_nomal_target_count" {
  name = "[P5][Network] NLB에 연결된 정상 Target 확인"
  type = "query alert"
  message = <<-EOF
    ## NLB에 연결된 정상 Target 이 0일 경우 NLB 사용 여부 확인하기
    - Time(Asia/Seoul): {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
  EOF
  tags = [    
    "monitor:Network-NLB-NomalTargetCount",
    "team:skcc",
    "Network"
  ]
  query = "avg(last_1h):avg:aws.networkelb.healthy_host_count{*} by {loadbalancer}.weighted() > 3"
  priority = 5
  notify_audit = false
  require_full_window = false
  notify_no_data = false
  renotify_interval = 0
  include_tags = true
  evaluation_delay = 900
  new_group_delay = 60
}

#13
resource "datadog_monitor" "network_NLB_port_alloc_error" {
  name = "[P5][Network] NLB 클라이언트 IP 변환 작업 동안의 임시 포트 할당 오류 수"
  type = "query alert"
  message = <<-EOF
    ## 클라이언트 IP 변환 작업동안의 임시 포트 할당 오류 수가 1이상인 경우 체크
    - Time(Asia/Seoul): {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
  EOF
  tags = [    
    "monitor:Network-NLB-PortAllocError",
    "team:skcc",
    "Network"
  ]
  query = "sum(last_5m):sum:aws.networkelb.port_allocation_error_count{*} by {loadbalancer}.as_count() > 1"
  priority = 5
  notify_audit = false
  require_full_window = false
  notify_no_data = false
  renotify_interval = 0
  include_tags = true
  evaluation_delay = 900
  new_group_delay = 60
}

#14
resource "datadog_monitor" "nlb_unhealthy_hosts" {
  name = "[P5][Network] NLB Unhealthy Hosts"
  type = "metric alert"
  message = <<-EOF
    ## NLB 비정상 체크
    - Time(Asia/Seoul): {{local_time 'last_triggered_at' 'Asia/Seoul'}}
    - Notify: @slack-SKCC_Digital_Service-ict_shieldus_argos_info
  EOF
  tags = [    
    "monitor:Network-NLB-UnhealthyHosts",
    "team:skcc",
    "Network"
  ]
  query = "max(last_5m):max:aws.networkelb.un_healthy_host_count{loadbalancer:*, aws_account:123456789012} by {name} > 1"  
  priority = 5
  notify_audit = false
  require_full_window = false
  notify_no_data = false
  renotify_interval = 0
  include_tags = true
  evaluation_delay = 900
  new_group_delay = 60
}




# # 알림 생성
# resource "datadog_monitor" "network_elb_response_time" {
#     name          = "[P4][Network] ELB 응답시간이 {{value}} 초 이상 입니다"
#     type          = "query alert"
#     query         = "avg(last_5m):avg:aws.applicationelb.target_response_time.average{loadbalancer:*} by {name} > 5"
#     message = <<EOF
# ## EKS ELB Response Time
# | ELB | Response Time |  
# |:---|:---|  
# | {{name}} | {{value}} |


# Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
# Noti:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @webhook-alert_collect @webhook-alert_collect2
# EOF
#     tags                = ["Network", "ELB", "ResponseTime", "team:skcc", "monitor:Network-ELB-ResponseTime-01"]
#     notify_audit        = false
#     # restricted_roles    = ["write"]
#     timeout_h           = 0
#     include_tags        = true
#     require_full_window = false
#     new_group_delay      = 300
#     notify_no_data      = false
#     escalation_message  = "AWS ELB 의 응답시간이 {{value}} 초 이상 입니다. 원인 파악 및 조치가 필요합니다."
#     priority            = 4
    
#     # 알림 조건 설정
#     monitor_thresholds  {
#         critical = 5
#     }

#     # monitor_threshold_windows {
#     #     trigger_window  = "last_30m"
#     #     recovery_window = "last_30m"
#     # }

#     renotify_interval = 60
# }

# =========