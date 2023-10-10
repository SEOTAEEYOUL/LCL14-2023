"""
Get organization information returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.organizations_api import OrganizationsApi

import datadog_helper

datadog_helper.init_datadog_session( )

public_id = datadog_helper.get_public_id( )

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = OrganizationsApi(api_client)
    response = api_instance.get_org(
        public_id = public_id
    )

    print(response)