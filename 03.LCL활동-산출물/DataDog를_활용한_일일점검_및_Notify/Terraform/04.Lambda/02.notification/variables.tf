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


variable "function_name" {
    type = string
    description = "The name of function"
}

variable "slack_webhook_url" {
    type = string
}

variable "slack_channel" {
    type = string
}

variable "dydb_system_check_name" {
    type = string
}

variable "dydb_alert_list_name" {
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