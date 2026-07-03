# scripts/approve_decision.ps1
param(
    [Parameter(Mandatory=$true)][string]$Token,
    [Parameter(Mandatory=$true)][string]$DecisionId,
    [Parameter(Mandatory=$true)][double]$Stake,
    [string]$ExpectedClose
)
$uri = "http://127.0.0.1:8000/approve_decision"
$body = @{
    decision_id = $DecisionId
    stake = $Stake
    expected_close = $ExpectedClose
} | ConvertTo-Json
$headers = @{ Authorization = "Bearer $Token"; "Content-Type" = "application/json" }
Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $body
