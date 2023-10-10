# -----------------------------------------------------------------------------
terraform {
  required_version = ">= 1.1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.50.0"
    }
  }
}

provider "aws" {
  # alias      = "shared"
  # The security credentials for AWS Account A.
  # access_key = "**********"
  # secret_key = "**********+**********"
  region                  = "ap-northeast-2"
  # profile                 = "AdminRoleNetwork"
  # profile                 = "skcc_aa05"
  profile                 = "lcl14"
  # profile                 = "terraform_stg"
  # shared_credentials_files = ["C:\\Users\\Administrator\\.aws\\credentials"]
  # shared_credentials_files = ["~/.aws/credentials"]
  # shared_credentials_files = ["$HOME/.aws/credentials"]
  # shared_config_files      = ["$HOME/.aws/config"]


  
  # assume_role {
    # The role ARN within Account B to AssumeRole into. Created in step 1.
    # role_arn     = "arn:aws:iam::123456789012:role/AssumableAdminRole"
    # session_name = "terraform-session-shared"
  
    # (Optional) The external ID created in step 1c.
    # external_id = "skcc_aa05"
  # }

  default_tags {
    tags = {
      ServiceName         = "LCL14"
      Environment         = "dev"
      Personalinformation = "yes"
    }
  }
}

# provider "aws" {
#  alias                   = "shared"
#  region                  = "ap-northeast-2"
  # shared_credentials_file = "~/.aws/credentials"
  # profile                 = "default"
  # assume_role {
    # The role ARN within Account B to AssumeRole into. Created in step 1.
    # role_arn     = "arn:aws:iam::123456789012:role/AssumableAdminRole"
    # session_name = "terraform-session-shared"
    # (Optional) The external ID created in step 1c.
  # }
# }
# -----------------------------------------------------------------------------
