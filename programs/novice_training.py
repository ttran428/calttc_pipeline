import pandas as pd
from typing import List, Dict, Tuple, Set

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
PLAYERS_PER_TIMESLOT = 16
WAITLIST_PER_TIMESLOT = 3


class Player:
	SID = ""
	email = ""
	level = ""

	def __init__(self, name, SID, email, level):
		self.name = name
		self.SID = SID
		self.email = email
		self.level = level

	def __repr__(self):
		return f'SID: {self.SID}, EMAIL: {self.email}'


def add_player_to_possible_timeslots(
	p: Player, time: str, four: List[Player], five: List[Player], six: List[Player]
) -> Tuple[List, List, List]:
	"""
	Helper method to add player P with preference TIME to the list of players who can play at time TIME

	:param p: Player that is to be added to a time slot
	:param time: Time slot that the player has submitted a preference for
	:param four: List of players who can play at 4pm, not including player p
	:param five: List of players who can play at 5pm, not including player p
	:param six: List of players who can play at 6pm, not including player p
	:return: Tuple of list of players who are available to play at 4pm, 5pm and 6pm respectively
	"""
	four_copy = four.copy()
	five_copy = five.copy()
	six_copy = six.copy()
	if time == FOUR:
		four_copy.append(p)
	if time == FIVE:
		five_copy.append(p)
	if time == SIX:
		six_copy.append(p)
	return four_copy, five_copy, six_copy


def get_all_players_for_timeslot(seen: Set[Player], possible_players: List[Player], curr_players: List[Player],
								 num_players: int) -> \
	Tuple[Set, List]:
	"""
	Helper method to assign the first PLAYER_PER_TIMESLOT players to sign up for a given time (who have not already
	been assigned a timeslot) to that timeslot. This method does not care about whether players put the a timeslot as
	their first or second preference.

	:param seen: Set of players that have already been assigned a timeslot and thus cannot be assigned again
	:param possible_players: List of players who have signed up for this time slot as a possible preference
	:param curr_players: List of players who are currently signed up for this time already (to be added to for waitlist)
	:param num_players: Number of players to be added for the timeslot
	:return: Tuple of set of players who have been assigned a timeslot (either previously or into this timeslot) and
		list of players to play in this timeslot
	"""
	count = 0
	players = curr_players.copy()
	seen_set = seen.copy()
	while count < num_players and count < len(possible_players):
		player = possible_players[count]
		if player not in seen_set:
			seen_set.add(player)
			players.append(player)
		count += 1
	return seen_set, players


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
	Greedy algorithm to try to assign as many players as possible into a timeslot they are okay with by:
	1. For each time slot, find all the players who can possibly play then
	2. Actually assign players into a time slot, filling up time slots with less possible players first

	:param input_df: Novice training signup CSV parsed into a pandas dataframe
	:return: Novice training timing assignments parsed into a dataframe
	"""
	# Create novice training dataframe.
	possible_players_four = []
	possible_players_five = []
	possible_players_six = []
	# Add player to the set of the of times that they can play in
	for index, player in input_df.iterrows():
		possible_players_four, possible_players_five, possible_players_six \
			= add_player_to_possible_timeslots(Player(player[NAME], player[SID], player[EMAIL], player[LEVEL]), player[FIRST_PREF],
											   possible_players_four, possible_players_five, possible_players_six)

		# If they signed up with a second prefernce, also add them to the list of players for the second time preference
		if player[SECOND_PREF]:
			possible_players_four, possible_players_five, possible_players_six \
				= add_player_to_possible_timeslots(Player(player[NAME], player[SID], player[EMAIL], player[LEVEL]), player[SECOND_PREF],
												   possible_players_four, possible_players_five, possible_players_six)

	seen = set()
	output = dict()
	# Fill up the time slots with the least number of players who can play in that slot first
	if len(possible_players_four) <= len(possible_players_five) and len(
		possible_players_four
	) <= len(possible_players_six):
		seen, four = get_all_players_for_timeslot(seen, possible_players_four, [], PLAYERS_PER_TIMESLOT)
		if len(possible_players_five) <= len(possible_players_six):
			seen, five = get_all_players_for_timeslot(seen, possible_players_five, [], PLAYERS_PER_TIMESLOT)
			seen, six = get_all_players_for_timeslot(seen, possible_players_six, [], PLAYERS_PER_TIMESLOT)
		else:
			seen, six = get_all_players_for_timeslot(seen, possible_players_six, [], PLAYERS_PER_TIMESLOT)
			seen, five = get_all_players_for_timeslot(seen, possible_players_five, [], PLAYERS_PER_TIMESLOT)
	elif len(possible_players_five) <= len(possible_players_four) and len(
		possible_players_five
	) <= len(possible_players_six):
		seen, five = get_all_players_for_timeslot(seen, possible_players_five, [], PLAYERS_PER_TIMESLOT)
		if len(possible_players_four) <= len(possible_players_six):
			seen, four = get_all_players_for_timeslot(seen, possible_players_four, [], PLAYERS_PER_TIMESLOT)
			seen, six = get_all_players_for_timeslot(seen, possible_players_six, [], PLAYERS_PER_TIMESLOT)
		else:
			seen, six = get_all_players_for_timeslot(seen, possible_players_six, [], PLAYERS_PER_TIMESLOT)
			seen, four = get_all_players_for_timeslot(seen, possible_players_four, [], PLAYERS_PER_TIMESLOT)
	else:
		seen, six = get_all_players_for_timeslot(seen, possible_players_six, [], PLAYERS_PER_TIMESLOT)
		if len(possible_players_four) <= len(possible_players_five):
			seen, four = get_all_players_for_timeslot(seen, possible_players_four, [], PLAYERS_PER_TIMESLOT)
			seen, five = get_all_players_for_timeslot(seen, possible_players_five, [], PLAYERS_PER_TIMESLOT)
		else:
			seen, five = get_all_players_for_timeslot(seen, possible_players_five, [], PLAYERS_PER_TIMESLOT)
			seen, four = get_all_players_for_timeslot(seen, possible_players_four, [], PLAYERS_PER_TIMESLOT)

	# Add the waitlist for each time slot
	four.append(Player("---", "---", "---", "---"))
	five.append(Player("---", "---", "---", "---"))
	six.append(Player("---", "---", "---", "---"))
	seen, four = get_all_players_for_timeslot(seen, possible_players_four, four, WAITLIST_PER_TIMESLOT)
	seen, five = get_all_players_for_timeslot(seen, possible_players_five, five, WAITLIST_PER_TIMESLOT)
	seen, six = get_all_players_for_timeslot(seen, possible_players_six, six, WAITLIST_PER_TIMESLOT)

	df = pd.DataFrame()
	df = populate_time(df, four, "4 - 5 PM")
	df = populate_time(df, five, "5 - 6 PM")
	df = populate_time(df, six, "6 - 7 PM")
	return df
