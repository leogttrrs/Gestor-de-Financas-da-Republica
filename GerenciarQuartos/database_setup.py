import sqlite3

def conectar_db():
    conn = sqlite3.connect('quartos.db')
    return conn

def criar_tabela_quartos(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quartos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER UNIQUE NOT NULL,
            tamanho REAL NOT NULL,
            capacidade INTEGER NOT NULL,
            status TEXT NOT NULL,
            moradores_ids_str TEXT
        )
    """)
    conn.commit()