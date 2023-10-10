# -----------------------------------------------------------------------------
provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
  
  default_tags {
    tags = {
      ServiceName         = var.service_name
      Environment         = var.environment
      Personalinformation = var.personalinformation
      owner               = var.owner
    }
  }
}
# -----------------------------------------------------------------------------