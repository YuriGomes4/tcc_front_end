import requests
from . import config as sv_config

def dispositivos_usr():
    url_base = sv_config.get('url_base')  # http://127.0.0.1:5000

    update_url = f"{url_base}/api/v1/dispositivos/user"

    params = {
        'email': sv_config.get('email')
    }

    response = requests.get(update_url, params=params)

    if response.status_code == 200:
        #print(response.json()['result'])
        return response.json()['result']
    
def residencias_usr(token):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias"

    headers = {
        'x-access-token': token
    }

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return []
    
def areas_resid(token, id_resid):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/{id_resid}/areas"

    headers = {
        'x-access-token': token
    }

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return []
    
def verificar_token(token):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/auth/verify"

    headers = {
        'x-access-token': token
    }

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False