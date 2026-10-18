# Assistente do Servidor Enshrouded

Bot para Telegram que permite iniciar o servidor dedicado de Enshrouded no computador local com o comando `/ligar`.

## Origem do projeto

Este projeto é um clone reaproveitado do meu [assistente para servidor de Palworld](https://github.com/R2T01/script_server_palworld), adaptado para iniciar e verificar um servidor dedicado de Enshrouded.

## Funcionalidades

- Verifica se o processo `enshrouded_server.exe` já está em execução
- Permite iniciar o servidor com o comando `/ligar`
- Permite encerrar o servidor com o comando `/desligar`
- Restringe o uso por IDs de usuário autorizados
- Exibe informações iniciais com o comando `/start`
- Funciona no Windows

## Requisitos

- Python 3.9 ou superior
- Windows
- Telegram Bot Token
- Caminho do executável do servidor dedicado de Enshrouded (`enshrouded_server.exe`)

## Instalação

1. Clone o repositório e entre na pasta do projeto:

   ```bash
   git clone <url-do-repositorio>
   cd "Script EnshroudedServer"
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Copie o arquivo `.env.example` para `.env` e preencha corretamente:

   ```env
   TELEGRAM_TOKEN=seu_token_aqui
   USUARIOS_PERMITIDOS=12345678,87654321
   CAMINHO_SERVIDOR=C:\caminho\para\enshrouded_server.exe
   PASTA_DO_SCRIPT=caminho\para\o\script\python
   ```

### Variáveis de ambiente

- `TELEGRAM_TOKEN`: token gerado pelo BotFather no Telegram
- `USUARIOS_PERMITIDOS`: lista de IDs permitidos para usar o bot, separados por vírgula
- `CAMINHO_SERVIDOR`: caminho completo para `enshrouded_server.exe`
- `PASTA_DO_SCRIPT`: diretório em que o script será executado (usado pelo `run.bat`)

## Como executar

### Opção 1: diretamente com Python

```bash
python Script.py
```

### Opção 2: usando o arquivo batch

```bash
run.bat
```

## Comandos do bot

- `/start` — mostra uma mensagem de boas-vindas com o ID do usuário
- `/ligar` — inicia o servidor de Enshrouded, caso ele não esteja em execução
- `/desligar` — encerra o servidor de Enshrouded, caso ele esteja em execução

## Observações importantes

- O bot verifica o processo `enshrouded_server.exe` usando o comando `tasklist` do Windows.
- O comando `/desligar` solicita o encerramento de `enshrouded_server.exe` e verifica o status a cada 2 segundos por até 60 segundos. Só confirma o desligamento quando o processo não aparece mais; se ele continuar ativo ou não for possível verificar, o bot avisa que não conseguiu confirmar. Nenhum encerramento forçado é tentado.
- O salvamento do progresso durante o encerramento depende do próprio servidor de Enshrouded; o bot não consegue garantir que todo o progresso foi salvo.
- Se o `USUARIOS_PERMITIDOS` estiver vazio, qualquer usuário pode executar os comandos.
- Se `CAMINHO_SERVIDOR` não apontar para o executável do servidor ou estiver incorreto, a inicialização falhará.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
