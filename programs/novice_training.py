import pandas as pd
import math
from typing import List, Dict, Tuple, Set

SID = "Student ID"
NAME = "Name (First and Last)"
EMAIL = "Email"
FIRST_PREF = "Preferred Session"
SECOND_PREF = "Second Choice Session"
LEVEL = "Player Level (B, I, A)"

FOUR = "4-5 PM"
FIVE = "5-6 PM"
SIX = "6-7 PM"
PLAYERS_PER_TIMESLOT = 20
NUM_SESSIONS = 3


def add_players(players: pd.DataFrame, sessions: Dict, added: Set) -> Dict:
	"""
	Adds players to session dictionary.

	Parameters
	------
	players: pd.DataFrame
		Input from create_nt spliced
	sessions: Dict
		Contains each session with players put into it
	added: Set
		Contains SID of players already added

	Returns
	-------
	sessions: Dict
		contains each session with players put into it

	"""
	for index, player in players.iterrows():
		first_session = sessions[player[FIRST_PREF]]
		second_session = sessions[player[SECOND_PREF]] if isinstance(player[SECOND_PREF], str) else sessions[player[FIRST_PREF]]

		if player[SID] in added:
			continue
		elif len(first_session) < PLAYERS_PER_TIMESLOT:
			first_session.append(player)
		elif len(second_session) < PLAYERS_PER_TIMESLOT:
			second_session.append(player)
		else:
			if len(first_session) <= len(second_session):
				first_session.append(player)
			else:
				second_session.append(player)
		added.add(player[SID])
	return sessions


def sessions_to_df(sessions: Dict) -> pd.DataFrame:
	"""
	Parameters
	----------
	sessions: Dict
		Contains each session with players put into it

	Returns
	-------
	output_df: pd.DataFrame
		converted sessions to dataframe
	"""
	output_df = pd.DataFrame(columns=[FOUR, "4:Level", "4:Email", "4:Attendance",
	                                  FIVE, "5:Level", "5:Email", "5:Attendance",
	                                  SIX, "6:Level", "6:Email", "6:Attendance"])
	four = sessions[FOUR]
	five = sessions[FIVE]
	six = sessions[SIX]

	count = 0
	while four or five or six:
		if count == PLAYERS_PER_TIMESLOT:
			output_df = output_df.append({FOUR: "----------------------", FIVE: "----------------------", SIX: "----------------------"}, ignore_index=True)
			output_df = output_df.append({FOUR: "WAITLIST", FIVE: "WAITLIST", SIX: "WAITLIST"}, ignore_index=True)
			output_df = output_df.append({FOUR: "----------------------", FIVE: "----------------------", SIX: "----------------------"}, ignore_index=True)

		row = {}
		p1 = four.pop(0) if four else None
		p2 = five.pop(0) if five else None
		p3 = six.pop(0) if six else None

		if p1 is not None:
			row[FOUR] = p1[NAME]
			row["4:Level"] = p1[LEVEL]
			row["4:Email"] = p1[EMAIL]

		if p2 is not None:
			row[FIVE] = p2[NAME]
			row["5:Level"] = p2[LEVEL]
			row["5:Email"] = p2[EMAIL]

		if p3 is not None:
			row[SIX] = p3[NAME]
			row["6:Level"] = p3[LEVEL]
			row["6:Email"] = p3[EMAIL]

		output_df = output_df.append(row, ignore_index=True)
		count += 1

	return output_df



def create_nt(input_df: pd.DataFrame) -> pd.DataFrame:
	"""
	Takes (Players_Per_Timeslot x  num_sessions) amount of players and then puts them into their first preference.
	If a player is above Players_Per_Timeslot, then put player into second choice. If still waitlisted, put into
	whichever choice has less waitlisted people.

	After, put everyone else in based on if there are free spots, or whichever preference has less waitlisted people.

	Parameters
	------
	input_df: pd.DataFrame
		Novice training signup CSV parsed into a pandas dataframe

	Returns
	-------
	output_df: pd.DataFrame
		Novice training timing assignments parsed into a dataframe
	"""

	earliest_signups = input_df.iloc[:PLAYERS_PER_TIMESLOT * NUM_SESSIONS]
	later_signups = input_df.iloc[PLAYERS_PER_TIMESLOT * NUM_SESSIONS:]

	added = set() # checks if player has filled out form multiple times
	sessions = {FOUR: [], FIVE: [], SIX: []}

	add_players(earliest_signups, sessions, added)
	add_players(later_signups, sessions, added)

	output_df = sessions_to_df(sessions)

	return output_df
