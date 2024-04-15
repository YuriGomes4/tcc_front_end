import requests
from . import config as sv_config

def editar_usuario(token, nome, email, senha):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/auth/usuario"

    headers = {
        'x-access-token': token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'name': nome,
        'email': email,
    }

    if senha != "":
        data['password'] = senha

    response = requests.put(update_url, headers=headers, data=data)

    if response.status_code == 200:
        return True
    else:
        return False

def ver_usuario(token):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/auth/usuario"

    headers = {
        'x-access-token': token
    }

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return {}

def ver_areas(token):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/areas"

    headers = {
        'x-access-token': token
    }

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return []

def criar_conta(nome, email, senha):
    url_base = sv_config.get('url_base')

    create_url = f"{url_base}/api/auth/signup"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'name': nome,
        'email': email,
        'password': senha
    }

    response = requests.post(create_url, headers=headers, data=data)

    if response.status_code == 201:
        return True
    else:
        return False

def login(email, senha):
    url_base = sv_config.get('url_base')

    login_url = f"{url_base}/api/auth/login"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'email': email,
        'senha': senha
    }

    response = requests.post(login_url, headers=headers, data=data)

    if response.status_code == 201:
        return response.json()['token']
    else:
        return "aaa"

def ver_area(token, id_area):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/1/areas/{id_area}"

    headers = {
        'x-access-token': token
    }

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return {}
    
def editar_area(token, id_area, nome):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/1/areas/{id_area}"

    headers = {
        'x-access-token': token
    }

    data = {
        'nome': nome
    }

    response = requests.put(update_url, headers=headers, params=data)

    if response.status_code == 200:
        return True
    else:
        return False

def add_area(token, nome, residencia):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/{residencia}/areas"

    headers = {
        'x-access-token': token
    }

    data = {
        'nome': nome,
    }

    response = requests.post(update_url, headers=headers, params=data)

    if response.status_code == 200:
        return True
    else:
        return False
    
def excluir_area(token, id_area):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/1/areas"

    headers = {
        'x-access-token': token
    }

    data = {
        'id': id_area
    }

    response = requests.delete(update_url, headers=headers, params=data)

    if response.status_code == 200:
        return True
    else:
        return False

def ver_residencia(token, id_resid):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/{id_resid}"

    headers = {
        'x-access-token': token
    }

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return {}
    
def editar_residencia(token, id_resid, nome):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/{id_resid}"

    headers = {
        'x-access-token': token
    }

    data = {
        'nome': nome
    }

    response = requests.put(update_url, headers=headers, params=data)

    if response.status_code == 200:
        return True
    else:
        return False
    
def excluir_residencia(token, id_resid):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias/{id_resid}"

    headers = {
        'x-access-token': token
    }

    response = requests.delete(update_url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False

def add_residencia(token, nome):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/residencias"

    headers = {
        'x-access-token': token
    }

    data = {
        'nome': nome
    }

    response = requests.post(update_url, headers=headers, params=data)

    if response.status_code == 200:
        return True
    else:
        return False

def dispositivos_usr(token):
    url_base = sv_config.get('url_base')  # http://127.0.0.1:5000

    update_url = f"{url_base}/api/v1/dispositivos/user"

    headers = {
        'x-access-token': token
    }

    response = requests.get(update_url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return []
    
def editar_dispositivo(token, id_disp, nome, codigo, residencia, area):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/dispositivos"

    headers = {
        'x-access-token': token
    }

    data = {
        'id': id_disp,
        'nome': nome,
        'codigo': codigo,
        'residencia': residencia,
        'area': area
    }

    response = requests.put(update_url, headers=headers, params=data)

    if response.status_code == 200:
        return True
    else:
        return False
    
def excluir_dispositivo(token, id_disp):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/dispositivos"

    headers = {
        'x-access-token': token
    }

    data = {
        'id': id_disp
    }

    response = requests.delete(update_url, headers=headers, params=data)

    if response.status_code == 200:
        return True
    else:
        return False
    
def add_dispositivo(token, tipo, nome, codigo, residencia, area):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/dispositivos"

    headers = {
        'x-access-token': token
    }

    data = {
        'tipo': tipo,
        'nome': nome,
        'codigo': codigo,
        'residencia': residencia,
        'area': area
    }

    response = requests.post(update_url, headers=headers, params=data)

    if response.status_code == 200:
        return True
    else:
        return False
    
def ver_dispositivo(token, id_disp):
    url_base = sv_config.get('url_base')

    update_url = f"{url_base}/api/v1/dispositivos"

    headers = {
        'x-access-token': token
    }

    params = {
        'id': id_disp
    }

    response = requests.get(update_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['result']
    else:
        return {}
    
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