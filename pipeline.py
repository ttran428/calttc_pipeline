import click
import pandas as pd

from programs import novice_training as nt, donuts as donuts

# Make sure all global variables match the form.
SID = "Student ID"
NAME = "Name (First and Last)"
EMAIL = "Email"


def create_training_df(input: str) -> pd.DataFrame:
    input_df = pd.read_csv(f"./inputs/{input}")
    # Validate input file that it has the required fields
    if not SID in input_df or not NAME in input_df or not EMAIL in input_df:
        raise ValueError("Make sure form has fields: SID, Name, and Email formatted correctly.")
    return input_df

def create_donut_df(input: str) -> pd.DataFrame:
    input_df = pd.read_csv(f"./inputs/{input}")
    if not "OFFICERS" in input_df or not "GENERAL" in input_df:
        raise ValueError("Make sure csv has two columns: 'OFFICERS' and 'GENERAL'")
    return input_df


@click.command()
@click.option("--form", default="nt", help="nt=Novice Training, at=Advanced training, rr=Round Robin",)
@click.option("--input", default="test_form", help="the filepath to the input file")
@click.option( "--output", default="test_form", help="the filepath to the output file")
def main(form: str, input: str, output: str):

    if form == "donut_semester":
        input_df = create_donut_df(input)
        groups = donuts.create_donuts(input_df, True)
        output_txt = open(f"outputs/{output}", "w")
        output_txt.write(groups)
        output_txt.close()
    elif form == "donut_weekly":
        input_df = create_donut_df(input)
        groups = donuts.create_donuts(input_df, False)
        output_txt = open(f"outputs/{output}", "w")
        output_txt.write(groups)
        output_txt.close()

    elif form == "nt":
        input_df = create_training_df(input)
        output_df = nt.create_nt(input_df)
        output_df.to_csv(f"outputs/{output}", index=False, mode="w+")
    elif form == "at":
        input_df = create_training_df(input)
        output_df = nt.create_nt(input_df)
        output_df.to_csv(f"outputs/{output}", index=False, mode="w+")
    elif form == "rr":
        input_df = create_training_df(input)
        output_df = nt.create_nt(input_df)
        output_df.to_csv(f"outputs/{output}", index=False, mode="w+")
    else:
        raise ValueError(
            "Please check type again. Options for form are: "
            "nt, at, rr, donut_semester, donut_weekly. Otherwise not implemented."
        )

    print("pipeline worked!")


if __name__ == "__main__":
    main()
