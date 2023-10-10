import time
from datadog import initialize, api

from pprint import pprint


import datadog_helper

datadog_helper.init_datadog_session( )

# Define the metric query for CPU usage
# query = 'system.cpu.load.1m{*}'
# query = 'avg:system.cpu.user{*}'
query = 'avg:aws.rds.cpuutilization{dbclusteridentifier:sksh-argos-p-aurora-mysql}'


# Fetch the metric data
end = int(time.time())
start = end - 300  # Fetch data for the last 5 minutes
# start = end - 3600


# Define the instance identifier for Aurora MySQL
instance_identifier = 'sksh-argos-p-aurora-mysql'

# Make the API call
try:
    result = api.Metric.query(start=start, end=end, query=query)

    if 'series' in result:
        if len(result['series']) > 0:
            series = result['series'][0]  # Assuming only one series is returned
            pprint(series)
            for point in series['pointlist']:
                pprint(point)
                timestamp = point[0]
                value = point[1]
                if value > 90:
                    print(f"{series['scope']} Not OK -> {value:.2f}%")
                    break  # Exit the loop if CPU usage exceeds 90%
            else:
                print(f"{series['scope']} OK -> {value:.2f}%")
        else:
            print("No metric data available for the query.")
    else:
        print("No metric data available for the query.")
except Exception as e:
    print(f"Query execution failed. Error: {str(e)}")