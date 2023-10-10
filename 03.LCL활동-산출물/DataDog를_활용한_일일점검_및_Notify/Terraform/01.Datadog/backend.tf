# -----------------------------------------------------------------------------
terraform {
  required_version = ">= 0.9.5"
  
  required_providers {
    datadog = {
      source = "DataDog/datadog"
    }
  }


  backend "s3" {
    # S3 버킷 이름
    bucket         = "s3-terraform-argos"
    # bucket key 
    key            = "terraform/datadog/terraform.tfstate"
    region         = "ap-northeast-2"
    profile        = "lcl14"

    # 잠금에 사용할 dynamoDB 테이블
    # dynamodb_table = "TerraformStateLock"
    dynamodb_table = "dydb-terraform-argos"
    encrypt        = true
    # acl          = "bucket-owner-full-control"
  }
}
# -----------------------------------------------------------------------------