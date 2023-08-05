import abc
from typing import Dict, Any


class PiperTask(abc.ABC):

    @abc.abstractmethod
    def perform(self, context: str, config: Dict[str, Any]) -> None:
        pass

