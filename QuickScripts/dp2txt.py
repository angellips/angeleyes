# simple skeleton of dynamic prompts 2 txt for use in cc-study

# to-do
# add better comments
# add ability to select iteration rate through each file (independently), e.g., 3-2 = red, blue, orange | tree, flower, flower. total number of prompts added to txt == higher iteration rate
# a better way to do the w_var dictionary

import os
import re

all_wildcards = []
w_list = []
count = 0

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
	print(all_wildcards)

for x in p:
	x = re.sub('\s_', '_', x)
	x = re.sub(';', '', x)
	x = re.sub('__', '', x)
	w_list.append(x)	
	list_void(w_list, count)	
	count += 1
	print(count)