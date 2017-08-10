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

Data directory:
* ```The use of software in research (Responses) 24 Oct 14 - Form Responses 1.csv``` - the raw (anonymised) data from the survey
* ```software_in_research_parasable.csv``` - data after processing to make comma separation more straightforward
* ```Software-in-research-cleaning.openrefine.tar.gz``` - OpenRefine export detailing the cleaning steps
 * ```Software-in-research-cleaned.csv``` - data ready for analysis

Scripts in the main directory:

Cleaning done in OpenRefine: files and cleaning steps saved in data dir
Enumerate main cleaning steps.

Splitting of packages used by people done in Python

Analysis completed in Python.
Link to virtual environments.
