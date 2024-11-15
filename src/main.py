from src.modules.project.project_manager.project_manager import ProjectManager, ProjectModuleImporter
from src.modules.parsers.argparser.argparser import ProjectMainParser

if __name__ == '__main__':
    # Initial parser for project type.
    main_parser = ProjectMainParser()
    main_parser.parse()
    # Import the project modules depending on the parsed project type.
    project_module_importer = ProjectModuleImporter(main_parser)
    # Run the loaded project.
    project_manager = ProjectManager(main_parser, project_module_importer)
    project_manager.run_projects()
    pass


