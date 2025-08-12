Write-Host "Proje klasoru temizleniyor..." -ForegroundColor Green
Write-Host ""

Write-Host "[*] __pycache__ klasorleri siliniyor..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Name "__pycache__" | ForEach-Object { 
    Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue 
}

Write-Host "[*] .pyc dosyalari siliniyor..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Include "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[*] .pyo dosyalari siliniyor..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Include "*.pyo" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[*] .pyd dosyalari siliniyor..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Include "*.pyd" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[*] Gecici dosyalar siliniyor..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Include "*.tmp", "*.temp", "*.log" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[*] IDE dosyalari siliniyor..." -ForegroundColor Yellow
if (Test-Path ".vscode") { Remove-Item -Path ".vscode" -Recurse -Force }
if (Test-Path ".idea") { Remove-Item -Path ".idea" -Recurse -Force }

Write-Host ""
Write-Host "[+] Temizlik tamamlandi!" -ForegroundColor Green
Write-Host "[+] Proje klasoru temiz tutuldu." -ForegroundColor Green

Read-Host "Devam etmek icin Enter'a basin"
