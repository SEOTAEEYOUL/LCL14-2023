# -----------------------------------------------------------------------------
resource "aws_dynamodb_table" "dynamodb_table" {
    name           = "dydb_${var.dynamodb_table_name}"


    # billing_mode = "PROVISIONED"
    # read_capacity  = 30
    # write_capacity = 30
    billing_mode   = "PAY_PER_REQUEST"

    hash_key       = "check_dtm"  # 파티션 키
    range_key      = "monitor_id"    # 정렬키
    #   read_capacity  = 5              # 테이블 일기 용량, billing_mode 가 "PAY_PER_REQUEST" 일 때 불필요
    #   write_capacity = 5              # 테이블 쓰기 용량, billing_mode 가 "PAY_PER_REQUEST" 일 때 불필요
    
    stream_enabled   = true
    stream_view_type = "NEW_AND_OLD_IMAGES"

    # 점검자원 ID
    # 파티션키
    attribute {
        name = "check_dtm"
        type = "S"   # S(String), N(Number)
    }

    # 점검일시분초
    # 정렬키
    attribute {
        name = "monitor_id"
        type = "S"
    }


    # 점검일시분초
    attribute {
        name = "monitor_priority"
        type = "S"
    }

    attribute {
        name = "monitor_name"
        type = "S"
    }

    # # 점검결과
    # # 'Y' 양호, 'C' 확인 필요, 'N' 불량
    # attribute {
    #     name = "check_result"
    #     type = "S"  
    # }

    # # 상세 결과값
    # attribute {
    #     name = "check_result_detail"
    #     type = "S"
    # }
    
    // 기존 테이블에 TTL 추가하지 않음
    # ttl {
    #     attribute_name = "TimeToExist"
    #     enabled        = false
    # }

    ttl {
        attribute_name = "check_dtm"
        enabled        = true
    }

    global_secondary_index {
        name               = "monitor_priority_monitor_name_index" # index 명
        hash_key           = "monitor_priority"              # index 로 사용할 attribute 명
        range_key          = "monitor_name" 
        write_capacity     = 5 # Billing_mode 가 PROVISIONED 일 경우 설정
        read_capacity      = 5 # Billing_mode 가 PROVISIONED 일 경우 설정
        projection_type    = "INCLUDE"
        non_key_attributes = ["check_result_detail"]
    }

    tags = {
        Name        = "dydb-${var.dynamodb_table_name}"
    }
}
# -----------------------------------------------------------------------------
resource "aws_dynamodb_table" "dynamodb_alert_table" {
    name           = "dydb_${var.dynamodb_alert_table_name}"


    # billing_mode = "PROVISIONED"
    # read_capacity  = 30
    # write_capacity = 30
    billing_mode   = "PAY_PER_REQUEST"

    hash_key       = "day_"     # 파티션 키
    range_key      = "id"       # 정렬키
    #   read_capacity  = 5              # 테이블 일기 용량, billing_mode 가 "PAY_PER_REQUEST" 일 때 불필요
    #   write_capacity = 5              # 테이블 쓰기 용량, billing_mode 가 "PAY_PER_REQUEST" 일 때 불필요
    
    stream_enabled   = true
    stream_view_type = "NEW_AND_OLD_IMAGES"

    # 점검자원 ID
    # 파티션키
    attribute {
        name = "day_"
        type = "S"   # S(String), N(Number)
    }

    # 점검일시분초
    # 정렬키
    attribute {
        name = "id"
        type = "S"
    }

    attribute {
        name = "time"
        type = "S"   # S(String), N(Number)
    }

    # 점검일시분초
    # 정렬키
    attribute {
        name = "alert_id"
        type = "S"
    }

    # ttl {
    #     attribute_name = "check_dtm"
    #     enabled        = true
    # }

    global_secondary_index {
        name               = "time_alert_id_index" # index 명
        hash_key           = "time"                # index 로 사용할 attribute 명
        range_key          = "alert_id" 
        write_capacity     = 5 # Billing_mode 가 PROVISIONED 일 경우 설정
        read_capacity      = 5 # Billing_mode 가 PROVISIONED 일 경우 설정
        projection_type    = "INCLUDE"
        non_key_attributes = ["payload"]
    }

    tags = {
        Name        = "dydb-${var.dynamodb_alert_table_name}"
    }
}
# -----------------------------------------------------------------------------