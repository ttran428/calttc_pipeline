import click
import pandas as pd

from programs import advanced_training as at, round_robin as rr, novice_training2 as nt2

# Make sure all global variables match the form.
SID = "Student ID Number"
NAME = "Name (First and Last)"
EMAIL = "Email"
FIRST_PREF = "Section Preference"
SECOND_PREF = "Second Choice Section (optional)"
FOUR = "Friday 4:00 to 5:00 PM"
FIVE = "Friday 5:00 to 6:00 PM"
SIX = "Friday 6:00 to 7:00 PM"
PLAYERS_PER_TIMESLOT = 16


def valid_input(input_df: pd.DataFrame) -> bool:
    # Validates input file for all files.
    return SID in input_df and NAME in input_df and EMAIL in input_df


@click.command()
@click.option(
    "--form",
    default="nt",
    help="nt=Novice Training, at=Advanced training, rr=Round Robin",
)
@click.option("--input", default="test_form", help="the filepath to the csv input file")
@click.option(
    "--output", default="test_form", help="the filepath to the csv output file"
)
def main(form: str, input: str, output: str):

    input_df = pd.read_csv(f"./inputs/{input}")

    # Validate input file that it has the required fields
    if not valid_input(input_df):
        raise ValueError(
            "Make sure form has fields: " "SID, Name, and Email formatted correctly."
        )

    # creates the desired file
    if form == "nt":
        output_df = nt2.create_nt(input_df)
    elif form == "at":
        output_df = at.create_at(input_df)
    elif form == "rr":
        output_df = rr.create_rr(input_df)
    else:
        raise ValueError(
            "Please check type again. Options for form are: "
            "nt, at, rr. Otherwise not implemented."
        )

    # index=False means you don't write indices of row
    # w+ allows you to create file before writing if it doesn't exist
    output_df.to_csv(f"outputs/{output}", index=False, mode="w+")
    print("pipeline worked!")


if __name__ == "__main__":
    main()
