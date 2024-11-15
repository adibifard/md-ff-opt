from abc import ABC, abstractmethod
from typing import List

from src.modules.simulation.component.substance.substance import ReactionSubstanceInterface
from src.modules.thermodynamics.reactions.reaction_properties import ReactionPropertiesInterface

class ReactionInterface(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def properties(self) -> ReactionPropertiesInterface:
        pass

    @properties.setter
    @abstractmethod
    def properties(self, value: ReactionPropertiesInterface):
        pass


    @property
    @abstractmethod
    def reactants(self) -> List[ReactionSubstanceInterface]:
        pass

    @reactants.setter
    @abstractmethod
    def reactants(self, value: List[ReactionSubstanceInterface]):
        pass

    @property
    @abstractmethod
    def products(self) -> List[ReactionSubstanceInterface]:
        pass

    @products.setter
    @abstractmethod
    def products(self, value: List[ReactionSubstanceInterface]):
        pass

    @abstractmethod
    def add_reactant(self, reactant: ReactionSubstanceInterface):
        pass

    @abstractmethod
    def add_product(self, product: ReactionSubstanceInterface):
        pass
