import numpy as np 
import math
import random
import pandas as pd
from typing import Dict, List



class Donut:
	"""
	This class creates donut chats. There are two methods:

	1) make_semester_groups. This will make groups for the whole semester.
	The pros is that it tries to avoid duplicate/similar groups. The cons is that
	creating all of the donut chats for the whole semester is problematic as new members
	get added in all of the time, and we also have to remove inactive members.

	2) make_single_group. This will make groups for just one week. The pros is that we do not
	have the problem of before of adding in new members and inactive members; you just change
	the input sheet to add/delete new names. The cons is that it is random (besides making sure
	officers are in each group), which means that you could have duplicate/similar groups
	over the weeks. However, with enough members, you shouldn't be matched with a lot of the
	same people on expectation (Ted think).


	made by Michael Whitmeyer, who sucks at coding, so
	deal with it.
	"""

	def __init__(self, members: pd.DataFrame):
		"""
		Parameters
		----------
		members: pd.DataFrame
		    contains two columns mapping 'officer' to list of officers
		    and 'general' to list of ALL members (including officers).

		"""

		self.prev_groups = set()
		self.weekly_groups = []
		self.officers = [x for x in list(members['OFFICERS']) if isinstance(x, str)]
		self.general = [x for x in list(members['GENERAL']) if isinstance(x, str)]


	def make_semester_groups(self, group_size=4, num_weeks=6):
		"""
		Makes groups containing group_size number of people

		includes at least one officer in each group

		tries to avoid duplicating groups from previous weeks
		by looking at self.prev_groups

		returns: a list of lists of lists. innermost list is specific group
		middle lists are the lists of groups for each group. you get it.
		"""

		percentage = len(self.officers) / (len(self.officers) + len(self.general))

		print("each group should be roughly", percentage * 100, "percent officers")

		num_officers_each_group = group_size * percentage
		print(" --> there should be between", math.floor(num_officers_each_group), "and",
			math.ceil(num_officers_each_group), "in each group, with any luck")

		num_groups = len(self.general) // group_size
		without_offs = list(set(self.general) - set(self.officers))

		for j in range(num_weeks):
			random.shuffle(without_offs)
			random.shuffle(self.officers)

			officer_groups = np.array_split(self.officers, num_groups)
			gen_groups = np.array_split(without_offs, num_groups)
			gen_groups = np.flip(gen_groups)

			groups = []

			for i in range(num_groups):
				group = list(np.append(officer_groups[i], gen_groups[i]))
				groups.append(group)
				self.prev_groups.add(tuple(group))

			self.weekly_groups.append(groups)

		total_num_groups = num_groups * num_weeks
		total_unique_groups = len(self.prev_groups)
		print("total duplicate groups = ", total_num_groups - total_unique_groups)

		return self.weekly_groups

	def make_weekly_groups(self, group_size=4) -> List[List]:
		"""
		Parameters
		----------
		group_size: int
			How big each donut group should be

		Returns
		-------
		groups: List
			List of each group.
		"""
		num_groups = len(self.general) // group_size
		groups = [[] for _ in range(num_groups)]
		without_offs = [x for x in self.general if x not in self.officers]

		print("STATISTICS\n------------")
		print(f"There are total {len(self.general)} members and {len(self.officers)} officers.")
		print(f"There are {num_groups} groups with {len(self.officers) / num_groups} officers in each group.")
		print(f"Average group size is {len(self.general) / num_groups}")

		random.shuffle(without_offs)
		random.shuffle(self.officers)

		while self.officers:
			for group in groups:
				if self.officers:
					group.append(self.officers.pop())
				else:
					# start taking from general so first groups don't have more members
					# Assumes more members than groups. o.w. could break
					group.append(without_offs.pop())

		while without_offs:
			for group in groups:
				if without_offs:
					group.append(without_offs.pop())

		return groups

def format_to_string(groups: List[List]) -> str:
	"""
	Formats groups to string format to put into text file.
	"""
	groups_str = ""
	count = 1
	for group in groups:
		groups_str += f"Group {count}: {group} \n"
		count += 1
	return groups_str



def create_donuts(members: pd.DataFrame, semester=True):
	donut = Donut(members)
	if semester:
		sem_groups = donut.make_semester_groups()
		sem_groups_str = ""
		count = 1
		for groups in sem_groups:
			sem_groups_str += f"Week {count}\n-----------------------\n"
			sem_groups_str += f"{format_to_string(groups)}\n"
			count += 1
		return sem_groups_str

	else:
		groups = donut.make_weekly_groups()
		return format_to_string(groups)













