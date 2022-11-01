# simple skeleton structure of script to analyze prompt texts and create normalized data for use in cc-study

import os
import re
import itertools
from itertools import chain
from collections import Counter

files = os.listdir('sample_images')

all_modifiers = []
all_seeds = []
most_common = []

for x in files:
    find = re.search('.*\d[-]\d+[-]\w+', x)
    if find != None:
        mods = find.string.replace('.png', '')
        mods = mods.replace(';', '')
        mods = mods.split('-')
        seed_clean = mods[:-1]
        seed_clean.pop(0)
        all_seeds.append(seed_clean)
        mods.pop(0)
        mods.pop(0)
        mods = mods[0].split()
        all_modifiers.insert(0, mods) # nested list

all_modifiers = (list(chain.from_iterable(all_modifiers))) # flatten nested list

for m in range(10):
    most = (Counter(all_modifiers).most_common(10)[m][0])
    most_common.append(most) # creates top 10 list of most used modifiers

dp = "{"

for x in most_common:
    dp = dp + f"{x}" + "|"

dp = dp[:-1] + "}"

count = 0
for x in itertools.permutations(most_common):
    count += 1

while not(count % 8) == False:
    count += 1



print(f"The following would generate {count} different variations in Dynamic Prompting:")
print(dp)
print(f"Settings of Batch Size: {batch_size} and Batch Count: 8 are needed to run all permutations")

#    else: print("No PNG files found!"), need to modify this so it spits that if nothing happens and says completed if pngs != []
