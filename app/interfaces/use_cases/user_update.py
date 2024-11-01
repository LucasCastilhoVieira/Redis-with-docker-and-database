from abc import ABC, abstractmethod
from typing import Dict
class UserUpdateInterface(ABC):
    
    @abstractmethod
    def update_user(self, cpf: str, telefone: str, email: str) -> Dict:
        pass