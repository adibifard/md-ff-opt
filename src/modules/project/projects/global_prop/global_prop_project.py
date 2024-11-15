import os
from typing import Dict

from src.utilities.manage_file_folder import get_and_sort_folders
from src.utilities.handle_data_struct import find_dict_from_lod
from src.modules.simulation.sim_case.lammps_sim_case import LAMMPSSimCase
from src.modules.project.projects.project_interface import ProjectInterface
from src.modules.simulation.sim_case.sim_case_interface import SimCaseFileFolderManager
from utilities.files.file_reader import GeneralFileReader
from src.modules.simulation.lammps_parser import LammpsLogParser
from src.modules.simulation.forcefield.forcefield import SWFF
from src.modules.simulation.component.particle.particles import Particles
from src.modules.simulation.properties.property_reader.property_reader import JSONParticlePropertyReader
from src.modules.project.projects.global_prop.global_prop_project_configs import GlobalPropProjectConfigs
from src.modules.simulation_postprocessor.global_props_postprocessor import GlobalPropsPostProcessor
from src.modules.simulation.sim_data.data_processors.pandas_df_processor import PandasSimDataProcessor
from src.modules.project.inout_data.project_data import GlobalScalerProjectData
from src.modules.simulation.sim_data.data_interface import ThermoData

class GlobalPropProject(ProjectInterface):

    def __init__(self, global_prop_name=None, path_to_proj_dir=None, simulations_dir=None, logs_dir=None,
                 path_to_sim_cases=None,
                 path_to_log_files=None, time_step0=None, particle_types=None):
        self._global_prop_name = global_prop_name
        self._path_to_proj_dir = path_to_proj_dir
        self._simulations_dir = simulations_dir
        self._logs_dir = logs_dir
        self._path_to_sim_cases = path_to_sim_cases
        self._path_to_log_files = path_to_log_files
        self.time_step0 = time_step0
        self._particle_types = particle_types

        self._project_outputs = dict()
        self._configs = GlobalPropProjectConfigs

    @property
    def configs(self):
        return self._configs

    @property
    def path_to_proj_dir(self):
        return self._path_to_proj_dir

    @path_to_proj_dir.setter
    def path_to_proj_dir(self, value):
        self._path_to_proj_dir = value

    @property
    def simulations_dir(self):
        return self._simulations_dir

    @simulations_dir.setter
    def simulations_dir(self, value):
        self._simulations_dir = value

    @property
    def project_outputs(self) -> Dict:
        return self._project_outputs

    @classmethod
    def get_project_args(cls, parser):
        parser.add_argument('-p', '--project_path', type=str, required=True, help='Path to the project directory')
        parser.add_argument('-t0', '--time_step0', type=int, required=True,
                            help='Initial time-step to read the simulation output data')
        parser.add_argument('-gp', '--global_prop', type=str, required=True,
                            help='The name of the dumped global property')
        parser.add_argument('-pt', '--particles_type', nargs=2, type=str, required=True,
                            help='Type of particles (a pair of strings)',
                            default=["C", "C"])
        # parser.add_argument('-hl', '--h_liq', type=float, help='Liquid enthalpy (Kcal/mol)')
        parser.add_argument('-s', '--simulations_directory', type=str, help='Simulations directory',
                            default='simulations')
        parser.add_argument('-l', '--logs_directory', type=str, help='Logs directory', default=None)

    @staticmethod
    def check_var_in_project_args(project_args, arg):
        pass

    def set_project_argv(self, project_args):
        self.path_to_proj_dir = project_args.project_path
        self.simulations_dir = project_args.simulations_directory
        self._logs_dir = project_args.logs_directory
        self.time_step0 = project_args._time_step0
        self._particle_types = project_args.particles_type
        self._global_prop_name = project_args.global_prop
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
        proj_data = GlobalScalerProjectData()
        proj_data.add_attributes(f'{self._global_prop_name}_mean')
        proj_data.add_attributes(f'{self._global_prop_name}_std')

        _, sim_case_paths = get_and_sort_folders(self._path_to_sim_cases)
        # Path to the simulation config (its the same for all simulations)
        path_to_sim_config = "/Users/unconvrs/Documents/GitHub/co2hydrates/nefe_calc/src/modules/simulation/sim_case/simcase_configs.json"
        for sim_case_path in sim_case_paths:
            path_to_folder_of_log_file = self._path_to_log_files if self._logs_dir is not None else sim_case_path
            sim_case_file_folder = SimCaseFileFolderManager(sim_case_path, path_to_folder_of_log_file)
            lmp_log_parser = LammpsLogParser(GeneralFileReader(sim_case_file_folder.log_file_path))

            with LAMMPSSimCase(sim_case_file_folder, lmp_log_parser, Particles(JSONParticlePropertyReader()),
                               SWFF(), SimCaseConfigs(path_to_sim_config), ThermoData()) as current_sim_case:
                current_sim_case.read_input_data(["ff"])
                ff_file = os.path.basename(current_sim_case.forcefield.ff_file_path)
                ff_pairs = self.get_ff_pairs(current_sim_case.forcefield.params, self._particle_types)
                current_sim_case.read_output_data("global_props")
                with GlobalPropsPostProcessor(current_sim_case,
                                              PandasSimDataProcessor(current_sim_case.sim_out_data.data[
                                                                         "global_props"])) as global_props_processor:
                    current_sim_case = global_props_processor.process(self.time_step0, 'TimeStep',
                                                                      self._global_prop_name)

                    proj_data.add_data({'ff_filename': ff_file, 'epsilon': ff_pairs['eps'], 'sigma': ff_pairs['sigma'],
                                        f'{self._global_prop_name}_mean':
                                            current_sim_case.sim_out_data.data[self._global_prop_name]["mean"],
                                        f'{self._global_prop_name}_std':
                                            current_sim_case.sim_out_data.data[self._global_prop_name]["std"]})

        self.project_outputs[self._global_prop_name] = proj_data


if __name__ == "__main__":
    from src.modules.project.inout_data.project_output_writer import LAMMPSProjectScalerGlobalOutputWriter

    project_path = '/Users/unconvrs/Documents/GitHub/co2hydrates/nefe_calc/data/co2_co2/exp_match/density_DHvap'
    h_prop_project = GlobalPropProject(global_prop_name='v_Hout_mean', path_to_proj_dir=project_path,
                                       simulations_dir='simulations', time_step0=10000,
                                       particle_types=['C', 'C'])

    h_prop_project.run()
    LAMMPSProjectScalerGlobalOutputWriter(h_prop_project).dump()
    pass
