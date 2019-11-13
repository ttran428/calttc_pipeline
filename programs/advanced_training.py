import pandas as pd

SID = "Student ID Number"
NAME = "Name (First and Last)"
EMAIL = "Email"


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
