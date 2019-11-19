import pandas as pd
from typing import List, Tuple, Set

SID = "Student ID Number"
NAME = "Name (First and Last)"
EMAIL = "Email"
FIRST_PREF = "Section Preference"
SECOND_PREF = "Second Choice Section (optional)"
LEVEL = "Player Level"
NAME = "Name (First and Last)"
FOUR = "Friday 4:00 to 5:00 PM"
FIVE = "Friday 5:00 to 6:00 PM"
SIX = "Friday 6:00 to 7:00 PM"


class Player:
	SID = ""
	email = ""
	level = ""
	name = ""
	time = ""

	def __init__(self, name, SID, email, level, time=''):
		self.name = name
		self.SID = SID
		self.email = email
		self.level = level
		self.time = time

	def __repr__(self):
		return f'SID: {self.SID}, EMAIL: {self.email}'


def time_to_list(four: List[Player], five: List[Player], six: List[Player], time: str) -> List:
	"""
	Gets the list of players for the given timeslot
	:param four: List of players who can play at 4pm
	:param five: List of players who can play at 5pm
	:param six: List of players who can play at 6pm
	:param time: Time of list of player we care about
	:return: List of players at timeslot TIME
	"""
	if time == FOUR:
		return four
	if time == FIVE:
		return five
	if time == SIX:
		return six
	return None


def populate_time(df: pd.DataFrame, players: List[Player], time: str) -> pd.DataFrame:
	"""
	Helper method to populate the player name, level, and email for a given time slot in the dataframe.

	:param df: Dataframe that should contain all the player info for previous time slots
	:param players: List of players for the specified time slot
	:param time: Time slot that we are currently populating
	:return: Dataframe with updated player info to also contain the current time slot.
	"""
	curr_df = pd.DataFrame()
	curr_df.insert(curr_df.shape[1], time, [p.name for p in players], True)
	curr_df.insert(curr_df.shape[1], "Level (B, I, A)", [p.level for p in players], True)
	curr_df.insert(curr_df.shape[1], "Email", [p.email for p in players], True)
	return pd.concat([df, curr_df], axis=1)


def create_nt(input_df: pd.DataFrame) -> pd.DataFrame:
	"""
	Algorithm is as follows:
	1. Only consider the first 48 people (3 timeslots of 16 people each)
	2. Assign people to their first preference time slot, in order of who signed up earliest.
	3. If a timeslot already has 16 people:
		- If the person has a second preference, put them in their second time preference
		- If the person doesn't have a second preference, find the last person to have signed up for the current time
		  slot and move them to their second preference

	:param input_df: Novice training signup CSV parsed into a pandas dataframe
	:return: Novice training timing assignments parsed into a dataframe
	"""
	nonwaitlist = input_df[:48]
	waitlist = input_df[48:]
	four = []
	five = []
	six = []
	full_timeslots = {}

	for index, player in nonwaitlist.iterrows():
		Player
		p = None
		if player[SECOND_PREF]:
			p = Player(player[NAME], player[SID], player[EMAIL], player[LEVEL], player[SECOND_PREF])
		else:
			p = Player(player[NAME], player[SID], player[EMAIL], player[LEVEL])
		curr_list = time_to_list(four, five, six, player[FIRST_PREF])
		# Case 1: Timeslot for first preference for the player is not full -> add them to the list
		if (len(curr_list) < 16):
			curr_list.append(p)
			if (len(curr_list) == 16):
				full_timeslots.add(player[FIRST_PREF])
		# Case 2: Timeslot for first preference is full, has a second time slot -> add them to the list for the second time slot
		elif (player[SECOND_PREF]):
			second_list = time_to_list(four, five, six, player[SECOND_PREF])
			if (len(second_list) < 16):
				p.time = 0
				curr_list.append(p)
			if (len(second_list) == 16):
				full_timeslots.add(player[SECOND_PREF])
		# Case 3: Timeslot for first and second preference is full -> move someone from first preference list to their second preference
		# Case 4: Timeslot for first full, doesn't have second -> move someone from first preference list to their second preference
		else:
			for removeable_player in reversed(curr_list):
				if (removeable_player.time != '' and removeable_player.time not in full_timeslots):
					# Add exchange player to new list
					moved_list = time_to_list(four, five, six, removeable_player.time)
					moved_list.append(removeable_player)
					if (len(moved_list) == 16):
						full_timeslots.add(removeable_player.time)
					# Remove exchange player from current list
					curr_list.remove(removeable_player)
					# Add new player to current list
					curr_list.append(p)
					break

	df = pd.DataFrame()
	df = populate_time(df, four, "4 - 5 PM")
	df = populate_time(df, five, "5 - 6 PM")
	df = populate_time(df, six, "6 - 7 PM")
	return df
