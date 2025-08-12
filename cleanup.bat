@echo off
echo Proje klasoru temizleniyor...
echo.

echo [*] __pycache__ klasorleri siliniyor...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul

echo [*] .pyc dosyalari siliniyor...
del /s /q *.pyc 2>nul

echo [*] .pyo dosyalari siliniyor...
del /s /q *.pyo 2>nul

echo [*] .pyd dosyalari siliniyor...
del /s /q *.pyd 2>nul

echo [*] Gecici dosyalar siliniyor...
del /s /q *.tmp 2>nul
del /s /q *.temp 2>nul
del /s /q *.log 2>nul

echo [*] IDE dosyalari siliniyor...
if exist .vscode rd /s /q .vscode 2>nul
if exist .idea rd /s /q .idea 2>nul

echo.
echo [+] Temizlik tamamlandi!
echo [+] Proje klasoru temiz tutuldu.
pause
