variable "stages" {
  type    = list(string)
  # default = ["vpc", "iam", "secgrp", "ecr", "eks", "elb", "storage", "cloudfront", "wafv2", "rds", "ec2"]
  # default = ["dev", "stg", "prd"]
  default = ["lcl14"]
}