import scipy.constants as sc
import math

# Physical constants.
kB = sc.value('Boltzmann constant in eV/K')
eV = sc.value('electron volt')
mu_const = sc.value('atomic mass constant')


class Particle:

    def __init__(self, name, mass=None, charge=None, count=None):
        self.name = name
        self._mass = mass
        self._charge = charge
        self._count = count
        self._k = None
        self._mu = None
        self._omega = None

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value: float):
        if not isinstance(value, float):
            raise TypeError("Mass must be a float.")
        self._mass = value

    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Charge must be an integer.")
        self._charge = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Count must be an integer.")
        self._count = value

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, value: float):
        if not isinstance(value, float):
            raise TypeError("mu must be a float.")
        self._mu = value

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value: float):
        if not isinstance(value, float):
            raise TypeError("k must be a float.")
        self._k = value

    @property
    def omega(self):
        return self._omega

    @omega.setter
    def omega(self, value: float):
        if not isinstance(value, float):
            raise TypeError("omega must be a float.")
        self._omega = value

    def __eq__(self, other):
        if not isinstance(other, Particle):
            return NotImplemented

        return (self.name == other.name)

    def __repr__(self):
        attributes = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({attributes})"


if __name__ == "__main__":
    particle = Particle(name='ch4')
    print(repr(particle))
