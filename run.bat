@echo off
:: Altera a codificação do terminal para UTF-8 (corrige acentos)
chcp 65001 > nul

:: Define o título da janela do terminal
title Monitor Servidor Enshrouded

echo ===================================================
echo   Iniciando Assistente do Servidor Enshrouded...
echo ===================================================

:: Navega automaticamente para a pasta onde este arquivo .bat está salvo
cd /d "%~dp0"

:: Carrega as variáveis do arquivo .env (caso exista)
if exist .env (
    for /f "usebackq tokens=1* delims==" %%A in (".env") do (
        if not "%%A"=="" if not "%%A"=="#" (
            set "%%A=%%B"
        )
    )
) else (
    echo [AVISO] Arquivo .env não encontrado nesta pasta!
)

:: Executa o script utilizando o caminho absoluto correto do Python
C:\Users\Rafael\AppData\Local\Python\pythoncore-3.15-64\python.exe Script.py

:: Caso o script pare por algum motivo, a janela não fecha sozinha
echo.
echo [AVISO] O script foi encerrado.
pause