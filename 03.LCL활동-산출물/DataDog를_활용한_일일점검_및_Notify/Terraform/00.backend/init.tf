# -----------------------------------------------------------------------------
# tarraform backend status 관리를 위한 s3 bucket & dynamodb table 생성
# -----------------------------------------------------------------------------
# S3 bucket for backend
resource "aws_s3_bucket" "tfstate" {
  bucket = "s3-terraform-argos"
  # acl    = "private"
  
  object_lock_enabled = true
  tags = {
    Name = "S3 Remote Terraform State Store"
  }
}

# 2023.06.22 - AWS 정책 변경으로 depens_on 추가
resource "aws_s3_bucket_acl" "tfstate_bucket_acl" {
  bucket     = aws_s3_bucket.tfstate.id
  acl        = "private"
  depends_on = [aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership]
}

# Resource to avoid error "AccessControlListNotSupported: The bucket does not allow ACLs"
# S3 Bucket Ownership Controls
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_ownership_controls
resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
  bucket = aws_s3_bucket.tfstate.id
  rule {
    object_ownership         = "BucketOwnerPreferred"
  }
}

resource aws_s3_bucket_versioning s3_ver {
	bucket = aws_s3_bucket.tfstate.bucket

  versioning_configuration {
    status = "Enabled"
    # mfa_delete = "Enabled"
  }
}

resource aws_s3_bucket_server_side_encryption_configuration s3_enc {
	bucket = aws_s3_bucket.tfstate.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# DynamoDB for terraform state lock
# resource "aws_dynamodb_table" "terraform_state_lock" {
#   count           = length(var.stages)
#   name            = format("dydb_%s_terraform", var.stages[count.index])
#   hash_key        = "LockID"
#   billing_mode    = "PAY_PER_REQUEST"
#   attribute {
#     name = "LockID"
#     type = "S"
#   }
#   tags = {
#     "Name" = "DynamoDB Terraform State Lock Table"
#   }
# }

# DynamoDB for terraform state lock
resource "aws_dynamodb_table" "terraform_state_lock" {
  # name            = "terraform_state_lock"
  name            = "dydb-terraform-argos"
  hash_key        = "LockID"
  billing_mode    = "PAY_PER_REQUEST"
  attribute {
    name = "LockID"
    type = "S"
  }
  tags = {
    "Name" = "DynamoDB Terraform State Lock Table"
  }
}
# -----------------------------------------------------------------------------