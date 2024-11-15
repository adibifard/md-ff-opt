from abc import ABC, abstractmethod
from typing import List, Dict

from utilities.files.file_reader import GeneralFileReader


class ForceFieldInterface(ABC):
    @property
    @abstractmethod
    def ff_file_path(self) -> str:
        pass

    @ff_file_path.setter
    @abstractmethod
    def ff_file_path(self, value: str):
        pass

    @property
    @abstractmethod
    def style(self) -> str:
        pass

    @style.setter
    @abstractmethod
    def style(self, value: str):
        pass

    @property
    @abstractmethod
    def ff_keys(self) -> List:
        pass

    @ff_keys.setter
    @abstractmethod
    def ff_keys(self, value: List):
        pass

    @property
    @abstractmethod
    def params(self) -> List[Dict]:
        pass

    @params.setter
    @abstractmethod
    def params(self, value: List[Dict]):
        pass

    @abstractmethod
    def read_params(self, ff_file_path):
        pass


class TwoBodyForceFieldInterface(ForceFieldInterface):
    def __init__(self):
        self._ff_keys = ["p1", "p2"]

    @property
    def ff_keys(self) -> List:
        return self._ff_keys

    @ff_keys.setter
    def ff_keys(self, value: List):
        for item in value:
            if 'p1' not in item or 'p2' not in item:
                raise ValueError("Force field must contain keys 'p1' and 'p2'")
        self._ff_keys = value


class ThreeBodyForceFieldInterface(ForceFieldInterface):
    def __init__(self):
        self._ff_keys = ["p1", "p2", "p3"]

    @property
    def ff_keys(self) -> List:
        return self._ff_keys

    @ff_keys.setter
    def ff_keys(self, value: List):
        for item in value:
            if 'p1' not in item or 'p2' not in item or 'p3' not in item:
                raise ValueError("Force field must contain keys 'p1', 'p2' and 'p2'")
        self._ff_keys = value


class SWFF(ThreeBodyForceFieldInterface):
    def __init__(self):
        super().__init__()
        self._ff_file_path = None
        self._ff_keys.extend(["eps", "sigma", "a", "lambda", "gamma", "cos(theta0)", "A", "B", "p", "q", "tol"])
        self._style = 'sw'
        self._params = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @property
    def ff_file_path(self) -> str:
        return self._ff_file_path

    @ff_file_path.setter
    def ff_file_path(self, value: str):
        self._ff_file_path = value

    @property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(self, value: str):
        if value != 'sw':
            raise 'The style should only set to: sw'
        else:
            self._style = value

    @property
    def params(self) -> List[Dict]:
        return self._params

    @params.setter
    def params(self, value: List[Dict]):
        if all(len(d) == 14 for d in value):
            self._params = value
        else:
            raise ('Error: incorrect number of key-value pairs in the force field params.')

    def read_params(self, ff_file_path):
        self.ff_file_path = ff_file_path
        if len(self.params) != 0:
            return self.params
        else:
            for line in GeneralFileReader(self.ff_file_path).read():
                stripped_line = line.strip()
                if not stripped_line:
                    continue

                if stripped_line.startswith('#'):
                    continue
                else:
                    if self.ff_keys:
                        values = stripped_line.split()
                        if len(values) == len(self.ff_keys):
                            entry = dict(zip(self.ff_keys, values))
                            self.params.append(entry)
                        else:
                            print(f"Warning: Line '{stripped_line}' does not match header length and was skipped.")
        return self.params

    def __str__(self):
        return "Stillinger-Webber potential"

    def __repr__(self):
        attributes = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({attributes})"
