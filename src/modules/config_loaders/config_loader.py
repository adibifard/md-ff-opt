import json
import os
from abc import ABC, abstractmethod


class ConfigLoaderInterface(ABC):
    @abstractmethod
    def load_configs(self):
        pass

    @property
    @abstractmethod
    def configs_path(self):
        pass


class ConfigLoader(ConfigLoaderInterface):
    def __init__(self, configs_path: str):
        self._configs_path = configs_path

    @property
    def configs_path(self):
        return self._configs_path

    def load_configs(self):
        with open(self.configs_path, 'r') as config_file:
            return json.load(config_file)


class MultipleConfigLoader(ConfigLoader):
    def __init__(self, configs_paths):
        self._configs_path = configs_paths

    @property
    def configs_path(self):
        return self._configs_path

    def load_configs(self):
        configs_dict = {}
        for config_path in self.configs_path:
            with open(config_path, 'r') as config_file:
                new_configs = json.load(config_file)
                for key, value in new_configs.items():
                    if key in configs_dict:
                        configs_dict[key].update(value)
                    else:
                        configs_dict[key] = value

        return configs_dict


class SimCaseConfigs:
    class DirectoryPaths:
        REL_PATH_FE_DATA = 'fe_input_data/'  # Folder containing input data for free-energy calculations.
        REL_PATH_MSD_DATA = 'msd_data/'

    class FileExtensions:
        GLOBAL_PROPS_TIME_AVERAGE = '.prop'
        PRINT_PROPS = '.printprop'
        RDF_DATA = '.rdf'

    class FileNames:
        LAMMPS_LOG_FILE_TEMPLATE_NAME = 'log.lammps'
        GLOBAL_PROPS_TIME_AVERAGED = 'GlobalPropsTimeAvg.prop'
        NEFE_IRWORK_BACKWARD_FILENAME = None
        NEFE_IRWORK_FORWARD_FILENAME = None
