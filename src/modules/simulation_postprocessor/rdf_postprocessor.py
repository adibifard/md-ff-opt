import numpy as np

from src.modules.simulation_postprocessor.postprocessor_interface import PostProcessorInterface
from src.modules.simulation.sim_case.lammps_sim_case import SimCaseInterface
from src.modules.simulation.sim_case.lammps_sim_case import LAMMPSSimCase
from utilities.files.file_reader import GeneralFileReaderInterface


class HydrationNumberCalculator(PostProcessorInterface):
    def __init__(self, sim_case: SimCaseInterface, rdf_file_reader: GeneralFileReaderInterface):
        self._sim_case = sim_case
        self._rdf_file_reader = rdf_file_reader

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @property
    def sim_case(self):
        return self._sim_case

    @sim_case.setter
    def sim_case(self, value):
        self._sim_case = value

    @property
    def rdf_reader(self):
        return self._rdf_file_reader

    @rdf_reader.setter
    def rdf_reader(self, value):
        self._rdf_file_reader = value

    @staticmethod
    def _get_starting_index(rdf_lines, initial_time_step):
        # find index of the line where time-step >=initial_time_step
        for index, line in enumerate(rdf_lines):
            if not line.startswith('#'):
                if len(line.split()) == 2 and int(line.split()[0]) >= initial_time_step:
                    return index
                    break

    def process(self, gr_col, nr_col):
        rdf_list = self.rdf_reader.read()
        n = []
        for rdf in rdf_list:
            dg = rdf["data"].iloc[:, gr_col].diff()
            diff_array = dg.to_numpy()
            # Find indices where the sign changes
            sign_changes = np.where(np.diff(np.sign(diff_array)) == 2)[0]

            if sign_changes.size > 0:
                # The first transition from negative to positive
                negative_index = sign_changes[0]
                positive_index = negative_index + 1
                # print(f"Negative Index: {negative_index}, Positive Index: {positive_index}")
                n_for_negative_index = rdf["data"].iloc[negative_index, nr_col]
                n_for_positive_index = rdf["data"].iloc[positive_index, nr_col]
                n_avg = 0.5 * (n_for_negative_index + n_for_positive_index)
                n.append(n_avg)
            else:
                print("No transition from negative to positive found.")

        # Find the mean and sd of the n.
        if len(n) != 0:
            n_array = np.array(n)
            n_mean = np.mean(n_array)
            n_std_dev = np.std(n_array)
            self.sim_case.sim_out_data.data["nw"] = {"mean": n_mean, "std": n_std_dev}
        else:
            raise ValueError(f'Could not calculate hydration number for the following file: {self.rdf_reader.input_file_path}')



if __name__ == '__main__':
    from src.modules.simulation.sim_file_reader.prop_profile_data_reader import PropProfileReader

    rdf_reader = PropProfileReader()
    lmp_sim_case = LAMMPSSimCase('../../../data/simulations/water_co2_hydrate3',
                                 '../../../data/simulations/water_co2_hydrate3')
    lmp_sim_case.read_output_data(["rdf"])

    hydration_num_processor = HydrationNumberCalculator(lmp_sim_case)
    hydration_num_processor.process(600000, 1, 8, 9)
    pass
