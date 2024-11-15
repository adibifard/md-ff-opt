from abc import ABC, abstractmethod
from utilities.files.file_reader import GeneralFileReaderInterface


class SimOutputReaderInterface(ABC):

    @abstractmethod
    def read(self):
        pass

    @property
    @abstractmethod
    def general_file_reader(self) -> GeneralFileReaderInterface:
        pass
