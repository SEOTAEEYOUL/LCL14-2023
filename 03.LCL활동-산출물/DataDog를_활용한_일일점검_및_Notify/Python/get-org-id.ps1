# Curl command
curl -X POST "https://api.datadoghq.com/api/v1/org" `
-H "Accept: application/json" `
-H "Content-Type: application/json" `
-H "DD-API-KEY: ${DD_API_KEY}" `
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" `
-d @- << EOF
{
  "name": "New child org"
}
EOF