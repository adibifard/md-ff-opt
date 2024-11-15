from abc import ABC, abstractmethod


class ReactionPropertiesInterface(ABC):

    @property
    @abstractmethod
    def dH(self):
        pass

    @dH.setter
    @abstractmethod
    def dH(self, value):
        pass


class PhysicalReactionProperties(ReactionPropertiesInterface):
    def __int__(self):
        self._dH = None

    @property
    def dH(self) -> float:
        return self._dH

    @dH.setter
    def dH(self, value: float):
        self._dH = value


class ChemicalReactionProperties(ReactionPropertiesInterface):
    def __int__(self):
        self._dH = None

    @property
    def dH(self) -> float:
        return self._dH

    @dH.setter
    def dH(self, value: float):
        self._dH = value
