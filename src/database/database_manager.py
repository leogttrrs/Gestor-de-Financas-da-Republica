import sqlite3
from typing import List, Dict, Any


class DatabaseManager:
    def __init__(self, db_path: str = "republica.db"):
        self.db_path = db_path
        self._connection = None
        self._criar_tabelas()

    def __enter__(self):
        self._connection = self._obter_conexao()
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection:
            if exc_type is None:
                self._connection.commit()
            else:
                self._connection.rollback()
            self._connection.close()
            self._connection = None

    def _obter_conexao(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _criar_tabelas(self):
        with self._obter_conexao() as conn:
            cursor = conn.cursor()

            # Tabela Usuario
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpf TEXT NOT NULL UNIQUE,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('administrador','morador')),
                    senhaCriptografada TEXT NOT NULL,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela Republica
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS republica (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                administrador_id INTEGER NOT NULL UNIQUE,
                                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (administrador_id) REFERENCES usuario(id) ON DELETE CASCADE
                            )
                        """)

            # Tabela Quarto
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS quarto (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                numero_quarto INTEGER NOT NULL,
                                tamanho INTEGER NOT NULL,
                                republica_id INTEGER NOT NULL,
                                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (republica_id) REFERENCES republica(id) ON DELETE CASCADE,
                                UNIQUE(numero_quarto, republica_id)
                            )
                        """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contrato (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    morador_id INTEGER NOT NULL,
                    quarto_id INTEGER,
                    data_inicio DATE NOT NULL,
                    data_fim DATE,
                    valor_aluguel DECIMAL(10,2) NOT NULL,
                    status TEXT NOT NULL DEFAULT 'ativo' CHECK (status IN ('agendado', 'ativo', 'finalizado')),
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (quarto_id) REFERENCES quarto(id) ON DELETE SET NULL,
                    FOREIGN KEY (morador_id) REFERENCES usuario(id) ON DELETE CASCADE
                )
            """)

            # Tabela Divida
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS divida (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    morador_id INTEGER NOT NULL,
                    valor DECIMAL(10,2) NOT NULL,
                    descricao TEXT,
                    data_vencimento DATE NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'quitada')),
                    FOREIGN KEY (morador_id) REFERENCES usuario(id) ON DELETE CASCADE
                )
            """)

            # Tabela Historico
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS historico (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                evento TEXT NOT NULL,
                                morador_nome TEXT,
                                divida_descricao TEXT,
                                valor REAL,
                                detalhes TEXT
                            )
                        """)

            # Tabela Recorrencia
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recorrencia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    valor DECIMAL(10,2) NOT NULL,
                    data_inicio DATE NOT NULL,
                    data_fim DATE NOT NULL,
                    periodicidade TEXT NOT NULL CHECK (periodicidade IN ('semanal', 'mensal', 'bimestral', 'trimestral', 'anual')),
                    descricao TEXT,
                    ativo BOOLEAN NOT NULL DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela Pagamento
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pagamento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    divida_id INTEGER NOT NULL,
                    valor DECIMAL(10,2) NOT NULL,
                    data_pagamento DATE NOT NULL,
                    status TEXT NOT NULL DEFAULT 'confirmado' CHECK (status IN ('pendente', 'confirmado', 'cancelado')),
                    FOREIGN KEY (divida_id) REFERENCES divida(id) ON DELETE CASCADE
                )
            """)

            # Tabela Ocorrencia
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ocorrencia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    morador_id INTEGER NOT NULL,
                    descricao TEXT NOT NULL,
                    data_ocorrencia TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status BOOL NOT NULL,
                    prioridade TEXT NOT NULL DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta', 'urgente')),
                    categoria TEXT,
                    FOREIGN KEY (morador_id) REFERENCES usuario(id) ON DELETE CASCADE
                )
            """)

            # Tabela Alerta
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    republica_id INTEGER NOT NULL,
                    descricao TEXT NOT NULL,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (republica_id) REFERENCES republica(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def executar_query(self, query: str, parametros: tuple = ()) -> List[Dict[str, Any]]:
        with self._obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            colunas = [desc[0] for desc in cursor.description]
            resultados = cursor.fetchall()
            return [dict(zip(colunas, linha)) for linha in resultados]

    def executar_comando(self, comando: str, parametros: tuple = ()) -> int:
        with self._obter_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(comando, parametros)
            conn.commit()
            return cursor.lastrowid if comando.strip().upper().startswith('INSERT') else cursor.rowcount

    def executar_transacao(self, comandos: List[tuple]) -> bool:
        try:
            with self._obter_conexao() as conn:
                cursor = conn.cursor()
                for comando, parametros in comandos:
                    cursor.execute(comando, parametros)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f" Erro na transação: {e}")
            return False

    def verificar_integridade(self) -> Dict[str, Any]:
        with self._obter_conexao() as conn:
            cursor = conn.cursor()

            cursor.execute("PRAGMA foreign_key_check")
            problemas_fk = cursor.fetchall()

            cursor.execute("PRAGMA integrity_check")
            integridade = cursor.fetchone()[0]

            return {
                "integridade_geral": integridade,
                "problemas_chaves_estrangeiras": len(problemas_fk),
                "detalhes_problemas": problemas_fk
            }

    def obter_estatisticas(self) -> Dict[str, int]:
        estatisticas = {}
        tabelas = [
            'usuario', 'republica',
            'quarto', 'contrato', 'divida', 'pagamento',
            'ocorrencia', 'alerta', 'recorrencia'
        ]

        with self._obter_conexao() as conn:
            cursor = conn.cursor()
            for tabela in tabelas:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                estatisticas[tabela] = cursor.fetchone()[0]

        return estatisticas

    def backup_database(self, backup_path: str) -> bool:
        try:
            with self._obter_conexao() as conn:
                with open(backup_path, 'w') as f:
                    for linha in conn.iterdump():
                        f.write('%s\n' % linha)
            print(f"Backup criado com sucesso: {backup_path}")
            return True
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return False