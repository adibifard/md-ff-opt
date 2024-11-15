import os
from typing import Dict
import __main__

from src.modules.project.inout_data.project_data import GlobalScalerProjectData
from src.modules.project.projects.project_interface import ProjectInterface
from src.utilities.handle_data_struct import find_dict_from_lod
from src.utilities.manage_file_folder import get_file_names_and_paths
from src.modules.simulation.sim_case.lammps_sim_case import LAMMPSSimCase
from src.modules.simulation.sim_data.data_interface import ThermoData
from src.modules.thermodynamics.reactions.physical_reaction import PhysicalReaction
from src.modules.simulation.properties.property_reader.property_reader import JSONReactionPropertyReader
from src.modules.simulation.sim_case.sim_case_interface import SimCaseFileFolderManager
from src.modules.simulation.lammps_parser import LammpsLogParser
from utilities.files.file_reader import GeneralFileReader
from src.modules.simulation.component.particle.particles import Particles
from src.modules.simulation.forcefield.forcefield import SWFF
from src.modules.simulation.properties.property_reader.property_reader import JSONParticlePropertyReader
from src.modules.simulation.properties.property_calculator.simcase.enthalpy.enthalpy_change import ReactionEnthalpyChangeCalculator
from src.modules.simulation.properties.property_calculator.particle.particle_property_calculator import SubstancePropertyCalculator
from src.modules.config_loaders.config_loader import MultipleConfigLoader, ConfigLoader

# This will give you the full path to the main file
main_file_path = __main__.__file__
main_file_dir = os.path.dirname(os.path.abspath(main_file_path))


