# AWS
aws_secret_manager_name = "secret_manager_aws_argos"
aws_profile             = "lcl14"
aws_region              = "ap-northeast-2"
aws_access_key          = "**********"
aws_secret_access_key   = "**********"

service_name            = "lcl14"
environment             = "prd"
personalinformation     = "no"
owner                   = "lcl14"
function_name           = "lcl14_function_01"

# dynamodb
dynamodb_table_name     = "dydb_system_check_argos"
s3_bucket_name          = "s3-bucket-argos" 
s3_url                  = "https://s3-bucket-argos.s3.ap-northeast-2.amazonaws.com/"
s3_aws_logo_url         = "https://s3-bucket-argos.s3.ap-northeast-2.amazonaws.com/icon/aws.png"
s3_title_icon_url       = "https://s3-bucket-argos.s3.ap-northeast-2.amazonaws.com/icon/check-detail.png"

# slack
slack_secret_manager_name = "secret_manager_slack_argos"
# slack_webhook_webhook = "https://hooks.slack.com/services/**********"
slack_incoming_webhook  = "https://hooks.slack.com/services/**********"
slack_channel           = "# lcl14"


# datadog
dd_secret_manager_name  = "secret_manager_datadog_argos"
dd_api_key              = "**********"
dd_app_key              = "**********"
dd_public_id            = "**********"
