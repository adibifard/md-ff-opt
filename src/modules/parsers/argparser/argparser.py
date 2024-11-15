from abc import ABC, abstractmethod
import argparse
from typing import Any, List, Optional


class MainParserInterface(ABC):
    @property
    @abstractmethod
    def global_args(self) -> argparse.Namespace:
        pass

    @global_args.setter
    @abstractmethod
    def global_args(self, value: argparse.Namespace):
        pass

    @abstractmethod
    def parse(self):
        pass


class ProjectMainParserInterface(MainParserInterface):
    @property
    @abstractmethod
    def project_argv(self) -> List[str]:
        pass

    @project_argv.setter
    @abstractmethod
    def project_argv(self, value: List[str]):
        pass


class ProjectMainParser(ProjectMainParserInterface):
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser()
        self._global_args: Optional[argparse.Namespace] = None
        self._project_argv: Optional[List[str]] = None


    @property
    def global_args(self) -> argparse.Namespace:
        return self._global_args

    @global_args.setter
    def global_args(self, value: argparse.Namespace):
        self._global_args = value

    @property
    def project_argv(self) -> List[str]:
        return self._project_argv

    @project_argv.setter
    def project_argv(self, value: List[str]):
        self._project_argv = value

    def parse(self):
        if self.global_args is not None and self.project_argv is not None:
            return self.parser, self.global_args, self.project_argv
        # Initial parser for project type
        self.parser = argparse.ArgumentParser(description="Run specific projects")
        self.parser.add_argument('-tp', '--type_of_project', required=True, help='Type of project to run')
        self.global_args, self.project_argv = self.parser.parse_known_args()
        return self.parser, self.global_args, self.project_argv
