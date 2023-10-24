from abc import ABC, abstractmethod


class ConnectionEngine(ABC):
    @classmethod
    @abstractmethod
    def start(cls, db_credentials: dict):
        pass
