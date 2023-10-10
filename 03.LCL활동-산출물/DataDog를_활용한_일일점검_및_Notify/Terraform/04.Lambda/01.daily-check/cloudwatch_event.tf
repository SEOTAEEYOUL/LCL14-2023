resource "aws_cloudwatch_event_rule" "cloudwatch-event-rule-lambda" {
    name                  = "cloudwatch-event-rule-09-${var.function_name}"
    description           = "Schedule lambda function"
    # cron(분 시 일 월 요일) 
    # schedule_expression   = "cron(0 0 * * ? *)" # 9:00 AM in Asia/Seoul
    schedule_expression   = "cron(0 0,11 * * ? *)" # 9:00 AA, 8:00 PM in Asia/Seoul
    # schedule_expression   = "rate(5 minutes)" # rate(60 minutes) cron(0 20 * * ? *)
}

resource "aws_cloudwatch_event_target" "lambda-function-target" {
    target_id             = "cloudwatch-event-target-${var.function_name}"
    rule                  = aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda.name
    arn                   = aws_lambda_function.lambda_function.arn

    input_transformer {
        input_template = jsonencode({
            # lambda_url = aws_lambda_function.lambda_function.function_name
            lambda_url = aws_lambda_function_url.lambda_function_url.function_url
        })
    }

    depends_on = [aws_lambda_function_url.lambda_function_url]
}

resource "aws_lambda_permission" "allow_cloudwatch" {
    statement_id        = "AllowExecutionFromCloudWatch"
    action              = "lambda:InvokeFunction"
    function_name       = aws_lambda_function.lambda_function.function_name
    principal           = "events.amazonaws.com"
    source_arn          = aws_cloudwatch_event_rule.cloudwatch-event-rule-lambda.arn
}