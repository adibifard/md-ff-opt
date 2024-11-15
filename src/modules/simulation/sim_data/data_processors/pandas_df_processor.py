import pandas as pd
from pandas import Series

from src.modules.simulation.sim_data.data_processors.sim_data_processor_interface import SimDataProcessorInterface


class PandasSimDataProcessor(SimDataProcessorInterface):
    def __init__(self, pd_df: pd.DataFrame):
        self._sim_data = pd_df

    @property
    def sim_data(self) -> pd.DataFrame:
        return self._sim_data

    @sim_data.setter
    def sim_data(self, value: pd.DataFrame):
        self._sim_data = value

    def process(self, time_step0: int, time_step_col_name: str, processing_col_name: str):
        # Filter the DataFrame based on the Time-Step column and t0.
        filtered_data = self.sim_data[self.sim_data[time_step_col_name] > time_step0]

        # Calculate the average and standard deviation for the specified column.
        average = filtered_data[processing_col_name].mean()
        std_dev = filtered_data[processing_col_name].std()
        if average is not None and std_dev is not None:
            processed_data = {'mean': average, 'std': std_dev}
            # Return the results as a dictionary or any format you prefer.
            return processed_data
        else:
            raise ValueError(f'Could not calculate mean and std for the given data-frame')
