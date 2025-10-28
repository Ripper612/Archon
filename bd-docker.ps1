# bd-docker.ps1 - Convenience script to run beads (bd) commands in Docker
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

$workspace = $PWD.Path
$beadsHome = "$HOME\.beads"

# Ensure the beads home directory exists
if (!(Test-Path $beadsHome)) {
    New-Item -ItemType Directory -Path $beadsHome | Out-Null
}

# Run beads in Docker with volume mounts
docker run --rm -v "${workspace}:/workspace" -v "${beadsHome}:/home/beads/.beads" -w /workspace beads $Args
