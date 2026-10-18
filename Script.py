import os
import subprocess
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

# --- CONFIGURAÇÃO DO LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# --- CONFIGURAÇÕES VIA VARIÁVEIS DE AMBIENTE ---
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")

# Converte a string separada por vírgula em uma lista de inteiros
usuarios_raw = os.getenv("USUARIOS_PERMITIDOS", "")
USUARIOS_PERMITIDOS = [int(u.strip()) for u in usuarios_raw.split(",") if u.strip().isdigit()]

CAMINHO_SERVIDOR = os.getenv("CAMINHO_SERVIDOR")
# ---------------------

def servidor_ja_esta_rodando():
    """Verifica se o processo do PalServer já existe no Gerenciador de Tarefas"""
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq PalServer.exe"', shell=True).decode('cp1252')
        return "PalServer.exe" in output
    except Exception as e:
        logging.error(f"Erro ao verificar processos ativos: {e}")
        return False

async def ligar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Validação usando a lista tratada
    if len(USUARIOS_PERMITIDOS) > 0 and user_id not in USUARIOS_PERMITIDOS:
        logging.warning(f"Tentativa de acesso não autorizada do ID: {user_id}")
        await update.message.reply_text("❌ Você não tem permissão para rodar este comando.")
        return

    logging.info(f"Comando recebido do usuário {user_id}. Verificando status do servidor...")

    if servidor_ja_esta_rodando():
        logging.info("Comando ignorado: O servidor de Palworld já está aberto.")
        await update.message.reply_text("⚠️ O servidor de Palworld já está ligado e rodando no PC!")
        return

    await update.message.reply_text("🤖 Comando recebido! Iniciando o servidor de Palworld...")
    
    try:
        flags = subprocess.CREATE_NEW_CONSOLE | subprocess.HIGH_PRIORITY_CLASS
        subprocess.Popen([CAMINHO_SERVIDOR], creationflags=flags)
        logging.info("Servidor inicializado com sucesso!")
        await update.message.reply_text("🚀 Servidor inicializado com sucesso no PC!")
    except Exception as e:
        logging.error(f"Erro ao abrir o servidor: {e}")
        await update.message.reply_text(f"❌ Erro ao abrir o servidor: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = f"Olá! Eu sou o assistente do seu servidor.\nSeu ID do Telegram é: {user_id}\n\nUse o comando /ligar para iniciar o Palworld."
    await update.message.reply_text(msg)


def main():
    if not TOKEN_TELEGRAM:
        logging.error("TELEGRAM_TOKEN não encontrado no arquivo .env")
        return

    application = Application.builder().token(TOKEN_TELEGRAM).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ligar", ligar))

    logging.info("Bot do Telegram iniciado e aguardando comandos...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()