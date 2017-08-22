#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np
import csv
import math

STOREFILENAME = './output/'
NEW_RESULTS = './output/summary_csvs/'
OLD_RESULTS = './results_from_original_2014_analysis/'
LIST_OF_RESULT_NAMES = [
    'Question 1.csv',
    'Question 2.csv',
    'Question 3.csv',
    'Question 4.csv',
    'Question 5.csv',
    'Question 6.csv',
    'Question 6.csv',    
    'Question 7.csv',
    'Question 8.csv',
    'Question 9.csv',
    'Question 10.csv',
    'Question 11.csv',
    'Extra question 1.csv',
    'Extra question 2.csv',
    'Extra question 3.csv',
    'Extra question 4.csv',
    ]


def import_csv_to_df(filename):
    """
    Imports a csv file into a Pandas dataframe
    :params: get an xls file and a sheetname from that file
    :return: a df
    """
    
    return pd.read_csv(filename)


def export_to_csv(df, location, filename):
    """
    Exports a df to a csv file
    :params: a df and a location in which to save it
    :return: nothing, saves a csv
    """

    return df.to_csv(location + filename)


def create_dict_dfs(location):
    """
    Creates a dict of dfs from a bunch of csvs
    :params: location of the csvs
    :return: a dict of dfs
    """
    dict_dfs = {}

    for current in LIST_OF_RESULT_NAMES:
        df_current = import_csv_to_df(location + current)
        dict_dfs[current] = df_current

    return dict_dfs


def compare_results(dfs_old, dfs_new):
    """
    Compares results of two sets of dataframes
    :params: two dicts of dfs containing results for comparison
    :return: a dict of dfs showing percentage differences between
             columns that have been compared
    """

    dfs_summary_comparison = {}


    # Go through the dfs containing the new results
    for key in dfs_new:
        # Highlight if a dataframe is missing
        if dfs_old[key] is None:
            print('We are missing a dataframe for ' + str(key))

        # The field we want to join on is the first column in both dfs
        # Hence grab the first column name of each df
        old_df_join_col = dfs_old[key].columns[0]
        new_df_join_col = dfs_new[key].columns[0]

#        print(old_df_join_col)
#        print(new_df_join_col)

        # Set (by hand) relevant column name in the old data and automatically
        # select it in the new data (the column has "uestion" in it)
        old_data_colname = 'Number'
        new_data_colname = [col for col in dfs_new[key].columns if 'uestion' in col][0]

#        print(old_data_colname)
#        print(new_data_colname)

        df_compare = pd.merge(dfs_new[key], dfs_old[key], left_on=new_df_join_col, right_on=old_df_join_col, how='outer')
        # Drop the percentage column, because it's uneeded and could cause confusion
        df_compare.drop('percentage', 1, inplace=True)

        print(df_compare.isnull())

        # Store results in dict of dfs
#        dfs_summary_comparison[key] = df_compare

    return

def main():
    """
    Main function to run program
    """

    # Read old and new results into separate dict of dfs
    dfs_old = create_dict_dfs(OLD_RESULTS)
    dfs_new = create_dict_dfs(NEW_RESULTS)

    # Compare results
    compare_results(dfs_old, dfs_new)

    # Save the comparisons to csvs
#    for key in dfs_summary_comparison:
#        filename = key
#        export_to_csv(dfs_summary_comparison[key], STOREFILENAME + 'comparison_summary_csvs/', filename)

if __name__ == '__main__':
    main()
