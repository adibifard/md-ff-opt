from abc import ABC, abstractmethod

import pandas as pd


class HeaderInterface(ABC):
    @abstractmethod
    def add_header_column(self):
        pass

    @abstractmethod
    def remove_header_column(self):
        pass

    @abstractmethod
    def add_data(self):
        pass

    @property
    @abstractmethod
    def header_columns(self):
        pass

    @property
    @abstractmethod
    def header_data(self):
        return


class LAMMPSProjectFFDevHeader(HeaderInterface):

    def __init__(self, header_columns_names: list[str] = ['ff_filename', 'epsilon', 'sigma']):
        self._header_columns = header_columns_names
        # Initialize heade_data as a dataframe
        self._header_data = pd.DataFrame(columns=self.header_columns)

    def add_header_column(self, new_column_name: list[str], new_column_data=None):
        self.header_data[new_column_name] = new_column_data

    def remove_header_column(self, removed_column_names: list[str]):
        self._header_data.drop(removed_column_names, axis=1, inplace=True)

    def add_data(self, data: list):
        new_row = pd.DataFrame([data], columns=self.header_columns)

        # Append the new row to the existing DataFrame
        # Assuming you want to ignore the index, or you can add a specific index if you need
        self.header_data = self.header_data.append(new_row, ignore_index=True)


    @property
    def header_columns(self):
        return self._header_columns


    @property
    def header_data(self):
        return self._header_data
