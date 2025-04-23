# Importação de módulos necessários
# Final: Define constantes imutáveis
# os: Permite interagir com o sistema operacional
# dotenv: Carrega variáveis de ambiente de um arquivo .env
# discord: Biblioteca para interagir com a API do Discord
# responses: Módulo personalizado para lidar com respostas
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# 0. Carregar o Token do bot de algum lugar seguro
# Define o diretório base onde o arquivo .env está localizado
BASEDIR = os.path.abspath(os.path.dirname('.venv/.env'))

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(BASEDIR, '.env'))

# Obtém o token do bot armazenado na variável de ambiente "TOKEN"
TOKEN: Final[str] = os.getenv('TOKEN')

# 1. Setup do bot
# Configura os intents do bot, que definem quais eventos ele pode escutar
intents: Intents = Intents.default()
intents.message_content = True # Habilita o acesso ao conteúdo das mensagens

# Cria uma instância do cliente do Discord com os intents configurados
client: Client = Client(intents=intents)

# 2. Funcionalidade da mensagem
# Função assíncrona para enviar mensagens de resposta
async def send_message(message: Message, user_message: str) -> None:
    # Verifica se a mensagem do usuário está vazia
    if not user_message:
        print('(Mensagem estava vazia porque os intents não foram habilitados provavelmente)')
        return

    # Verifica se a mensagem é privada (começa com "?")
    if is_private := user_message[0] == '?':
        user_message = user_message[1:] # Remove o "?" do início da mensagem

    try:
        # Obtém a resposta para a mensagem do usuário usando a função get_response
        response: str = get_response(user_message)

        # Envia a resposta como mensagem privada ou no canal público
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        # Captura e exibe erros que possam ocorrer durante o envio da mensagem
        print(e)

# 3. Lidando com o startup do bot
# Evento chamado quando o bot está pronto e conectado ao Discord
@client.event
async def on_ready() -> None:
    # Exibe no console que o bot está online
    print(f'{client.user} está online!')

# 4. Lidando com mensagens recebidas
# Evento chamado sempre que uma mensagem é recebida
@client.event
async def on_message(message: Message) -> None:
    # Ignora mensagens enviadas pelo próprio bot
    if message.author == client.user:
        return

    # Extrai informações da mensagem recebida
    username: str = str(message.author) # Nome do autor da mensagem
    user_message: str = message.content # Conteúdo da mensagem
    channel: str = str(message.channel) # Canal onde a mensagem foi enviada

    # Exibe no console informações sobre a mensagem recebida
    print(f'[{channel}] {username}: "{user_message}"')

    # Chama a função para processar e enviar uma resposta
    await send_message(message, user_message)


# 5. Entry Point principal
# Função principal que inicia o bot
def main() -> None:
    # Inicia o cliente do Discord usando o token do bot
    client.run(token=TOKEN)

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    main()