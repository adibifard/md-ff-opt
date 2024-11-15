import os
import re
from abc import ABC, abstractmethod

from src.modules.simulation.sim_data.data_interface import ThermoData
from src.modules.simulation.component.particle.particles import Particles
from src.modules.simulation.forcefield.forcefield import ForceFieldInterface
from src.modules.config_loaders.config_loader import SimCaseConfigs

class SimCaseFileFolderManager:
    configs = SimCaseConfigs

    def __init__(self, sim_case_path, path_to_folder_of_log_file):
        self._sim_case_path = sim_case_path
        self.path_to_folder_of_log_file = path_to_folder_of_log_file
        self.log_file_path = self._get_log_file_path()

    @property
    def sim_case_path(self):
        return self._sim_case_path

    def _get_log_file_path(self):
        sim_number = re.findall(r'\d+$', self.sim_case_path)
        sim_number = sim_number[0] if sim_number else None
        if self._sim_case_path != self.path_to_folder_of_log_file:
            log_file_name = self.configs.LAMMPS_LOG_FILE_TEMPLATE_NAME + "." + str(sim_number)
        else:
            log_file_name = self.configs.FileNames.LAMMPS_LOG_FILE_TEMPLATE_NAME
        for root, dirs, files in os.walk(self.path_to_folder_of_log_file):
            if log_file_name in files:
                return os.path.join(root, log_file_name)


class SimCaseInterface(ABC):
    '''
    class methods
    '''
    @abstractmethod
    def read_output_data(self):
        raise NotImplementedError("Subclasses must implement read_data()")


    '''
    class attributes
    '''


    @property
    @abstractmethod
    def sim_case_file_folder(self) -> SimCaseFileFolderManager:
        pass

    @sim_case_file_folder.setter
    @abstractmethod
    def sim_case_file_folder(self, value: SimCaseFileFolderManager):
        pass

    @property
    @abstractmethod
    def sim_out_data(self):
        pass

    @sim_out_data.setter
    @abstractmethod
    def sim_out_data(self, value):
        pass

    @property
    @abstractmethod
    def thermo_data(self) -> ThermoData:
        pass

    @thermo_data.setter
    @abstractmethod
    def thermo_data(self, value: ThermoData):
        pass

    @property
    @abstractmethod
    def particles(self) -> Particles:
        pass

    @particles.setter
    @abstractmethod
    def particles(self, value: Particles):
        if not isinstance(value, Particles):
            raise TypeError("The particles must be of type Particles.")

    @property
    @abstractmethod
    def forcefield(self) -> ForceFieldInterface:
        pass

    @forcefield.setter
    @abstractmethod
    def forcefield(self, value: ForceFieldInterface):
        if not isinstance(value, ForceFieldInterface):
            raise TypeError("The force field must be of type ForceFieldInterface.")
