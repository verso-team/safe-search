param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

Write-Host "SAFE:SEARCH API smoke test" -ForegroundColor Cyan
Write-Host "Target: $BaseUrl"

$health = Invoke-RestMethod `
    -Method Get `
    -Uri "$BaseUrl/health"

if ($health.status -ne "ok") {
    throw "Health check failed."
}

$payload = @{
    text = "영상 유포 협박을 받고 있는데 어디로 신고해야 할지 모르겠어요."
} | ConvertTo-Json -Compress

$body = [System.Text.Encoding]::UTF8.GetBytes($payload)

$result = Invoke-RestMethod `
    -Method Post `
    -Uri "$BaseUrl/api/v1/analyze" `
    -ContentType "application/json; charset=utf-8" `
    -Body $body

$requiredProperties = @(
    "primary_intent",
    "secondary_intents",
    "emotional_state",
    "urgency",
    "confidence",
    "suspected_harm_type",
    "emotional_support_message",
    "situation_summary",
    "immediate_actions",
    "safe_search_queries",
    "recommended_agencies",
    "requires_human_review",
    "safety_notice"
)

foreach ($property in $requiredProperties) {
    if (-not ($result.PSObject.Properties.Name -contains $property)) {
        throw "Missing response property: $property"
    }
}

if ($result.immediate_actions.Count -gt 3) {
    throw "immediate_actions exceeds 3 items."
}

if (-not $result.recommended_agencies) {
    throw "No official agency returned."
}

foreach ($agency in $result.recommended_agencies) {
    if (-not $agency.is_official) {
        throw "Non-official agency returned: $($agency.name)"
    }
}

Write-Host ""
Write-Host "PASS" -ForegroundColor Green
Write-Host "Intent: $($result.primary_intent)"
Write-Host "Urgency: $($result.urgency)"
Write-Host "Confidence: $($result.confidence)"
Write-Host "Actions: $($result.immediate_actions.Count)"
Write-Host "Agencies: $($result.recommended_agencies.Count)"
