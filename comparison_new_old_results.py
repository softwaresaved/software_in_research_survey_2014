#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np
import csv
import math
from lookups/universities_lookup import universities

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

    return df.to_csv(location + filename, index = False)


def create_dict_dfs(location, old):
    """
    Creates a dict of dfs from a bunch of csvs, lowercases column names
    :params: location of the csvs, a parameter which says whether working with the old or the new analysis results
    :return: a dict of dfs
    """
    
    def q1_clean(df):
        """
        Replaces the short university name from the old analysis with the
        extended university name use with the new analysis
        :params: a df with short university names, and a dictionary imported from a lookup table
        :return: a df with extended university names
        """
        for key in universities:
            df.replace(key, universities[key], inplace=True)
        return df
    
    dict_dfs = {}

    for current in LIST_OF_RESULT_NAMES:
        # Import
        df_current = import_csv_to_df(location + current)
        # make column names lowercase
        df_current.columns = [x.lower() for x in df_current.columns]
        # Go through the cols and if they're object types, convert the
        # strings to lowercase
        for col in df_current:
            if df_current[col].dtype == object:
                df_current[col] = df_current[col].astype(str).str.lower()
        if old == True: 
            if current == 'Question 1.csv':
               df_current = q1_clean(df_current)

        # Store in dict of dfs
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
        # First of all, ensure that there's a corresponding
        # dataframe in the old data, otherwise we're missing something
        if dfs_old[key] is None:
            print('We are missing a dataframe for ' + str(key))

        # The field we want to join on is the first column in both dfs
        # Hence grab the first column name of each df
        old_df_join_col = dfs_old[key].columns[0]
        new_df_join_col = dfs_new[key].columns[0]

        # Now need to compare the new and old data. It's quite easy because in the old
        # data, the relevant column is always called "number", so we set...
        old_data_colname = 'number'
        # and in the new data, the relevant column has the word "question"
        # in it, so we set...
        new_data_colname = [col for col in dfs_new[key].columns if 'question' in col][0]

        # Now we create a new dataframe by merging the new and old data (for each question, we're still in the for loop above)
        df_compare = pd.merge(dfs_new[key], dfs_old[key], left_on=new_df_join_col, right_on=old_df_join_col, how='outer')
        # Make the col names more intuitive
        df_compare.rename(columns = {old_data_colname:'old_analysis', new_data_colname:'new_analysis'}, inplace = True)

        df_compare.set_index(df_compare[df_compare.columns[0]], inplace = True)

        # Drop the percentage column, and I'm worried it might cause confusion
        df_compare.drop('percentage', 1, inplace=True)

#        print(df_compare.isnull())

        # Store results in dict of dfs
        dfs_summary_comparison[key] = df_compare

    return dfs_summary_comparison

def main():
    """
    Main function to run program
    """

    # Read old and new results into separate dict of dfs
    dfs_old = create_dict_dfs(OLD_RESULTS, True)
    dfs_new = create_dict_dfs(NEW_RESULTS, False)

    dfs_summary_comparison = {}

    # Compare results
    dfs_summary_comparison = compare_results(dfs_old, dfs_new)
    
#    print(dfs_summary_comparison)

    # Save the comparisons to csvs
    for key in dfs_summary_comparison:
        export_to_csv(dfs_summary_comparison[key], STOREFILENAME + 'comparison_summary_csvs/', key)

if __name__ == '__main__':
    main()
