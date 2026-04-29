param(
    [int]$Start = 1,
    [int]$End = 23,
    [string]$Model = "gpt-5.5",
    [switch]$AutoCommit,
    [switch]$AllowDirty
)

$ErrorActionPreference = "Continue"

$Root = Get-Location
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogDir = Join-Path $Root "logs\codex_queue_$Timestamp"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

Write-Host "Repo: $Root"
Write-Host "Model: $Model"
Write-Host "Task range: $Start to $End"
Write-Host "Logs: $LogDir"
Write-Host "AutoCommit: $AutoCommit"

if (-not $AllowDirty) {
    $dirtyBefore = git status --porcelain
    if ($dirtyBefore) {
        Write-Host ""
        Write-Host "Repo has uncommitted changes. Commit/stash first, or rerun with -AllowDirty."
        git status --short
        exit 1
    }
}

git status --short | Out-File (Join-Path $LogDir "git_status_before.txt")

$tasks = @()

foreach ($task in Get-ChildItem -Path "tasks" -Filter "*.md") {
    if ($task.Name -match '^(\d{3})_') {
        $n = [int]$Matches[1]
        if ($n -ge $Start -and $n -le $End) {
            $tasks += $task
        }
    }
}

$tasks = $tasks | Sort-Object Name

if ($tasks.Count -eq 0) {
    Write-Host "No task files found in selected range."
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

    git status --short | Out-File (Join-Path $LogDir "${taskName}_git_status_before.txt")

    $prompt = Get-Content $task.FullName -Raw

    $prompt |
        codex exec --cd . -m $Model -c sandbox_mode=workspace-write -c approval_policy=never - *>&1 |
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

    if ($AutoCommit) {
        $dirtyAfter = git status --porcelain
        if ($dirtyAfter) {
            git add .
            git commit -m "Run $taskName"
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Auto-commit failed after $($task.Name). Stopping queue."
                exit $LASTEXITCODE
            }
        } else {
            Write-Host "No file changes after $($task.Name); skipping commit."
        }
    }
}

git status --short | Out-File (Join-Path $LogDir "git_status_final.txt")
git diff --stat | Out-File (Join-Path $LogDir "git_diff_stat_final.txt")
git diff | Out-File (Join-Path $LogDir "git_diff_final.patch")

Write-Host ""
Write-Host "All selected tasks finished."
Write-Host "Review with:"
Write-Host "git log --oneline --decorate -n 20"
Write-Host "git status"
Write-Host "git diff"
Write-Host "Logs saved to: $LogDir"
