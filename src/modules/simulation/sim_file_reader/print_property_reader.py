import pandas as pd

from utilities.files.file_reader import GeneralFileReaderInterface


class PrintPropertyReader():
    def __init__(self, general_file_reader: GeneralFileReaderInterface):
        self._general_file_reader = general_file_reader
        self._file_lines = None
        self._data_df = None



    @property
    def data_df(self):
        return self._data_df

    @data_df.setter
    def data_df(self, value):
        self._data_df = value

    def read(self):
        if self._data_df is not None:
            return self._data_df

        self._file_lines = self._general_file_reader.read()

        # Get the header and the column names.
        header_line = self._file_lines[0].lstrip('#').strip()
        column_names = [item.split(':')[0] for item in self._file_lines[1].strip().split(', ')]

        # Process each line to extract data
        data = []
        for line in self._file_lines[1:]:
            # Splitting each line by ', ' and further splitting by ':' to separate keys and values
            record = {kv.split(':')[0]: float(kv.split(':')[1]) for kv in line.strip().split(', ')}
            data.append(record)

        # Creating a DataFrame from the extracted data
        self._data_df = pd.DataFrame(data)

        return self._data_df


if __name__ == "__main__":
    prop_file_path = "/Users/unconvrs/Documents/GitHub/co2hydrates/nefe_calc/data/epm2/rest00/GlobalPropCalculated.prop"
    print_prop_reader = PrintPropertyReader(prop_file_path)
    print_props_df = print_prop_reader.read()
    print(print_props_df)
    pass
