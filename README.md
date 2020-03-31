# CalTTC Pipeline
Cal Table Tennis automated pipeline for signups.


# Setup
- Setup virtualenv for Python 3.7.4. (Instructions tbd if you don't know how)
- Clone this repo
- run `pip install -r requirements.txt` inside your virtualenv


# How to Use
1) Get the right input sheet. 
    a) For nt and rr, Download the sheet from the Google Signup Form in CSV FORM(!!!) for that week.
    b) For donuts, you have to create the csv. Easiest way to do it is go into Excel/Google Sheets, and create two columns:
    One named "OFFICERS" and one named "GENERAL". In each column should be the names of officers, and all members (including officers).
    Export this as a csv file.
2) Move the file into `calttc_pipeline/inputs/`
3) Run:
    `python pipeline.py --form=form --input=input_filename --output=output_filename`
4) The form options are: 'nt', 'at', 'rr', 'donut_weekly', 'donut_semester'.
5) Your file should appear in `calttc_pipeline/outputs/` under the output name.
6) Go to Google Sheets and import the csv! If it is donuts, it is stored as a .txt file, so you just have to open it in Word/Google Docs.

For example, let's say you are making the advanced training list and it is called `at_week9_input.csv`.
You want it to show up as `at_week9_output.csv`. Therefore the command you would type is:
    `python pipeline.py --form=at --input=at_week9_input.csv --output=at_week9_output.csv`

Notes:
- Make sure you remember it's in CSV form and that '.csv'
- Do not commit real input files with people's real SIDs.
