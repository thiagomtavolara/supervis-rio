import sqlite3

from flask_socketio import SocketIO, emit
import time

import socketio

# Função para criar o banco de dados e a tabela
def criar_banco_dados():
    # Conectar ao banco de dados (se não existir, será criado)
    conn = sqlite3.connect('dados_planta.db')

    # Criar uma tabela se não existir
    conn.execute('''
        CREATE TABLE IF NOT EXISTS variaveis (
            id INTEGER PRIMARY KEY,
            T0 REAL,
            T1 REAL,
            T2 REAL,
            T3 REAL,
            P0 REAL,
            P1 REAL,
            P2 REAL,
            P3 REAL,
            B1 REAL,
            B2 REAL,
            B3 REAL
        )
    ''')

    # Fechar a conexão
    conn.close()

# Função para inserir dados na tabela
def inserir_dados(T0, T1, T2, T3, P0, P1, P2, P3, B1, B2, B3):
    # Conectar ao banco de dados
    conn = sqlite3.connect('dados_planta.db')

    # Inserir dados na tabela
    dados = (T0, T1, T2, T3, P0, P1, P2, P3, B1, B2, B3)
    conn.execute('''
        INSERT INTO variaveis (T0, T1, T2, T3, P0, P1, P2, P3, B1, B2, B3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)

    # Commit para salvar as alterações
    conn.commit()

    # Fechar a conexão
    conn.close()

# Função para consultar dados na tabela
def consultar_dados():
    # Conectar ao banco de dados
    conn = sqlite3.connect('dados_planta.db')

    # Consultar dados
    cursor = conn.execute('SELECT * FROM variaveis')
    for row in cursor:
        print(row)

    # Fechar a conexão
    conn.close()


# Função para obter os dados mais recentes do banco de dados
def obter_dados():
  conn = sqlite3.connect('dados_planta.db')
  cursor = conn.cursor()
  cursor.execute('SELECT T0, T1, T2, T3, P0, P1, P2, P3, B1, B2, B3 FROM variaveis ORDER BY id DESC LIMIT 1')
  dados = cursor.fetchone()
  conn.close()
  return dados

# Função para atualizar os dados e enviar via Socket.IO
def atualizar_e_enviar_dados():
  while True:
    dados = obter_dados()
    socketio.emit('atualizar_dados', dados)
    time.sleep(5)  # Aguardar 5 segundos antes de verificar novamente




# Criar o banco de dados e a tabela
##criar_banco_dados()

# Inserir dados de exemplo na tabela
inserir_dados(5, 26, 5, 22.8, 10.1, 9.8, 9.9, 10.2, 3.5, 4.0, 3.8)

# Consultar e exibir os dados da tabela
print("Dados armazenados na tabela:")
consultar_dados()