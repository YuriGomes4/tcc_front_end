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