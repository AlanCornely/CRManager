import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "crm_estoque.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables from database.sql if they don't exist
    sql_file = os.path.join(os.path.dirname(__file__), "database.sql")
    if os.path.exists(sql_file):
        with open(sql_file, 'r', encoding='utf-8') as f:
            script = f.read()
            # Note: SQLite does not support AUTO_INCREMENT (uses AUTOINCREMENT instead, or INTEGER PRIMARY KEY).
            script = script.replace("AUTO_INCREMENT", "AUTOINCREMENT")
            # SQLite does not support multiple foreign keys precisely like MySQL, but we'll try running it if DB is empty
            try:
                cursor.executescript(script)
            except sqlite3.Error as e:
                # Tables likely already exist or syntax differences
                pass
    
    # Safely alter table to add columns for CLIENTES and PRODUTOS
    try:
        cursor.execute("ALTER TABLE CLIENTES ADD COLUMN role VARCHAR(50) DEFAULT 'Cliente'")
    except Exception:
        pass
        
    try:
        cursor.execute("ALTER TABLE CLIENTES ADD COLUMN spent DECIMAL(10, 2) DEFAULT 0.0")
    except Exception:
        pass

    # Insert Breadscrum LTDA if missing
    cursor.execute("SELECT COUNT(*) FROM CLIENTES WHERE nome = 'Breadscrum LTDA'")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO CLIENTES (nome, email, role, spent) 
            VALUES ('Breadscrum LTDA', 'contato@breadscrum.com', 'Cliente', 10500.0)
        ''')

    # Also make sure there are some mock data in PRODUTOS 
    cursor.execute("SELECT COUNT(*) FROM PRODUTOS")
    if cursor.fetchone()[0] == 0:
        produtos = [
            ('Teclado Mecânico Sem Fio', 'SKU-001', 145, 620.0),
            ('Fone de Ouvido Noise Cancelling', 'SKU-004', 67, 1210.0),
        ]
        for p in produtos:
            cursor.execute('''
                INSERT INTO PRODUTOS (nome, categoria_id, sku, quantidade_atual, preco_venda, preco_custo, data_cadastro, ativo)
                VALUES (?, 1, ?, ?, ?, 0.0, '2025-01-01', 1)
            ''', p)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
