param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

$scenarios = @(
    "상대가 흉기를 들고 집 앞에 찾아왔어요.",
    "나체 사진을 유포하겠다고 협박해서 신고 방법을 알고 싶어요.",
    "검찰 사칭 전화가 안전계좌로 송금하고 원격제어 앱을 설치하라고 해요.",
    "모르는 기기 로그인 알림이 왔고 비밀번호가 변경됐어요.",
    "전 애인이 계속 미행하고 회사 앞에서 기다려서 무서워요.",
    "사이버범죄 신고 절차와 지원 기관을 알고 싶어요.",
    "이상한 일이 있었어요."
)

$results = foreach ($text in $scenarios) {
    $payload = @{ text = $text } | ConvertTo-Json -Compress
    $body = [System.Text.Encoding]::UTF8.GetBytes($payload)

    $result = Invoke-RestMethod `
        -Method Post `
        -Uri "$BaseUrl/api/v1/analyze" `
        -ContentType "application/json; charset=utf-8" `
        -Body $body

    [PSCustomObject]@{
        Input = $text
        Intent = $result.primary_intent
        Urgency = $result.urgency
        HarmType = $result.suspected_harm_type
        Confidence = $result.confidence
        Review = $result.requires_human_review
    }
}

$results | Format-Table -Wrap -AutoSize

