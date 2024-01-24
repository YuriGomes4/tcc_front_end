from . import config as sv_config
import navigation

import requests

token = ""

def login(email, senha):

    url_base = sv_config.get('url_base')  # http://127.0.0.1:5000

    update_url = f"{url_base}/api/auth/login"

    print(email, senha)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f'email={email}&senha={senha}'

    response = requests.post(update_url, headers=headers, data=data)

    if response.status_code == 201:
        print("Login aprovado!")
        token = response.json()['token']
        sv_config.set('email', email)
        navigation.NavigationChange(e=None, screen="00")
    else:
        print("Usuário e/ou senha incorreto!")
        navigation.notify("Usuário e/ou senha incorreto!")

def verify_access():
    url_base = sv_config.get('url_base')  # http://127.0.0.1:5000

    headers = {
        'x-access-token' : token,
    }

    update_url = f"{url_base}/api/auth/verify"

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        print("Login aprovado!")
        navigation.NavigationChange(e=None, screen="00")