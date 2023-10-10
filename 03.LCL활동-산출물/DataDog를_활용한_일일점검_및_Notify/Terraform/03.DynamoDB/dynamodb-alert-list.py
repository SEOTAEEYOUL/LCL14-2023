import boto3
from datetime import datetime

def count_items_by_priority(date_value):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'dydb_alert_history_lcl14'  # 테이블 이름을 여기에 입력하세요

    date_attribute = 'date'
    priority_attribute = 'alert_priority'


    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression=f"#{date_attribute} = :date_value",
        ExpressionAttributeNames={
            f"#{date_attribute}": date_attribute,
        },
        ExpressionAttributeValues={
            ":date_value": date_value,
        },
        ProjectionExpression=priority_attribute
    )

    count_by_priority = {}

    for item in response['Items']:
        priority = item.get(priority_attribute)
        count_by_priority[priority] = count_by_priority.get(priority, 0) + 1

    return count_by_priority

if __name__ == "__main__":
# '20230708'에 해당하는 날짜의 count를 priority 별로 세는 예시

    table = dynamodb.Table(table_name)
    today = datetime.now().strftime('%Y%m%d')

    # date_value = '20230708'
    count_results = count_items_by_priority(today)

    for priority, count in count_results.items( ):
        print(f"Priority: {priority}, Count: {count}")