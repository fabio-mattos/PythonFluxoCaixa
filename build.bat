@echo off
setlocal enabledelayedexpansion

set "APP_NAME=FluxoCaixaFAPEU"
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ============================================
echo   Build - Fluxo de Caixa FAPEU
echo ============================================

where python >nul 2>nul
if errorlevel 1 (
    echo [ERRO] Python nao encontrado no PATH.
    exit /b 1
)

echo.
echo [1/4] Instalando dependencias...
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt
if errorlevel 1 goto :erro

python -m pip show pyinstaller >nul 2>nul
if errorlevel 1 (
    echo Instalando PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 goto :erro
)

echo.
echo [2/4] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%APP_NAME%.spec" del /q "%APP_NAME%.spec"

if not exist ".env" (
    echo [ERRO] .env nao encontrado. Ele sera embutido no executavel e e obrigatorio para o build.
    exit /b 1
)

echo.
echo [3/4] Gerando executavel...
python -m PyInstaller ^
    --name "%APP_NAME%" ^
    --onefile ^
    --windowed ^
    --collect-all customtkinter ^
    --add-data ".env;." ^
    --add-data "consulta.sql;." ^
    app.py
if errorlevel 1 goto :erro

echo.
echo [4/4] Copiando arquivos de apoio para dist\...
copy /y "FLUXO DE CAIXA_labtrans.xlsx" "dist\FLUXO DE CAIXA_labtrans.xlsx" >nul

echo.
echo ============================================
echo   Build concluido!
echo   Executavel: dist\%APP_NAME%.exe
echo   (.env e consulta.sql ja estao embutidos no .exe;
echo    mantenha apenas a planilha .xlsx ao lado dele)
echo ============================================
goto :fim

:erro
echo.
echo [ERRO] Falha durante o build.
exit /b 1

:fim
endlocal
