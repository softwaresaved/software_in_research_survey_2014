#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import csv
import matplotlib.pyplot as plt
import math


DATAFILENAME = "./data/The-use-of-software-in-research-Responses-24-Oct-14-Form-Responses-1-csv.csv"
STOREFILENAME = "./output/software_in_research_parasable.csv"

def import_csv_to_df(filename):
    """
    Imports a csv file into a Pandas dataframe
    :params: get an xls file and a sheetname from that file
    :return: a df
    """

    return pd.read_csv(filename)
    
def export_df_to_csv(df, filename):
    """
    Imports a csv file into a Pandas dataframe
    :params: get an xls file and a sheetname from that file
    :return: a df
    """

    return df.to_csv(filename)


def separate_software_packages(df):
    """
    Separates the rather messy user-entered free text for which software packages people use
    I replace semi-colons and carriage returns with commas. Strings without either of these
    separators are very time-consuming and difficult to parse. However, one-word answers
    are easy to parse. Hence, I locate these. The location of all parsable strings is recorded
    in a new column and the non-parsable strings are over-written with NaN.
    :params: get an xls file and a sheetname from that file
    :return: a df
    """

    # Replace semi-colons with commas
    df['Question 11: Please provide the name(s) of the main research software you use.'] = df['Question 11: Please provide the name(s) of the main research software you use.'].str.replace(';',',')
    # Replace carriage returns with commas
    df['Question 11: Please provide the name(s) of the main research software you use.'] = df['Question 11: Please provide the name(s) of the main research software you use.'].str.replace('\n',',')
    # Store the location of the parsable strings (i.e. the ones with commas)
    df['Q11_valid_data'] = df['Question 11: Please provide the name(s) of the main research software you use.'].str.contains(',')

    # Add to the parsable strings by also storing the location of one-word strings
    df['Q11_valid_data'] = (df['Q11_valid_data']) | (df['Question 11: Please provide the name(s) of the main research software you use.'].str.count(' ') == 0)

    
    print('The dataframe contains the following number of parsable rows:')
    print(df['Q11_valid_data'].value_counts())
    
    return   


def main():
    """
    Main function to run program
    """
    
    # Read survey data from csv
    df = import_csv_to_df(DATAFILENAME)

    separate_software_packages(df)
    
    export_df_to_csv(df, STOREFILENAME)

if __name__ == '__main__':
    main()
