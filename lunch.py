#!/usr/bin/env python
#
# Script that selects two people randomly from a weighted list
# of employees.

# Extended by larsfp@cl.no 20110422. 

import random

class Lunchpicker():

    # List of people, with amount of 10% slices they work
    employees = {
		'One': 10,
		'Two': 10,
		'Noop'	: 10
		}

    def pick(self):
		weighted_list = []
		for employee in self.employees:
		    weighted_list += [employee] * self.employees[employee]
		shop = random.choice(weighted_list)
		return shop

if __name__ == "__main__":
	picker = Lunchpicker()
	print "Shop: %s" % picker.pick()

