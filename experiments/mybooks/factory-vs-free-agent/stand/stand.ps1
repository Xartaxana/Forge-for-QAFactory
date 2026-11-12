# The MyBooks stand without Docker: one portable PostgreSQL 16 server and, per arm of the comparison run, its own
# database, mail catcher, application copy and test repository copy. Nothing is shared between the arms but the
# PostgreSQL server process, so one arm's seed or stock change never reaches the other.
#
#   powershell -File stand.ps1 -Action services                 # PostgreSQL on 5433 + a Mailpit per arm
#   powershell -File stand.ps1 -Action setup  -Arm factory      # copies, env files, migrations, prod build, seed
#   powershell -File stand.ps1 -Action start  -Arm factory      # the app, detached; waits for /api/health
#   powershell -File stand.ps1 -Action seed   -Arm factory      # wipe the arm's data back to the fixed set
#   powershell -File stand.ps1 -Action status                   # every port and health in one table
#   powershell -File stand.ps1 -Action stop   -Arm factory      # stop the arm's app (never the database)
#
# Rules it keeps: the shell's working folder is never changed (PROJECT.md); nothing is deleted - an existing arm
# folder or env file is reused as it is; no secret is printed; the pristine clones under <StandRoot>\MyBooks and
# <StandRoot>\test-automation-framework are only read.
param(
    [Parameter(Mandatory = $true)][ValidateSet('services', 'setup', 'start', 'seed', 'status', 'stop')][string]$Action,
    [ValidateSet('factory', 'free')][string]$Arm,
    [string]$StandRoot = 'C:\QAFactory\mybooks-stand'
)
$ErrorActionPreference = 'Stop'

$Arms = @{
    factory = @{ Port = 3000; Db = 'bookstore';      Smtp = 1025; MailUi = 8025 }
    free    = @{ Port = 3001; Db = 'bookstore_free'; Smtp = 1026; MailUi = 8026 }
}
$PgPort = 5433
$PgBin = Join-Path $StandRoot 'tools\pgsql\bin'
$PgData = Join-Path $StandRoot 'pgdata'
$Logs = Join-Path $StandRoot 'logs'
$LiveApp = Join-Path $StandRoot 'MyBooks'
$LiveTests = Join-Path $StandRoot 'test-automation-framework'
# The role and its password are the public values of the project's own docker-compose.yml, not a secret.
$PgUser = 'bookstore'; $PgPass = 'bookstore'

function Test-Port([int]$Port) {
    [bool](Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue)
}

function Wait-Port([int]$Port, [int]$Seconds = 60) {
    for ($i = 0; $i -lt $Seconds; $i++) { if (Test-Port $Port) { return $true }; Start-Sleep -Seconds 1 }
    return $false
}

