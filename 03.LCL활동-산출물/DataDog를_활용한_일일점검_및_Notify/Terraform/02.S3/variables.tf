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


variable "s3_name" {
    type = string
}

variable "s3_bucket_name" {
    type = string
}

variable "file_paths" {
    type    = list(string)
    default = [ "template/index.html", "template/system_check.html" ]
}