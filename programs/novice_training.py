import pandas as pd
from typing import List, Dict, Tuple, Set

SID = "Student ID Number"
NAME = "Name (First and Last)"
EMAIL = "Email"
FIRST_PREF = "Section Preference"
SECOND_PREF = "Second Choice Section (optional)"
FOUR = "Friday 4:00 to 5:00 PM"
FIVE = "Friday 5:00 to 6:00 PM"
SIX = "Friday 6:00 to 7:00 PM"
PLAYERS_PER_TIMESLOT = 16

# Helper method to add student with SID and preference TIME to list of players
# who could possibly play at each time slot
def append_time_group(
    sid: str, time: str, four: List[str], five: List[str], six: List[str]
) -> Tuple[List, List, List]:
    four_copy = four.copy()
    five_copy = five.copy()
    six_copy = six.copy()
    if time == FOUR:
        four_copy.append(sid)
    if time == FIVE:
        five_copy.append(sid)
    if time == SIX:
        six_copy.append(sid)
    return (four_copy, five_copy, six_copy)


# Helper method to get the first PLAYERS_PER_TIMESLOT number of players who have
# not yet been assigned a time slot
def add_new_players(seen: Set, possible_players: List[str]) -> Tuple[Set, List]:
    count = 0
    players = []
    seen_set = seen.copy()
    while count < PLAYERS_PER_TIMESLOT and count < len(possible_players):
        player = possible_players[count]
        if player not in seen_set:
            seen_set.add(player)
            players.append(player)
        count += 1
    return (seen_set, players)


def create_nt(input_df: pd.DataFrame) -> pd.DataFrame:
    # Create novice training dataframe.
    possible_players_four = []
    possible_players_five = []
    possible_players_six = []
    # Add player to the set of the of times that they can play in
    for index, player in input_df.iterrows():
        (
            possible_players_four,
            possible_players_five,
            possible_players_six,
        ) = append_time_group(
            player[SID],
            player[FIRST_PREF],
            possible_players_four,
            possible_players_five,
            possible_players_six,
        )
        # If they signed up with a second prefernce, also add them to the list of players for the second time preference
        if player[SECOND_PREF]:
            (
                possible_players_four,
                possible_players_five,
                possible_players_six,
            ) = append_time_group(
                player[SID],
                player[SECOND_PREF],
                possible_players_four,
                possible_players_five,
                possible_players_six,
            )

    seen = set()
    output = dict()
    # Fill up the time slots with the least number of players who can play in that slot first
    # hahahahaha sphagetti code
    if len(possible_players_four) <= len(possible_players_five) and len(
        possible_players_four
    ) <= len(possible_players_six):
        seen, four = add_new_players(seen, possible_players_four)
        output[FOUR] = four
        if len(possible_players_five) <= len(possible_players_six):
            seen, five = add_new_players(seen, possible_players_five)
            output[FIVE] = five
            seen, six = add_new_players(seen, possible_players_six)
            output[SIX] = six
        else:
            seen, six = add_new_players(seen, possible_players_six)
            output[SIX] = six
            seen, five = add_new_players(seen, possible_players_five)
            output[FIVE] = five
    elif len(possible_players_five) <= len(possible_players_four) and len(
        possible_players_five
    ) <= len(possible_players_six):
        seen, five = add_new_players(seen, possible_players_five)
        output[FIVE] = five
        if len(possible_players_four) <= len(possible_players_six):
            seen, four = add_new_players(seen, possible_players_four)
            output[FOUR] = four
            seen, six = add_new_players(seen, possible_players_six)
            output[SIX] = six
        else:
            seen, six = add_new_players(seen, possible_players_six)
            output[SIX] = six
            seen, four = add_new_players(seen, possible_players_four)
            output[FOUR] = four
    else:
        seen, six = add_new_players(seen, possible_players_six)
        output[SIX] = six
        if len(possible_players_four) <= len(possible_players_five):
            seen, four = add_new_players(seen, possible_players_four)
            output[FOUR] = four
            seen, five = add_new_players(seen, possible_players_five)
            output[FIVE] = five
        else:
            seen, five = add_new_players(seen, possible_players_five)
            output[FIVE] = five
            seen, four = add_new_players(seen, possible_players_four)
            output[FOUR] = four

    min_length = max(len(four), len(five), len(six))
    df = pd.DataFrame({k: pd.Series(v[:min_length]) for k, v in output.items()})
    return df
