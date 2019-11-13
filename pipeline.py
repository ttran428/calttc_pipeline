import click
import pandas as pd

# Make sure all global variables match the form.
SID = "Student ID Number"
NAME = "Name (First and Last)"
EMAIL = "Email"


def valid_input(input_df: pd.DataFrame) -> bool:
    # Validates input file for all files.
    return SID in input_df and NAME in input_df and EMAIL in input_df


def create_nt(input_df: pd.DataFrame) -> pd.DataFrame:
    # Create novice training dataframe.
    pass


def create_at(input_df: pd.DataFrame) -> pd.DataFrame:
    # Create advanced training dataframe.
    data = []
    i = 0
    for index, player in input_df.iterrows():
        data.append({"Name": player[NAME], "Email": player[EMAIL]})
        i += 1

        # create the lines for waitlisted people after
        if i == 16:
            data.append({"Name": "", "Email": ""})
            data.append({"Name": "WAITLIST", "Email": "WAITLIST"})
            data.append(
                {"Name": "---------------------", "Email": "---------------------"}
            )

    output_df = pd.DataFrame(data)
    return output_df


def create_rr(input_df: pd.DataFrame) -> pd.DataFrame:
    # Create round robin dataframe.
    pass


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
        output_df = create_nt(input_df)
    elif form == "at":
        output_df = create_at(input_df)
    elif form == "rr":
        output_df = create_rr(input_df)
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
