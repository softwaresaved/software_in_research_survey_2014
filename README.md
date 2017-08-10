# Software in research survey - 2014

Licence for software in LICENCE file. Licence for data in LICENCE_DATA file.

Data comes from 2014 software in research survey. Original analysis done in Excel. This is a repeat of that work.

## Summary of process

1. Get raw survey results from survey software (iSurvey)
1. Anonymise data
    * Removing email addresses
    * Delete answers from the "Any final comments" question
    * Save as ```The use of software in research (Responses) 24 Oct 14 - Form Responses 1.csv```
1. Clean "Question 11: Please provide the name(s) of the main research software you use."
    * Use ```parse_text_column.py``` to correct user mistakes when entering comma-separated list
    * Replaces semi-colons, carriage returns and other mistakes for commas
    * Save as ```software_in_research_parasable.csv```
1. Clean responses in OpenRefine
    * Use ```Software-in-research-cleaning.openrefine.tar.gz``` for cleaning
    * Uniformises university names (i.e. replaces "University College London" with "UCL")
    * Separates comma separated answers into multiple columns
    * Uniformises names of software (i.e. replaces "MS Excel" with "Microsoft Excel")
    * Save as ```Software-in-research-cleaned.csv```
1. Analyse results
 
## Files

Input files in data directory:
 * ```The use of software in research (Responses) 24 Oct 14 - Form Responses 1.csv``` - the raw (anonymised) data from the survey
 * ```Software-in-research-cleaned.csv``` - the raw anonymised data after cleaning and so ready for analysis
 * ```Software-in-research-cleaning.openrefine.tar.gz``` - the export file from OpenRefine detailing the cleaning steps
 
Processed files in the output directory:
* software_in_research_parasable.csv - the raw (anonymised) data after being processed to make comma separation more straightforward (see below for details)

Scripts in the main directory:

Cleaning done in OpenRefine: files and cleaning steps saved in data dir
Enumerate main cleaning steps.

Splitting of packages used by people done in Python

Analysis completed in Python.
Link to virtual environments.
