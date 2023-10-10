variable "aws_profile" {
    description = "AWS Profile"
    type        = string
    # default     = ""
}

variable "aws_region" {
    description = "AWS Region"
    type        = string
    # default     = ""
}

variable "service_name" {
    type        = string
}

variable "environment" {
    type        = string
}

variable "personalinformation" {
    type        = string
}

variable "owner" {
    type        = string
}

variable "dynamodb_table_name" {
    description = "Dynamodb table name (space is not allowed)"
    type = string
}

variable "dynamodb_alert_table_name" {
    description = "Dynamodb table name (space is not allowed)"
    type = string
}
