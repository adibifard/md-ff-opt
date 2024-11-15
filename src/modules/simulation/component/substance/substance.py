from abc import ABC, abstractmethod


class ReactionSubstanceInterface(ABC):

    @property
    @abstractmethod
    def mass(self) -> float:
        pass

    @mass.setter
    @abstractmethod
    def mass(self, value: float):
        pass

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
    def stoch_coeff(self) -> float:
        pass

    @stoch_coeff.setter
    @abstractmethod
    def stoch_coeff(self, value: float):
        pass

    @property
    @abstractmethod
    def enthalpy(self) -> float:
        pass

    @enthalpy.setter
    def enthalpy(self, value: float):
        pass


class PhysicalReactionSubstance(ReactionSubstanceInterface):

    def __init__(self, name, mass=None, stoch_coeff=None, enthalpy=None):
        self._name = name
        self._mass = mass
        self._stoch_coeff = stoch_coeff
        self._enthalpy = enthalpy

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        if value <= 0:
            raise ValueError("Mass of a substance must be positive!")
        self._mass = value

    @property
    def stoch_coeff(self):
        return self._stoch_coeff

    @stoch_coeff.setter
    def stoch_coeff(self, value):
        if value <= 0:
            raise ValueError("The stoichiometric coefficient must be positive!")
        self._stoch_coeff = value

    @property
    def enthalpy(self) -> float:
        return self._enthalpy

    @enthalpy.setter
    def enthalpy(self, value: float):
        self._enthalpy = value


class LAMMPSPhysicalReactionSubstance(PhysicalReactionSubstance):
    def __init__(self, name, mass=None, stoch_coeff=None, enthalpy=None, sim_folder=None):
        super().__init__(name, mass, stoch_coeff, enthalpy)
        self.sim_folder = sim_folder
