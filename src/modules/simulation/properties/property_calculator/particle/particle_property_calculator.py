import scipy.constants as sc
import math
from abc import ABC, abstractmethod

from src.modules.simulation.component.particle.particle import Particle
from src.modules.simulation.component.substance.substance import ReactionSubstanceInterface
from src.modules.simulation.sim_case.sim_case_interface import SimCaseInterface

# Physical constants.
kB = sc.value('Boltzmann constant in eV/K')
eV = sc.value('electron volt')
mu_const = sc.value('atomic mass constant')


class PropertyChangeCalculatorInterface(ABC):
    @abstractmethod
    def calculate(self):
        pass


class ParticlePropertyCalculator:
    """
    This class is responsible for calculating various properties of a Particle instance.
    """

    def __init__(self):
        pass

    def calculate_omega_from_k(self, particle: Particle):
        """
        Calculate the angular frequency (omega) of a particle based on its spring constant (k).

        Parameters:
        particle (Particle): The Particle instance for which omega is to be calculated.

        Returns:
        float: The calculated angular frequency (omega) if successful, None otherwise.

        Raises:
        TypeError: If the input is not an instance of Particle.
        """
        if not isinstance(particle, Particle):
            raise TypeError("The input must be a Particle instance.")

        if particle.mass != 0 and particle.k is not None:
            particle.omega = math.sqrt(particle.k * eV / (particle.mass * mu_const))  # [1/s]
        else:
            raise ValueError(f"Could not calculate omega for particle: {particle.name}.")

    def calculate_mu(self, particle: Particle, total_mass):
        """
        Calculate the reduced mass (mu) of a particle.

        Parameters:
        particle (Particle): The Particle instance for which mu is to be calculated.
        total_mass (float): The total mass against which the reduced mass is to be calculated.

        Returns:
        float: The calculated reduced mass (mu) if successful, None otherwise.

        Raises:
        TypeError: If the input is not an instance of Particle.
        """
        if not isinstance(particle, Particle):
            raise TypeError("The input must be a Particle instance.")

        if total_mass != 0:
            particle.mu = particle.mass / total_mass
        else:
            raise ValueError(f"Could not calculate mu for particle: {particle.name}.")


class SubstancePropertyCalculator:
    def __init__(self):
        pass

    def calculate_enthalpy(self, substance, sim_case: SimCaseInterface, prop_file_key, time_step_key, enthalpy_key,
                           time_step0):
        sim_case.read_output_data([prop_file_key])
        global_props_df = sim_case.sim_out_data.data[prop_file_key]
        substance.enthalpy = global_props_df[global_props_df[time_step_key] > time_step0][enthalpy_key].mean()
