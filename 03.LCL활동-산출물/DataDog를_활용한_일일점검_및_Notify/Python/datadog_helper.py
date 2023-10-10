import os
import pprint
from dotenv import load_dotenv
from datetime import date, datetime

import datadog
from datadog import api
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.organizations_api import OrganizationsApi



def get_datadog_keys():
    # load .env
    load_dotenv()  
    return os.getenv('API_KEY'), os.getenv('APP_KEY'), os.getenv('PUBLIC_ID')

def get_api_key():
    # load .env
    load_dotenv()  
    return os.getenv('API_KEY')

def get_app_key():
    # load .env
    load_dotenv()  
    return os.getenv('APP_KEY')

def get_public_id():
    # load .env
    load_dotenv()  
    return os.getenv('PUBLIC_ID')

# Boto3 세션 을 초기화하고 객체를 사용자에게 반환
def init_datadog_session():
    api_key, app_key, public_id = get_datadog_keys()

    # API 키와 애플리케이션 키를 설정합니다.
    options = {
    "api_key": api_key,
    "app_key": app_key,
    }

    datadog.initialize(**options)

    
    os.environ['DD_SITE']    = 'datadoghq.com'
    os.environ['DD_API_KEY'] = api_key
    os.environ['DD_APP_KEY'] = app_key
