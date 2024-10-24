from abc import ABC, abstractmethod
from typing import Dict

class UserDeleteInterface(ABC):
    @abstractmethod
    def delete_user(self, cpf: str) -> Dict: pass
        