import json
from abc import ABC, abstractmethod
import argparse
import importlib
import os

from src.modules.parsers.argparser.argparser import ProjectMainParserInterface
from src.modules.project.inout_data.project_output_writer import LAMMPSProjectScalerGlobalOutputWriter, LAMMPSProjectProfileOutputWriter

from src.modules.project.projects.global_prop.global_prop_project import GlobalPropProject
from src.modules.project.projects.dissociation_enthalpy.dissociation_enthalpy_project import DissociationEnthalpyProject
from src.modules.project.projects.solubility.solubility_project import SolubilityProject
from src.utilities.manage_file_folder import SourceCodeFileFinder
from src.modules.project.projects.project_interface import ProjectInterface


class ModuleImporterInterface(ABC):
    @abstractmethod
    def import_modules(self):
        pass


class ProjectModuleImporter(ModuleImporterInterface):
    REL_PATH_TO_PROJECTS = "../projects"
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    ABS_PATH_TO_PROJECTS = os.path.join(CURRENT_DIR, REL_PATH_TO_PROJECTS)

    def __init__(self, main_parser: ProjectMainParserInterface):
        self._main_parser = main_parser
        self._project_modules = None
        self._project_class = None

    def import_modules(self):
        if self._project_modules is not None and self._project_class is not None:
            return self._project_modules, self._project_class

        # Determine the directory of the current script.
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the JSON configuration file.
        json_file_path = os.path.join(script_dir, 'projects_modules.json')

        # Load the configuration from JSON file.
        with open(json_file_path, 'r') as config_file:
            project_mapping = json.load(config_file)

        # Get the project type from the main input arguments.
        project_type = self._main_parser.global_args.type_of_project
        config = project_mapping.get(project_type)

        if config:
            # Convert path to module format.
            path_to_module = config['module'].replace(os.sep, '.').replace('/', '.').rstrip('.py')
            class_name = config['class']
            self._project_modules = importlib.import_module(path_to_module, package=None)
            self._project_class = getattr(self._project_modules, class_name, None)

            return self._project_modules, self._project_class
        else:
            raise ValueError(f"Unknown project type: {project_type}")


class ProjectManager:
    def __init__(self, main_parser: ProjectMainParserInterface, project_module_importer: ModuleImporterInterface):
        self.project_class = None
        self._main_parser = main_parser
        self._project_module_importer = project_module_importer

    def run_projects(self):

        project_type = self._main_parser.global_args.type_of_project
        self.project_class: ProjectInterface = self._get_project_class(project_type)

        if hasattr(self.project_class, 'get_project_args'):
            project_parser = argparse.ArgumentParser(add_help=False)
            self.project_class.get_project_args(project_parser)
            project_args = project_parser.parse_args(self._main_parser.project_argv)
        else:
            project_args = self._main_parser.args

        # Set the project-specific arguments and run it.
        self.project_class.set_project_argv(project_args)
        self.project_class.run()
        LAMMPSProjectScalerGlobalOutputWriter(self.project_class).dump() if 'global' in self.project_class.output_req else ...
        LAMMPSProjectProfileOutputWriter(self.project_class).dump() if 'profile' in self.project_class.output_req else ...

    @staticmethod
    def _get_project_class(project_type: str):
        if project_type is None:
            raise ValueError('Project type is not specified')

        if project_type == "dhdiss":
            project_class = DissociationEnthalpyProject()
        elif project_type == "sol":
            project_class = SolubilityProject()
        elif project_type == "gp":
            project_class = GlobalPropProject()
        else:
            raise ValueError('Wrong project type!')

        return project_class
