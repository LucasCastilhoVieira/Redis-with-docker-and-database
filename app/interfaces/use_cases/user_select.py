from abc import ABC, abstractmethod
from typing import Dict


class UserSelectInfoInterface(ABC):
    @abstractmethod
    def select_user(self, cpf: str) -> Dict:
        pass