function New-Secret([int]$Length = 32) {
    $bytes = New-Object byte[] $Length
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    -join ($bytes | ForEach-Object { 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'[$_ % 56] })
}

function Read-EnvFile([string]$Path) {
    $map = @{}
    foreach ($line in Get-Content $Path) {
        if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)=(.*)$') { $map[$Matches[1]] = $Matches[2] }
    }
    $map
}

function Use-Env([hashtable]$Map) { foreach ($k in $Map.Keys) { Set-Item -Path "Env:$k" -Value $Map[$k] } }

function Get-MailpitExe {
    $cmd = Get-Command mailpit -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $found = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter mailpit.exe -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if (-not $found) { throw 'mailpit.exe not found: winget install --id axllent.mailpit' }
    $found.FullName
}

function Start-Services {
    New-Item -ItemType Directory -Force $Logs | Out-Null
    if (-not (Test-Path (Join-Path $PgData 'PG_VERSION'))) {
        $pw = Join-Path $StandRoot 'tools\pg-pwfile.txt'
        Set-Content -Path $pw -Value $PgPass -NoNewline -Encoding ascii
        & (Join-Path $PgBin 'initdb.exe') -D $PgData -U $PgUser --pwfile=$pw -A scram-sha-256 -E UTF8 --locale=C | Select-Object -Last 2
    }
    if (-not (Test-Port $PgPort)) {
        Start-Process -FilePath (Join-Path $PgBin 'pg_ctl.exe') -WindowStyle Hidden -ArgumentList @(
            'start', '-D', "`"$PgData`"", '-l', "`"$(Join-Path $Logs 'postgres.log')`"", '-o', "`"-p $PgPort -c listen_addresses=localhost`"")
        if (-not (Wait-Port $PgPort 60)) { throw "PostgreSQL did not open port $PgPort; see $Logs\postgres.log" }
    }
    $env:PGPASSWORD = $PgPass
    foreach ($name in $Arms.Keys) {
        $db = $Arms[$name].Db
        $has = & (Join-Path $PgBin 'psql.exe') -h localhost -p $PgPort -U $PgUser -d postgres -tAc "select 1 from pg_database where datname='$db'"
        if ("$has".Trim() -ne '1') { & (Join-Path $PgBin 'createdb.exe') -h localhost -p $PgPort -U $PgUser $db }
    }
    $mailpit = Get-MailpitExe
    foreach ($name in $Arms.Keys) {
        $a = $Arms[$name]
        if (-not (Test-Port $a.Smtp)) {
            Start-Process -FilePath $mailpit -WindowStyle Hidden -ArgumentList @('--smtp', "127.0.0.1:$($a.Smtp)", '--listen', "127.0.0.1:$($a.MailUi)") `
                -RedirectStandardOutput (Join-Path $Logs "mailpit-$name.log") -RedirectStandardError (Join-Path $Logs "mailpit-$name.err")
            if (-not (Wait-Port $a.Smtp 30)) { throw "Mailpit of arm $name did not open port $($a.Smtp)" }
        }
    }
    Show-Status
}

function Copy-Tree([string]$From, [string]$To, [string[]]$SkipDirs) {
    if (Test-Path $To) { "reused as it is: $To"; return }
    $args = @($From, $To, '/E', '/NFL', '/NDL', '/NJH', '/NJS', '/NP', '/R:1', '/W:1')
    if ($SkipDirs) { $args += '/XD'; $args += $SkipDirs }
    & robocopy @args | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy $From -> $To failed with $LASTEXITCODE" }
    "copied: $To"
}

function Write-ArmEnv([string]$Name) {
    $a = $Arms[$Name]
    $app = Join-Path $StandRoot "arm-$Name\MyBooks"
    $tests = Join-Path $StandRoot "arm-$Name\test-automation-framework"
    $envLocal = Join-Path $app '.env.local'
    if (Test-Path $envLocal) { "reused as it is: $envLocal" }
    else {
        # The admin's password is the one the test repository's own fixture expects; it is read, never printed.
        $fixture = Get-Content (Join-Path $LiveTests 'core\fixtures\admin.fixture.ts') -Raw
        if ($fixture -notmatch "password:\s*['""]([^'""]+)['""]") { throw 'admin password not found in core/fixtures/admin.fixture.ts' }
        $adminPass = $Matches[1]
        $base = "http://localhost:$($a.Port)"
        $lines = @(
            "POSTGRES_PRISMA_URL=postgresql://${PgUser}:${PgPass}@localhost:$PgPort/$($a.Db)?schema=public",
            "NEXTAUTH_URL=$base",
            "NEXTAUTH_SECRET=$(New-Secret 44)",
            'SMTP_HOST=localhost',
            "SMTP_PORT=$($a.Smtp)",
            'SMTP_USER=',
            'SMTP_PASS=',
            'SMTP_FROM=Bookstore <no-reply@bookstore.local>',
            'ADMIN_EMAIL=admin@bookstore.com',
            "ADMIN_PASSWORD=$adminPass",
            'USER_EMAIL=user@bookstore.com',
            "USER_PASSWORD=$(New-Secret 16)",
            'ENABLE_TEST_ENDPOINTS=true',
            "TEST_SECRET=$(New-Secret 32)",
            'REQUIRE_EMAIL_VERIFICATION=',
            'RATE_LIMIT_DISABLED=true',
            'TAX_RATE=0.08',
            'LOW_STOCK_THRESHOLD=5'
        )
        [IO.File]::WriteAllLines($envLocal, $lines)
        Copy-Item $envLocal (Join-Path $app '.env')          # prisma and the seed read .env
        "written: $envLocal and .env (values not shown)"
    }
    $testEnv = Join-Path $tests '.env'
    if (Test-Path $testEnv) { "reused as it is: $testEnv" }
    else {
        $e = Read-EnvFile $envLocal
        $base = "http://localhost:$($a.Port)"
        # NODE_ENV=prod: the only profile of the test repository that talks to the app and not to the HAR mock server.
        $lines = @(
            'NODE_ENV=prod', "BASE_URL=$base", "API_URL=$base/api",
            "EMAIL_USER=$($e.ADMIN_EMAIL)", "EMAIL_PASS=$($e.ADMIN_PASSWORD)",
            "USER_EMAIL=$($e.USER_EMAIL)", "USER_PASSWORD=$($e.USER_PASSWORD)", "TEST_SECRET=$($e.TEST_SECRET)",
            "MAILPIT_URL=http://localhost:$($a.MailUi)"
        )
        [IO.File]::WriteAllLines($testEnv, $lines)
        New-Item -ItemType Directory -Force (Join-Path $tests 'storage-state') | Out-Null
        "written: $testEnv (values not shown)"
    }
}

function Invoke-Seed([string]$Name) {
    $app = Join-Path $StandRoot "arm-$Name\MyBooks"
    Use-Env (Read-EnvFile (Join-Path $app '.env.local'))
    $env:NODE_ENV = 'development'
    & npm.cmd --prefix $app run db:seed | Select-Object -Last 6
    if ($LASTEXITCODE -ne 0) { throw "db:seed of arm $Name failed with $LASTEXITCODE" }
    "seeded: arm $Name at $(Get-Date -Format s)"
}

function Initialize-Arm([string]$Name) {
    if (-not (Test-Port $PgPort)) { throw 'PostgreSQL is not running: -Action services first' }
    $root = Join-Path $StandRoot "arm-$Name"
    New-Item -ItemType Directory -Force $root | Out-Null
    Copy-Tree $LiveApp (Join-Path $root 'MyBooks') @('.next')
    Copy-Tree $LiveTests (Join-Path $root 'test-automation-framework') @('test-results', 'playwright-report')
    Write-ArmEnv $Name
    $app = Join-Path $root 'MyBooks'
    Use-Env (Read-EnvFile (Join-Path $app '.env.local'))
    & node (Join-Path $app 'node_modules\prisma\build\index.js') migrate deploy --schema (Join-Path $app 'prisma\schema.prisma') | Select-Object -Last 3
    if ($LASTEXITCODE -ne 0) { throw "prisma migrate deploy of arm $Name failed with $LASTEXITCODE" }
    $env:NODE_ENV = 'production'
    & npm.cmd --prefix $app run build | Select-Object -Last 4
    if ($LASTEXITCODE -ne 0) { throw "next build of arm $Name failed with $LASTEXITCODE" }
    Invoke-Seed $Name
    "app commit:   $(git -C $app rev-parse HEAD)"
    "tests commit: $(git -C (Join-Path $root 'test-automation-framework') rev-parse HEAD)"
}

function Start-Arm([string]$Name) {
    $a = $Arms[$Name]
    $app = Join-Path $StandRoot "arm-$Name\MyBooks"
    New-Item -ItemType Directory -Force $Logs | Out-Null
    if (-not (Test-Port $a.Port)) {
        Use-Env (Read-EnvFile (Join-Path $app '.env.local'))
        $env:NODE_ENV = 'production'
        Start-Process -FilePath node -WorkingDirectory $app -WindowStyle Hidden `
            -ArgumentList @('node_modules\next\dist\bin\next', 'start', '-p', "$($a.Port)") `
            -RedirectStandardOutput (Join-Path $Logs "app-$Name.log") -RedirectStandardError (Join-Path $Logs "app-$Name.err")
        if (-not (Wait-Port $a.Port 90)) { throw "the app of arm $Name did not open port $($a.Port); see $Logs\app-$Name.err" }
    }
    Invoke-RestMethod "http://localhost:$($a.Port)/api/health" | ConvertTo-Json -Compress
}

function Stop-Arm([string]$Name) {
    $conn = Get-NetTCPConnection -State Listen -LocalPort $Arms[$Name].Port -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $conn) { "arm ${Name}: the app is not running"; return }
    Stop-Process -Id $conn.OwningProcess -Force
    "arm ${Name}: stopped pid $($conn.OwningProcess)"
}

function Show-Status {
    "PostgreSQL :$PgPort  listening=$(Test-Port $PgPort)"
    foreach ($name in ($Arms.Keys | Sort-Object)) {
        $a = $Arms[$name]
        $health = 'down'
        if (Test-Port $a.Port) {
            try { $health = (Invoke-RestMethod "http://localhost:$($a.Port)/api/health" -TimeoutSec 10 | ConvertTo-Json -Compress) } catch { $health = "error: $($_.Exception.Message)" }
        }
        "arm $name  app :$($a.Port) $health | db $($a.Db) | mailpit smtp :$($a.Smtp) ui :$($a.MailUi) listening=$(Test-Port $a.Smtp)"
    }
}

if ($Action -in 'setup', 'start', 'seed', 'stop' -and -not $Arm) { throw "-Action $Action needs -Arm factory|free" }
switch ($Action) {
    'services' { Start-Services }
    'setup'    { Initialize-Arm $Arm }
    'start'    { Start-Arm $Arm }
    'seed'     { Invoke-Seed $Arm }
    'stop'     { Stop-Arm $Arm }
    'status'   { Show-Status }
}
