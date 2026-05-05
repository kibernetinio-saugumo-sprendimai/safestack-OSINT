param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
$venvActivate = Join-Path $scriptDir ".venv\Scripts\Activate.ps1"

if (Test-Path $venvActivate) {
    & $venvActivate
}

python -m cli.ss_osint @Args
