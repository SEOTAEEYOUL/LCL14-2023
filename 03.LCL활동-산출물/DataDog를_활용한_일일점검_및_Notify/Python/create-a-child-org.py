# from datadog import initialize, api

# # Datadog API 및 애플리케이션 키 설정
# options = {
#     "api_key": "**********",
#     "app_key": "**********",
# }


# # Datadog 초기화
# initialize(**options)

# # 조직 정보 가져오기
# organization = api.Organizations.get()
# org_id = organization['id']
# print(f"조직 ID: {org_id}")


"""
Create a child organization returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.organizations_api import OrganizationsApi
from datadog_api_client.v1.model.organization_billing import OrganizationBilling
from datadog_api_client.v1.model.organization_create_body import OrganizationCreateBody
from datadog_api_client.v1.model.organization_subscription import OrganizationSubscription

body = OrganizationCreateBody(
    billing=OrganizationBilling(
        type="parent_billing",
    ),
    name="New child org",
    subscription=OrganizationSubscription(
        type="pro",
    ),
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = OrganizationsApi(api_client)
    response = api_instance.create_child_org(body=body)

    print(response)
