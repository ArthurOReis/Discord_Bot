from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client

def load_token(env_path: str) -> Final[str]:
    """Carrega o token do bot a partir do arquivo '.env'"""
    load_dotenv(env_path)
    return os.getenv('TOKEN')

def initialize_client() -> Client:
    """Inicializa e retorna o cliente do Discord com os intents configurados."""
    intents: Intents = Intents.default()
    intents.message_content = True
    return Client(intents=intents)