# -*- coding: utf-8 -*-
import datadog
from datadog import api


import json
from pprint import pprint

import jmespath
import xlsxwriter
import argparse
import datetime
import time

# from time import time
# from json import dump

import json
from pprint import pprint

import warnings

import datadog_helper


datadog_helper.init_datadog_session( )

warnings.filterwarnings('ignore', category=FutureWarning, module='botocore.client')

now = datetime.datetime.now()
now_time = now.strftime("%y%m%d")
excel_name = now_time + '_datadog_alert_report.xlsx'

xlsx = xlsxwriter.Workbook(excel_name, {'remove_timezone': True})

title_format       = xlsx.add_format({'bold':True, 'font_size':13, 'align': 'left'})
coltitle_format    = xlsx.add_format({'bold':True, 'font_color':'white', 'bg_color':'#393839', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
colname_format     = xlsx.add_format({'bold':True, 'font_color':'white', 'bg_color':'#1E4E79', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
colname_left_format= xlsx.add_format({'bold':True, 'font_color':'white', 'bg_color':'#1E4E79', 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
string_format      = xlsx.add_format({'align': 'left', 'valign': 'vcenter'})
wrap_format        = xlsx.add_format({'text_wrap': True, 'valign': 'vcenter'})
nextline_format    = xlsx.add_format({'bg_color':'#BFBFBF', 'valign': 'vcenter'})
date_format        = xlsx.add_format({'num_format': 'yyyy/mm/dd hh:mm', 'valign': 'vcenter', 'align': 'left'})
currency_format    = xlsx.add_format({'num_format': '$#,##0.00'})
number_format      = xlsx.add_format({'num_format': '#,##0.00', 'align': 'right', 'valign': 'vcenter'})
integer_format     = xlsx.add_format({'num_format': '#,##0', 'align': 'right', 'valign': 'vcenter'})


# {'created': '2022-07-29T07:34:32.306527+00:00',
#  'created_at': 1659080072000,
#  'creator': {'email': 'gp.hong@sk.com',
#              'handle': 'gp.hong@sk.com',
#              'id': 4269767,
#              'name': 'Hong Gil Pyo'},
#  'deleted': None,
#  'id': 78571814,
#  'matching_downtimes': [],
#  'message': 'MariaDB Memory\n'
#             '{{name}} : {{value}}\n'
#             "Time(Asia/Seoul) : {{local_time 'last_triggered_at' "
#             "'Asia/Seoul'}} @slack-SKCC_Digital_Service-ict_shieldus_argos",
#  'modified': '2023-04-28T02:37:15.784374+00:00',
#  'multi': True,
#  'name': '[P2][DB] MariaDB ({{name.name}})  Freeable memory({{value}}) is too '
#          'low',
#  'options': {'evaluation_delay': 900,
#              'include_tags': True,
#              'new_group_delay': 60,
#              'notification_preset_name': 'hide_query',
#              'notify_audit': False,
#              'notify_no_data': False,
#              'renotify_interval': 0,
#              'require_full_window': False,
#              'silenced': {},
#              'thresholds': {'critical': 210000000.0, 'warning': 430000000.0}},
#  'org_id': 708429,
#  'overall_state': 'Warn',
#  'overall_state_modified': '2023-05-10T22:39:14+00:00',
#  'priority': 2,
#  'query': 'avg(last_5m):avg:aws.rds.freeable_memory{dbinstanceidentifier:*,dbinstanceclass:db.t3.medium,engine:mariadb,!dbinstanceidentifier:sksh-argos-p-aurora-mysql-master-rci,!dbinstanceidentifier:sksh-argos-p-aurora-mysql-reader-rci} '
#           'by {name} < 210000000',
#  'restricted_roles': None,
#  'tags': ['team:skcc', 'MariaDB', 'MEM'],
#  'type': 'query alert'}
# [P2][DB] MariaDB ({{name.name}})  Freeable memory({{value}}) is too low


def report_datadog_alert( ):

    Columns = ["No.", "Id", "Team", "Name", "Priority", "Created", "Modified", "Creator", "Query", "Options", "Tags", "Type", "Message"]

    result_sheet = xlsx.add_worksheet('Datadog Alert')
    # result_sheet.set_column('A:Z', cell_format=wrap_format)

    # result_sheet.write(0, 0, "EKS Cluster List", title_format)
    col = 0 
    for ColName in Columns:
        result_sheet.write(1, col, ColName, colname_format)
        col += 1

    result_sheet.set_column('A:A', 5)   # No.
    result_sheet.set_column('B:B', 10)  # Id
    result_sheet.set_column('C:C', 10)  # Team
    result_sheet.set_column('D:D', 72)  # Name
    result_sheet.set_column('E:E', 9)   # Priority
    result_sheet.set_column('F:F', 17)  # Created
    result_sheet.set_column('G:G', 17)  # Modified
    result_sheet.set_column('H:H', 32)  # Creator
    result_sheet.set_column('I:I', 82)  # Query
    result_sheet.set_column('J:J', 52)  # Options
    result_sheet.set_column('K:K', 82)  # Tags
    result_sheet.set_column('L:L', 12)  # Type
    result_sheet.set_column('M:M', 102)  # Message

    # Alert 목록을 가져옵니다.
    alert_list = api.Monitor.get_all()
    print("-------")
    print('Alert 목록:')
    # pprint(alert_list)
    row = 2
    alert_cnt = 0
    team_cnt = {}
    skcc_alert_cnt = 0
    # 행 고정 : 2번째 행을 고정합니다.
    result_sheet.freeze_panes(row, 0)

    with open('alert_list.py', 'w', encoding='utf-8') as file:
        file.write('alert_list      = [\n') 
        for alert in alert_list:
            # pprint(alert)
            print(alert['name'])
            # print(alert['name'].encode('utf-8'))
            alert_output = jmespath.search('[id, name, priority, created, modified, creator, query, options, tags, type, message]', alert)

            id, name, priority, created, modified, creator, query, options, tags, type, message = alert_output
            # pprint(alert_output)



            # "Name", "Priority", "Created", "Modified", "Creator", "Query", "Option", "Tags", "Type", "Message"    
            result_sheet.write(row, 0, alert_cnt + 1, integer_format) # "No.",    
            result_sheet.write(row, 1, id, integer_format) # Id
            result_sheet.write(row, 3, name, wrap_format) # "Name", 
            result_sheet.write(row, 4, f'P{priority}', string_format) # "Priority", 
            result_sheet.write(row, 5, created, date_format) # "Created",
            result_sheet.write(row, 6, modified, date_format) # "Modified"
            # result_sheet.write(row, 6, json.dumps(creator, indent=2), wrap_format) # "Creator"
            result_sheet.write(row, 7, "\n".join([f"{key}: {value}" for key, value in creator.items()]), wrap_format) # "Created",
            
            result_sheet.write(row, 8, query, wrap_format) # "Query"
            result_sheet.write(row, 9, json.dumps(options, indent=2), wrap_format) # "Option"
            # result_sheet.write(row, 9, json.dumps(tags, indent=2), wrap_format)  # Tags
            result_sheet.write(row, 10, '\n'.join(tags), wrap_format)  # Tags
            print(tags)
            is_found = False
            monitor = '-'
            for tag in tags:
                if "team:" in tag:
                    team = tag.split(":")[1].strip( )
                    # print(f">> team:{team}")
                    result_sheet.write(row, 2, team, string_format)
                    is_found = True
                if "monitor:" in tag:
                    monitor = tag.split(":")[-1].strip( )
                    print(f">> monitor:{monitor}")

            if is_found == False:
                team = '-'
                result_sheet.write(row, 2, team, string_format)

            if team in team_cnt:
                team_cnt[team] += 1
            else:
                team_cnt[team] = 1


            result_sheet.write(row, 11, type, string_format)  # Type
            result_sheet.write(row, 12, message, wrap_format)  # Message


            print(f"priority[{priority}], team[{team}]")
            if priority == 1 or priority == 2:
                if team == 'skcc':
                    skcc_alert_cnt += 1
                    data = {
                        'no': skcc_alert_cnt,
                        'monitor_id': id,
                        'name': name,
                        # 'dynamodb_key': f'SYSTEM-SKCC-{skcc_alert_cnt:02d}',
                        'dynamodb_key': id if monitor == '-' else monitor,
                        'query': query
                    }
                    # Write the JSON data entry to the file
                    pprint(data)
                    # Format the JSON data with indentation
                    # formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
                    # file.write(formatted_data)
                    # json.dump(data, file, indent=4, ensure_ascii=False)
                    json_str = json.dumps(data, indent=4, ensure_ascii=False)
                    indented_json_str = "\n".join(" " * 4 + line for line in json_str.splitlines())
                    file.write(indented_json_str)
                    # Write the formatted JSON data entry to the file
                    file.write(',\n') # Add a new line after each entry
                    # file.write('\n')  # Add a new line after each entry
                    

            row += 1
            alert_cnt += 1
        
        file.write(']\n') 

    # print(team_cnt)
    print("-Datadog Alert List ["+ str(alert_cnt) +"]")
    team_cnt_str = ", ".join([f"\"{key}\":[{value}]" for key, value in team_cnt.items()])
    result_sheet.write(0, 0, f"Datadog Alert List(Total[{alert_cnt}], {team_cnt_str})", title_format)


    # 필터링
    # 필터링을 적용할 데이터 # 범위를 설정합니다.
    result_sheet.autofilter(1, 0, alert_cnt, col-1)
    
    print("Done.\n") 



    
def main( ):  
    print("Datadog Alert")
    start_time = time.time()
    report_datadog_alert( )
    end_time = time.time()
    print(f"Program execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    # region_args, profile_args = get_arguments()
    # main(region_args, profile_args)
    main( )
    xlsx.close( )
    now = datetime.datetime.now()

    print(now) 