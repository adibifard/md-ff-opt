from abc import ABC, abstractmethod
from typing import List


class DataReaderInterface(ABC):
    @abstractmethod
    def read(self) -> List[str]:
        pass


class GeneralFileReaderInterface(DataReaderInterface):

    @property
    @abstractmethod
    def input_file_path(self):
        pass

    @input_file_path.setter
    @abstractmethod
    def input_file_path(self, value):
        pass

    @property
    @abstractmethod
    def file_lines(self):
        pass


class GeneralFileReader(GeneralFileReaderInterface):
    def __init__(self, file_path):
        self._input_file_path = file_path
        self._file_lines = []

    @property
    def input_file_path(self):
        return self._input_file_path

    @input_file_path.setter
    def input_file_path(self, value):
        self._input_file_path = value

    @property
    def file_lines(self):
        return self._file_lines

    def read(self) -> List[str]:
        if len(self._file_lines) != 0:
            return self._file_lines
        else:
            try:
                with open(self.input_file_path, 'r') as file:
                    self._file_lines = file.readlines()
            except FileNotFoundError:
                raise FileNotFoundError(f'File {self.input_file_path} not found')
            except Exception as e:
                raise e

        return self._file_lines
