import pandas as pd

from utilities.files.file_reader import GeneralFileReader, GeneralFileReaderInterface


class GlobalTimeAvgPropertyReader:
    def __init__(self, general_file_reader: GeneralFileReaderInterface):
        self._file_lines = None
        self._data_df = None
        self._general_file_reader = general_file_reader

    @property
    def data_df(self):
        return self._data_df

    @data_df.setter
    def data_df(self, value):
        self._data_df = value

    @property
    def general_file_reader(self) -> GeneralFileReaderInterface:
        return self._general_file_reader



    def read(self, header_line_number):
        if self.data_df is not None:
            return self.data_df

        lines = self.general_file_reader.read()

        # Get the name of the columns and the data-type dictionary.
        column_names, dtype_dict = self.preprocess_header(lines, header_line_number)

        # Read the file into a DataFrame using the modified header line
        self.data_df = pd.read_csv(self.general_file_reader.input_file_path, delim_whitespace=True, skiprows=2, header=None,
                                   names=column_names, dtype=dtype_dict)

        return self.data_df

    @staticmethod
    def preprocess_header(file_lines, header_line_number):
        # Remove the '#' character from the header line
        header_line = file_lines[header_line_number].lstrip('#').strip()
        column_names = header_line.split()
        # The time-step column is of type integer
        dtype_dict = {column: float for column in column_names}
        dtype_dict[column_names[0]] = int

        return column_names, dtype_dict


if __name__ == "__main__":
    # file_path = "/Users/unconvrs/Documents/GitHub/co2hydrates/nefe_calc/data/simulations/water_co2_hydrate_sw_1/GlobalPropsTimeAvg.prop"
    # file_path_macbook = "/Users/unconvrs/Documents/GitHub/co2hydrates/nefe_calc/data/rdf_simulations/water_co2_hydrate3/GlobalPropsTimeAvg.prop"
    rel_file_path_imac = "../../../../data/simulations/water_co2_hydrate_sw_1/GlobalPropsTimeAvg.prop"
    general_file_reader = GeneralFileReader(rel_file_path_imac)
    global_file_reader = GlobalTimeAvgPropertyReader(general_file_reader)
    data_df = global_file_reader.read(header_line_number=2)
    print(data_df)
    pass
