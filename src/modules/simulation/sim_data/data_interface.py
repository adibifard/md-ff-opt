from abc import ABC, abstractmethod
from typing import Dict


class SimDataInterface(ABC):
    @abstractmethod
    def add(self):
        raise NotImplementedError("Subclasses must implement add()")

    @property
    @abstractmethod
    def data(self) -> Dict:
        pass

    @data.setter
    @abstractmethod
    def data(self, value: Dict):
        pass



class OutputSimData(SimDataInterface):
    def __init__(self):
        self._data = dict()

    @property
    def data(self) -> Dict:
        return self._data

    @data.setter
    def data(self, value: Dict):
        self._data = value

    def add(self, key, data):
        self.data[key] = data
        return self


class ThermoData:
    def __init__(self, T=None, p=None, vol=None):
        self._Temp = T
        self._Press = p
        self._Vol = vol

    @property
    def Temp(self) -> float:
        return self._Temp

    @Temp.setter
    def Temp(self, value: float):
        if value >= 0:
            self._Temp = value
        else:
            raise ('Error: absolute temperature must be positive.')

    @property
    def Press(self) -> float:
        return self._Press

    @Press.setter
    def Press(self, value: float):
        if value >= 0:
            self._Press = value
        else:
            raise ('Error: pressure cannot be negative.')

    @property
    def Vol(self) -> float:
        return self._Vol

    @Temp.setter
    def Vol(self, value: float):
        if value > 0:
            self._Vol = value
        else:
            raise ('Error: volume must be positive.')

    def is_all_none(self):
        # Using all() with a generator expression to check if all attributes are None
        return all(value is None for value in vars(self).values())

