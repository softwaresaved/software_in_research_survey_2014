#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import csv
import matplotlib.pyplot as plt
import math


DATAFILENAME = "./data/Software-in-research-cleaning.csv"
STOREFILENAME = "./output/"

def import_csv_to_df(filename):
    """
    Imports a csv file into a Pandas dataframe
    :params: get an xls file and a sheetname from that file
    :return: a df
    """

    return pd.read_csv(filename)
    
def export_df_to_csv(df, filename):
    """
    Saves a df as a
    :params: get an xls file and a sheetname from that file
    :return: a df
    """

    return df.to_csv(filename)

def strip_whitespace(df):
    """Removes leading and trailing whitespace
    :params: a df
    :return: a df without leading or trailing whitespace
    """
    
    for column in df.columns:
        try:
            df[column] = df[column].str.strip()
        except:
            print('Skipping... cannot stip whitespace from non-string columns' )
    return df




def get_groupings(df):

    # Some (a minority) of the Qs have multiple answers in different columns. Want to find these
    # questions and group them to make analysis easy later
    grouped_cols = {}
    for col in df.columns:
        # Question-related cols names are of the form "Question <number>: <question text> <possibly, another number>"
        # Identify col names with a ":"
        if ':' in col:
            # Get the first part of the col name string before the ":"
            # This will be used as the key in the grouped cols dict
            short_name = col.split(':')[0]
            # If there's no key for the short name, make one
            if short_name not in grouped_cols:
                no_list = []
                # Create a list as the value, because you can append to a list
                # later, but can't append to a string
                no_list.append(col)
                grouped_cols[short_name] = no_list
            else:
                # If the key already exists, just append the new col name to the value
                grouped_cols[short_name].append(col)
    
    return grouped_cols

def get_counts(df,grouped_cols):

    # Storing results as a dict of dfs
    univariate_summary_dfs = {}

    # Go through each of the questions (single and grouped) and get a count
    # and percentage for them
    for key in grouped_cols:
        # Store a name for the question to be used later
        # as a colname. Note that the splits are needed
        # to remove erroneous numbers from the names of the
        # grouped questions
        current_question = grouped_cols[key][0].split('.')[0].split('?')[0]
        
        # Create a df with a single column by stacking
        # Obviously, stacking a df for a question that's contained
        # in one column does not affect the df
        df_temp = df[grouped_cols[key]].stack()
        df_counts = pd.DataFrame(data = (df_temp.value_counts(sort = True)), columns = [current_question] )
        # Add percentage col
        df_counts['percentage']= round(100*df_counts[current_question]/df_counts[current_question].sum(),0)
        # Store
        univariate_summary_dfs[key] = df_counts

    return univariate_summary_dfs

def plot_bar_charts(dict_of_dfs):
    """
    Takes a two-column dataframe and plots it
    :params: a dataframe with two columns (one labels, the other a count), a filename for the resulting chart, a title, and titles for the
    two axes (if title is None, then nothing is plotted), and a truncate variable which cuts down the number of
    rows plotted (unless it's 0 at which point all rows are plotted)
    :return: Nothing, just prints a chart
    """

    for key in dict_of_dfs:
        df_temp = dict_of_dfs[key]
        title = df_temp.columns[0]
        df_temp[title].plot(kind='bar',legend=None,title=title)
        plt.savefig(STOREFILENAME + key + '.png', format = 'png', dpi = 150)
    return



def main():
    """
    Main function to run program
    """
    
    # Read survey data from csv
    df = import_csv_to_df(DATAFILENAME)

    # Strip annoying whitespace from cols containing strings
    df = strip_whitespace(df)

    # Record which questions span 1 col and which span multiple cols
    grouped_cols = get_groupings(df)

    # Perform basic counts and percentages for each question
    # Store results in dict of dfs
    univariate_summary_dfs = get_counts(df,grouped_cols)

    plot_bar_charts(univariate_summary_dfs)
    
    export_df_to_csv(df, STOREFILENAME)

if __name__ == '__main__':
    main()
