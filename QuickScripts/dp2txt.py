# simple skeleton of dynamic prompts 2 txt for use in cc-study

# TO-DO:
# add better comments
# maybe add ability (is it needed, really?) to select iteration rate through each file (independently), e.g., 3-2 = red, blue, orange | tree, flower, flower. total number of prompts added to txt == higher iteration rate
# a better way to do the w_var dictionary

import os
import re
from itertools import chain

all_wildcards = []
w_list = []
count = 0
a_count = []

p = "__color__; __plant__".split(';')


def list_void(w_list, count):
	
	w_var = {'{}'.format(x):x for x in w_list}

	list_gen(w_var.get(f"{x}"), count)

def list_gen(wildcard, count):

	file = open(f"{wildcard}.txt", "r+")
	lines = file.readlines()
	wildcard_list = []
	for x in lines:
		x = x.strip('\n')
		wildcard_list.append(x)
		print(wildcard_list)

	all_wildcards.append(wildcard_list)
	file.close()
	print(all_wildcards)

def txt_gen(all_wildcards, count):

	# print(count)
	for x in range(count):
		a_count.append(x)
		print(a_count)

	for x in a_count:
		print(x)
		for x in all_wildcards[x]:
			print(x)
			print("hello")

			# maybe pass to a dict or something idk

for x in p:
	x = re.sub('\s_', '_', x)
	x = re.sub(';', '', x)
	x = re.sub('__', '', x)
	w_list.append(x)	
	list_void(w_list, count)	
	count += 1
	print(count)

txt_gen(all_wildcards, count)