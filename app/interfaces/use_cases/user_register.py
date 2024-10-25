from abc import ABC, abstractmethod
from typing import Dict
class UserRegisterInterface(ABC):
    
    @abstractmethod
    def user_register(self, nome: str, cpf: str, telefone: int, email: str) -> Dict: pass
    