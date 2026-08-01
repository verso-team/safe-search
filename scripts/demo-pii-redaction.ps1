param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 아래 값은 기능 검증용 가상 데이터다.
$payload = @{
    text = @"
검찰 사칭 전화가 010-1234-5678로 왔습니다.
안전계좌번호 123-456-789012로 송금하고
인증번호 654321을 보내라고 합니다.
답장은 victim@example.com으로 보내라고 했습니다.
"@
} | ConvertTo-Json -Compress

$body = [System.Text.Encoding]::UTF8.GetBytes($payload)

$result = Invoke-RestMethod `
    -Method Post `
    -Uri "$BaseUrl/api/v1/analyze" `
    -ContentType "application/json; charset=utf-8" `
    -Body $body

[PSCustomObject]@{
    Intent = $result.primary_intent
    Urgency = $result.urgency
    HarmType = $result.suspected_harm_type
    SafetyNotice = $result.safety_notice
} | Format-List
