import time
import threading
import subprocess
import os
from flask import Flask, render_template, request, jsonify
from dash_application.dash import create_dash_application
from flask_socketio import SocketIO, emit

import banco_de_dados_configuracoes
import banco_de_dados_experimentos

app = Flask(__name__)
create_dash_application(app)

# Defina uma chave secreta para o SocketIO
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

# Defina a rota inicial
@app.route('/')
def index():
    if not os.path.exists('dados_experimentos.db'): 
        banco_de_dados_experimentos.criar_banco_dados()
        banco_de_dados_experimentos.inserir_banco_dados(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    if not os.path.exists('dados_planta.db'):
        banco_de_dados_configuracoes.criar_banco_dados()
        banco_de_dados_configuracoes.inserir_banco_dados(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
  
    dados_experimentos = banco_de_dados_experimentos.consultar_ultimo_id_banco_dados()
    dados_configuracoes = banco_de_dados_configuracoes.consultar_ultimo_id_banco_dados()

    return render_template('index.html', dados_experimentos=dados_experimentos, dados_configuracoes=dados_configuracoes)

# Defina a rota para os dados
@app.route('/dados')
def dados():
    dados_experimentos = banco_de_dados_experimentos.consultar_ultimo_id_banco_dados()
    dados_configuracoes = banco_de_dados_configuracoes.consultar_ultimo_id_banco_dados()
    return jsonify({
        'dados_experimentos': dados_experimentos,
        'dados_configuracoes': dados_configuracoes
    })

# Defina a rota para a página tempo real
@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

# Defina a rota para a página de experimentos
@app.route('/experimentos')
def experiments():
    return render_template('experiments.html')

# Defina a rota para a página de experimentos
@app.route('/sobre')
def about():
    return render_template('about.html')

# Defina a rota para iniciar o Arduino
@app.route('/start_arduino', methods=['GET'])
def start_arduino():
    try:
        arduino_path = r'C:\Users\usuario\AppData\Local\Programs\Arduino IDE\Arduino IDE.exe'
        subprocess.Popen([arduino_path])
        return jsonify({"status": "success", "message": "Arduino IDE started"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Defina a rota para atualizar os dados
@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.json
    try:
        banco_de_dados_configuracoes.atualizar_banco_dados(
            1,
            data['T0'], data['T1'], data['T2'], data['T3'],
            data['P0'], data['P1'], data['P2'], data['P3'],
            data['B1'], data['B2'], data['B3']
        )
        return jsonify({"status": "success", "message": "Data updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Defina a rota para o SocketIO
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    emit('message', {'data': 'Connected'})
    thread = threading.Thread(target=send_data)
    thread.start()

# Defina a rota para enviar os dados
def send_data():
    while True:
        dados_experimentos = banco_de_dados_experimentos.consultar_ultimo_id_banco_dados()
        dados_configuracoes = banco_de_dados_configuracoes.consultar_ultimo_id_banco_dados()
        socketio.emit('update_data', {
            'dados_experimentos': dados_experimentos,
            'dados_configuracoes': dados_configuracoes
        })
        time.sleep(5)


if __name__ == '__main__':
    banco_de_dados_configuracoes.criar_banco_dados()
    socketio.run(app, debug=True)
