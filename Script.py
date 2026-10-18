import asyncio
import os
import subprocess
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Carrega as variáveis definidas no arquivo .env
load_dotenv(override=True)

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
    """Verifica se o processo do EnshroudedServer já existe no Gerenciador de Tarefas"""
    output = subprocess.check_output(
        'tasklist /FI "IMAGENAME eq enshrouded_server.exe"',
        shell=True,
    ).decode("cp1252")
    return "enshrouded_server.exe" in output

async def ligar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Validação usando a lista tratada
    if len(USUARIOS_PERMITIDOS) > 0 and user_id not in USUARIOS_PERMITIDOS:
        logging.warning(f"Tentativa de acesso não autorizada do ID: {user_id}")
        await update.message.reply_text("❌ Você não tem permissão para rodar este comando.")
        return

    logging.info(f"Comando recebido do usuário {user_id}. Verificando status do servidor...")

    try:
        servidor_rodando = servidor_ja_esta_rodando()
    except (OSError, subprocess.SubprocessError, UnicodeDecodeError) as e:
        logging.error(f"Erro ao verificar o status do servidor: {e}")
        await update.message.reply_text(f"❌ Não foi possível verificar o status do servidor: {e}")
        return

    if servidor_rodando:
        logging.info("Comando ignorado: O servidor de Enshrouded já está aberto.")
        await update.message.reply_text("⚠️ O servidor de Enshrouded já está ligado e rodando no PC!")
        return

    await update.message.reply_text("🤖 Comando recebido! Iniciando o servidor de Enshrouded...")
    
    try:
        flags = subprocess.CREATE_NEW_CONSOLE | subprocess.HIGH_PRIORITY_CLASS
        subprocess.Popen([CAMINHO_SERVIDOR], creationflags=flags)
        logging.info("Servidor inicializado com sucesso!")
        await update.message.reply_text("🚀 Servidor inicializado com sucesso no PC!")
    except Exception as e:
        logging.error(f"Erro ao abrir o servidor: {e}")
        await update.message.reply_text(f"❌ Erro ao abrir o servidor: {e}")

async def desligar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(USUARIOS_PERMITIDOS) > 0 and user_id not in USUARIOS_PERMITIDOS:
        logging.warning(f"Tentativa de acesso não autorizada do ID: {user_id}")
        await update.message.reply_text("❌ Você não tem permissão para rodar este comando.")
        return

    logging.info(f"Comando recebido do usuário {user_id}. Verificando status do servidor...")

    try:
        servidor_rodando = servidor_ja_esta_rodando()
    except (OSError, subprocess.SubprocessError, UnicodeDecodeError) as e:
        logging.error(f"Erro ao verificar o status do servidor: {e}")
        await update.message.reply_text(f"❌ Não foi possível verificar o status do servidor: {e}")
        return

    if not servidor_rodando:
        logging.info("Comando ignorado: O servidor de Enshrouded já está desligado.")
        await update.message.reply_text("⚠️ O servidor de Enshrouded já está desligado.")
        return

    erro_solicitacao = None
    try:
        resultado = subprocess.run(
            ["taskkill", "/IM", "enshrouded_server.exe", "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
        )
        if resultado.returncode != 0:
            erro_solicitacao = f"taskkill retornou código de saída {resultado.returncode}"
            logging.error(f"Erro ao solicitar o encerramento do servidor: {erro_solicitacao}")
    except (OSError, subprocess.SubprocessError) as e:
        erro_solicitacao = str(e)
        logging.error(f"Erro ao solicitar o encerramento do servidor: {e}")

    await update.message.reply_text(
        "Solicitação de desligamento do servidor enviada. Acompanharei por até 60 segundos o status e notificarei aqui quando o servidor desligar."
    )
    if erro_solicitacao:
        logging.warning(
            "A solicitação de encerramento encontrou um erro; verificando o status mesmo assim."
        )

    loop = asyncio.get_running_loop()
    prazo = loop.time() + 60
    while True:
        try:
            servidor_rodando = servidor_ja_esta_rodando()
        except (OSError, subprocess.SubprocessError, UnicodeDecodeError) as e:
            logging.error(f"Erro ao verificar o status do servidor: {e}")
            await update.message.reply_text(
                f"❌ Não foi possível confirmar se o servidor encerrou: {e}"
            )
            return

        if not servidor_rodando:
            logging.info("Encerramento do servidor confirmado pela verificação do processo.")
            await update.message.reply_text(
                "✅ O servidor de Enshrouded foi desligado com sucesso."
            )
            return

        tempo_restante = prazo - loop.time()
        if tempo_restante <= 0:
            mensagem = (
                "⚠️ O servidor ainda está em execução; não foi possível confirmar "
                "o desligamento após 60 segundos. Nenhum encerramento forçado foi tentado."
            )
            if erro_solicitacao:
                mensagem += f"\nErro ao solicitar o encerramento: {erro_solicitacao}"
            logging.warning("O servidor continuava em execução após o tempo de espera.")
            await update.message.reply_text(mensagem)
            return

        await asyncio.sleep(min(2, tempo_restante))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = f"Olá! Eu sou o assistente do seu servidor.\nSeu ID do Telegram é: {user_id}\n\nUse /ligar para iniciar ou /desligar para encerrar o servidor de Enshrouded."
    await update.message.reply_text(msg)


def main():
    if not TOKEN_TELEGRAM:
        logging.error("TELEGRAM_TOKEN não encontrado no arquivo .env")
        return

    application = Application.builder().token(TOKEN_TELEGRAM).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ligar", ligar))
    application.add_handler(CommandHandler("desligar", desligar))

    logging.info("Bot do Telegram iniciado e aguardando comandos...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()