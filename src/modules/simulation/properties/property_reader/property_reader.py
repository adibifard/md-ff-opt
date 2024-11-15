from abc import ABC, abstractmethod
import json
import os

from src.modules.simulation.component.particle.particle import Particle
from src.modules.thermodynamics.reactions.reaction_interface import ReactionInterface
from src.modules.simulation.component.substance.substance import LAMMPSPhysicalReactionSubstance
from src.modules.thermodynamics.reactions.physical_reaction import PhysicalReaction


class PropertyReaderInterface(ABC):
    @abstractmethod
    def read_properties(self):
        pass


class JSONReader(PropertyReaderInterface):
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def read_json(self):
        try:
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find the JSON file at {self.json_file_path}")
        except json.JSONDecodeError:
            return "Error decoding JSON."
        except Exception as e:
            raise e


class JSONParticlePropertyReader(JSONReader):
    REL_PATH_TO_PARTICLE_DATABASE = '../../../../../assets/particles_database/particles_prop.json'
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    ABS_PATH_TO_PARTICLE_DATABASE = os.path.join(CURRENT_DIR, REL_PATH_TO_PARTICLE_DATABASE)

    def __init__(self):
        super().__init__(self.ABS_PATH_TO_PARTICLE_DATABASE)

    def read_properties(self, particle: Particle):
        db_particles = self.read_json()
        for db_particle in db_particles:
            if db_particle['name'].lower() == particle.name.lower():
                particle.mass = db_particle["mass"]
                particle.charge = db_particle["charge"]
                return f"Successfully read the {particle.name} properties from the database."

        return "Particle not found."


class JSONReactionPropertyReader(JSONReader):
    REL_PATH_TO_REACTION_DATABASE = '../../../../../assets/reactions_database/physical_reactions.json'
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    ABS_PATH_TO_REACTION_DATABASE = os.path.join(CURRENT_DIR, REL_PATH_TO_REACTION_DATABASE)

    def __init__(self):
        super().__init__(self.ABS_PATH_TO_REACTION_DATABASE)

    def read_properties(self, reaction: ReactionInterface):
        db_reactions = self.read_json()
        for db_reaction in db_reactions:
            if db_reaction['name'].lower() == reaction.name.lower():
                # Add reactants.
                for db_reactant in db_reaction['reactants']:
                    reactant_to_add = LAMMPSPhysicalReactionSubstance(db_reactant["name"], db_reactant["mass"],
                                                                      db_reactant["stoch_coeff"], None,
                                                                      db_reactant["sim_foldername_relpath"])
                    reaction.add_reactant(reactant_to_add)
                # Add products.
                for db_product in db_reaction['products']:
                    product_to_add = LAMMPSPhysicalReactionSubstance(db_product["name"], db_product["mass"],
                                                                     db_product["stoch_coeff"], None,
                                                                     db_product["sim_foldername_relpath"])
                    reaction.add_product(product_to_add)
                return f"Successfully read the {reaction.name} properties from the database."

        return "Reaction not found."


if __name__ == "__main__":
    json_reader = JSONParticlePropertyReader()
    test_particle = Particle("ch4")
    json_reader.read_properties(test_particle)
    json_reaction_reader = JSONReactionPropertyReader()
    test_reaction = PhysicalReaction("si_co2_hydrate_dissociation")
    json_reaction_reader.read_properties(test_reaction)
    pass
