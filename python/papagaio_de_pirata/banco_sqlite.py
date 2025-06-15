import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "contas.db"

def conectar():
    conn = sqlite3.connect(DB_PATH)
    return conn

def inicializar_banco():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                vencimento TEXT NOT NULL,
                url TEXT,
                status TEXT DEFAULT 'pendente'
            )
        ''')
        conn.commit()

def adicionar_conta(nome, vencimento, url):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contas (nome, vencimento, url) VALUES (?, ?, ?)",
            (nome, vencimento, url)
        )
        conn.commit()

def listar_contas(status=None):
    with conectar() as conn:
        cursor = conn.cursor()
        if status:
            cursor.execute("SELECT * FROM contas WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM contas")
        return cursor.fetchall()

def contas_proximas(dias=3):
    hoje = datetime.today().date()
    limite = hoje.replace(day=hoje.day + dias)
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM contas
            WHERE status = 'pendente'
            AND vencimento <= ?
        ''', (limite.isoformat(),))
        return cursor.fetchall()

def marcar_como_paga(id_conta):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE contas SET status = 'pago' WHERE id = ?", (id_conta,))
        conn.commit()
