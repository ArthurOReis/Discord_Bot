from random import choice, randint
import requests
from bs4 import BeautifulSoup

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

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
        return f'Erro ao acessar o link: {e}'
    except Exception as e:
        return f'Erro ao processar título: {e}'