$ErrorActionPreference = "Continue"

$Model = "gpt-5.4"
$Root = Get-Location
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogDir = Join-Path $Root "logs\codex_$Timestamp"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

Write-Host "Repo: $Root"
Write-Host "Model: $Model"
Write-Host "Logs: $LogDir"

git status --short | Out-File (Join-Path $LogDir "git_status_before.txt")

$tasks = Get-ChildItem -Path "tasks" -Filter "*.md" | Sort-Object Name

if ($tasks.Count -eq 0) {
    Write-Host "No task files found in tasks/"
    exit 1
}

foreach ($task in $tasks) {
    $taskName = [System.IO.Path]::GetFileNameWithoutExtension($task.Name)
    $logFile = Join-Path $LogDir "$taskName.log"

    Write-Host ""
    Write-Host "=============================="
    Write-Host "Running task: $($task.Name)"
    Write-Host "Log: $logFile"
    Write-Host "=============================="

    $Error.Clear()

    Get-Content $task.FullName -Raw |
        codex exec --cd . -m $Model - 2>&1 |
        Tee-Object -FilePath $logFile

    $exitCode = $LASTEXITCODE

    git status --short | Out-File (Join-Path $LogDir "${taskName}_git_status_after.txt")
    git diff --stat | Out-File (Join-Path $LogDir "${taskName}_diff_stat.txt")

    if ($exitCode -ne 0) {
        Write-Host ""
        Write-Host "Task failed with exit code ${exitCode}: $($task.Name)"
        Write-Host "Stopping queue."
        exit $exitCode
    }
}

git status --short | Out-File (Join-Path $LogDir "git_status_final.txt")
git diff --stat | Out-File (Join-Path $LogDir "git_diff_stat_final.txt")
git diff | Out-File (Join-Path $LogDir "git_diff_final.patch")

Write-Host ""
Write-Host "All tasks finished."
Write-Host "Review with:"
Write-Host "git status"
Write-Host "git diff"
Write-Host "Logs saved to: $LogDir"