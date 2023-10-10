# backend

Terraform 수행시 상태 저장을 위한 S3 와 lock table 인 DynamoDB 를 생성함

1. lcl14 구성 생성 - aws configure --profile lcl14
2. aws configure list-profiles
3. token 를 얻어옴 - aws sts get-caller-identity
4. terraform init
5. terraform plan
6. terraform apply

## AWS S3 ACL 정책 변경으로 인한 오류 - 2023.04 변경분 반영
- Resource to avoid error "AccessControlListNotSupported: The bucket does not allow ACLs"  
- S3 Bucket Ownership Controls  
- [Resource: aws_s3_bucket_ownership_controls](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_ownership_controls)  
> [Error AccessControlListNotSupported when trying to create a bucket ACL in AWS](https://stackoverflow.com/questions/76049290/error-accesscontrollistnotsupported-when-trying-to-create-a-bucket-acl-in-aws)

## 사전 작업
### aws configure list
```
PS > aws configure list
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************C47Y shared-credentials-file
secret_key     ****************jNsK shared-credentials-file
    region           ap-northeast-2      config-file    ~/.aws/config
PS > 
```

### aws configure, aws configure --profile lcl14 설정

#### ~/.aws/config
```
[default]
region = ap-northeast-2
output = json
[profile lcl14]
region = ap-northeast-2
output = json
```

#### ~/.aws/credentias
```
[default]
aws_access_key_id = **********
aws_secret_access_key = **********+QljNsK
[lcl14]
aws_access_key_id = **********
aws_secret_access_key = **********/cUs8AWm7
```

#### aws configure list-profiles
```
PS > aws configure list-profiles
default
skcc_aa05
ca07456
argos_iam
argos_network
argos_dev
argos_stg
argos_prd
argos
AdminRolePrd
AdminRoleStg
AdminRoleDev
AdminRoleNetwork
terraform_prd
terraform_stg
terraform_network
manguard
ca074562
is07456
lcl14
PS > 
```

#### 구성 지정
- $Env:AWS_PROFILE="lcl14", export AWS_PROFILE="lcl14"
- aws sts get-caller-identity
```
PS > $Env:AWS_PROFILE="lcl14"  
PS > aws sts get-caller-identity
{
    "UserId": "**********",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/is07456"
}

PS > 
```

## terraform 
### init
```powershell
PS > terraform init

Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/aws versions matching ">= 3.50.0"...
- Installing hashicorp/aws v5.4.0...
- Installed hashicorp/aws v5.4.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider  
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when   
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see 
any changes that are required for your infrastructure. All Terraform commands 
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
PS > 
```

### plan
```
PS > terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions 
are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_dynamodb_table.terraform_state_lock will be created
  + resource "aws_dynamodb_table" "terraform_state_lock" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "dydb-terraform-lcl14"
      + read_capacity    = (known after apply)
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)
      + tags             = {
          + "Name" = "DynamoDB Terraform State Lock Table"
        }
      + tags_all         = {
          + "Environment"         = "prd"
          + "Name"                = "DynamoDB Terraform State Lock Table"
          + "Personalinformation" = "yes"
          + "ServiceName"         = "LCL14"
        }
      + write_capacity   = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }
    }

  # aws_s3_bucket.tfstate will be created
  + resource "aws_s3_bucket" "tfstate" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "s3-terraform-lcl14"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = true
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "Name" = "S3 Remote Terraform State Store"
        }
      + tags_all                    = {
          + "Environment"         = "prd"
          + "Name"                = "S3 Remote Terraform State Store"
          + "Personalinformation" = "yes"
          + "ServiceName"         = "LCL14"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)
    }

  # aws_s3_bucket_acl.tfstate_bucket_acl will be created
  + resource "aws_s3_bucket_acl" "tfstate_bucket_acl" {
      + acl    = "private"
      + bucket = (known after apply)
      + id     = (known after apply)
    }

  # aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership will be created
  + resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
      + bucket = (known after apply)
      + id     = (known after apply)

      + rule {
          + object_ownership = "BucketOwnerPreferred"
        }
    }

  # aws_s3_bucket_server_side_encryption_configuration.s3_enc will be created
  + resource "aws_s3_bucket_server_side_encryption_configuration" "s3_enc" {
      + bucket = "s3-terraform-lcl14"
      + id     = (known after apply)

      + rule {
          + apply_server_side_encryption_by_default {
              + sse_algorithm = "AES256"
            }
        }
    }

  # aws_s3_bucket_versioning.s3_ver will be created
  + resource "aws_s3_bucket_versioning" "s3_ver" {
      + bucket = "s3-terraform-lcl14"
      + id     = (known after apply)

      + versioning_configuration {
          + mfa_delete = (known after apply)
          + status     = "Enabled"
        }
    }

Plan: 6 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + dynamodb_table = {
      + attribute                   = [
          + {
              + name = "LockID"
              + type = "S"
            },
        ]
      + billing_mode                = "PAY_PER_REQUEST"
      + deletion_protection_enabled = null
      + global_secondary_index      = []
      + hash_key                    = "LockID"
      + local_secondary_index       = []
      + name                        = "dydb-terraform-lcl14"
      + range_key                   = null
      + replica                     = []
      + restore_date_time           = null
      + restore_source_name         = null
      + restore_to_latest_time      = null
      + stream_enabled              = null
      + table_class                 = null
      + tags                        = {
          + Name = "DynamoDB Terraform State Lock Table"
        }
      + tags_all                    = {
          + Environment         = "prd"
          + Name                = "DynamoDB Terraform State Lock Table"
          + Personalinformation = "yes"
          + ServiceName         = "LCL14"
        }
      + timeouts                    = null
    }
  + s3_bucket_arn  = (known after apply)
  + s3_bucket_name = "s3-terraform-lcl14"

──────────────────────────────────────────────────────────────────────────────────────────────── 

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take     
exactly these actions if you run "terraform apply" now.
PS >
```

### apply
```
PS > terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions 
are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_dynamodb_table.terraform_state_lock will be created
  + resource "aws_dynamodb_table" "terraform_state_lock" {
      + arn              = (known after apply)
      + billing_mode     = "PAY_PER_REQUEST"
      + hash_key         = "LockID"
      + id               = (known after apply)
      + name             = "dydb-terraform-lcl14"
      + read_capacity    = (known after apply)
      + stream_arn       = (known after apply)
      + stream_label     = (known after apply)
      + stream_view_type = (known after apply)
      + tags             = {
          + "Name" = "DynamoDB Terraform State Lock Table"
        }
      + tags_all         = {
          + "Environment"         = "prd"
          + "Name"                = "DynamoDB Terraform State Lock Table"
          + "Personalinformation" = "yes"
          + "ServiceName"         = "LCL14"
        }
      + write_capacity   = (known after apply)

      + attribute {
          + name = "LockID"
          + type = "S"
        }
    }

  # aws_s3_bucket.tfstate will be created
  + resource "aws_s3_bucket" "tfstate" {
      + acceleration_status         = (known after apply)
      + acl                         = (known after apply)
      + arn                         = (known after apply)
      + bucket                      = "s3-terraform-lcl14"
      + bucket_domain_name          = (known after apply)
      + bucket_prefix               = (known after apply)
      + bucket_regional_domain_name = (known after apply)
      + force_destroy               = false
      + hosted_zone_id              = (known after apply)
      + id                          = (known after apply)
      + object_lock_enabled         = true
      + policy                      = (known after apply)
      + region                      = (known after apply)
      + request_payer               = (known after apply)
      + tags                        = {
          + "Name" = "S3 Remote Terraform State Store"
        }
      + tags_all                    = {
          + "Environment"         = "prd"
          + "Name"                = "S3 Remote Terraform State Store"
          + "Personalinformation" = "yes"
          + "ServiceName"         = "LCL14"
        }
      + website_domain              = (known after apply)
      + website_endpoint            = (known after apply)
    }

  # aws_s3_bucket_acl.tfstate_bucket_acl will be created
  + resource "aws_s3_bucket_acl" "tfstate_bucket_acl" {
      + acl    = "private"
      + bucket = (known after apply)
      + id     = (known after apply)
    }

  # aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership will be created
  + resource "aws_s3_bucket_ownership_controls" "s3_bucket_acl_ownership" {
      + bucket = (known after apply)
      + id     = (known after apply)

      + rule {
          + object_ownership = "BucketOwnerPreferred"
        }
    }

  # aws_s3_bucket_server_side_encryption_configuration.s3_enc will be created
  + resource "aws_s3_bucket_server_side_encryption_configuration" "s3_enc" {
      + bucket = "s3-terraform-lcl14"
      + id     = (known after apply)

      + rule {
          + apply_server_side_encryption_by_default {
              + sse_algorithm = "AES256"
            }
        }
    }

  # aws_s3_bucket_versioning.s3_ver will be created
  + resource "aws_s3_bucket_versioning" "s3_ver" {
      + bucket = "s3-terraform-lcl14"
      + id     = (known after apply)

      + versioning_configuration {
          + mfa_delete = (known after apply)
          + status     = "Enabled"
        }
    }

Plan: 6 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + dynamodb_table = {
      + attribute                   = [
          + {
              + name = "LockID"
              + type = "S"
            },
        ]
      + billing_mode                = "PAY_PER_REQUEST"
      + deletion_protection_enabled = null
      + global_secondary_index      = []
      + hash_key                    = "LockID"
      + local_secondary_index       = []
      + name                        = "dydb-terraform-lcl14"
      + range_key                   = null
      + replica                     = []
      + restore_date_time           = null
      + restore_source_name         = null
      + restore_to_latest_time      = null
      + stream_enabled              = null
      + table_class                 = null
      + tags                        = {
          + Name = "DynamoDB Terraform State Lock Table"
        }
      + tags_all                    = {
          + Environment         = "prd"
          + Name                = "DynamoDB Terraform State Lock Table"
          + Personalinformation = "yes"
          + ServiceName         = "LCL14"
        }
      + timeouts                    = null
    }
  + s3_bucket_arn  = (known after apply)
  + s3_bucket_name = "s3-terraform-lcl14"

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_dynamodb_table.terraform_state_lock: Creating...
aws_s3_bucket.tfstate: Creating...
aws_s3_bucket.tfstate: Creation complete after 2s [id=s3-terraform-lcl14]
aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership: Creating...
aws_s3_bucket_versioning.s3_ver: Creating...
aws_s3_bucket_server_side_encryption_configuration.s3_enc: Creating...
aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership: Creation complete after 0s [id=s3-terraform-lcl14]
aws_s3_bucket_acl.tfstate_bucket_acl: Creating...
aws_s3_bucket_server_side_encryption_configuration.s3_enc: Creation complete after 0s [id=s3-terraform-lcl14]
aws_s3_bucket_acl.tfstate_bucket_acl: Creation complete after 1s [id=s3-terraform-lcl14,private]
aws_s3_bucket_versioning.s3_ver: Creation complete after 1s [id=s3-terraform-lcl14]
aws_dynamodb_table.terraform_state_lock: Creation complete after 6s [id=dydb-terraform-lcl14]

Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

Outputs:

dynamodb_table = {
  "arn" = "arn:aws:dynamodb:ap-northeast-2:123456789012:table/dydb-terraform-lcl14"
  "attribute" = toset([
    {
      "name" = "LockID"
      "type" = "S"
    },
  ])
  "billing_mode" = "PAY_PER_REQUEST"
  "deletion_protection_enabled" = false
  "global_secondary_index" = toset([])
  "hash_key" = "LockID"
  "id" = "dydb-terraform-lcl14"
  "local_secondary_index" = toset([])
  "name" = "dydb-terraform-lcl14"
  "point_in_time_recovery" = tolist([
    {
      "enabled" = false
    },
  ])
  "range_key" = tostring(null)
  "read_capacity" = 0
  "replica" = toset([])
  "restore_date_time" = tostring(null)
  "restore_source_name" = tostring(null)
  "restore_to_latest_time" = tobool(null)
  "server_side_encryption" = tolist([])
  "stream_arn" = ""
  "stream_enabled" = false
  "stream_label" = ""
  "stream_view_type" = ""
  "table_class" = "STANDARD"
  "tags" = tomap({
    "Name" = "DynamoDB Terraform State Lock Table"
  })
  "tags_all" = tomap({
    "Environment" = "prd"
    "Name" = "DynamoDB Terraform State Lock Table"
    "Personalinformation" = "yes"
    "ServiceName" = "LCL14"
  })
  "timeouts" = null /* object */
  "ttl" = tolist([
    {
      "attribute_name" = ""
      "enabled" = false
    },
  ])
  "write_capacity" = 0
}
s3_bucket_arn = "arn:aws:s3:::s3-terraform-lcl14"
s3_bucket_name = "s3-terraform-lcl14"
PS > 
```

#### terraform state list
```
PS > terraform state list
aws_dynamodb_table.terraform_state_lock
aws_s3_bucket.tfstate
aws_s3_bucket_acl.tfstate_bucket_acl
aws_s3_bucket_ownership_controls.s3_bucket_acl_ownership
aws_s3_bucket_server_side_encryption_configuration.s3_enc
aws_s3_bucket_versioning.s3_ver
PS > 
```


#### terraform output
```
PS > terraform output
dynamodb_table = {
  "arn" = "arn:aws:dynamodb:ap-northeast-2:123456789012:table/dydb-terraform-lcl14"
  "attribute" = toset([
    {
      "name" = "LockID"
      "type" = "S"
    },
  ])
  "billing_mode" = "PAY_PER_REQUEST"
  "deletion_protection_enabled" = false
  "global_secondary_index" = toset([])
  "hash_key" = "LockID"
  "id" = "dydb-terraform-lcl14"
  "local_secondary_index" = toset([])
  "name" = "dydb-terraform-lcl14"
  "point_in_time_recovery" = tolist([
    {
      "enabled" = false
    },
  ])
  "range_key" = tostring(null)
  "read_capacity" = 0
  "replica" = toset([])
  "restore_date_time" = tostring(null)
  "restore_source_name" = tostring(null)
  "restore_to_latest_time" = tobool(null)
  "server_side_encryption" = tolist([])
  "stream_arn" = ""
  "stream_enabled" = false
  "stream_label" = ""
  "stream_view_type" = ""
  "table_class" = "STANDARD"
  "tags" = tomap({
    "Name" = "DynamoDB Terraform State Lock Table"
  })
  "tags_all" = tomap({
    "Environment" = "prd"
    "Name" = "DynamoDB Terraform State Lock Table"
    "Personalinformation" = "yes"
    "ServiceName" = "LCL14"
  })
  "timeouts" = null /* object */
  "ttl" = tolist([
    {
      "attribute_name" = ""
      "enabled" = false
    },
  ])
  "write_capacity" = 0
}
s3_bucket_arn = "arn:aws:s3:::s3-terraform-lcl14"
s3_bucket_name = "s3-terraform-lcl14"
PS > 
```
