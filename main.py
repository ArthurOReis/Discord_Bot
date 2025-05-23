# Importação de módulos necessários
# Final: Define constantes imutáveis
# os: Permite interagir com o sistema operacional
# dotenv: Carrega variáveis de ambiente de um arquivo .env
# discord: Biblioteca para interagir com a API do Discord
# responses: Módulo personalizado para lidar com respostas
from typing import Final
import os
from discord import Message, File
from startup import load_token, initialize_client
from responses import get_response, get_link, get_media

# 0. Carregar o Token do bot de algum lugar seguro
# Define o diretório base onde o arquivo .env está localizado
BASEDIR = os.path.abspath(os.path.dirname('.venv/.env'))

# Carrega o token do bot usando o módulo startup
TOKEN: Final[str] = load_token(os.path.join(BASEDIR, '.env'))

# Inicializa o cliente do Discord
client = initialize_client()

# 2. Funcionalidade da mensagem
# Função assíncrona para enviar mensagens de resposta
async def send_message(message: Message, user_message: str) -> None:
    # Inicializa a variável para armazenar a segunda substring
    second_substring: str = ""

    # Tenta extrair a segunda substring, caso exista
    try:
        second_substring = user_message[len("!baixar"):].strip()
    except IndexError:
        pass  # Deixa a variável vazia se não houver substrings suficientes

    # Verifica se a mensagem do usuário está vazia
    if not user_message:
        print('(Mensagem estava vazia porque os intents não foram habilitados provavelmente)')
        return

    if user_message.lower().startswith("!baixar"):
        # Usa a variável second_substring no comando "!baixar"
        if second_substring:

            file_path = get_media(second_substring)
            if file_path.startswith("Erro"):
                await message.channel.send(file_path)
            else:
                await message.channel.send(file=File(file_path))

            # Verifica se o arquivo existe antes de deletar
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Arquivo {file_path} deletado com sucesso.")
                except Exception as e:
                    print(f"Erro ao deletar o arquivo {file_path}: {e}")
            else:
                print(f"Arquivo {file_path} não encontrado para exclusão.")

            link_response = get_link(second_substring)
            await message.channel.send(link_response)
        else:
            await message.channel.send("Erro: Nenhum argumento encontrado para o comando '!baixar'.")
        return

    # Verifica se a mensagem é privada (começa com "?")
    if user_message.startswith("?"):
        try:
            # Obtém a resposta para a mensagem do usuário
            response: str = get_response(user_message)
            # Envia a resposta como mensagem privada
            await message.author.send(response)
        except Exception as e:
            # Captura erros ao enviar mensagens privadas
            print(f"Erro ao enviar mensagem privada: {e}")

    else:
        try:
            # Obtém a resposta para a mensagem do usuário
            response: str = get_response(user_message)
            # Envia a resposta no canal público
            await message.channel.send(response)
        except Exception as e:
            # Captura erros ao enviar mensagens no canal
            print(f"Erro ao enviar mensagem no canal: {e}")

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