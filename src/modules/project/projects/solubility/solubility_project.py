import argparse
import os
from typing import Dict
import __main__

from modules.config_loaders.config_loader import ConfigLoader, MultipleConfigLoader
from modules.simulation.sim_data.data_interface import ThermoData
from src.modules.project.inout_data.project_data import GlobalScalerProjectData
from src.modules.project.projects.project_interface import ProjectInterface
from src.modules.simulation.component.particle.particles import Particles
from src.modules.simulation.forcefield.forcefield import SWFF
from src.modules.simulation.lammps_parser import LammpsLogParser
from src.modules.simulation.properties.property_reader.property_reader import JSONParticlePropertyReader
from src.modules.simulation.sim_case.sim_case_interface import SimCaseFileFolderManager
from utilities.files.file_reader import GeneralFileReader
from src.modules.simulation.sim_case.lammps_sim_case import LAMMPSSimCase
from src.utilities.handle_data_struct import find_dict_from_lod
from src.utilities.manage_file_folder import get_and_sort_folders

# This will give you the full path to the main file
main_file_path = __main__.__file__
main_file_dir = os.path.dirname(os.path.abspath(main_file_path))


class SolubilityProject(ProjectInterface):
    REL_PATH_FROM_SRC_GENERAL_PROJECT_CONFIGS = "modules/project/general_project_configs.json"
    REL_PATH_FROM_SRC_DISS_PROJ_CONFIG = "modules/project/projects/solubility/solubility_configs.json"
    CONFIGS_PATH = [os.path.join(main_file_dir, REL_PATH_FROM_SRC_GENERAL_PROJECT_CONFIGS),
                    os.path.join(main_file_dir, REL_PATH_FROM_SRC_DISS_PROJ_CONFIG)]

    def __init__(self, density_pofiles_fn=None, path_to_proj_dir=None, simulations_dir=None, logs_dir=None, path_to_sim_cases=None,
                 path_to_log_files=None, time_step0=None, particle_types=None):

        self._time_stepf = None
        self._density_pofiles_fn = density_pofiles_fn
        self._path_to_proj_dir = path_to_proj_dir
        self._simulations_dir = simulations_dir
        self._logs_dir = logs_dir
        self._path_to_sim_cases = path_to_sim_cases
        self._path_to_log_files = path_to_log_files
        self._time_step0 = time_step0
        self._particle_types = particle_types

        self._project_outputs = dict()
        self._configs = MultipleConfigLoader(self.CONFIGS_PATH).load_configs()
        self.output_req = ["profile"]

    @property
    def path_to_proj_dir(self) -> str:
        return self._path_to_proj_dir

    @path_to_proj_dir.setter
    def path_to_proj_dir(self, value):
        self._path_to_proj_dir = value

    @property
    def simulations_dir(self) -> str:
        return self._simulations_dir

    @simulations_dir.setter
    def simulations_dir(self, value):
        self._simulations_dir = value

    @property
    def project_outputs(self) -> Dict:
        return self._project_outputs

    @property
    def configs(self):
        return self._configs

    @classmethod
    def get_project_args(cls, parser):
        parser.add_argument('-p', '--project_path', type=str, required=True, help='Path to the project directory')
        parser.add_argument('-ts0', '--time_step0', type=int, required=True,
                            help='Initial time-step to read the simulation output data')
        parser.add_argument('-tsf', '--time_stepf', type=int, required=True,
                            help='Final time-step to read the simulation output data')
        parser.add_argument('-dp', '--density_profile_filenames', nargs='+', type=str, required=True,
                            help='The name of the dumped density profiles')
        parser.add_argument('-pt', '--particles_type', nargs=2, type=str, required=True,
                            help='Type of particles (a pair of strings)',
                            default=["C", "C"])
        parser.add_argument('-s', '--simulations_directory', type=str, help='Simulations directory',
                            default='simulations')
        parser.add_argument('-l', '--logs_directory', type=str, help='Logs directory', default=None)

    def set_project_argv(self, project_args):
        self.path_to_proj_dir = project_args.project_path
        self.simulations_dir = project_args.simulations_directory
        self._density_pofiles_fn = project_args.density_profile_filenames
        self._logs_dir = project_args.logs_directory
        self._time_step0 = project_args.time_step0
        self._time_stepf = project_args.time_stepf
        self._particle_types = project_args.particles_type
        # Update paths based on the new arguments
        self._set_path_to_sim_cases_n_log_files()

    def _set_path_to_sim_cases_n_log_files(self):
        try:
            self._path_to_sim_cases = os.path.join(self._path_to_proj_dir, self.simulations_dir)
        except Exception as e:
            raise e
        try:
            self._path_to_log_files = os.path.join(self._path_to_proj_dir,
                                                   self._logs_dir) if self._logs_dir is not None else None
        except Exception as e:
            raise e

    @staticmethod
    def get_ff_pairs(ff_params, particle_types):
        ff_pairs = find_dict_from_lod(ff_params,
                                      {'key': 'p1', 'value': particle_types[0]},
                                      {'key': 'p2', 'value': particle_types[1]})
        return ff_pairs

    def run(self):
        density_profile_inputs = {"file_names": self._density_pofiles_fn, "starting_tstep": 1000, "final_tstep": 2000,
                                  "skipping_rows": 1}

        output_data_to_read = {"density_profiles": density_profile_inputs}
        proj_data = GlobalScalerProjectData()
        _, sim_case_paths = get_and_sort_folders(self._path_to_sim_cases)

        # Specify the path to the simulation config file
        path_to_sim_config = os.path.join(main_file_dir, 'modules/simulation/sim_case/simcase_configs.json')
        for sim_case_path in sim_case_paths:
            path_to_folder_of_log_file = self._path_to_log_files if self._logs_dir is not None else sim_case_path
            sim_case_file_folder = SimCaseFileFolderManager(sim_case_path, path_to_folder_of_log_file)
            lmp_log_parser = LammpsLogParser(GeneralFileReader(sim_case_file_folder.log_file_path))
            with LAMMPSSimCase(sim_case_file_folder=sim_case_file_folder,
                               lmp_log_parser=lmp_log_parser,
                               particles=Particles(JSONParticlePropertyReader()), forcefield=SWFF(),
                               config_loader=ConfigLoader(path_to_sim_config), thermo_data=ThermoData()) as current_sim_case:
                current_sim_case.read_input_data(["ff"])
                ff_file = os.path.basename(current_sim_case.forcefield.ff_file_path)
                ff_pairs = self.get_ff_pairs(current_sim_case.forcefield.params, self._particle_types)
                current_sim_case.read_output_data(output_data_to_read)

                proj_data.add_data({'ff_filename': ff_file, 'epsilon': ff_pairs['eps'], 'sigma': ff_pairs['sigma'],
                                    'density_profiles': current_sim_case.sim_out_data.data['density_profiles']})

                self.project_outputs['density_profiles'] = proj_data


if __name__ == "__main__":
    solubility_project = SolubilityProject()
    parser = argparse.ArgumentParser(description="Test the class behavior")
    solubility_project.get_project_args(parser)

    project_args = parser.parse_args(['--myarg', '10'])
    # Set project args
    solubility_project.set_project_argv(project_args)
