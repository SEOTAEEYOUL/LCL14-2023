import boto3

dynamodb = boto3.client('dynamodb', region_name='ap-northeast-2')

# Specify the existing and new table names
existing_table_name = 'dynamodb_system_check_lcl14'
new_table_name = 'dynamodb_system_check_lcl14_backup'

# Retrieve the details of the existing table
response = dynamodb.describe_table(TableName=existing_table_name)
table_details = response['Table']

# Create a new table with the desired name and the same schema as the existing table
new_table_details = {
    'TableName': new_table_name,
    'AttributeDefinitions': table_details['AttributeDefinitions'],
    'KeySchema': table_details['KeySchema'],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 5,  # Adjust this value as per your needs
        'WriteCapacityUnits': 5  # Adjust this value as per your needs
    }
}

dynamodb.create_table(**new_table_details)

# Wait for the new table to be created
dynamodb.get_waiter('table_exists').wait(TableName=new_table_name)

# Copy the data from the existing table to the new table
scan_paginator = dynamodb.get_paginator('scan')
scan_iterator = scan_paginator.paginate(TableName=existing_table_name)

for page in scan_iterator:
    items = page['Items']
    if items:
        put_requests = [{'PutRequest': {'Item': item}} for item in items]
        batch_write_params = {
            'RequestItems': {
                new_table_name: put_requests
            }
        }
        # Perform batch write operation in batches of 25 items
        while put_requests:
            batch = put_requests[:25]
            batch_write_params['RequestItems'][new_table_name] = batch
            dynamodb.batch_write_item(**batch_write_params)
            put_requests = put_requests[25:]

print("Table renamed successfully!")
