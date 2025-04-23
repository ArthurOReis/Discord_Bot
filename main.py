# from http.client import responses
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# 0. Carregar o Token do bot de algum lugar seguro

BASEDIR = os.path.abspath(os.path.dirname('.venv/.env'))
load_dotenv(os.path.join(BASEDIR, '.env'))
TOKEN: Final[str] = os.getenv('TOKEN')

# 1. Setup do bot

intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

# 2. Funcionalidade da mensagem

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Mensagem estava vazia porque os intents não foram habilitados provavelmente)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# 3. Lidando com o startup do bot

@client.event
async def on_ready() -> None:
    print(f'{client.user} está online!')

# 4. Lidando com mensagens recebidas

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


# 5. Entry Point principal

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()