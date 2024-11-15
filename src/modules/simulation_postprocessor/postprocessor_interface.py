
from abc import ABC, abstractmethod
from src.modules.simulation.sim_case.lammps_sim_case import SimCaseInterface

class PostProcessorInterface(ABC):
    @abstractmethod
    def process(self):
        raise NotImplementedError("Subclasses must implement process()")

    @property
    @abstractmethod
    def sim_case(self) -> SimCaseInterface:
        pass

    @sim_case.setter
    @abstractmethod
    def sim_case(self, value: SimCaseInterface):
        pass

