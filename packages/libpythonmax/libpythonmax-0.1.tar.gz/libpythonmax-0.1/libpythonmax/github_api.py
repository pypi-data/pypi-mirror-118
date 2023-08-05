import requests


def buscar_avatar(usuario):
    """
    Busca o avatar de um usuário no Github
    :param usuario: sr com o nome de um usuário no github
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/{usuario}'
    res = requests.get(url)
    return res.json()['avatar_url']


if __name__ == '__main__':
    print("Link avatar usuário: ", buscar_avatar('maxProgrammer'))
