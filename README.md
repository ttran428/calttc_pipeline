# CalTTC Pipeline
Cal Table Tennis automated pipeline for signups.


# Setup
- Setup virtualenv for Python 3.7.4. (Instructions tbd if you don't know how)
- Clone this repo
- run `pip install -r requirements.txt` inside your virtualenv


# How to Use
1) Download the sheet from the Google Signup Form in CSV FORM(!!!) for that week.
2) Move the file into `calttc_pipeline/inputs/`
3) Run:
    `python pipeline.py --form=form --input=input_filename --output=output_filename`
4) The form options are: 'nt', 'at', 'rr'. 
5) Your file should appear in `calttc_pipeline/outputs/` under the output name.

For example, let's say you are making the advanced training list and it is called `at_week9_input.csv`.
You want it to show up as `at_week9_output.csv`. Therefore the command you would type is:
    `python pipeline.py --form=at --input=at_week9_input.csv --output=at_week9_output.csv`
    
Notes:
- Make sure you remember it's in CSV form and that '.csv'
- Run flake8 before you push
- Do not commit real input files with people's real SIDs.