import os
from random import choice, randint
import requests
from bs4 import BeautifulSoup
import yt_dlp

# Testando a função de respostas prontas com base na entrada do usuário
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    # Respostas baseadas em palavras-chave
    if lowered == '':
        return 'Você tá muito quieto...'
    elif 'oi' in lowered:
        return 'Eae!'
    elif 'tchau' in lowered:
        return 'Tchau! :)'
    elif 'batata' in lowered:
        return 'Tomate'
    elif 'javascript' in lowered:
        return 'Typescript!'
    elif 'rodar dado' in lowered:
        return f'Resultado: {randint(1,6)}'
    else:
        return choice(['Não entendi! :(',
                       'Pode repetir?',
                       'Tente falar alguma palavra-chave'])

# Função para obter o título de um link do YouTube
def get_link(link_input: str) -> str:
    try:
        # Faz a requisição GET para o link do YouTube
        response = requests.get(link_input)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        # Faz o parsing do HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrai o título da página
        title = soup.find('title').text

        if not title:
            return 'Título não encontrado.'

        return title
    except requests.exceptions.RequestException as e:
        # Retorna erro caso a requisição falhe
        return f'Erro ao acessar o link: {e}'
    except Exception as e:
        # Retorna erro caso ocorra algum problema no processamento
        return f'Erro ao processar título: {e}'

# Função para baixar mídia de um link do YouTube
def get_media(link_input: str, output_dir: str = "temp") -> str:
    try:
        # Verifica se o link é válido
        if not link_input.startswith("https"):
            return "Erro: O link fornecido não é válido."

        # Cria o diretório de saída, se não existir
        os.makedirs(output_dir, exist_ok=True)

        # Configurações para o yt-dlp
        ydl_opts = {
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Nome do arquivo de saída
            'format': 'bestvideo+bestaudio/best',  # Melhor qualidade de vídeo e áudio
            'merge_output_format': 'mp4'  # Formato de saída
        }

        # Faz o download do vídeo usando yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link_input, download=True)
            return ydl.prepare_filename(info)

    except Exception as e:
        # Retorna erro caso o download falhe
        return f"Erro ao baixar o vídeo com yt_dlp: {e}"
