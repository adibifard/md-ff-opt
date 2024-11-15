from abc import ABC, abstractmethod


class SimDataProcessorInterface(ABC):
    @property
    @abstractmethod
    def sim_data(self):
        pass

    @sim_data.setter
    @abstractmethod
    def sim_data(self, value):
        pass

    @abstractmethod
    def process(self):
        pass







