from flask import Flask, render_template, request, jsonify
from dash_application.dash import create_dash_application
import sqlite3
from flask_socketio import SocketIO, emit
import threading
import time

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

# Função para obter os dados mais recentes do banco de dados


def obter_dados():
    conn = sqlite3.connect('dados_planta.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT T0, T1, T2, T3, P0, P1, P2, P3, B1, B2, B3 FROM variaveis ORDER BY id DESC LIMIT 1')
    dados = cursor.fetchone()
    conn.close()
    return dados

# Rota para a página index


@app.route('/')
def index():
    dados = obter_dados()
    return render_template('index.html', dados=dados)

# Function to update and send data


def atualizar_e_enviar_dados():
    dados_anteriores = None
    while True:
        dados = obter_dados()
        if dados != dados_anteriores:
            socketio.emit('atualizar_dados', dados)
            dados_anteriores = dados
        time.sleep(5)  # Update data every 5 seconds


# Rota para conectar o cliente ao servidor Socket.IO
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')


if __name__ == '__main__':
    # Iniciar a thread em segundo plano para atualizar e enviar os dados
    threading.Thread(target=atualizar_e_enviar_dados).start()
    # Iniciar o servidor Flask com Socket.IO
    socketio.run(app, debug=True)
