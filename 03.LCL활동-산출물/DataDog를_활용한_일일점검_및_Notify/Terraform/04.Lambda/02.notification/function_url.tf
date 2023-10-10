resource "aws_lambda_function_url" "lambda_function_url" {
    function_name      = aws_lambda_function.lambda_function.function_name
    authorization_type = "NONE"
}