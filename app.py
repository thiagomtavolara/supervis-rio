import subprocess
import os
from flask import Flask, render_template, request, jsonify
from dash_application.dash import create_dash_application
import sqlite3
from flask_socketio import SocketIO, emit
import threading
import time
import funcoes_banco_de_dados

app = Flask(__name__)

create_dash_application(app)


# Defina uma chave secreta para o SocketIO
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

# Rota para a página "Home"
@app.route('/')
def index():
    dados = funcoes_banco_de_dados.consultar_ultimo_id_banco_dados()

    return render_template('index.html', dados=dados)


@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

# Rota para a página "Experimentos"


@app.route('/experimentos')
def experiments():
    return render_template('experiments.html')

# Rota para a página "Sobre"


@app.route('/sobre')
def about():
    return render_template('about.html')


# Rota para iniciar o Arduino TÁ FUNCIONANDO
@app.route('/start_arduino', methods=['GET'])
def start_arduino():
    try:
        # Caminho para o executável do Arduino IDE (ajuste conforme necessário)
        arduino_path = r'C:\Users\usuario\AppData\Local\Programs\Arduino IDE\Arduino IDE.exe'

        # Inicia o Arduino IDE
        subprocess.Popen([arduino_path])

        return jsonify({"status": "success", "message": "Arduino IDE started"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Rota para armazenar no banco de dados as configurações TÁ FUNCIONANDO


@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.json
    try:
        funcoes_banco_de_dados.inserir_banco_dados(
            data['T0'], data['T1'], data['T2'], data['T3'], data['P0'], data['P1'], data['P2'], data['P3'], data['B1'], data['B2'], data['B3'])

        return jsonify({"status": "success", "message": "Data updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Rota para conectar o cliente ao servidor Socket.IO
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')


if __name__ == '__main__':
    funcoes_banco_de_dados.criar_banco_dados()
    # Iniciar o servidor Flask com Socket.IO
    socketio.run(app, debug=True)
