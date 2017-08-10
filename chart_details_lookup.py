#!/usr/bin/env python
# encoding: utf-8


# Schema for values is:
# <plot title>: just text
# <how to sort for plot>: True or False"

plot_details = {
'Question 1':['Q1: Where are you based?', False],
'Question 2':['Q2: Which roles apply to you?', False],
'Question 3':['Q3: Which discipline best applies to you?', False],
'Question 4':['Q4: Who provides the majority of your funding?', False],
'Question 5':['Q5: How long have you worked in research?', True],
'Question 6':['Q6: Do you use research software?', False],
'Question 7':['Q7: What would happen if you could no longer use research software?', False],
'Question 8':['Q8: Do you develop your own research software?', False],
'Question 9':['Q9: Have you received softare development training?', False],
'Question 10':['Q10: Have you ever included software development costs in a bid?', False],
'Question 11':['Q11: What are you main research tools?', False],
'Extra question 1':['EQ1: What is your job title?', False],
'Extra question 2':['EQ2: What is your gender?', False],
'Extra question 3':['EQ3: Employment ontract type', False],
'Extra question 4':['EQ4: Preferred operating system', False]
}

reordered_axes = {
'Question 5':['Less than a year', '1-5 years', '6-10 years', '11-15 years', '15-20 years', 'More than 20 years']
}