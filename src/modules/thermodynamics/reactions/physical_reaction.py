from src.modules.thermodynamics.reactions.reaction_interface import ReactionInterface
from src.modules.simulation.component.substance.substance import ReactionSubstanceInterface
from typing import List
from src.modules.thermodynamics.reactions.reaction_properties import PhysicalReactionProperties


class PhysicalReaction(ReactionInterface):
    def __init__(self, reaction_name):
        self._name = reaction_name
        self._reactants = []
        self._products = []
        self._properties = PhysicalReactionProperties()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def properties(self) -> PhysicalReactionProperties:
        return self._properties

    @properties.setter
    def properties(self, value: PhysicalReactionProperties):
        if not isinstance(value, PhysicalReactionProperties):
            raise TypeError("Object must be of type PhysicalReactionProperties.")

        self._properties = value

    @property
    def reactants(self) -> List[ReactionSubstanceInterface]:
        return self._reactants

    @reactants.setter
    def reactants(self, value: List[ReactionSubstanceInterface]):
        self._reactants = value

    @property
    def products(self) -> List[ReactionSubstanceInterface]:
        return self._products

    @products.setter
    def products(self, value: List[ReactionSubstanceInterface]):
        self._products = value

    def add_reactant(self, reactant: ReactionSubstanceInterface):
        self._reactants.append(reactant)
        return self

    def add_product(self, product: ReactionSubstanceInterface):
        self._products.append(product)
        return self
