from random import choice, randint

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