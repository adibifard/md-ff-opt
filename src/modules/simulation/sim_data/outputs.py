from abc import ABC, abstractmethod



class OutputDataInterface(ABC):
    @abstractmethod
    def read(self):
        pass





class RDFReader(OutputDataInterface):
    pass

