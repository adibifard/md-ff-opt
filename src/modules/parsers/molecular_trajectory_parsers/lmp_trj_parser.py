import pandas as pd

from src.modules.parsers.molecular_trajectory_parsers.mol_traj_parser_interface import MolTrajParserInterface
from utilities.files.file_reader import GeneralFileReaderInterface, GeneralFileReader


class LAMMPSTrajParser(MolTrajParserInterface):

    def __init__(self, general_file_reader: GeneralFileReaderInterface):
        self._general_file_reader = general_file_reader
        self._parsed_data = []

    @property
    def general_file_reader(self):
        return self._general_file_reader

    @property
    def parsed_data(self):
        return self._parsed_data

    def parse(self):
        if self.parsed_data:
            return self.parsed_data

        timestep = None
        lines = self.general_file_reader.file_lines
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("ITEM: TIMESTEP"):
                timestep = int(lines[i + 1].strip())
                i += 2  # Move past the TIMESTEP line and its value
            elif line.startswith("ITEM: ATOMS"):
                # Extracting column names from this line
                columns = line.split()[2:]  # The column names start from the third element
                atoms_data = []
                i += 1  # Move to the first line of atom data
                while not lines[i].startswith("ITEM:"):
                    atom_data = lines[i].split()
                    atoms_data.append(atom_data)
                    i += 1
                    if i >= len(lines):  # Check to prevent index out of range
                        break
                # Convert atom data to DataFrame and append to trajectory data
                if atoms_data:
                    df = pd.DataFrame(atoms_data, columns=columns).apply(pd.to_numeric, errors='ignore')
                    self.parsed_data.append({'time-step': timestep, 'atoms': df})
                continue  # Continue to the next iteration of the loop
            i += 1  # General increment for the while loop

        return self.parsed_data


if __name__ == "__main__":
    path_to_lmp_trj_file = "/Users/unconvrs/Documents/GitHub/co2hydrates/nefe_calc/data/exp_match/DHdiss/H_co2/base_case_ff/simulations/water_co2_sw_001/NPT_Trajectory.lammpstrj"
    file_reader = GeneralFileReader(path_to_lmp_trj_file)
    file_reader.read()
    lmp_trj_parser = LAMMPSTrajParser(file_reader)
    lmp_trj_parser.parse()
    print(lmp_trj_parser.parsed_data[0]['time-step'])
    pass
