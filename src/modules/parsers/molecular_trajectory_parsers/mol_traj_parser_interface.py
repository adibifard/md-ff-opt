from abc import ABC, abstractmethod
from utilities.files.file_reader import GeneralFileReaderInterface


class MolTrajParserInterface(ABC):

    @abstractmethod
    def parse(self):
        pass

    @property
    @abstractmethod
    def general_file_reader(self) -> GeneralFileReaderInterface:
        pass

    @property
    @abstractmethod
    def parsed_data(self):
        pass


