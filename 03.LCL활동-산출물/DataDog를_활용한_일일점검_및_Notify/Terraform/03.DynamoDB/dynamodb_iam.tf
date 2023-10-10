data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "dynamodb_policy" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem"
    ]
    resources = [
      "arn:aws:dynamodb:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/"
    ]
  }
}

# resource "aws_iam_policy" "lambda" {
#   name = "policy_${var.function_name}"
#   policy = templatefile("policy.json.tftpl", {
#     aws_account_id = data.aws_caller_identity.current.account_id
#     aws_region     = var.aws_region,
#     function_name  = var.function_name
#   })
# }

# resource "aws_iam_role_policy_attachment" "iam_for_lambda" {
#   role = aws_iam_role.lambda.name
#   policy_arn = aws_iam_policy.lambda.arn
# }


resource "aws_iam_policy" "dynamodb_policy" {
  name        = "lambda_dynamodb_policy"
  description = "Allows Lambda to access DynamoDB"
  policy      = data.aws_iam_policy_document.dynamodb_policy.json
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_dynamodb_role_lcl14"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "dynamodb_policy_attachment" {
  policy_arn = aws_iam_policy.dynamodb_policy.arn
  role       = aws_iam_role.lambda_role.name
}



# resource "aws_iam_role" "lambda_role" {
#  name = "iam_for_lambda_lcl14"

#  assume_role_policy = jsonencode({
#    "Version" : "2012-10-17",
#    "Statement" : [
#      {
#        "Effect" : "Allow",
#        "Principal" : {
#          "Service" : "lambda.amazonaws.com"
#        },
#        "Action" : "sts:AssumeRole"
#      }
#    ]
#   })
# }
          


# resource "aws_iam_policy" "dynamodb_policy" {
#   name        = "lambda_dynamodb_policy"
#   description = "Allows Lambda to access DynamoDB"
  
#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": [
#         "dynamodb:GetItem",
#         "dynamodb:PutItem"
#       ],
#       "Resource": "arn:aws:dynamodb:REGION:ACCOUNT_ID:table/TABLE_NAME"
#     }
#   ]
# }
# EOF
# }

# resource "aws_iam_role_policy_attachment" "lambda_policy" {
#    role = aws_iam_role.lambda_role.name
#    policy_arn = "arn:aws:iam::aws:policy/servicerole/AWSLambdaBasicExecutionRole"
# }
          
# resource "aws_iam_role_policy" "dynamodb-lambda-policy" {
#    name = "dynamodb_lambda_policy"
#    role = aws_iam_role.lambda_role.id
#    policy = jsonencode({
#       "Version" : "2012-10-17",
#       "Statement" : [
#         {
#            "Effect" : "Allow",
#            "Action" : ["dynamodb:*"],
#            "Resource" : "${aws_dynamodb_table.dynamodb_table.arn}"
#         }
#       ]
#    })
# }