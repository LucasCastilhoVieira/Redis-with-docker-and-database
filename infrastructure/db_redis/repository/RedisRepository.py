from app.interfaces.redis_repository import RedisUserInterface
from infrastructure.db_redis.settings.connection import RedisConnectionHandler
import json





class UserRedisRepository(RedisUserInterface):
    def __init__(self):
        self.redis = RedisConnectionHandler().connect()
    
    def insert_redis(self, nome: str, cpf: str, telefone: str, email: str): 
        user_json = {
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "email": email
        }
        
        info = json.dumps(user_json)
        self.redis.set(cpf, info)
    
    def search_user_on_redis(self, cpf):
        search = self.redis.get(cpf)
        if search is None:
            return None
        else:
            user_info = json.loads(search)
            return user_info
    
    
    def delete_user_redis(self, cpf):
        self.redis.delete(cpf)
        
        
    def update_user_redis(self, cpf: str, email = '', telefone = ''):
        user = self.redis.get(cpf)
        if user is None:
            return None
        else:
            user_redis = json.loads(user)
            if not email:
                user_redis['telefone'] = telefone
            if not telefone:
                user_redis['email'] = email
                
            if email and telefone:
                user_redis['telefone'] = telefone
                user_redis['email'] = email
            user = json.dumps(user_redis)
            self.redis.set(cpf, user)        

