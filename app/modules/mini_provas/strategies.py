from abc import ABC, abstractmethod
import random
from typing import List

class RandomizationStrategy(ABC):
    """ Padrão GoF: Strategy """
    @abstractmethod
    def execute(self, items: List) -> List: pass

class ShuffleStrategy(RandomizationStrategy):
    def execute(self, items: List) -> List:
        items_copy = items.copy()
        random.shuffle(items_copy)
        return items_copy

class NoOpStrategy(RandomizationStrategy):
    def execute(self, items: List) -> List: return items