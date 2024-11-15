from abc import ABC, abstractmethod


class PropertyCalculatorInterface(ABC):

    @abstractmethod
    def calculate(self):
        pass

