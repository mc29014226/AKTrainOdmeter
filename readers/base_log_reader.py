from abc import ABC, abstractmethod

from models.train import Train


class BaseLogReader(ABC):
    @abstractmethod
    def read_tail(self, train: Train, remote_path: str, line_count: int = 800) -> str:
        """Return the newest section of a train log as text."""
        raise NotImplementedError
