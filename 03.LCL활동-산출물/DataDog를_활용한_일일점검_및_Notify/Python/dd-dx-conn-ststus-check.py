import requests

# Enter your Datadog API and application keys
api_key = "**********"
app_key = "**********"

# Enter the monitor ID associated with the DX connection status monitor
monitor_id = "116390058"


def check_dx_connection_status(api_key, app_key, monitor_id):
    # Set up the Datadog API endpoint
    url = f"https://api.datadoghq.com/api/v1/monitor/116390058"

    # Set the headers with the API and application keys
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }

    # Send the GET request to retrieve the monitor details
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        monitor_details = response.json()
        print(str(monitor_details) + "\n\n")

        # Extract the monitor status
        status = monitor_details.get("overall_state")
        name = monitor_details.get("name")
        priority = monitor_details.get("priority")

        # Check if the connection is up or down
        if status == "OK":
            print(
                "# EventName: "
                + str(name)
                + "\n"
                + "# Status: "
                + "AWS Direct Connect connection is up!"
                + "\n"
                + "# Priority: "
                + str(priority)
            )
        else:
            print("Please Check the DX connection.")
    else:
        print("Failed to retrieve monitor details. Check your API keys and monitor ID.")


# Call the function to check the DX connection status
check_dx_connection_status(api_key, app_key, monitor_id)
