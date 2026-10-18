# Assistente do Servidor Palworld

Bot para Telegram que permite iniciar o servidor de Palworld no computador local com um comando simples via Telegram.

## Funcionalidades

- Verifica se o processo `PalServer.exe` já está em execução
- Permite iniciar o servidor com o comando `/ligar`
- Restringe o uso por IDs de usuário autorizados
- Exibe informações iniciais com o comando `/start`
- Funciona em ambiente Windows

## Requisitos

- Python 3.9 ou superior
- Sistema operacional Windows
- Telegram Bot Token
- Caminho do executável do servidor Palworld (`PalServer.exe`)

## Instalação

1. Clone o repositório e entre na pasta do projeto:

   ```bash
   git clone <url-do-repositorio>
   cd "Script PalServer"
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
   CAMINHO_SERVIDOR=C:\caminho\para\o\PalServer.exe
   PASTA_DO_SCRIPT=caminho\para\o\script\python
   ```

### Variáveis de ambiente

- `TELEGRAM_TOKEN`: token gerado pelo BotFather no Telegram
- `USUARIOS_PERMITIDOS`: lista de IDs permitidos para usar o bot, separados por vírgula
- `CAMINHO_SERVIDOR`: caminho completo para `PalServer.exe`
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
- `/ligar` — inicia o servidor de Palworld, caso ele não esteja em execução

## Observações importantes

- O bot verifica o processo `PalServer.exe` usando o comando `tasklist` do Windows.
- Se o `USUARIOS_PERMITIDOS` estiver vazio, qualquer usuário pode executar os comandos.
- Se `CAMINHO_SERVIDOR` estiver incorreto, a inicialização do servidor falhará.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
