Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

$BuildRoot = Join-Path $RepoRoot "build\lambda"
$PackageDir = Join-Path $BuildRoot "package"
$RequirementsFile = Join-Path $BuildRoot "requirements.txt"
$ZipFile = Join-Path $BuildRoot "reliora-ticket-execution.zip"

Write-Host "Building Reliora Lambda deployment package..."

if (Test-Path $BuildRoot) {
    Remove-Item $BuildRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $PackageDir | Out-Null

Write-Host "Exporting locked production dependencies..."

Push-Location $RepoRoot

try {
    uv export `
        --frozen `
        --no-dev `
        --no-emit-project `
        --format requirements.txt `
        --output-file $RequirementsFile

    if ($LASTEXITCODE -ne 0) {
        throw "uv export failed with exit code $LASTEXITCODE"
    }

    Write-Host "Installing Linux x86_64 / Python 3.12 dependencies..."

    uv pip install `
        --no-installer-metadata `
        --no-compile-bytecode `
        --no-build `
        --python-platform x86_64-manylinux2014 `
        --python 3.12 `
        --target $PackageDir `
        -r $RequirementsFile

    if ($LASTEXITCODE -ne 0) {
        throw "uv pip install failed with exit code $LASTEXITCODE"
    }

    Write-Host "Copying Reliora application package..."

    Copy-Item `
        -Path (Join-Path $RepoRoot "src\reliora") `
        -Destination (Join-Path $PackageDir "reliora") `
        -Recurse `
        -Force

    Get-ChildItem `
        -Path $PackageDir `
        -Directory `
        -Recurse `
        -Filter "__pycache__" |
        Remove-Item -Recurse -Force

    Get-ChildItem `
        -Path $PackageDir `
        -File `
        -Recurse `
        -Include "*.pyc", "*.pyo" |
        Remove-Item -Force

    Write-Host "Creating Lambda ZIP..."

    Compress-Archive `
        -Path (Join-Path $PackageDir "*") `
        -DestinationPath $ZipFile `
        -CompressionLevel Optimal `
        -Force
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Lambda package created:"
Write-Host $ZipFile