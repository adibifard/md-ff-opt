from abc import abstractmethod

from src.modules.simulation.properties.property_calculator.particle.particle_property_calculator import PropertyChangeCalculatorInterface


class EnthalpyChangeCalculatorInterface(PropertyChangeCalculatorInterface):
    @property
    @abstractmethod
    def hi(self) -> float:
        pass

    @hi.setter
    @abstractmethod
    def hi(self, value: float):
        pass

    @property
    @abstractmethod
    def hf(self) -> float:
        pass

    @hf.setter
    @abstractmethod
    def hf(self, value: float):
        pass

    @property
    @abstractmethod
    def dh(self) -> float:
        pass

    @dh.setter
    @abstractmethod
    def dh(self, value: float):
        pass