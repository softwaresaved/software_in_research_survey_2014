# Software in research survey - 2014

## Introduction

In 2012 the Software Sustainability Institute ran a survey of researchers at 15 research-intensive universities in the UK to uncover their attitudes to software. For reasons that will be explained in more detail in a forthcoming blog post, the analysis of these results was conducted in Excel. To improve the transparency and reproducibility of these results, this analysis has now been repeated in Python.

## Important points

* Licence for the code and data can be found in the the LICENCE and LICENCE_DATA files respectively.
* The code runs on Python 3.
* The data derives from the [2014 software in research survey](http://dx.doi.org/10.5281/zenodo.14809).

## Summary of process

1. Get raw survey results from survey software ([iSurvey](https://www.isurvey.soton.ac.uk/))
1. Anonymise data by manually deleting "Email" and "Further comments" fields.
1. Make Question 11 parsable in Python
1. Clean responses in OpenRefine
1. Analyse results in Python
1. Compare results in Python

## How to reproduce the results of this analysis

### Set up

Get the files and data:
1. [Clone the git repository](https://help.github.com/articles/cloning-a-repository/)

Prepare for cleaning:
1. [Download and install OpenRefine](http://openrefine.org/download.html)

Prepare for running Python:
1. If not already installed, [install virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/):
   * ```pip install virtualenv```
1. Create a project folder:
   * ```virtualenv -p <location of Python3 install directory> <name of project>```
1. Activate the virtual environment:
   * ```source <name of project>/bin/activate ```
1. Install libraries:
   * ```pip install -r requirements.txt ```

### Clean the data

There are two ways you can investigate the data cleaning. The first option is easy, and the second is thorough.

First option: the easy one

1. Navigate to the main directory ```software_in_research_survey_2014```
1. Run  ```parse_text_column.py```:
    * ``` python parse_text_column.py```
1. This will take the original survey data and parse the user-entered (and hence, very messy) answers to Question 11 ("What software do you use in your research?). This produces ```software_in_research_parasable.csv```.
1. Open OpenRefine and import ```Software-in-research-cleaning.openrefine.tar.gz```. This takes ```software_in_research_parasable.csv``` and conducts the following cleaning steps:
    1. Removes responses from universities not included in the study
    1. Rationalises user responses (e.g. "Cambridge uni" and "Uni Cambridge" become "University of Cambridge", "MS Excel" and "Excel" become "Microsoft Excel", etc.)
1. Export the cleaned data from OpenRefine as ```Software-in-research-cleaning.csv```

Second option: the thorough one

1. Navigate to the main directory ```software_in_research_survey_2014```
1. Run  ```parse_text_column.py``` to take the original survey data and parse the user-entered (and hence, very messy) answers to Question 11 ("What software do you use in your research?). This produces ```software_in_research_parasable.csv```.
1. Open a first instance of OpenRefine and import ```Software-in-research-cleaning.openrefine.tar.gz```
1. Extract the cleaning steps from the first instance of OpenRefine as [described in the documentation](https://github.com/OpenRefine/OpenRefine/wiki/History) (see "Replaying Operations").
1. Open a second instance of OpenRefine and import ```software_in_research_parasable.csv```
1. Apply the extracted cleaning steps from the first instance of OpenRefine to the data now held in the second instance of OpenRefine. This will conduct the following cleaning steps:
    1. Removes responses from universities not included in the study
    1. Rationalises user responses (e.g. "Cambridge uni" and "Uni Cambridge" become "University of Cambridge", "MS Excel" and "Excel" become "Microsoft Excel", etc.)
1. Export the cleaned data from OpenRefine as ```Software-in-research-cleaning.csv```

### Run the analysis

1. Run ```survey_2014_analysis.py```:
    * ```python survey_2014_analysis.py```
1. This summarises the reseponses to the survey, by groups the answers to each question and counting how many times each one occurs. It stores the results in a series csv files (one per question) in the ```output/summary_csvs/``` directory.
1. Run ```comparison_new_old_results.py```:
    * ```python comparison_new_old_results.py```
1. This takes the results of the summary files produced by the ```survey_2014_analysis.py``` and compares them against the results from the original analysis. It stores the results of that analysis in a series of csv files (one per question) in the ```output/comparison_summary_csvs/``` directory.

## Files and scripts

The following is a quick reference for the files and scripts, just in case you're wondering what everything does.

Data directory:
* ```Software-in-research-cleaning.openrefine.tar.gz``` - OpenRefine export detailing the cleaning steps
* ```The use of software in research (Responses) 24 Oct 14 - Form Responses 1.csv``` - the raw (anonymised) data from the survey
* ```software_in_research_parasable.csv``` - data after processing to make comma separation more straightforward
* ```Software-in-research-cleaning.csv``` - data ready for analysis

Main directory:
* ```parse_text_column.py``` - used to create ```software_in_research_parasable.csv``` described above
* ```requirements.txt``` - describes libraries used by the Python scripts. See "Running the analysis" for details.
* ```chart_details_lookup.py``` - stores info about charts to make design neater
* ```survey_2014_analysis.py``` - main script for analysing survey responses
* ```comparison_new_old_results.py``` - script to compare results from original Excel-based analysis of survey results and the results generated by ```survey_2014_analysis.py```

Other directories
* ```results_from_original_2014_analysis``` - results from original Excel-based analysis of survey results, [available from Zenodo](http://dx.doi.org/10.5281/zenodo.14809)
    * This includes ```ResearchSoftwareSurvey2014Results.xlsx``` - which is the original analysis conducted in Excel
* ```output``` - all charts and results stored as csvs
