import os
import parser

import pandas as pd

from src.modules.project.projects.project_interface import ProjectInterface
from src.modules.simulation.component.particle.particles import Particles
from src.modules.simulation.properties import JSONParticlePropertyReader
from src.modules.simulation.forcefield.forcefield import SWFF
from src.modules.simulation.lammps_parser import LammpsLogParser
from src.modules.simulation.sim_case.lammps_sim_case import LAMMPSSimCase
from src.modules.simulation.sim_case.sim_case_interface import SimCaseFileFolderManager
from utilities.files.file_reader import GeneralFileReader
from src.utilities.manage_file_folder import get_and_sort_folders, find_files_with_extension


class diffusivity_project(ProjectInterface):

    def __init__(self):
        self._path_to_proj_dir = None
        self._simulations_dir = None
        self._project_outputs = dict()
        self._logs_dir = None
        self._path_to_sim_cases = None
        self._path_to_log_files = None
        self._time_step0 = None
        self._particle_types = None

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

    @project_outputs.setter
    def project_outputs(self, value: Dict):
        self._project_outputs = value

    def _set_path_to_sim_cases_n_log_files(self):
        try:
            self._path_to_sim_cases = os.path.join(self._path_to_proj_dir, self.simulations_dir)
        except Exception as e:
            raise e

        try:
            self._path_to_log_files = os.path.join(self._path_to_proj_dir, self._logs_dir) if self._logs_dir is not None else None
        except Exception as e:
            raise e

    def get_project_args(cls):
        parser.add_argument('-p', '--project_path', type=str, help='Path to the project directory')
        parser.add_argument('-pt', '--particles_type', nargs=2, type=str, help='Type of particles (a pair of strings)',
                            default=["C", "O"])
        parser.add_argument('-t0', '--time_step0', type=int,
                            help='Initial time-step to start reading the diffusivity data')
        parser.add_argument('-s', '--simulations_directory', type=str, help='Simulations directory',
                            default='simulations')
        parser.add_argument('-l', '--logs_directory', type=str, help='Logs directory', default=None)

    def set_project_argv(self, project_args):
        self.path_to_proj_dir = project_args.project_path
        self.simulations_dir = project_args.simulations_directory
        self._logs_dir = project_args.logs_directory
        self._time_step0 = project_args._time_step0
        self._particle_types = project_args.particles_type

        # Determine the path to the sim cases and the log files.
        self._set_path_to_sim_cases_n_log_files()

    def run(self):
        diffusivity = pd.DataFrame(columns=['ff_file', 'epsilon', 'sigma', 'D', 'std'])
        _, sim_case_paths = get_and_sort_folders(self._path_to_sim_cases)
        for sim_case_path in sim_case_paths:
            path_to_folder_of_log_file = self._path_to_log_files if self.logs_dir is not None else sim_case_path
            sim_case_file_folder = SimCaseFileFolderManager(sim_case_path, path_to_folder_of_log_file)
            lmp_log_parser = LammpsLogParser(GeneralFileReader(sim_case_file_folder.log_file_path))
            with LAMMPSSimCase(sim_case_file_folder, lmp_log_parser, Particles(JSONParticlePropertyReader()), SWFF()) as current_sim_case:
                current_sim_case.read_input_data(["ff"])
                props_filename = find_files_with_extension(sim_case_file_folder.sim_case_path, ".prop")

                with HydrationNumberCalculator(current_sim_case, rdf_reader) as nw_calculator:
                    nw_calculator.process(self._grcol_num, self._nrcol_num)
                    ff_file = os.path.basename(current_sim_case.forcefield.ff_file_path)
                    ff_pairs = find_dict_from_lod(current_sim_case.forcefield.params,
                                                  {'key': 'p1', 'value': self._particle_types[0]},
                                                  {'key': 'p2', 'value': self._particle_types[1]})
                    nw.loc[len(nw)] = {'ff_file': ff_file, 'epsilon': ff_pairs['eps'], 'sigma': ff_pairs['sigma'],
                                       'nw': current_sim_case.sim_out_data.data["nw"]["mean"],
                                       'std': current_sim_case.sim_out_data.data["nw"]["std"]}

        self.project_outputs["nw"] = nw
