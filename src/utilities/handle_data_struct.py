
from numpy import *
import scipy.constants as sc

import csv
import os

# Find a dictionary matching certain keys from a list of dictionary
def find_dict_from_lod(list_of_dicts,key_val_search1,key_val_search2):
    for dictionary in list_of_dicts:
        if dictionary.get(key_val_search1["key"]) == key_val_search1["value"] and dictionary.get(key_val_search2["key"]) == key_val_search2["value"]:
            return dictionary
            break  # Break the loop if you only need the first match


# A method to determine arithmetic average of a variable
def calculate_average(pd_dataframe,column_name):
    pass



