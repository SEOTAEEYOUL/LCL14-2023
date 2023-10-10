# -----------------------------------------------------------------------------
# vpc id 
output "s3_bucket_name" {
    value = aws_s3_bucket.tfstate.bucket
    description = "The name of the s3 bucket"
}

output "s3_bucket_arn" {
    value = aws_s3_bucket.tfstate.arn
    description = "The ARN of the S3 bucket"
}

#unique private backend subnet list 
output "dynamodb_table" {
    value = aws_dynamodb_table.terraform_state_lock
}
# -----------------------------------------------------------------------------