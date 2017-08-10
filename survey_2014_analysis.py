#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import csv
import matplotlib.pyplot as plt
import math
import seaborn as sns
from textwrap import wrap


# Get details for plots from look up table
from chart_details_lookup import plot_details
from chart_details_lookup import reordered_axes


DATAFILENAME = "./data/Software-in-research-cleaning.csv"
STOREFILENAME = "./output/"

def import_csv_to_df(filename):
    """
    Imports a csv file into a Pandas dataframe
    :params: get an xls file and a sheetname from that file
    :return: a df
    """
    
    return pd.read_csv(filename)


def strip_whitespace(df):
    """Removes leading and trailing whitespace
    :params: a df
    :return: a df without leading or trailing whitespace
    """
    
    for column in df.columns:
        try:
            df[column] = df[column].str.strip()
        except:
            print('Skipping... cannot stip whitespace from non-string columns (Do not panic, it is fine)')
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
        df_counts = pd.DataFrame(data = (df_temp.value_counts(sort=True)), columns = [current_question] )
        # Add percentage col
        df_counts['percentage']= round(100*df_counts[current_question]/df_counts[current_question].sum(),0)
        # Store
        univariate_summary_dfs[key] = df_counts

    return univariate_summary_dfs

def plot_basic_charts(dict_of_dfs):
    """
    Create a basic plot for each question. Plots of more specific interest will
    be created in a separate function, because it's impossible to automate it.
    :params: a dict of dataframe, the imported plot details
    :return: A list of saved charts
    """

    for key in dict_of_dfs:
        df_temp = dict_of_dfs[key]
        count_colname = df_temp.columns[0]
        percent_colname = df_temp.columns[1]

        title = plot_details[key][0]
        labels = df_temp.index
        labels = [ '\n'.join(wrap(l, 12)) for l in labels ]
        plt.subplots_adjust(bottom=.3)

        # Create plot for counts
        fig = df_temp[count_colname].plot(kind='bar',legend=None,title=title)
        fig.set_xticks(df_temp.index)
        fig.set_xticklabels(labels)
        

        plt.ylabel('Count')
        plt.savefig(STOREFILENAME + 'basic_counts/' + key + '.png', format = 'png', dpi = 150)
        # Need to clear the frame otherwise I just get the same
        # plot stored twice!
        plt.clf()
        # Create plots for percentages
        df_temp[percent_colname].plot(kind='bar',legend=None,title=title)
        plt.ylabel('Percentage')
        plt.savefig(STOREFILENAME + 'basic_percentage/' + key + '.png', format = 'png', dpi = 150)
    return


def plot_basic_seaborn(dict_of_dfs):

    for key in dict_of_dfs:
        # Read the dfs one at the time
        df_temp = dict_of_dfs[key]
        # Title's from the lookup table
        title = plot_details[key][0]
        count_colname = df_temp.columns[0]
        # Some of the labels are really long
        # we need to cut them up
        labels = df_temp.index
        labels = [ '\n'.join(wrap(l, 12)) for l in labels ]
        # Now plot
        sns.barplot(x = labels, y = df_temp[count_colname], data = df_temp).set_title(title)
        plt.subplots_adjust(bottom=.3)
#        plt.tight_layout()
        plt.ylabel('Count')
        plt.xticks(rotation=90)
        plt.savefig(STOREFILENAME + 'basic_counts/' + key + '.png', format = 'png', dpi = 150)

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

    plot_basic_charts(univariate_summary_dfs)


#    plot_basic_seaborn(univariate_summary_dfs)


if __name__ == '__main__':
    main()
