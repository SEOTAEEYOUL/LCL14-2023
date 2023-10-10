import requests

# Datadog API 및 애플리케이션 키 설정
api_key = '**********'
app_key = '**********'

# 요청 URL
url = 'https://api.datadoghq.com/api/v1/organization'

# API 요청 헤더
headers = {
    'Content-Type': 'application/json',
    'DD-API-KEY': api_key,
    'DD-APPLICATION-KEY': app_key
}

# API 요청 보내기
response = requests.get(url, headers=headers)

# 응답 확인
if response.status_code == 200:
    org_id = response.json()['id']
    print(f"조직 ID: {org_id}")
else:
    print(f"API 요청 실패. 응답 코드: {response.status_code}")
