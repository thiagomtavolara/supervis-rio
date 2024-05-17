from flask import Flask, render_template, request, jsonify
from dash_application.dash import create_dash_application
import sqlite3
from flask_socketio import SocketIO, emit
import threading
import time
import funcoes_banco_de_dados

app = Flask(__name__)

create_dash_application(app)


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


@app.route('/')
def index():
    dados = funcoes_banco_de_dados.consultar_ultimo_id_banco_dados()

    return render_template('index.html', dados=dados)


# Rota para conectar o cliente ao servidor Socket.IO
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')


if __name__ == '__main__':
    # Iniciar o servidor Flask com Socket.IO
    socketio.run(app, debug=True)
