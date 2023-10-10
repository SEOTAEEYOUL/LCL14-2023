# # 시크릿 매니저에서 시크릿을 생성
# resource "aws_secretsmanager_secret" "aws_secret" {
#     name = var.aws_secret_manager_name
# }

# # 시크릿의 값을 정의
# resource "aws_secretsmanager_secret_version" "aws_secret_version" {
#     secret_id     = aws_secretsmanager_secret.aws_secret.id
#     secret_string = jsonencode({
#         aws_access_key        = var.aws_access_key,
#         aws_secret_access_key = var.aws_secret_access_key,
#     })
# }

# ---------------------------------------------------------------
# 시크릿 매니저에서 시크릿을 생성
resource "aws_secretsmanager_secret" "datadog_secret" {
    name = var.dd_secret_manager_name
}

# 시크릿의 값을 정의
resource "aws_secretsmanager_secret_version" "datadog_secret_version" {
    secret_id     = aws_secretsmanager_secret.datadog_secret.id
    secret_string = jsonencode({
        api_key   = var.dd_api_key,
        app_key   = var.dd_app_key,
        public_id = var.dd_public_id
    })
}

# ---------------------------------------------------------------
# 시크릿 매니저에서 시크릿을 생성
resource "aws_secretsmanager_secret" "slack_secret" {
    name = var.slack_secret_manager_name
}

# 시크릿의 값을 정의
resource "aws_secretsmanager_secret_version" "slack_secret_version" {
    secret_id     = aws_secretsmanager_secret.slack_secret.id
    secret_string = jsonencode({
        incoming_webhook = var.slack_incoming_webhook,
        channel          = var.slack_channel
    })
}

