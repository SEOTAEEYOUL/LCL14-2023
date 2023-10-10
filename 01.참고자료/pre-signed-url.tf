provider "aws" {
  region = "ap-northeast-2"
}

data "aws_s3_bucket_object" "system_check" {
  bucket = "s3-bucket-lcl14"
  key    = "system_check.html"
}

resource "aws_s3_bucket_object_presigned_url" "presigned_url" {
  bucket       = data.aws_s3_bucket_object.system_check.bucket
  key          = data.aws_s3_bucket_object.system_check.key
  expires      = "1800"
  allowed_methods = ["GET"]
}