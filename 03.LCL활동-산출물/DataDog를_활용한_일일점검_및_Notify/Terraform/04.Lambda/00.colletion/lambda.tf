# resource "aws_lambda_function" "lambda" {
#   function_name = var.function_name
#   filename      = "lambda.zip"
#   handler       = "handler"
#   role          = aws_iam_role.lambda.arn

#   source_code_hash = filebase64sha256("lambda.zip")
#   runtime = "go1.x"

#   environment {
#     variables = {
#       foo = "bar"
#     }
#   }
# }

/* 
 * Arquive the script
 */
data "archive_file" "python_lambda_package" {  
    type = "zip"  
    source_file = "${path.module}/code/lambda_function.py" 
    # source_dir  = "${path.module}/code" 
    output_path = "${path.module}/artifacts/lambda.zip"
}

/*
 *  Create the lamda function
 */
resource "aws_lambda_function" "lambda_function" {
    function_name    = var.function_name
    # filename         = "lambda.zip"
    filename         = data.archive_file.python_lambda_package.output_path
    source_code_hash = data.archive_file.python_lambda_package.output_base64sha256
    role             = aws_iam_role.lambda.arn
    runtime          = "python3.9"
    handler          = "lambda_function.lambda_handler"
    # timeout          = 10
    timeout          = 900

    # Store Lambda function ARN in a local value
    environment {
        variables = {
            # SLACK_WEBHOOK_URL       = var.slack_webhook_url
            # SLACK_CHANNEL           = var.slack_channel
            DYDB_SYSTEM_CHECK_NAME  = var.dydb_system_check_name
            DYDB_ALERT_LIST_NAME    = var.dydb_alert_list_name
            S3_BUCKET_NAME          = var.s3_bucket_name
            S3_COLLECTION_TEMPLATE  = var.s3_collection_template
            S3_URL                  = var.s3_url
            S3_AWS_LOGO_URL         = var.s3_aws_logo_url
            S3_TITLE_ICON_URL       = var.s3_title_icon_url
        }
    }
}