from typing import List

from src.modules.simulation.component.particle.particle import Particle
from src.modules.simulation.properties.property_reader.property_reader import PropertyReaderInterface, JSONParticlePropertyReader


class Particles:
    def __init__(self, property_reader: PropertyReaderInterface):
        self._particles = []
        self._num_particles = 0
        self._num_particle_types = 0
        self.property_reader = property_reader

    def _update_particle_number_type(self, particle):
        if not any(p.name == particle.name for p in self.particles):
            self._num_particle_types += 1
        self._num_particles += 1

    def add_particle(self, particle: Particle):
        self.property_reader.read_properties(particle) if particle.mass == None or particle.charge == None else ...
        self._update_particle_number_type(particle)
        self.particles.append(particle)
        return self

    @property
    def particles(self) -> List[Particle]:
        return self._particles

    @particles.setter
    def particles(self, value: List[Particle]):
        self._particles = value

    @property
    def num_particles(self):
        return self._num_particles

    @property
    def num_particle_types(self):
        return self._num_particle_types

    def __len__(self):
        return len(self.particles)

    def __eq__(self, other):
        if not isinstance(other, Particles):
            return NotImplemented
        are_equal_as_sets = set(self.particles) == set(other.particles)

        return are_equal_as_sets

    def __repr__(self):
        attributes = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({attributes})"

    def __str__(self):
        return f"A list of particles containing {len(self.particles)} particle(s)."


if __name__ == "__main__":
    my_particle = Particle("ch4")
    my_2nd_particle = Particle("ch4")
    my_3rd_particle = Particle("h2o")
    particles = Particles(JSONParticlePropertyReader())
    particles.add_particle(my_particle).add_particle(my_2nd_particle).add_particle(my_3rd_particle)
    size_particles = len(particles)
    print(str(particles))
    print(repr(particles))
    pass
