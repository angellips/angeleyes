# simple skeleton structure of script to analyze prompt texts and create normalized data for use in cc-study

# c_prompts and s_prompts txt files must exist before running (fix later)

import os
import re
import itertools
from itertools import chain
from collections import Counter
from difflib import SequenceMatcher

files = os.listdir('sample_images')

all_seeds = []
single_modifiers = []
single_most = []
chunk_modifiers = []
chunk_most = []

for x in files:
    find = re.search('.*\d[-]\d+[-]\w+', x)                 # finds match in format of "00001-2259320428-green", inherently excludes all other files.
    if find != None:
        find = re.sub('(?<![a-z])-(?![a-z])', '_', x)
        find = re.sub('(?<![a-z])-(?!\d)', '_', x)
        mods = find.replace('.png', '')
        c_mods = mods.split('_')
        c_mods = c_mods[1:]
        chunk_modifiers.append(c_mods[0].split(";"))        # creates chunk-modifiers, e.g., "hello world; blue sky; cool dog", returns each ; separated chunk of text
        s_mods = mods.replace(';', '')
        s_mods = s_mods.split('_')
        s_mods = s_mods[1:]
        single_modifiers.append(s_mods[0].split())                  # creates single modifiers, e.g., "hello", "world", "blue", etc..
        mods = mods.split('-')
        seed_clean = mods[1:]
        seed_clean = seed_clean[0].split('_')
        seed_clean = seed_clean[:-1]
        all_seeds.append(seed_clean)  # creates nested list of all seeds

chunk_modifiers = (list(chain.from_iterable(chunk_modifiers)))        # flatten nested list
single_modifiers = (list(chain.from_iterable(single_modifiers)))      # flatten nested list

for m in range(5):
    s_most = (Counter(single_modifiers).most_common(5)[m][0])
    single_most.append(s_most)                                        # creates top 5 list of most used single modifiers
    
    if re.search('^\w', (Counter(chunk_modifiers).most_common(5)[m][0])) != None:   # fixes lack of space after c_mods = mods.split('-')
        c_most = (Counter(chunk_modifiers).most_common(5)[m][0])
        c_most = " " + c_most
        chunk_most.append(c_most)
    else:
        c_most = (Counter(chunk_modifiers).most_common(5)[m][0])
        chunk_most.append(c_most)

dp = ""

for x in single_most:
    dp = dp + f"{x}" + " "

count = 0
prompts = []
for x in itertools.permutations(single_most):
    count += 1
    prompts.append(x)

del_lines = open('s_prompts.txt', 'r+')                 # clear all lines from s_prompts.txt (if any) and then open for appending prompt variations
del_lines.truncate(0)
del_lines.close()
p_txt = open("s_prompts.txt","a")

for x in (map(str, prompts)):                           # alters truple elements into strings and then cleans them up for writing to txt
    x = x[1:]
    x = x[:-1]
    x = x.replace("'", "")
    x = x.replace(",", "")
    p_txt.write(x.strip() + "\n")

p_txt.close()

count = 0
prompts = []
for x in itertools.permutations(chunk_most):
    count += 1
    prompts.append(x)                                   

del_lines = open('c_prompts.txt', 'r+')                 # clear all lines from c_prompts.txt (if any) and then open for appending prompt variations
del_lines.truncate(0)
del_lines.close()
p_txt = open("c_prompts.txt","a")

for x in (map(str, prompts)):                           # alters truple elements into strings and then cleans them up for writing to txt
    x = x[1:]
    x = x[:-1]
    x = x.replace("'", "")
    x = x.replace(", ", ";")
    p_txt.write(x.strip() + "\n")

p_txt.close()

while not(count % 8) == False:
    count += 1

batch_size = int(count / 8) # batch num * batch count in Dynamic Prompting sets the *max* number of images to produce; count of img would remain same and is produced via combinatorial option.

print(f"\nThe following will generate {count} prompt permutations in Dynamic Prompting:")
print("\n" + dp)
print(f"\nThe following settings are needed to produce all permutations using the combinatorial option:\n\nBatch Size: {batch_size} \nBatch Count: 8")
print("\nText files containing all prompt permutations for top used single and chunk modifiers generated!\nUse with Prompts from File extension!\n")

# rough structure of sequence matching code for modifiers

count = 0

lst1 = []
lst2 = []
lst3 = []
whatever = []

for x in itertools.combinations(single_most, 2):
    lst3.append(x)

for x in lst3:
    count += 1

for x, y in lst3:
    lst1.append(x)
    lst2.append(y)

w_count = 0

for x in range(count):
    # print(lst1[x], lst2[x])
    y = [lst1[x], lst2[x], (SequenceMatcher(None, lst1[x], lst2[x]).ratio())]
    whatever.append(y)
    w_count += 1

values = []

for x in range(w_count):

    values.append([whatever[x][0] + " " + whatever[x][1], [whatever[x][2]]])

print(values)


# add sort and filtering (include this earlier in code during the single/chunk_most analysis)