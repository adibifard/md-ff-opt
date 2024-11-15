from src.modules.simulation.sim_data.data_processors.sim_data_processor_interface import SimDataProcessorInterface
from src.modules.simulation_postprocessor.postprocessor_interface import PostProcessorInterface
from src.modules.simulation.sim_case.lammps_sim_case import SimCaseInterface


class GlobalPropsPostProcessor(PostProcessorInterface):
    def __init__(self, sim_case: SimCaseInterface, pd_df_processor: SimDataProcessorInterface):
        self._sim_case = sim_case
        self._pd_df_processor = pd_df_processor

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
    def pd_df_processor(self):
        return self._pd_df_processor

    @pd_df_processor.setter
    def pd_df_processor(self, value):
        self._pd_df_processor = value

    def process(self, time_step0: int, time_step_col_name: str, processing_col_name: str):
        # Check if the sim_case already has the processed data
        if processing_col_name in self.sim_case.sim_out_data.data:
            print(f"Processed data for '{processing_col_name}' already exists. Skipping calculation.")
            return self.sim_case

        # Get the global props.
        processed_data = self.pd_df_processor.process(time_step0, time_step_col_name, processing_col_name)
        self.sim_case.sim_out_data.add(processing_col_name, processed_data)
        return self.sim_case
