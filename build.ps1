param (
    [switch]$InstallRequirements = $true
)

Write-Host "Building System Monitor Pro with PyInstaller..." -ForegroundColor Cyan

if ($InstallRequirements) {
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host "Running PyInstaller..." -ForegroundColor Yellow
pyinstaller --noconfirm SystemMonitorPro.spec

Write-Host "Build completed successfully! Executable is located at dist\SystemMonitorPro.exe" -ForegroundColor Green
