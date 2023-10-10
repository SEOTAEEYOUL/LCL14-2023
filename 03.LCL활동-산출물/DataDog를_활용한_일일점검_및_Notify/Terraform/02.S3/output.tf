output "s3_bucket_name" {
    value = aws_s3_bucket.s3_bucket.bucket
}

output "uploaded_objects" {
    value = [
        for key, obj in aws_s3_object.file_objects :
        {
            key      = obj.key
            location = format("%s/%s", obj.bucket, obj.key)
        }
    ]
}

