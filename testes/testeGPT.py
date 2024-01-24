from flask import Flask, request, render_template, redirect, url_for
import os
import requests

app = Flask(__name__)

import socket

def get_local_ip():
    try:
        # Cria um socket UDP para obter o endereço IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conecta a um servidor público (Google DNS) apenas para obter o endereço IP local
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return None

ip = get_local_ip()

# Defina o diretório onde os arquivos serão salvos no repositório local
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'O arquivo "{filename}" foi enviado com sucesso e salvo no repositório local.'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
