import pandas as pd
from programs import advanced_training as at

SID = "Student ID Number"
NAME = "Name (First and Last)"
EMAIL = "Email"


# function to create test data
def create_test_data(n: int) -> pd.DataFrame:
    test_data = []
    for i in range(n):
        test_data.append({NAME: "Teddy Tran", EMAIL: "ted@gmail.com", SID: str(i)})
        test_data.append(
            {NAME: "Michael Whitmeyer", EMAIL: "mike@gmail.com", SID: str(i * 10)}
        )
        test_data.append(
            {NAME: "Angela Guan", EMAIL: "angela@gmail.com", SID: str(i * 100)}
        )
        test_data.append(
            {NAME: "Jenna Kiyasu", EMAIL: "jenna@gmail.com", SID: str(i * 1000)}
        )
        test_data.append(
            {NAME: "Prachi Jha", EMAIL: "prachi@gmail.com", SID: str(i * 10000)}
        )
        test_data.append(
            {NAME: "Aarsh Shah", EMAIL: "aarsh@gmail.com", SID: str(i * 100000)}
        )
    return pd.DataFrame(test_data)


def test_create_at():
    input = create_test_data(3)
    real_output = at.create_at(input)

    expected_output = []
    for i in range(3):
        expected_output.append({"Name": "Teddy Tran", EMAIL: "ted@gmail.com"})
        expected_output.append({"Name": "Michael Whitmeyer", EMAIL: "mike@gmail.com"})
        expected_output.append({"Name": "Angela Guan", EMAIL: "angela@gmail.com"})
        expected_output.append({"Name": "Jenna Kiyasu", EMAIL: "jenna@gmail.com"})
        expected_output.append({"Name": "Prachi Jha", EMAIL: "prachi@gmail.com"})
        expected_output.append({"Name": "Aarsh Shah", EMAIL: "aarsh@gmail.com"})

    # insert the lines for waitlist
    expected_output.insert(16, {"Name": "", "Email": ""})
    expected_output.insert(17, {"Name": "WAITLIST", "Email": "WAITLIST"})
    expected_output.insert(
        18, {"Name": "---------------------", "Email": "---------------------"}
    )
    expected_output = pd.DataFrame(expected_output)

    assert expected_output.equals(real_output)
