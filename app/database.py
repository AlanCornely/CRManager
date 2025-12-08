import mysql.connector
from mysql.connector import Error
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "3306")
        self.database = os.getenv("DB_NAME", "crm_estoque")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.connection = None
    
    def get_connection(self):
        """Cria e retorna uma conexão com o banco de dados"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=int(self.port),
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
    
    def execute_query(self, query: str, params: tuple = None, fetch_one: bool = False):
        """Executa uma query SQL"""
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith("SELECT"):
                if fetch_one:
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.lastrowid
            
            return result
        except Error as e:
            print(f"Erro ao executar query: {e}")
            connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
    
    def execute_many(self, query: str, params_list: list):
        """Executa múltiplas queries"""
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.executemany(query, params_list)
            connection.commit()
            return True
        except Error as e:
            print(f"Erro ao executar múltiplas queries: {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

# Instância global do banco de dados
db = Database()