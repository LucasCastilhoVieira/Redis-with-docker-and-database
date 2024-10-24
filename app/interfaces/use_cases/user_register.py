from abc import ABC, abstractmethod
from typing import Dict
class UserRegisterInterface(ABC):
    
    @abstractmethod
    def user_register_db(self, nome: str, cpf: str, telefone: int, email: str) -> Dict: pass