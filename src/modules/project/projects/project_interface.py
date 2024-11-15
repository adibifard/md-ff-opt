from abc import ABC, abstractmethod
from typing import Dict
from src.modules.project.inout_data.project_data import GlobalScalerProjectData


class ProjectInterface(ABC):
    """Class-Level Attributes"""


    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_project_args(cls):
        pass

    @abstractmethod
    def set_project_argv(self):
        pass

    @property
    @abstractmethod
    def path_to_proj_dir(self) -> str:
        pass

    @path_to_proj_dir.setter
    @abstractmethod
    def path_to_proj_dir(self, value: str):
        pass

    @property
    @abstractmethod
    def simulations_dir(self) -> str:
        pass

    @simulations_dir.setter
    @abstractmethod
    def simulations_dir(self, value: str):
        pass

    @property
    @abstractmethod
    def project_outputs(self) -> Dict[str, GlobalScalerProjectData]:
        pass

    @property
    @abstractmethod
    def configs(self):
        pass
