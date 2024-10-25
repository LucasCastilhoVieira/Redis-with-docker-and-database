from abc import ABC, abstractmethod
from typing import Dict
from app.interfaces.models.Users import Users

class RedisUserInterface(ABC):
    
    @abstractmethod
    def insert_redis(self, nome: str, cpf: str, telefone: str, email: str): pass
    
    @abstractmethod
    def search_user_on_redis(self, cpf): pass
    
    @abstractmethod
    def delete_user_redis(self, cpf): pass
    
    
    @abstractmethod
    def update_user_redis(self, cpf: str, telefone = '', email = ''): pass