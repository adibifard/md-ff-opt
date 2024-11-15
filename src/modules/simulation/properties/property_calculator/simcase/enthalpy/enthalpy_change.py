from src.modules.thermodynamics.reactions.reaction_interface import ReactionInterface
from src.modules.simulation.properties.property_calculator.simcase.enthalpy.enthalpy_change_interface import EnthalpyChangeCalculatorInterface


class ReactionEnthalpyChangeCalculator(EnthalpyChangeCalculatorInterface):
    def __init__(self, reaction: ReactionInterface):
        self.reaction = reaction
        self._hi = None
        self._hf = None
        self._dh = None

    @property
    def hi(self) -> float:
        return self._hi

    @hi.setter
    def hi(self, value: float):
        self._hi = value

    @property
    def hf(self) -> float:
        return self._hf

    @hf.setter
    def hf(self, value: float):
        self._hf = value

    @property
    def dh(self) -> float:
        return self._dh

    @dh.setter
    def dh(self, value: float):
        self._dh = value

    def calculate(self):
        # First calculate the enthalpy of products.
        self.hi = 0
        for reactant in self.reaction.reactants:
            self.hi += reactant.stoch_coeff * reactant.enthalpy

        # Second calculate the enthalpy of reactants.
        self.hf = 0
        for product in self.reaction.products:
            self.hf += product.stoch_coeff * product.enthalpy

        # Calculate the changes in enthalpy.
        self.dh = self.hf - self.hi

        return self.dh


class PhaseEnthalpyChangeCalculator(EnthalpyChangeCalculatorInterface):
    def __init__(self, hi=None, hf=None):
        self._hi = hi
        self._hf = hf
        self._dh = None

    @property
    def hi(self) -> float:
        return self._hi

    @hi.setter
    def hi(self, value: float):
        self._hi = value

    @property
    def hf(self) -> float:
        return self._hf

    @hf.setter
    def hf(self, value: float):
        self._hf = value

    @property
    def dh(self) -> float:
        return self._dh

    @dh.setter
    def dh(self, value: float):
        self._dh = value

    def calculate(self):
        self.dh = self.hf - self.hi
        return self.dh


if __name__ == "__main__":
    from src.modules.thermodynamics.reactions.physical_reaction import PhysicalReaction

    hydrate_formation_reaction = PhysicalReaction()
