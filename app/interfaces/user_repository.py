from abc import ABC, abstractmethod
from typing import List
from app.interfaces.models.Users import Users



class UserRepositoryInterface(ABC):
    
    @abstractmethod
    def insert(self, nome: str, cpf: str, telefone: str, email: str): pass 
    
    @abstractmethod
    def select(self,cpf) -> List[Users]: pass
        
    @abstractmethod
    def remove_user(self, cpf): pass
    
    
    @abstractmethod
    def update_user(self, cpf: str, email = '', telefone = ''): pass
        
