param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$testValues = @(
    "010-1234-5678",
    "123-456-789012",
    "654321",
    "victim@example.com"
)

$payload = @{
    text = @"
검찰 사칭 전화가 010-1234-5678로 왔습니다.
안전계좌번호 123-456-789012로 송금하고
인증번호 654321을 보내라고 합니다.
답장은 victim@example.com으로 보내라고 했습니다.
"@
} | ConvertTo-Json -Compress

$requestFile = Join-Path $env:TEMP "safe-search-pii-request-$PID.json"
$responseFile = Join-Path $env:TEMP "safe-search-pii-response-$PID.json"

try {
    $utf8WithoutBom = New-Object System.Text.UTF8Encoding($false)

    [System.IO.File]::WriteAllText(
        $requestFile,
        $payload,
        $utf8WithoutBom
    )

    Invoke-WebRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/analyze" `
        -ContentType "application/json; charset=utf-8" `
        -InFile $requestFile `
        -OutFile $responseFile `
        -UseBasicParsing

    $json = [System.IO.File]::ReadAllText(
        $responseFile,
        [System.Text.Encoding]::UTF8
    )

    $result = $json | ConvertFrom-Json

    foreach ($value in $testValues) {
        if ($json.Contains($value)) {
            throw "민감정보가 API 응답에 노출되었습니다: $value"
        }
    }

    if ($result.safety_notice -notmatch "민감정보\s+4건") {
        throw "PII 마스킹 안내가 응답에서 확인되지 않습니다."
    }

    Write-Host ""
    Write-Host "PASS: UTF-8 응답과 PII 마스킹 검증 완료" -ForegroundColor Green
    Write-Host ""

    [PSCustomObject]@{
        Intent       = $result.primary_intent
        Urgency      = $result.urgency
        HarmType     = $result.suspected_harm_type
        SafetyNotice = $result.safety_notice
    } | Format-List
}
finally {
    Remove-Item $requestFile -Force -ErrorAction SilentlyContinue
    Remove-Item $responseFile -Force -ErrorAction SilentlyContinue
}
