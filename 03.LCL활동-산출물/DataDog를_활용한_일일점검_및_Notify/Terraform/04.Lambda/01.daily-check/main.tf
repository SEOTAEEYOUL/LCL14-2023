data "aws_caller_identity" "current" {}

locals {
    account_id = data.aws_caller_identity.current.account_id
    aws_reginn = var.aws_region
}