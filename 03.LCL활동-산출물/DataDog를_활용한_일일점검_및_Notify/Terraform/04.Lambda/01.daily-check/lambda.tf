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
data "archive_file" "lambda-archive" {  
    type = "zip"  
    # source_file = "${path.module}/code/lambda_function.py" 
    source_dir  = "${path.module}/code" 
    output_path = "${path.module}/artifacts/lambda.zip"
}

/*
 *  Create the lamda function
 */
resource "aws_lambda_function" "lambda_function" {
    function_name    = var.function_name
    # filename         = "lambda.zip"
    filename         = data.archive_file.lambda-archive.output_path
    source_code_hash = data.archive_file.lambda-archive.output_base64sha256
    role             = aws_iam_role.lambda.arn
    runtime          = "python3.9"
    handler          = "lambda_function.lambda_handler"
    # timeout          = 15
    timeout          = 300
    memory_size      = 128

    # Store Lambda function ARN in a local value
    environment {
        variables = {
            REGION                 = var.aws_region
            # SLACK_WEBHOOK_URL    = var.slack_incoming_webhook
            # SLACK_CHANNEL        = var.slack_channel
            # AWS_SECRET_NAME      = var.aws_secret_manager_name
            DD_SECRET_NAME         = var.dd_secret_manager_name
            SLACK_SECRET_NAME      = var.slack_secret_manager_name
            DYNAMODB_TABLE_NAME    = var.dynamodb_table_name
            S3_BUCKET_NAME         = var.s3_bucket_name
            S3_URL                 = var.s3_url
            S3_AWS_LOGO_URL        = var.s3_aws_logo_url
            S3_TITLE_ICON_URL      = var.s3_title_icon_url
        }
    }


    # Lambda 함수에 필요한 패키지를 포함시킬 Layer를 생성합니다.
    # 이때 requests 패키지를 사용하는 경우, 해당 패키지와 의존성을 포함시켜야 합니다.
    # Layer를 생성하기 위해 requests 패키지를 설치한 디렉토리에서 아래 명령을 실행해주세요.
    #
    # pip install -t layer requests python-dotenv datadog datadog_api_client
    #
    # 그리고 아래 디렉토리와 파일 구조를 가지도록 zip 파일을 생성합니다.
    # - requests-layer/
    #   - requests/
    #     - ...
    #   - requests-2.26.0.dist-info/
    #
    # 이렇게 생성한 requests-layer.zip 파일을 함께 업로드해야 합니다.
    # account_id = data.aws_caller_identity.current.account_id
    layers = [
            aws_lambda_layer_version.layer.arn            
        ]
}


resource "null_resource" "pip_install" {
    triggers = {
        shell_hash = "${sha256(file("${path.module}/requirements.txt"))}"
        # always_run = "${timestamp()}"
        # file_changed = md5("${path.module}/requirements.txt")
    }

    provisioner "local-exec" {
        interpreter = ["PowerShell", "-Command"]
        command = "python -m pip install -r requirements.txt -t ${path.module}/layer/python"
    }
}

data "archive_file" "layer" {  
    type = "zip"  
    # source_file = "${path.module}/code/lambda_function.py" 
    source_dir  = "${path.module}/layer" 
    output_path = "${path.module}/artifacts/layer.zip"
    
    depends_on  = [null_resource.pip_install]
}

resource "aws_lambda_layer_version" "layer" {
    layer_name          = "${var.function_name}_layer"

    # requests 패키지를 포함시킬 디렉토리를 지정합니다.
    # 아래 예시에서는 requests-layer 디렉토리에 패키지를 설치한 경우를 가정합니다.
    # 디렉토리와 파일 구조는 위에서 설명한 것과 동일해야 합니다.
    filename         = data.archive_file.layer.output_path
    source_code_hash = data.archive_file.layer.output_base64sha256
    compatible_runtimes = [ "python3.9", "python3.8", "python3.7", "python3.6" ]
}


# resource "datadog_integration_aws_lambda_arn" "main_collector" {
#     account_id = data.aws_caller_identity.current.account_id
#     lambda_arn = "arn:aws:lambda:ap-northeast-2:${account_id}:function:datadog-forwarder-Forwarder"
# }