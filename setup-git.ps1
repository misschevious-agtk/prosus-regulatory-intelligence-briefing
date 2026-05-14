# setup-git.ps1 -- one-shot local setup for the Legal Intelligence Briefing repo.
#
# What it does:
#   1. Sanity-checks that you are running it inside the project folder.
#   2. Cleans up any partial / broken .git stub from earlier attempts (safe;
#      aborts if it detects real commits to avoid data loss).
#   3. Cleans up the smoke-test fixtures Claude left behind.
#   4. Runs `git init` on branch main.
#   5. Sets your git identity locally (repo-only, not global).
#   6. Asks for your GitHub repo URL once.
#   7. Stages everything, makes the first commit, and connects the remote.
#
# After this finishes, run ONE command to publish to GitHub:
#
#       git push -u origin main
#
# Your browser will pop up for GitHub auth -- choose "Sign in with browser".
#
# Run from inside the project folder with:
#
#       powershell -ExecutionPolicy Bypass -File .\setup-git.ps1

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Note($msg) { Write-Host "    $msg" -ForegroundColor DarkGray }
function Write-Warn($msg) { Write-Host "!!  $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "X   $msg" -ForegroundColor Red }
function Write-OK($msg)   { Write-Host "OK  $msg" -ForegroundColor Green }

# ---- 1. Verify we are in the right folder
Write-Step "Verifying current folder..."
if (-not (Test-Path "README.md") -or -not (Test-Path "scripts\fetch_articles.py")) {
    Write-Err "This script must be run inside the prosus-legal-intelligence-briefing folder."
    Write-Err "Current folder: $(Get-Location)"
    Write-Err "Open File Explorer, navigate into the project folder, type 'powershell' in the address bar to open a new terminal here, and re-run."
    exit 1
}
Write-OK "In the right folder: $(Get-Location)"

# ---- 2. Clean up any broken .git stub (defensive; aborts if real commits exist)
if (Test-Path ".git") {
    Write-Step "Found existing .git folder, checking whether it is safe to remove..."
    $hasObjects = $false
    if (Test-Path ".git\objects") {
        $hasObjects = (Get-ChildItem -Path ".git\objects" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
    }
    if ($hasObjects) {
        Write-Err "Existing .git contains real commits; refusing to delete it."
        Write-Err "If you intended to start fresh, run 'git log' to see what is there, then move or delete .git yourself."
        exit 1
    }
    Write-Note "It is just an empty stub from an interrupted earlier init; safe to remove."
    Remove-Item -Recurse -Force ".git"
    Write-OK ".git stub removed."
} else {
    Write-Note "No existing .git folder; starting clean."
}

# ---- 3. Clean up smoke-test leftovers
if (Test-Path "findings\candidates\2026-05-13") {
    Write-Step "Removing Claude's smoke-test fixtures..."
    Remove-Item -Recurse -Force "findings\candidates\2026-05-13"
    Write-OK "Smoke-test fixtures removed."
}

# ---- 4. git init on main
Write-Step "Initialising repo on branch 'main'..."
git init -b main | Out-Null
Write-OK "Repo initialised."

# ---- 5. Local identity
Write-Step "Setting git identity (repo-local)..."
git config user.name "Klimentina Maleevska"
git config user.email "klimentina.maleevska@prosus.com"
Write-OK "Identity set: Klimentina Maleevska <klimentina.maleevska@prosus.com>"

# ---- 6. Ask for the repo URL
Write-Host ""
Write-Step "Need your GitHub repo URL."
Write-Note "On the GitHub repo page click the green 'Code' button, then 'HTTPS' tab,"
Write-Note "then copy the URL. It should look like:"
Write-Note "    https://github.com/<your-username>/prosus-legal-intelligence-briefing.git"
$url = Read-Host "Paste it here and press Enter"
$url = $url.Trim()
if (-not $url) {
    Write-Err "No URL given. Aborting."
    exit 1
}
if (-not $url.StartsWith("https://github.com/")) {
    Write-Err "URL does not look right; expected something starting with https://github.com/"
    Write-Err "Got: $url"
    exit 1
}
if (-not $url.EndsWith(".git")) {
    Write-Warn "URL does not end with .git; adding it."
    $url = "$url.git"
}

# ---- 7. Stage + first commit
Write-Step "Staging files..."
git add -A
$staged = (git diff --cached --name-only | Measure-Object -Line).Lines
Write-OK "Staged $staged file(s)."

Write-Step "Making first commit..."
git commit -m "Initial commit -- Legal Intelligence Briefing v0.1 (RSS scrape + HTML scrape + email ingest + entity-tagging and clustering ranker)" | Out-Null
Write-OK "First commit made."

# ---- 8. Connect remote
Write-Step "Connecting GitHub remote..."
git remote add origin $url
git remote -v

Write-Host ""
Write-Host "===== LOCAL SETUP COMPLETE =====" -ForegroundColor Green
Write-Host ""
Write-Host "One last command to publish to GitHub (run it in this same terminal):" -ForegroundColor Cyan
Write-Host ""
Write-Host "    git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "When it pops a browser, sign in to GitHub. After that, refresh your" -ForegroundColor DarkGray
Write-Host "repo page on github.com and you will see the full file tree." -ForegroundColor DarkGray
Write-Host ""
