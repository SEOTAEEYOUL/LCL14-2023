data "aws_caller_identity" "current" {}

data "terraform_remote_state" "collection_labmda" {
  backend = "s3"
  config  = {
    bucket  = "s3-terraform-argos"
    key     = "terraform/lambda/function03/terraform.tfstate"
    region  = "ap-northeast-2"
    encrypt = true
    # lock_table = "dydb_eks_iam_terraform"
    acl     = "bucket-owner-full-control"
    profile = local.aws_profile_name
  }
}

# resource 를 생성하기 위한 변수값을 local 변수로 정의 합니다.
locals {
    aws_account_id   = data.aws_caller_identity.current.account_id
    # aws_profile_name = "lcl14"
    aws_profile_name = var.aws_profile
}