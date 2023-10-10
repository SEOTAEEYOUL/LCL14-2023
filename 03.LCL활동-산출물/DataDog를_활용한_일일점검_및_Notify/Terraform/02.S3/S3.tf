# -----------------------------------------------------------------------------
# s3를 생성
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# tarraform backend status 관리를 위한 s3 bucket & dynamodb table 생성
# -----------------------------------------------------------------------------
# # s3 생성
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "s3-bucket-${var.s3_name}"
  # acl    = "private"
  
  object_lock_enabled = true
  tags = {
    Name ="s3-bucket-${var.s3_name}"
  }
}


resource "aws_s3_bucket_cors_configuration" "cors_configuration" {
    bucket = aws_s3_bucket.s3_bucket.id  

    cors_rule {
        allowed_headers = ["*"]
        allowed_methods = ["GET", "HEAD"]
        allowed_origins = ["*"]
        expose_headers  = ["ETag"]
        max_age_seconds = 3000
    }  
}

# 2023.06.22 - AWS 정책 변경으로 depens_on 추가
resource "aws_s3_bucket_acl" "s3_bucket_acl" {
    bucket     = aws_s3_bucket.s3_bucket.id
    acl        = "private"
    # acl        = "public-read"

    depends_on = [aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership]
}

# Resource to avoid error "AccessControlListNotSupported: The bucket does not allow ACLs"
# S3 Bucket Ownership Controls
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_ownership_controls
resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
    bucket = aws_s3_bucket.s3_bucket.id
    rule {
        object_ownership         = "BucketOwnerPreferred"
    }

    depends_on = [aws_s3_bucket_public_access_block.s3_bucket_public_access]
}

# Enable versioning for the S3 bucket
resource aws_s3_bucket_versioning s3_ver {
	bucket = aws_s3_bucket.s3_bucket.bucket

    versioning_configuration {
        status = "Enabled"
        # mfa_delete = "Enabled"
    }
}

# 속성 중 암호화 설정
# Enable server-side encryption for the S3 bucket
resource aws_s3_bucket_server_side_encryption_configuration s3_enc {
	bucket = aws_s3_bucket.s3_bucket.bucket
    rule {
        apply_server_side_encryption_by_default {
            sse_algorithm = "AES256"
        }
    }
}


# Allow public access to objects in the S3 bucket
resource "aws_s3_bucket_public_access_block" "s3_bucket_public_access" {
    bucket = aws_s3_bucket.s3_bucket.bucket

    block_public_acls       = false
    block_public_policy     = false
    ignore_public_acls      = false
    restrict_public_buckets = false
}




# 정책 설정
resource "aws_s3_bucket_policy" "s3-bucket-policy" {
    bucket = aws_s3_bucket.s3_bucket.id
    policy = data.aws_iam_policy_document.s3-bucket-policy-document.json

    depends_on = [aws_s3_bucket_public_access_block.s3_bucket_public_access]
}

# 정책 내용 설정
data "aws_iam_policy_document" "s3-bucket-policy-document" {
    statement  {  
        sid = "S3PolicyStmt-LCL14-AccessLogging"
        actions = [
            "s3:PutObject"                
        ]
        effect  = "Allow"
        resources = [
            "arn:aws:s3:::s3-bucket-${var.s3_name}/*"
        ]
        principals {
            type = "Service"
            identifiers  = ["logging.s3.amazonaws.com"]
        }
    }

    statement  { 
        sid = "S3PolicyStmt-LCL14-PublicAccess"
        actions = [                
            "s3:*"
        ]
        effect   = "Allow"
        resources = [
            "arn:aws:s3:::s3-bucket-${var.s3_name}",
            "arn:aws:s3:::s3-bucket-${var.s3_name}/*"
        ]
        principals {
            type        = "AWS"
            identifiers = ["*"]
        }
    }
}

# 수명 주기 설정
resource "aws_s3_bucket_lifecycle_configuration" "lifecycle_configuration" {
    bucket = aws_s3_bucket.s3_bucket.id

    rule {
        id = "log"

        expiration {
            days = 90
        }

        filter {
            and {
                prefix = "log/"

                tags = {
                    rule      = "log"
                    autoclean = "true"
                }
            }
        }

        status = "Enabled"

        transition {
            days          = 30
            storage_class = "STANDARD_IA"
        }

        transition {
            days          = 60
            storage_class = "GLACIER"
        }
    }

    rule {
        id = "tmp"

        filter {
            prefix = "tmp/"
        }

        expiration {
            date = "2023-01-13T00:00:00Z"
        }

        status = "Enabled"
    }
}

# 파일 업로드
# resource "aws_s3_object" "object" {
#     for_each        = fileset("uploads/", "*.html")
#     bucket          = aws_s3_bucket.s3_bucket.id
#     key             = each.value
#     source          = "uploads/${each.value}"
#     content_type    = "text/html"
#     etag            = filemd5("uploads/${each.value}")
#     acl             = "public-read"
# # }

resource "aws_s3_object" "file_objects" {
    for_each        = toset(var.file_paths)

    bucket          = aws_s3_bucket.s3_bucket.id
    # key             = basename(each.value)
    key             = each.value
    source          = each.value
    content_type    = "text/html"
    etag            = filemd5(each.value)
    # acl             = "public-read"
    acl             = "private"

    depends_on = [aws_s3_bucket_policy.s3-bucket-policy]
}

locals {
    # icon_files = fileset("icon", "**/*.png")  # icon 폴더 내의 모든 PNG 이미지 파일을 가져옵니다. 다른 이미지 확장자가 있다면 *.확장자 형태로 변경하면 됩니다.
    icon_files = fileset("icon", "**/*.*") 
}

resource "aws_s3_object" "icon_objects" {
    for_each = toset(local.icon_files)

    bucket   = aws_s3_bucket.s3_bucket.bucket
    key      = "icon/${each.value}"
    source   = "icon/${each.value}"
    etag     = filemd5("icon/${each.value}")
    acl      = "private"
}
# -----------------------------------------------------------------------------