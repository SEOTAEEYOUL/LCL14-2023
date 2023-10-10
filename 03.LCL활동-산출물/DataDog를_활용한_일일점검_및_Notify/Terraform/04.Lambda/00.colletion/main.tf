data "aws_caller_identity" "current" {}

locals {
    s3_bucket_name = var.s3_bucket_name
    function_name  = var.function_name
    aws_region     = var.aws_region
    aws_profile    = var.aws_profile
}