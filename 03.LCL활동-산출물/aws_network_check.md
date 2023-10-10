# AWS Direct Connect Connection Check

### 환경 변수

#### 자격증명(Datadog Keys)

api_key = "**********"
app_key = "**********"

#### Datadog 모니터 ID

monitor_id = "116390058"

### 스크립트 수행

$ python dd-dx-conn-ststus-check.py

#### 실행결과

```
{'id': 116390058, 'org_id': 708429, 'type': 'query alert', 'name': '[P1][Network] DX Connection Down ({{connectionid.name}})', 'message': '[참고 - 연결 정보]\n# Data망\n- dxcon-fh5l0k7k : 1st VIF (KINX)\n- dxcon-fg6pdahf : 2nd VIF (LG U+)\n# 신호수신망\n- dxcon-fh891mus : \x081st VIF (KINX)\n- dxcon-fg44j36q : 2nd VIF (KINX)\n- dxcon-fg6a3n0g : 3rd VIF (LG U+)\n# 고객센터망\n- dxcon-fgqxwnve : 1st VIF (SKCC / KINX)\n- dxcon-fh2s52kw : 2nd VIF (SKCC / KINX) \n\n@slack-skshieldusnextossdev-prd알람 \n@slack-SKCC_Digital_Service-ict_shieldus_argos\n@slack-SKCC_Digital_Service-ict_shieldus_argos_l1', 'tags': ['team:skcc', 'DOWN', 'Network'], 'query': 'max(last_5m):avg:aws.dx.connection_state{aws_account:123456789012} by {connectionid} < 1', 'options': {'thresholds': {'critical': 1.0}, 'notify_audit': False, 'require_full_window': False, 'notify_no_data': False, 'renotify_interval': 0, 'include_tags': True, 'evaluation_delay': 900, 'new_group_delay': 60, 'silenced': {}}, 'multi': True, 'created_at': 1681462142000, 'created': '2023-04-14T08:49:02.655103+00:00', 'modified': '2023-05-02T15:46:38.055414+00:00', 'deleted': None, 'restricted_roles': None, 'priority': 1, 'overall_state_modified': '2023-04-14T08:49:05+00:00', 'overall_state': 'OK', 'creator': {'name': None, 'handle': 'yjbang@sk.com', 'email': 'yjbang@sk.com', 'id': 4671517}}

# EventName: [P1][Network] DX Connection Down ({{connectionid.name}})

# Status: AWS Direct Connect connection is up!

# Priority: 1
```