class DissociationEnthalpyProject(ProjectInterface):
    REL_PATH_FROM_SRC_GENERAL_PROJECT_CONFIGS = "modules/project/general_project_configs.json"
    REL_PATH_FROM_SRC_DISS_PROJ_CONFIG = "modules/project/projects/dissociation_enthalpy/dissociation_enthalpy_configs.json"
    CONFIGS_PATH = [os.path.join(main_file_dir, REL_PATH_FROM_SRC_GENERAL_PROJECT_CONFIGS),
                    os.path.join(main_file_dir, REL_PATH_FROM_SRC_DISS_PROJ_CONFIG)]

    def __init__(self):
        self._reaction = None
        self._path_to_proj_dir = None
        self._simulations_dir = None
        self._project_outputs = dict()
        self._logs_dir = None
        self.path_to_sim_cases = None
        self.path_to_log_files = None
        self.time_step0 = None
        self._particle_types = None
        self._configs = MultipleConfigLoader(self.CONFIGS_PATH).load_configs()
        self.output_req = ["global"]

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
    def reaction(self):
        return self._reaction

    @reaction.setter
    def reaction(self, value):
        self._reaction = value

    @property
    def project_outputs(self) -> Dict:
        return self._project_outputs

    @project_outputs.setter
    def project_outputs(self, value: Dict):
        self._project_outputs = value

    # Modifies the parser arguments for this project.
    @classmethod
    def get_project_args(cls, parser):
        parser.add_argument('-p', '--project_path', type=str, required=True, help='Path to the project directory')
        parser.add_argument('-pt', '--particles_type', nargs=2, type=str, required=True, help='Type of particles (a pair of strings)',
                            default=["C", "O"])
        parser.add_argument('-rn', '--reaction_name', type=str, required=True, help='The name of the reaction')
        parser.add_argument('-t0', '--time_step0', type=int, required=True,
                            help='Initial time-step to read the simulation output data')
        parser.add_argument('-s', '--simulations_directory', type=str, help='Simulations directory',
                            default='simulations')
        parser.add_argument('-l', '--logs_directory', type=str, help='Logs directory', default=None)

    def set_project_argv(self, project_args):
        self.path_to_proj_dir = project_args.project_path
        self.reaction_name = project_args.reaction_name
        self.simulations_dir = project_args.simulations_directory
        self._logs_dir = project_args.logs_directory
        self.time_step0 = project_args.time_step0
        self._particle_types = project_args.particles_type
        # Instantiate the reaction object and populate its properties from the database.
        self._load_reaction_data()

        # Update paths based on the new arguments
        self._set_path_to_sim_cases_n_log_files()

    def _load_reaction_data(self):
        self.reaction = PhysicalReaction(self.reaction_name)
        JSONReactionPropertyReader().read_properties(self.reaction)

    def _set_path_to_sim_cases_n_log_files(self):
        try:
            self._path_to_sim_cases = os.path.join(self._path_to_proj_dir, self.simulations_dir)
        except Exception as e:
            raise e
        
        try:
            self._path_to_log_files = os.path.join(self._path_to_proj_dir, self._logs_dir) if self._logs_dir is not None else None
        except Exception as e:
            raise e

    def run(self):
        global product_sim_case
        proj_data = GlobalScalerProjectData()
        proj_data.add_attributes('dH_diss')

        # Use information from one of the reactants/products to get the list of simulation cases
        if self.reaction.reactants[0]:
            sim_case_filenames, _ = get_file_names_and_paths(
                os.path.join(self.path_to_proj_dir, self.reaction.reactants[0].sim_folder, self.simulations_dir))
        else:
            print("Warning: no reactants defined for the reaction.")

        for sim_case_filename in sim_case_filenames:
            for reactant in self.reaction.reactants:
                reactant_sim_case = self._set_sim_case(reactant, sim_case_filename)
                SubstancePropertyCalculator().calculate_enthalpy(reactant, reactant_sim_case, "global_props",
                                                                 "TimeStep", "v_HoutPerMol", self.time_step0)

            for product in self.reaction.products:
                product_sim_case = self._set_sim_case(product, sim_case_filename)
                SubstancePropertyCalculator().calculate_enthalpy(product, product_sim_case, "global_props",
                                                                 "TimeStep", "v_HoutPerMol", self.time_step0)
            # Calculate the enthalpy of dissociation.
            self.reaction.properties.dH = ReactionEnthalpyChangeCalculator(self.reaction).calculate()

            # Get the force field parameters using one of the simulation case objects (all simulation cases share the same force field parameters)
            sample_sim_case = reactant_sim_case
            sample_sim_case.read_input_data(["ff"])
            ff_file = os.path.basename(sample_sim_case.forcefield.ff_file_path)
            ff_pairs = find_dict_from_lod(sample_sim_case.forcefield.params,
                                          {'key': 'p1', 'value': self._particle_types[0]},
                                          {'key': 'p2', 'value': self._particle_types[1]})

            proj_data.add_data({'ff_filename': ff_file, 'epsilon': ff_pairs['eps'], 'sigma': ff_pairs['sigma'],
                                'dH_diss': self.reaction.properties.dH})

        self.project_outputs["dH_diss"] = proj_data

    def _set_sim_case(self, substance, sim_case_filename):
        # Path to the simulation config (its the same for all simulations)
        path_to_sim_config = os.path.join(main_file_dir, self.configs["DirectoryPaths"]["REL_PATH_SIMCASE_CONFIG"],
                                          self.configs["FileNames"]["SIMCASE_CONFIG_FILENAME"])
        sim_case_path = os.path.join(self.path_to_proj_dir, substance.sim_folder, self.simulations_dir,
                                     sim_case_filename)
        path_to_folder_of_log_file = self.path_to_log_files if self._logs_dir is not None else sim_case_path
        sim_case_file_folder = SimCaseFileFolderManager(sim_case_path, path_to_folder_of_log_file)
        lmp_log_parser = LammpsLogParser(GeneralFileReader(sim_case_file_folder.log_file_path))
        current_sim_case = LAMMPSSimCase(sim_case_file_folder, lmp_log_parser, Particles(JSONParticlePropertyReader()),
                                         SWFF(), ConfigLoader(path_to_sim_config), ThermoData())
        return current_sim_case


if __name__ == '__main__':
    thermo_data = ThermoData(T=258, p=100, vol=199003.12)
    dhdiss_project = DissociationEnthalpyProject("../../../data", thermo_data)
    dhdiss_project.run()
    sim_output_write = SimOutputWriter(fe_project)
    sim_output_write.dump()
