variable "aws_profile" {
    description = "AWS Profile"
    type        = string
    # default     = ""
}

variable "aws_access_key" {
    description = "AWS Access Key"
    type        = string
    # default     = ""
}

variable "aws_secret_access_key" {
    description = "AWS Secret Access Key"
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


variable "function_name" {
    type = string
    description = "The name of function"
}

variable "slack_incoming_webhook" {
    type = string
}

variable "slack_channel" {
    type = string
}

variable "aws_secret_manager_name" {
    type = string
}

variable "dd_secret_manager_name" {
    type = string
}

variable "slack_secret_manager_name" {
    type = string
}

variable "dd_api_key" {
    type = string
}

variable "dd_app_key" {
    type = string
}

variable "dd_public_id" {
    type = string
}

variable "dynamodb_table_name" {
    type = string
}

variable "s3_bucket_name" {
    type = string  
}

variable "s3_url" {
    type = string  
}

variable "s3_aws_logo_url" {
    type = string  
}

variable "s3_title_icon_url" {
    type = string
}