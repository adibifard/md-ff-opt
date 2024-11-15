from abc import ABC, abstractmethod
import pandas as pd

class ProjectDataInterface(ABC):

    pass



class ProjectData:
    def __init__(self):
        self.df = pd.DataFrame(columns=['ff_filename', 'epsilon', 'sigma'])
        # Cast columns to desired data types
        self.df = self.df.astype({
            'ff_filename': str,
            'epsilon': float,
            'sigma': float
        })



class GlobalScalerProjectData:
    def __init__(self):
        self.df = pd.DataFrame(columns=['ff_filename', 'epsilon', 'sigma'])
        # Cast columns to desired data types
        self.df = self.df.astype({
            'ff_filename': str,
            'epsilon': float,
            'sigma': float
        })

    def add_attributes(self, columns):
        # Ensure that columns is a list, even if a single column name is provided
        if isinstance(columns, str):
            columns = [columns]

        for column in columns:
            if column not in self.df.columns:
                self.df[column] = None

    def add_data(self, new_dat):

        self.df = pd.concat([self.df, pd.DataFrame([new_dat])], ignore_index=True)
