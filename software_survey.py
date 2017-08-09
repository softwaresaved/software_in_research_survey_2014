#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import csv
import matplotlib.pyplot as plt
import math


DATAFILENAME = "./data/The-use-of-software-in-research-Responses-24-Oct-14-Form-Responses-1-csv.csv"


def import_csv_to_df(filename):
    """
    Imports a csv file into a Pandas dataframe
    :params: get an xls file and a sheetname from that file
    :return: a df
    """

    return pd.read_csv(filename)


def main():
    """
    Main function to run program
    """
    
    # Read survey data from csv
    df = import_csv_to_df(DATAFILENAME)


if __name__ == '__main__':
    main()
