#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np
import csv
import math
# Get info from lookup files
from question_specific_lookups import universities_lookup
from question_specific_lookups import q4_lookup
from question_specific_lookups import q9_lookup
from question_specific_lookups import eq1_lookup

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


def create_dict_dfs(location, old):
    """
    Creates a dict of dfs from a bunch of csvs, lowercases column names
    :params: location of the csvs, a parameter which says whether working with the old or the new analysis results
    :return: a dict of dfs
    """
    
    def clean_by_replacing(df, dict_replace):
        """
        Replaces the names used in the old analysis with the
        names used in the new analysis to allow comparison
        :params: a df using old names, and a dictionary imported from a lookup table
        :return: a df using new names
        """
        for key in dict_replace:
            df.replace(key, dict_replace[key], inplace=True)
        return df
    
    dict_dfs = {}

    for current in LIST_OF_RESULT_NAMES:
        # Import
        df_current = import_csv_to_df(location + current)
        # make column names lowercase
        df_current.columns = [x.lower() for x in df_current.columns]
        # Go through the cols and if they're object types, convert the
        # strings to lowercase
        df_current = df_current.apply(lambda x: x.str.lower() if(x.dtype == 'object') else x)

        if old == True: 
            # Deal with Q1 differences
            if current == 'Question 1.csv':
               # Call a local function that runs a replace function to change the names
               df_current = clean_by_replacing(df_current, universities_lookup)
            if current == 'Extra question 1.csv':
               df_current = clean_by_replacing(df_current, eq1_lookup)
               # Because we've replaced multiple old names with the same new one,
               # we need to sum over the new names to get the total
               df_current = df_current.groupby('unnamed: 0').number.sum().reset_index()

        if old == False:
            # Drop the percentage column (only in the new data), because I'm worried it might cause confusion
            df_current.drop('percentage', 1, inplace=True)
            # Deal with Q9 differences
            if current == 'Question 4.csv':
               df_current = clean_by_replacing(df_current, q4_lookup)
               # Because we've replaced multiple old names with the same new one,
               # we need to sum over the new names to get the total
               df_current = df_current.groupby('unnamed: 0')['question 4: which funder currently provides the majority of your funding'].sum().reset_index()
               df_current.sort_values('question 4: which funder currently provides the majority of your funding', ascending=False, inplace = True)
            if current == 'Question 9.csv':
               df_current = clean_by_replacing(df_current, q9_lookup)
               
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

        # Use the first column (called 'unnamed: 0'), which holds the answer options, as the index
        df_compare.set_index('unnamed: 0', drop = True, inplace = True)

        df_compare['new_analysis_percentage'] = round(100*(df_compare['new_analysis'])/df_compare['new_analysis'].sum(),0)
        df_compare['old_analysis_percentage'] = round(100*(df_compare['old_analysis'])/df_compare['old_analysis'].sum(),0)
        df_compare['new_minus_old_percentage'] = df_compare['new_analysis_percentage']-df_compare['old_analysis_percentage']

        # Store results in dict of dfs
        dfs_summary_comparison[key] = df_compare

    return dfs_summary_comparison


def totals(dfs_summary_comparison):

    question_list = []
    new_list = []
    old_list = []

    for current in LIST_OF_RESULT_NAMES:
        question_list.append(current[:-4])    
        new_list.append(int(dfs_summary_comparison[current]['new_analysis'].sum()))
        old_list.append(int(dfs_summary_comparison[current]['old_analysis'].sum()))

    totals = {'question': question_list, 'new_analysis': new_list, 'old_analysis': old_list}

    df_totals = pd.DataFrame.from_dict(totals)
    df_totals.set_index('question', drop = True, inplace = True)
    df_totals['percentage_diff'] = round(100*(df_totals['new_analysis']-df_totals['old_analysis'])/df_totals['old_analysis'],0)

    return df_totals


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

    # Save the comparisons to csvs
    for key in dfs_summary_comparison:
        export_to_csv(dfs_summary_comparison[key], STOREFILENAME + 'comparison_summary_csvs/', key)

    # Get total responses per question and compare
    df_totals = totals(dfs_summary_comparison)

    # Save totals to csv
    export_to_csv(df_totals, STOREFILENAME + 'comparison_summary_csvs/', 'responses_per_question.csv')


if __name__ == '__main__':
    main()
