
data "aws_iam_policy_document" "lambda_assume_role_policy"{
    statement {
        effect  = "Allow"
        actions = ["sts:AssumeRole"]
        principals {
            type        = "Service"
            identifiers = ["lambda.amazonaws.com"]
        }
    }
}

resource "aws_iam_role" "lambda" {
    name = "iam_${var.function_name}"
    #   name = "lambda-lambdaRole-waf"
    assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}


resource "aws_iam_policy" "lambda" {
    name = "policy_${var.function_name}"
    policy = templatefile("policy.json.tftpl", {
        aws_account_id = data.aws_caller_identity.current.account_id
        aws_region     = var.aws_region,
        function_name  = var.function_name
    })
}

resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
    role = aws_iam_role.lambda.name
    policy_arn = aws_iam_policy.lambda.arn
}

data "aws_iam_policy_document" "secretsmanager_policy" {
  statement {
    actions   = ["secretsmanager:ListSecrets"]
    resources = ["*"]
  }
}