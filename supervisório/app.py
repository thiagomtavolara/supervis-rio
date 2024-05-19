import subprocess
import os
from flask import Flask, redirect, render_template, request, jsonify
from dash_application.dash import create_dash_application
import sqlite3
from flask_socketio import SocketIO, emit
import threading
import time
import funcoes_banco_de_dados

app = Flask(__name__)

create_dash_application(app)

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


@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

# Rota para a página "Experimentos"


@app.route('/experimentos')
def experiments():

    # Renderize o template 'experiments.html' passando o gráfico como um objeto
    return render_template('experiments.html')

# Rota para a página "Sobre"


@app.route('/sobre')
def about():
    return render_template('about.html')


# Defina uma chave secreta para o SocketIO
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)


@app.route('/index')
def index():
    dados = funcoes_banco_de_dados.consultar_ultimo_id_banco_dados()

    return render_template('index.html', dados=dados)


@app.route('/')
def home():
    return render_template('login.html')


# Rota para realizar o login
@app.route('/login', methods=['POST'])
def login():

    nome = request.form.get('username')
    senha = request.form.get('password')

 #Deixei um usuário e senha de teste para testar se o login funciona
 #Porém pode ser criado um sistema de usuario e senha com json ou banco de dados
    if nome == 'Thiago' and senha == '123':

        return redirect('/index')
    else:

        return redirect('/')

# Rota para conectar o cliente ao servidor Socket.IO
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')


if __name__ == '__main__':
    # Iniciar o servidor Flask com Socket.IO
    socketio.run(app, debug=True)
