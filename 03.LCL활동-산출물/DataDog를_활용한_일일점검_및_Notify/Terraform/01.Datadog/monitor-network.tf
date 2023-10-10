# # 알림 생성
# resource "datadog_monitor" "network_dx_down" {
#     name          = "[P1][Network] DX Connection Down ({{connectionid.name}})"
#     type          = "query alert"
#     query         = "max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1"
#     message = <<EOF
# [참고 - 연결 정보]
# ## Data망
# - dxcon-fh5l0k7k : 1st VIF (KINX)
# - dxcon-fg6pdahf : 2nd VIF (LG U+)

# ## 신호수신망
# - dxcon-fh891mus : 1st VIF (KINX)
# - dxcon-fg44j36q : 2nd VIF (KINX)
# - dxcon-fg6a3n0g : 3rd VIF (LG U+)

# ## 고객센터망
# - dxcon-fgqxwnve : 1st VIF (SKCC / KINX)
# - dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) 

# ## 비고
# Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
# Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos_l1 @webhook-alert_collect @webhook-alert_collect2
# EOF
#     tags                     = ["Network", "DX", "Down", "team:skcc", "monitor:Network-DX-Down-01"]
#     notify_audit             = false
#     # restricted_roles         = ["write"]
#     timeout_h                = 0
#     include_tags             = true
#     require_full_window      = false
#     new_group_delay          = 300
#     notify_no_data           = false
#     escalation_message       = "AWS Direct Connect 가 Down 되었습니다. 원인 파악 및 조치가 필요합니다."
#     priority                 = 1

#     notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


#     # 알림 조건 설정
#     monitor_thresholds  {
#         critical = 1
#     }

#     # monitor_threshold_windows {
#     #     trigger_window  = "last_30m"
#     #     recovery_window = "last_30m"
#     # }

#     renotify_interval = 60
# }

resource "datadog_monitor" "network_elb_response_time" {
    name          = "[P4][Network] ELB 응답시간이 {{value}} 초 이상 입니다"
    type          = "query alert"
    query         = "avg(last_5m):avg:aws.applicationelb.target_response_time.average{loadbalancer:*} by {name} > 5"
    message = <<EOF
## EKS ELB Response Time
| ELB | Response Time |  
|:---|:---|  
| {{name}} | {{value}} |


Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_info @webhook-alert_collect @webhook-alert_collect2
EOF
    tags                     = ["Network", "ELB", "ResponseTime", "team:skcc", "monitor:Network-ELB-ResponseTime-01"]
    notify_audit             = false
    # restricted_roles         = ["write"]
    timeout_h                = 0
    include_tags             = true
    require_full_window      = false
    new_group_delay          = 300
    notify_no_data           = false
    escalation_message       = "AWS ELB 의 응답시간이 {{value}} 초 이상 입니다. 원인 파악 및 조치가 필요합니다."
    priority                 = 4

    notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


    # 알림 조건 설정
    monitor_thresholds  {
        critical = 5
    }

    # monitor_threshold_windows {
    #     trigger_window  = "last_30m"
    #     recovery_window = "last_30m"
    # }

    renotify_interval = 60
}

# resource "datadog_monitor" "network_tgw_packet_drop_no_route" {
#     name          = "[P2][Network] TGW({{transitgatewayattachment.name}}) 경로 불일치로 패킷 Drop 발생"
#     type          = "query alert"
#     query         = "sum(last_5m):sum:aws.transitgateway.packet_drop_count_no_route{transitgateway:tgw-055c4967d80e517e2} by {transitgatewayattachment}.as_count() > 100"
#     message = <<EOF
# ## 최근 5분 동안 TGW({{transitgatewayattachment.name}}) PacketDropCountNoRoute
# {{#is_alert}}
# {{override_priority 'P2'}}
# {{/is_alert}}

# {{#is_warning}}
# {{override_priority 'P3'}}
# {{/is_warning}}

# ### 경로 불일치로 버려진 패킷의 수 : {{value}}
# ### Trangit GateWay : {{transitgatewayattachment.name}} 



# Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
# Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @webhook-alert_collect @webhook-alert_collect2
# EOF
#     tags                     = ["Network", "TGW", "PacketDrop", "NoRoute", "team:skcc", "monitor:Network-TGW-PacketDropNoRoute-01"]
#     notify_audit             = false
#     # restricted_roles         = ["write"]
#     timeout_h                = 0
#     include_tags             = true
#     require_full_window      = false
#     new_group_delay          = 300
#     notify_no_data           = false
#     escalation_message       = "TGW 의 경로 불일치로 패킷 Drop 발생, 원인 파악 및 조치가 필요합니다."
#     priority                 = 2

#     notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


#     # 알림 조건 설정
#     monitor_thresholds  {
#         critical = 100
#         warning  = 10
#     }

#     # monitor_threshold_windows {
#     #     trigger_window  = "last_30m"
#     #     recovery_window = "last_30m"
#     # }

#     renotify_interval = 60
# }

# resource "datadog_monitor" "network_tgw_packet_drop_blackhoe" {
#     name          = "[P2][Network] TGW({{transitgatewayattachment.name}}) Blackhole 경로 일치로 패킷 Drop 발생"
#     type          = "query alert"
#     query         = "sum(last_5m):sum:aws.transitgateway.packet_drop_count_blackhole{transitgateway:tgw-055c4967d80e517e2} by {transitgatewayattachment}.as_count() > 100"
#     message = <<EOF
# ## 최근 5분 동안 TGW({{transitgatewayattachment.name}}) PacketDropCountBlackhole 
# {{#is_alert}}
# {{override_priority 'P2'}}
# {{/is_alert}}

# {{#is_warning}}
# {{override_priority 'P3'}}
# {{/is_warning}}

# ### Blackhole 경로 일치로 버려진 패킷의 수 : {{value}}
# ### Trangit GateWay : {{transitgatewayattachment.name}} 



# Time(Asia/Seoul) : {{local_time 'last_triggered_at' 'Asia/Seoul'}}
# Notify:@slack-skshieldusnextossdev-prd알람 @slack-SKCC_Digital_Service-ict_shieldus_argos @webhook-alert_collect @webhook-alert_collect2
# EOF
#     tags                     = ["Network", "TGW", "PacketDrop", "Blackhoe", "team:skcc", "monitor:Network-TGW-PacketDropBlackhole-01"]
#     notify_audit             = false
#     # restricted_roles         = ["write"]
#     timeout_h                = 0
#     include_tags             = true
#     require_full_window      = false
#     new_group_delay          = 300
#     notify_no_data           = false
#     escalation_message       = "TGW 의 Blackhole 경로 일치로 패킷 Drop 발생, 확인 필요합니다."
#     priority                 = 2

#     notification_preset_name = "hide_query" # "show_all", "hide_query", "hide_handles", "hide_all"


#     # 알림 조건 설정
#     monitor_thresholds  {
#         critical = 100
#         warning  = 10
#     }

#     # monitor_threshold_windows {
#     #     trigger_window  = "last_30m"
#     #     recovery_window = "last_30m"
#     # }

#     renotify_interval = 60
# }
