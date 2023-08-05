from abc import ABC, abstractmethod
from typing import Dict


class Task(ABC):
    @staticmethod
    @abstractmethod
    def usage() -> Dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
