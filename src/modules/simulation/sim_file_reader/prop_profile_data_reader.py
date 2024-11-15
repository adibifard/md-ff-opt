import pandas as pd
from io import StringIO

from utilities.files.file_reader import GeneralFileReader, GeneralFileReaderInterface


class PropProfileReader:

    def __init__(self, general_file_reader: GeneralFileReaderInterface, initial_tstep, final_tstep, skipped_tsteps=1):
        self._general_file_reader = general_file_reader
        self._initial_tstep = initial_tstep
        self._final_tstep = final_tstep
        self._skipped_tsteps = skipped_tsteps
        self._prop_lines = None
        self._prop_list = []

    @property
    def initial_tstep(self):
        return self._initial_tstep

    @property
    def final_tstep(self):
        return self._final_tstep

    @property
    def skipped_tsteps(self):
        return self._skipped_tsteps

    @skipped_tsteps.setter
    def skipped_tsteps(self, value):
        self._skipped_tsteps = value

    @property
    def prop_list(self):
        return self._prop_list

    @prop_list.setter
    def prop_list(self, value):
        self._prop_list = value

    def _get_starting_final_index(self, num_args):
        # find index of the line where time-step >=initial_time_step
        found_ti = False
        found_tf = False
        for index, line in enumerate(self._prop_lines):
            if found_ti and found_tf:
                break
            else:
                if not line.startswith('#') and len(line.split()) == num_args:
                    if self.initial_tstep <= int(line.split()[0]) and not found_ti:
                        starting_index = index
                        found_ti = True
                    elif self.final_tstep <= int(line.split()[0]) and not found_tf:
                        final_index = index
                        found_tf = True

        return starting_index, final_index

    def _generate_dict_data_for_timestep(self, time_step, time_step_data_str, col_names, data_keys):
        current_df_data = pd.read_csv(StringIO(time_step_data_str), sep=" ", header=None,
                                      names=col_names, dtype=float)
        current_rdf_dict = dict.fromkeys(data_keys)
        current_rdf_dict["time_step"] = time_step
        current_rdf_dict["data"] = current_df_data

        return current_rdf_dict

    def read(self, num_args_per_tstep_line):
        if len(self.prop_list) != 0:
            return self.prop_list
        self._prop_lines = self._general_file_reader.read()
        rdf_keys = ["time_step", "data"]  # List of keys
        rdf_column_names = self._prop_lines[2].strip().split()[1:]  # Skips the '#' and splits the rest

        starting_index, final_index = self._get_starting_final_index(num_args_per_tstep_line)
        self.prop_list = []
        current_data = []
        current_data_str = ""
        if starting_index is not None and final_index is not None:
            for index, line in enumerate(self._prop_lines[starting_index:final_index]):
                if len(line.split()) == num_args_per_tstep_line:
                    if current_data_str:
                        current_rdf_dict = self._generate_dict_data_for_timestep(current_time_step, current_data_str,
                                                                                 rdf_column_names, rdf_keys)
                        self.prop_list.append(current_rdf_dict)

                    current_time_step = int(line.split()[0])
                else:
                    current_data_str += line.strip() + "\n"
        else:
            raise ("Starting index is None.")

        # Handle the last block of data after the loop
        if current_data_str:
            current_rdf_dict = self._generate_dict_data_for_timestep(current_time_step, current_data_str,
                                                                     rdf_column_names, rdf_keys)
            self.prop_list.append(current_rdf_dict)

        return self.prop_list


if __name__ == "__main__":
    density_file_path = "/Users/meisam/Documents/GitHub/co2hydrates/nefe_calc/data/exp_match/solubility/simulations/water_co2_hydrate1/MassDensityFine_guest.mden"
    general_file_reader = GeneralFileReader(density_file_path)
    initial_tstep, final_tstep, skipped_tstep = 651000, 651000, 1

    density_profile_reader = PropProfileReader(general_file_reader, initial_tstep, final_tstep, skipped_tstep)
    density_profile_reader.read(num_args_per_tstep_line=3)

    # Test with RDF data.
    rdf_file_path = "/Users/meisam/Documents/GitHub/co2hydrates/nefe_calc/data/exp_match/solubility/simulations/water_co2_hydrate1/rdf_all.rdf"
    general_file_reader = GeneralFileReader(rdf_file_path)
    initial_tstep, final_tstep, skipped_tstep = 1000, 1000, 1

    rdf_profile_reader = PropProfileReader(general_file_reader, initial_tstep, final_tstep, skipped_tstep)
    rdf_profile_reader.read(num_args_per_tstep_line=2)
    pass
