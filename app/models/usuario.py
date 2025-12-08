from app.database import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioModel:
    """Modelo para a tabela USUARIOS"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        """Verifica se a senha está correta"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str):
        """Gera hash da senha"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create(data: dict):
        query = """
        INSERT INTO USUARIOS (nome, email, senha_hash, cargo, permissao, ativo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        hashed_password = UsuarioModel.get_password_hash(data['senha'])
        params = (
            data['nome'], data['email'], hashed_password,
            data.get('cargo'), data.get('permissao'), data.get('ativo', True)
        )
        return db.execute_query(query, params)
    
    @staticmethod
    def get_all():
        query = "SELECT id_usuario, nome, email, cargo, permissao, ativo FROM USUARIOS"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(id_usuario: int):
        query = "SELECT id_usuario, nome, email, cargo, permissao, ativo FROM USUARIOS WHERE id_usuario = %s"
        return db.execute_query(query, (id_usuario,), fetch_one=True)
    
    @staticmethod
    def get_by_email(email: str):
        query = "SELECT * FROM USUARIOS WHERE email = %s"
        return db.execute_query(query, (email,), fetch_one=True)
    
    @staticmethod
    def authenticate(email: str, password: str):
        """Autentica usuário"""
        user = UsuarioModel.get_by_email(email)
        if not user:
            return None
        
        if not UsuarioModel.verify_password(password, user['senha_hash']):
            return None
        
        # Remove senha do resultado
        user.pop('senha_hash', None)
        return user
    
    @staticmethod
    def update(id_usuario: int, data: dict):
        query = """
        UPDATE USUARIOS SET
            nome = COALESCE(%s, nome),
            email = COALESCE(%s, email),
            cargo = COALESCE(%s, cargo),
            permissao = COALESCE(%s, permissao),
            ativo = COALESCE(%s, ativo)
        WHERE id_usuario = %s
        """
        params = (
            data.get('nome'), data.get('email'),
            data.get('cargo'), data.get('permissao'),
            data.get('ativo'), id_usuario
        )
        return db.execute_query(query, params)
    
    @staticmethod
    def update_password(id_usuario: int, new_password: str):
        """Atualiza senha do usuário"""
        hashed_password = UsuarioModel.get_password_hash(new_password)
        query = "UPDATE USUARIOS SET senha_hash = %s WHERE id_usuario = %s"
        return db.execute_query(query, (hashed_password, id_usuario))
    
    @staticmethod
    def delete(id_usuario: int):
        query = "DELETE FROM USUARIOS WHERE id_usuario = %s"
        return db.execute_query(query, (id_usuario,))