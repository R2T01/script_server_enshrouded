@echo off
:: Altera a codificação do terminal para UTF-8 (corrige acentos)
chcp 65001 > nul

:: Define o título da janela do terminal
title Monitor Servidor Palworld

echo ===================================================
echo   Iniciando Assistente do Servidor Palworld...
echo ===================================================

:: Carrega as variáveis do arquivo .env
if exist .env (
    for /f "usebackq tokens=1* delims==" %%A in (".env") do (
        if not "%%A"=="" if not "%%A"=="#" (
            set "%%A=%%B"
        )
    )
) else (
    echo [AVISO] Arquivo .env não encontrado nesta pasta!
)

:: Navega para a pasta definida na variável PASTA_DO_SCRIPT do .env
if defined PASTA_DO_SCRIPT (
    cd /d "%PASTA_DO_SCRIPT%"
)

:: Executa o script mantendo a janela aberta e visível
python.exe Script.py

:: Caso o script pare por algum motivo, a janela não fecha sozinha
echo.
echo [AVISO] O script foi encerrado.
pause